import os
import uuid
import shutil
from pathlib import Path
from typing import List
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc
import pandas as pd
import json
from datetime import datetime

from schemas import (
    FileUploadResponse, FileListResponse, 
    ImportProgressResponse, ImportedDataResponse,
    ErrorResponse
)


# 创建应用
app = FastAPI(
    title="Simple File Import API",
    description="简单的文件数据导入数据库接口",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置文件上传目录
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 允许的文件类型
ALLOWED_EXTENSIONS = {'.csv', '.xlsx', '.xls', '.txt', '.json'}
ALLOWED_MIME_TYPES = {
    'text/csv',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'text/plain',
    'application/json'
}

def get_file_extension(filename: str) -> str:
    """获取文件扩展名"""
    return os.path.splitext(filename)[1].lower()

async def parse_csv_file(file_path: str, max_rows: int = None) -> tuple:
    """解析CSV文件"""
    try:
        # 尝试不同的编码
        encodings = ['utf-8', 'gbk', 'gb2312', 'latin1']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            df = pd.read_csv(file_path, encoding='latin1')
        
        # 处理数据
        total_rows = len(df)
        if max_rows:
            df = df.head(max_rows)
        
        # 转换为字典列表，处理NaN值
        data_list = df.replace({pd.NA: None, float('nan'): None}).to_dict('records')
        
        return data_list, total_rows
        
    except Exception as e:
        raise ValueError(f"CSV解析失败: {str(e)}")

async def parse_excel_file(file_path: str, max_rows: int = None) -> tuple:
    """解析Excel文件"""
    try:
        df = pd.read_excel(file_path)
        
        total_rows = len(df)
        if max_rows:
            df = df.head(max_rows)
        
        # 转换为字典列表，处理NaN值
        data_list = df.replace({pd.NA: None, float('nan'): None}).to_dict('records')
        
        return data_list, total_rows
        
    except Exception as e:
        raise ValueError(f"Excel解析失败: {str(e)}")

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
        raise ValueError(f"JSON解析失败: {str(e)}")

async def parse_text_file(file_path: str, max_rows: int = None) -> tuple:
    """解析文本文件（按行导入）"""
    try:
        data_list = []
        encodings = ['utf-8', 'gbk', 'gb2312', 'latin1']
        content = None
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.readlines()
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            with open(file_path, 'r', encoding='latin1') as f:
                content = f.readlines()
        
        total_rows = len(content)
        for i, line in enumerate(content):
            if max_rows and i >= max_rows:
                break
            line = line.strip()
            if line:  # 跳过空行
                data_list.append({"line": line, "line_number": i + 1})
        
        return data_list, total_rows
        
    except Exception as e:
        raise ValueError(f"文本文件解析失败: {str(e)}")

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

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Simple File Import API",
        "version": "1.0.0",
        "endpoints": {
            "POST /upload": "上传文件并导入数据",
            "GET /files": "获取文件列表",
            "GET /files/{file_id}": "获取文件详情",
            "GET /files/{file_id}/data": "获取导入的数据",
            "DELETE /files/{file_id}": "删除文件记录",
            "GET /stats": "获取统计信息"
        }
    }

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
                data_list, total_rows = await parse_csv_file(file_path)
            elif ext in ['.xlsx', '.xls']:
                data_list, total_rows = await parse_excel_file(file_path)
            elif ext == '.json':
                data_list, total_rows = await parse_json_file(file_path)
            elif ext == '.txt':
                data_list, total_rows = await parse_text_file(file_path)
            
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
    from sqlalchemy import func
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )