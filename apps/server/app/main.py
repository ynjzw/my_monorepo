from fastapi import FastAPI,Depends,UploadFile,File,HTTPException,Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from sqlalchemy import func,desc,text
from sqlalchemy.orm import Session
from vosk import Model, KaldiRecognizer
from ollama import chat,ChatResponse

from schemas import FileUploadResponse, FileListResponse,ImportProgressResponse,ErrorResponse
from database import get_db,engine
from models import Nodes,UploadFileRecord, ImportedData,Link,family,world,Structure
from typing import List

import pymysql,uvicorn,os,uuid,logging,queue,json,pyttsx3,os
import sounddevice as sd
import pandas as pd

logger=logging.getLogger(__name__)

app=FastAPI()

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
BASE_PATH='/home/jack/my_monorepo/apps/server'
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

@app.get('/nodes')
def get_nodes(db:Session=Depends(get_db)):
    nodes = db.query(Nodes).all()
    return nodes

@app.get('/base_nodes')
def get_base_nodes(db:Session=Depends(get_db)):
    data = db.query(Nodes).filter(Nodes.type=='基础需求').all()
    return data

# 评论筛选规则请求体
class FilterRule(BaseModel):
    rule: str  # 规则描述，如“包含关键词xxx”或“长度大于10”
    comment: str  # 评论内容

def apply_rule(rule: str, comment: str) -> bool:
    """
    简单规则解析：
    - 包含关键词xxx
    - 长度大于N
    - 长度小于N
    后续可扩展
    """
    rule = rule.strip()
    # 检测无意义文字
    meaningless_words = ["哈哈哈", "啦啦啦", "啊啊啊", "123456", "abcdef"]
    if rule == "无意义文字":
        # 1. 检查是否为常见无意义词
        for w in meaningless_words:
            if w in comment:
                return False
        # 2. 检查是否为单一字符重复
        if len(set(comment)) == 1 and len(comment) > 3:
            return False
        # 3. 检查是否为同一词语重复
        import re
        match = re.match(r"^(\w+)(\\1){2,}$", comment)
        if match:
            return False
        return True
    elif rule == "重复文字":
        # 检查是否为同一词语重复
        import re
        match = re.match(r"^(\w+)(\\1){2,}$", comment)
        if match:
            return False
        # 检查是否为单一字符重复
        if len(set(comment)) == 1 and len(comment) > 3:
            return False
        return True
    elif rule.startswith('包含关键词'):
        keyword = rule.replace('包含关键词', '').strip()
        return keyword in comment
    elif rule.startswith('长度大于'):
        try:
            n = int(rule.replace('长度大于', '').strip())
            return len(comment) > n
        except:
            return False
    elif rule.startswith('长度小于'):
        try:
            n = int(rule.replace('长度小于', '').strip())
            return len(comment) < n
        except:
            return False
    else:
        # 默认通过
        return True

@app.post('/filter_comment')
def filter_comment(rule_data: FilterRule):
    """
    根据规则描述过滤评论，返回是否通过筛选
    """
    result = apply_rule(rule_data.rule, rule_data.comment)
    return {"passed": result}

@app.get('/maslow_needs')
def get_maslow_needs(db:Session=Depends(get_db)):
    data = db.query(Nodes).filter(Nodes.type=='马斯洛需求').all()
    return data

@app.get('/old_structure')
def get_old_structure(db:Session=Depends(get_db)):
    data = db.query(Structure).filter(Structure.type=='old').all()
    return data

@app.get('/new_structure')
def get_new_structure(db:Session=Depends(get_db)):
    data = db.query(Structure).filter(Structure.type=='new').all()
    return data

# AI评论筛选接口
@app.post('/ai_filter_comment')
def ai_filter_comment(rule_data: FilterRule):
    """
    使用AI模型，根据规则过滤评论，返回是否通过筛选
    """
    prompt = f"你是一个评论审核助手。请根据以下规则判断评论是否通过筛选。\n规则：{rule_data.rule}\n评论：{rule_data.comment}\n只回答True或False，不要解释。"
    try:
        response: ChatResponse = chat(messages=[{"role": "user", "content": prompt}])
        ai_result = response.message.content.strip()
        passed = ai_result.lower() == "true"
    except Exception as e:
        return {"error": str(e), "passed": False}
    return {"passed": passed}

@app.get('/link')
def get_link(db:Session=Depends(get_db)):
    link = db.query(Link).all()
    return link

@app.get('/family')
def get_family(db:Session=Depends(get_db)):
    data = db.query(family).all()
    return data

@app.get('/world')
def get_world(db:Session=Depends(get_db)):
    data = db.query(world).all()
    return data

def deduce_situation(data):
    pass

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def parse_csv_file(table_name,filepath,db:Session):
    """解析CSV文件"""
    try:
        logger.info("CSV解析开始")
        df = pd.read_csv(filepath)
        records = df.to_dict('records')
        total_rows = len(df)

        if(table_name=='nodes'):
            load_nodes_csv(records,db)
        if(table_name=='structure'):
            load_structure_csv(records,db)
        if(table_name=='link'):
            load_link_csv(records,db)

        logger.info("CSV解析成功")
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
        logger.info("Excel解析成功")
        return records,total_rows
    except Exception as e:
        logger.info(f"Excel解析错误: {str(e)}")
        return [],0

def parse_json_file(file_path: str, max_rows: int = None) -> tuple:
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
        
        return imported_count
        
    except Exception as e:
        db.rollback()
        raise e

def create_table(filename:str):
    table_name=os.path.splitext(filename)[0].lower()
    file_path=os.path.join(UPLOAD_DIR, filename)
    csv_file_path=os.path.join(BASE_PATH, file_path)
    try:
        # 读取CSV文件第一行获取字段名
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            header = f.readline().strip()
        
        fields = header.split(',')
        columns = []
        for field in fields:
            # 清理字段名（移除引号、空格等）
            clean_field = field.strip().strip('"').strip("'")
            columns.append(f"`{clean_field}` VARCHAR(255)")
        
        columns_sql = ', '.join(columns)
        
        # 使用 engine 执行SQL
        with engine.connect() as conn:
            sql = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({columns_sql}) DEFAULT CHARSET=utf8mb4"
            conn.execute(text(sql))
            conn.commit()
            
        logger.info(f"表 {table_name} 创建成功")
        
    except Exception as e:
        logger.error(f"创建表失败: {str(e)}")
        raise e
        
def load_nodes_csv(data_list: List[dict], db: Session):
    """
    将CSV数据导入到nodes表
    Args:
        data_list: 字典列表，每个字典包含name, value, x, y等字段
        db: 数据库会话
    Returns:
        int: 成功导入的记录数
    """
    if not data_list:
        logger.warning("没有数据需要导入")
        return 0
    
    success_count = 0
    error_count = 0

    for index,row in enumerate(data_list):
        try:
            # 提取数据，使用默认值处理缺失字段
            data = {
                'name': row.get('name', ''),
                'value': row.get('value', ''),
                'x': int(row.get('x') or (index * 100 + 100)),
                'y': int(row.get('y') or 100),
                'symbol': row.get('symbol') or 'circle',
                'symbol_size': int(row.get('symbol_size') or 20),
                'children': json.loads(row.get('children') or '[]'),
                'type':row.get('type', '')
            }
            
            # 验证必要字段
            if not data['name']:
                logger.warning(f"第 {index + 1} 行缺少 name 字段，跳过")
                error_count += 1
                continue
            
            # 创建记录
            file_record = Nodes(**data)
            db.add(file_record)
            success_count += 1
            
            # 每100条批量提交一次
            if success_count % 100 == 0:
                db.flush()
                logger.info(f"已处理 {success_count} 条记录")
                
        except Exception as e:
            error_count += 1
            logger.error(f"处理第 {index + 1} 行数据失败: {e}")
            logger.debug(f"问题数据: {row}")
            continue
    try:
        db.commit()
        logger.info(f"✅ 导入完成: 成功 {success_count} 条, 失败 {error_count} 条")
        return success_count
    except Exception as e:
        db.rollback()
        logger.error(f"❌ 提交事务失败: {e}")
        raise

