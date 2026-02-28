from fastapi import FastAPI, Depends,UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
import uvicorn,os
import pandas as pd
import json
from fastapi.responses import JSONResponse
from database import engine, Base, SessionLocal, get_db
from models import UploadFileRecord, ImportedData,Links,family,world
from sqlalchemy import desc
from schemas import (
    FileUploadResponse, FileListResponse, 
    ImportProgressResponse, ImportedDataResponse,
    ErrorResponse
)
from typing import List
import uuid,logging
import pyttsx3
import os
import queue, json
from ollama import chat,ChatResponse
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from sqlalchemy import func
from fastapi.responses import Response
import pymysql
# 创建数据表
Base.metadata.create_all(bind=engine)
logger=logging.getLogger(__name__)

app=FastAPI(
    title="Simple File Import API",
    description="简单的文件数据导入数据库接口",
    version="1.0.0"
)

origins = [
    "http://localhost:5173",    # Vite 开发服务器
    "http://localhost:8080",    # 其他前端服务器
    "http://localhost:3001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # 允许的来源列表
    allow_credentials=True,     # 允许携带 cookie
    allow_methods=["*"],        # 允许的方法
    allow_headers=["*"],        # 允许的头部
)

# 允许的文件类型
ALLOWED_EXTENSIONS = {'.csv', '.xlsx', '.xls', '.txt', '.json'}
ALLOWED_MIME_TYPES = {
    'text/csv',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'text/plain',
    'application/json'
}

# 配置文件上传目录
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
def get_file_extension(filename: str) -> str:
    """获取文件扩展名"""
    return os.path.splitext(filename)[1].lower()

def get_file_name(filename: str) -> str:
    """获取文件扩展名"""
    return os.path.splitext(filename)[0].lower()

@app.get('/')
def hello():
    return {'hello':'world'}

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    # 返回空响应
    return Response(status_code=204)  # 204 No Content

@app.get('/data')
def get_datas(db:Session=Depends(get_db)):
    data = db.query(ImportedData).all()
    return [item.to_dict() for item in data]

@app.get('/links')
def get_links(db:Session=Depends(get_db)):
    links = db.query(Links).all()
    return links

@app.get('/family')
def get_links(db:Session=Depends(get_db)):
    family = db.query(family).all()
    return family

@app.get('/world')
def get_world(db:Session=Depends(get_db)):
    data = db.query(world).all()
    return data


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def parse_csv_file(filepath):
    """解析CSV文件"""
    try:
        df = pd.read_csv(filepath)
        records = df.to_dict('records')
        total_rows = len(df)
        logger.info(df.head())
        return records,total_rows
    except Exception as e:
        print(f"CSV解析错误: {str(e)}")
        return [],0

def parse_excel_file(filepath):
    """解析Excel文件"""
    try:
        df = pd.read_excel(filepath)
        records = df.to_dict('records')
        total_rows = len(df)
        return records,total_rows
    except Exception as e:
        logger.info(f"Excel解析错误: {str(e)}")
        return [],0

async def parse_json_file(file_path: str, max_rows: int = None) -> tuple:
    """解析JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 处理不同的JSON结构
        if isinstance(data, list):
            data_list = data
            total_rows = len(data_list)
        elif isinstance(data, dict):
            # 如果JSON是对象，尝试找到包含数据的数组
            for key, value in data.items():
                if isinstance(value, list):
                    data_list = value
                    total_rows = len(data_list)
                    break
            else:
                data_list = [data]
                total_rows = 1
        else:
            data_list = [{"data": data}]
            total_rows = 1
        
        if max_rows:
            data_list = data_list[:max_rows]
        
        return data_list, total_rows
        
    except Exception as e:
        return [],0

def parse_text_file(filepath):
    """解析文本文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        lines = content.split('\n')
        data_list = []
        for i, line in enumerate(lines):
            if line.strip():  # 跳过空行
                data_list.append({
                    'line_number': i + 1,
                    'content': line.strip()
                })
        
        total_rows = len(data_list)
        logger.info(f"文本解析成功，共 {total_rows} 行")
        return data_list, total_rows  # ✅ 返回2个值
    except Exception as e:
        logger.info(f"文本解析错误: {str(e)}")
        return [],0

async def import_data_to_db(
    db: Session,
    file_record: UploadFileRecord,
    data_list: List[dict]
) -> int:
    """导入数据到数据库"""
    imported_count = 0
    
    try:
        for i, row_data in enumerate(data_list):
            imported_data = ImportedData(
                file_id=file_record.id,
                row_index=i + 1,
                data=row_data
            )
            db.add(imported_data)
            imported_count += 1
            
            # 批量提交，每100条提交一次
            if imported_count % 100 == 0:
                db.flush()
        
        db.commit()
        return imported_count
        
    except Exception as e:
        db.rollback()
        raise e


@app.post("/upload", response_model=FileUploadResponse, responses={400: {"model": ErrorResponse}})
async def upload_file(
    file: UploadFile = File(..., description="要上传的文件"),
    db: Session = Depends(get_db)
):
    """
    上传文件并导入数据到数据库
    
    - 支持 CSV、Excel、JSON、文本文件
    - 自动解析并导入数据
    - 返回文件处理状态
    """
    
    # 验证文件
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名不能为空")
    
    # 检查文件扩展名
    ext = get_file_extension(file.filename)
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件类型: {ext}，支持的类型: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    try:
        # 读取文件内容
        content = await file.read()
        file_size = len(content)
        
        # 文件大小限制 (100MB)
        if file_size > 100 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="文件大小不能超过100MB")
        
        # 生成唯一文件名
        file_id = str(uuid.uuid4())
        stored_filename = f"{file_id}{ext}"
        file_path = os.path.join(UPLOAD_DIR, stored_filename)
        
        # 保存文件
        with open(file_path, "wb") as f:
            f.write(content)
        
        # 创建文件记录
        file_record = UploadFileRecord(
            id=file_id,
            filename=stored_filename,
            original_filename=file.filename,
            file_size=file_size,
            file_type=ext[1:],  # 去掉点号
            file_path=file_path,
            status="processing"
        )
        db.add(file_record)
        db.flush()
        
        try:
            # 根据文件类型解析
            data_list = []
            total_rows = 0
            
            if ext == '.csv':
                load_csv(file)
                data_list, total_rows = parse_csv_file(file_path)
            elif ext in ['.xlsx', '.xls']:
                data_list, total_rows = parse_excel_file(file_path)
            elif ext == '.json':
                data_list, total_rows = await parse_json_file(file_path)
            elif ext == '.txt':
                data_list, total_rows = parse_text_file(file_path)
            
            # 更新总行数
            file_record.total_rows = total_rows
            
            # 导入数据到数据库
            imported_count = await import_data_to_db(db, file_record, data_list)
            
            # 更新文件记录状态
            file_record.status = "completed"
            file_record.imported_rows = imported_count
            file_record.message = f"成功导入 {imported_count} 行数据"
            
            db.commit()
            db.refresh(file_record)
            
        except Exception as e:
            file_record.status = "failed"
            file_record.message = str(e)
            db.commit()
            raise HTTPException(status_code=500, detail=f"数据处理失败: {str(e)}")
        
        return file_record.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

@app.get("/files", response_model=FileListResponse)
async def list_files(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    status: str = Query(None, description="按状态筛选"),
    db: Session = Depends(get_db)
):
    """获取文件列表"""
    query = db.query(UploadFileRecord)
    
    if status:
        query = query.filter(UploadFileRecord.status == status)
    
    total = query.count()
    files = query.order_by(desc(UploadFileRecord.created_at)).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": [f.to_dict() for f in files]
    }

@app.get("/files/{file_id}", response_model=FileUploadResponse)
async def get_file(
    file_id: str,
    db: Session = Depends(get_db)
):
    """获取文件详情"""
    file_record = db.query(UploadFileRecord).filter(UploadFileRecord.id == file_id).first()
    
    if not file_record:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    return file_record.to_dict()

@app.get("/files/{file_id}/progress", response_model=ImportProgressResponse)
async def get_import_progress(
    file_id: str,
    db: Session = Depends(get_db)
):
    """获取导入进度"""
    file_record = db.query(UploadFileRecord).filter(UploadFileRecord.id == file_id).first()
    
    if not file_record:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    progress = 0
    if file_record.total_rows > 0:
        progress = (file_record.imported_rows / file_record.total_rows) * 100
    
    return {
        "file_id": file_record.id,
        "filename": file_record.original_filename,
        "status": file_record.status,
        "total_rows": file_record.total_rows or 0,
        "imported_rows": file_record.imported_rows or 0,
        "progress": round(progress, 2),
        "message": file_record.message
    }

