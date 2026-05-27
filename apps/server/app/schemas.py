from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class FileUploadResponse(BaseModel):
    """文件上传响应"""
    id: str
    filename: str
    file_size: int
    file_size_format: str
    file_type: str
    status: str
    message: Optional[str] = None
    total_rows: Optional[int] = None
    imported_rows: Optional[int] = None
    created_at: str
    
    class Config:
        from_attributes = True

class FileListResponse(BaseModel):
    """文件列表响应"""
    total: int
    items: List[FileUploadResponse]

class ImportProgressResponse(BaseModel):
    """导入进度响应"""
    file_id: str
    filename: str
    status: str
    total_rows: int
    imported_rows: int
    progress: float  # 0-100
    message: Optional[str] = None

class ImportedDataResponse(BaseModel):
    """导入数据响应"""
    id: int
    file_id: str
    row_index: int
    data: Dict[str, Any]
    created_at: str
    
    class Config:
        from_attributes = True

class ErrorResponse(BaseModel):
    """错误响应"""
    code: int
    message: str
    details: Optional[Dict[str, Any]] = None

class PdfPathInput(BaseModel):
    pdf_path: str

class TextInput(BaseModel):
    text: str

class QuestionInput(BaseModel):
    question: str

class TripleResponse(BaseModel):
    triples: List[Dict[str, str]]

# 评论筛选规则请求体
class FilterRule(BaseModel):
    rule: str  # 规则描述，如“包含关键词xxx”或“长度大于10”
    comment: str  # 评论内容