def load_structure_csv(data_list: List[dict], db: Session):
    """
    将CSV数据导入到structure表
    Args:
        data_list: 字典列表，每个字典包含name, value, x, y等字段
        db: 数据库会话
    Returns:
        int: 成功导入的记录数
    """
    if not data_list:
        logger.warning("没有数据需要导入")
        return 0
    
    success_count = 0
    error_count = 0

    for index,row in enumerate(data_list):
        try:
            # 提取数据，使用默认值处理缺失字段
            data = {
                'name': row.get('name', ''),
                'value': row.get('value', ''),
                'x': int(row.get('x') or (index * 100 + 100)),
                'y': int(row.get('y') or 100),
                'symbol': row.get('symbol') or 'circle',
                'symbol_size': int(row.get('symbol_size') or 20),
                'children': json.loads(row.get('children') or '[]'),
                'type':row.get('type', '')
            }
            
            # 验证必要字段
            if not data['name']:
                logger.warning(f"第 {index + 1} 行缺少 name 字段，跳过")
                error_count += 1
                continue
            
            # 创建记录
            file_record = Structure(**data)
            db.add(file_record)
            success_count += 1
            
            # 每100条批量提交一次
            if success_count % 100 == 0:
                db.flush()
                logger.info(f"已处理 {success_count} 条记录")
                
        except Exception as e:
            error_count += 1
            logger.error(f"处理第 {index + 1} 行数据失败: {e}")
            logger.debug(f"问题数据: {row}")
            continue
    try:
        db.commit()
        logger.info(f"✅ 导入完成: 成功 {success_count} 条, 失败 {error_count} 条")
        return success_count
    except Exception as e:
        db.rollback()
        logger.error(f"❌ 提交事务失败: {e}")
        raise

def load_link_csv(data_list: List[dict], db: Session):
    """
    将CSV数据导入到link表
    Args:
        data_list: 字典列表，每个字典包含name, value, x, y等字段
        db: 数据库会话
    Returns:
        int: 成功导入的记录数
    """
    if not data_list:
        logger.warning("没有数据需要导入")
        return 0
    
    success_count = 0
    error_count = 0

    for index,row in enumerate(data_list):
        try:
            # 提取数据，使用默认值处理缺失字段
            data = {
                'source': row.get('source', ''),
                'value': row.get('value', ''),
                'symbol': row.get('symbol') or 'arrow',
                'target':row.get('target', '')
            }
            
            # 验证必要字段
            if not data['source']:
                logger.warning(f"第 {index + 1} 行缺少 source 字段，跳过")
                error_count += 1
                continue
            
            # 创建记录
            file_record = Link(**data)
            db.add(file_record)
            success_count += 1
            
            # 每100条批量提交一次
            if success_count % 100 == 0:
                db.flush()
                logger.info(f"已处理 {success_count} 条记录")
                
        except Exception as e:
            error_count += 1
            logger.error(f"处理第 {index + 1} 行数据失败: {e}")
            logger.debug(f"问题数据: {row}")
            continue
    try:
        db.commit()
        logger.info(f"✅ 导入完成: 成功 {success_count} 条, 失败 {error_count} 条")
        return success_count
    except Exception as e:
        db.rollback()
        logger.error(f"❌ 提交事务失败: {e}")
        raise
        
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
        stored_filename = file.filename
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
                create_table(file.filename)
                table_name=get_file_name(file.filename)
                data_list, total_rows = parse_csv_file(table_name,file_path,db)
            elif ext in ['.xlsx', '.xls']:
                data_list, total_rows = parse_excel_file(file_path)
            elif ext == '.json':
                data_list, total_rows = parse_json_file(file_path)
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
            db.rollback()
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


if __name__=='__main__':
    uvicorn.run('main:app',host='0.0.0.0',port=8000,reload=True)