@app.get("/files/{file_id}/data")
async def get_imported_data(
    file_id: str,
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """获取导入的数据"""
    # 检查文件是否存在
    file_record = db.query(UploadFileRecord).filter(UploadFileRecord.id == file_id).first()
    if not file_record:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    # 查询数据
    total = db.query(ImportedData).filter(ImportedData.file_id == file_id).count()
    data = db.query(ImportedData)\
        .filter(ImportedData.file_id == file_id)\
        .order_by(ImportedData.row_index)\
        .offset(skip).limit(limit).all()
    
    return {
        "file_id": file_id,
        "filename": file_record.original_filename,
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": [d.to_dict() for d in data]
    }

@app.delete("/files/{file_id}")
async def delete_file(
    file_id: str,
    db: Session = Depends(get_db)
):
    """删除文件记录和导入的数据"""
    file_record = db.query(UploadFileRecord).filter(UploadFileRecord.id == file_id).first()
    
    if not file_record:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    try:
        # 删除物理文件
        if os.path.exists(file_record.file_path):
            os.remove(file_record.file_path)
        
        # 删除导入的数据
        db.query(ImportedData).filter(ImportedData.file_id == file_id).delete()
        
        # 删除文件记录
        db.delete(file_record)
        db.commit()
        
        return {"message": "删除成功", "file_id": file_id}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")

@app.get("/stats")
async def get_statistics(db: Session = Depends(get_db)):
    """获取统计信息"""
    # 总文件数
    total_files = db.query(UploadFileRecord).count()
    
    # 总数据行数
    total_rows = db.query(ImportedData).count()
    
    # 成功/失败统计
    success_count = db.query(UploadFileRecord).filter(UploadFileRecord.status == "completed").count()
    failed_count = db.query(UploadFileRecord).filter(UploadFileRecord.status == "failed").count()
    pending_count = db.query(UploadFileRecord).filter(UploadFileRecord.status == "pending").count()
    
    # 文件类型统计
    
    type_stats = db.query(
        UploadFileRecord.file_type,
        func.count(UploadFileRecord.id).label('count')
    ).group_by(UploadFileRecord.file_type).all()
    
    # 最近上传
    recent_files = db.query(UploadFileRecord)\
        .order_by(desc(UploadFileRecord.created_at))\
        .limit(5).all()
    
    return {
        "total_files": total_files,
        "total_data_rows": total_rows,
        "status_stats": {
            "success": success_count,
            "failed": failed_count,
            "pending": pending_count
        },
        "file_type_stats": [
            {"type": stat[0], "count": stat[1]} for stat in type_stats
        ],
        "recent_uploads": [f.to_dict() for f in recent_files]
    }

@app.get("/speechtotext")
def speech_to_text():
    # 加载离线模型（确保模型路径正确）
    model_path = "model/vosk-model-small-cn-0.22"  # 替换为你的模型文件夹路径
    
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)  # 设置采样率为 16kHz
    audio_queue = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            logger.info(f"状态错误: {status}")
        audio_queue.put(bytes(indata))

    print("请开始说话...")
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16",
                           channels=1, callback=callback):
        while True:
            data = audio_queue.get()
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                result=json.loads(result)['text']
                result=result.replace(' ', '')
                return result
                break

@app.post("/chat")
def chat_with_ollama(text: str):
    engine=pyttsx3.init()
    print("欢迎使用 Ollama AI 对话功能！输入 '退出' 退出对话。")
    model = "deepseek-r1:1.5b"  # 使用的模型名称（确保已通过 Ollama 下载）
    # url = f"http://localhost:11434/api/chat"  # Ollama 本地 API 地址
    conversation = []  # 用于存储对话上下文

    while True:
        # 用户输入
        user_input=text
        if user_input.startswith("退出") :
            print("对话结束，再见！")
            engine.say("对话结束，再见！")
            engine.runAndWait()
            break
        else:
            print("你: ", user_input)

        # 添加用户消息到上下文
        
        conversation.append({"role": "user", "content": user_input})

        # 发送请求到 Ollama API
        response: ChatResponse = chat(model=model, stream=True, messages=[
            {"role": "system", "content": "你是一个友好的 AI 助手，随时准备回答用户的问题。"},
            {"role": "user", "content": user_input}
        ])

        # 实时输出 AI 回复
        print("AI: ", end="", flush=True)
        ai_response = ""
        for chunk in response:
            if chunk.message and chunk.message.content:
                data = chunk.message.content                     
                print(data, end="", flush=True)
                ai_response += data
        engine.say(ai_response)
        engine.runAndWait()
        print()
        
        # 将 AI 回复添加到上下文
        conversation.append({"role": "assistant", "content": ai_response})
        engine.stop()

def load_csv(
    file: UploadFile = File(..., description="要上传的文件")
):
    #打开csv文件
    config = {'host':'127.0.0.1',
          'port':3406,
          'user':'jack',
          'passwd':'',
          'charset':'utf8mb4',
          'local_infile':1
          }

    conn = pymysql.connect(**config)
    cur = conn.cursor()
    database = 'graph'
    table_name = get_file_name(file.filename)
    # file = open(csv_file_path, 'r',encoding='utf-8')
    #读取csv文件第一行字段名，创建表
    reader = file.readline()
    reader = reader.replace('\n','')
    b = reader.split(',')
    colum = ''
    for a in b:
        colum = colum + '`' + a + '`' + ' varchar(255),'
    colum = colum[:-1]
    #编写sql，create_sql负责创建表，data_sql负责导入数据
    create_sql = 'create table if not exists ' + table_name + ' ' + '(' + colum + ')' + ' DEFAULT CHARSET=utf8'
    data_sql = "LOAD DATA LOCAL INFILE '%s' INTO TABLE %s FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' IGNORE 1 LINES" % (file,table_name)
    
    #使用数据库
    cur.execute('use %s' % database)
    #设置编码格式
    cur.execute('SET NAMES utf8;')
    cur.execute('SET character_set_connection=utf8;')
    cur.execute('SET global local_infile = 1;')
    #执行create_sql，创建表
    cur.execute(create_sql)
    #执行data_sql，导入数据
    cur.execute(data_sql)
    conn.commit()
    #关闭连接
    conn.close()
    cur.close()

if __name__=='__main__':
    uvicorn.run('main:app',host='0.0.0.0',port=8000,reload=True)