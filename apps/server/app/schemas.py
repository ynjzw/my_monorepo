from pydantic import BaseModel, Field, field_validator
from typing import Optional,Union, List, Dict, Any
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

class FilePathInput(BaseModel):
    file_path: str

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

class Nodes(BaseModel):
    id: Optional[str] = Field(default=None, max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)
    x: float
    y: float
    symbol: str
    symbolSize: int
    
class NodeBatchIn(BaseModel):
    nodes: List[Nodes]

    @field_validator("nodes")
    @classmethod
    def check_not_empty(cls, v):
        if not v:
            raise ValueError("nodes 不能为空")
        if len(v) > 100000:
            raise ValueError("单次最多 10 万条")
        return v

class Link(BaseModel):
    id:str
    source: Optional[str] = Field(default=None, max_length=255)
    target: Optional[str] = Field(default=None, max_length=255)
    link_type: str
    
class LinkBatchIn(BaseModel):
    links: List[Link]

    @field_validator("links")
    @classmethod
    def check_not_empty(cls, v):
        if not v:
            raise ValueError("links 不能为空")
        if len(v) > 100000:
            raise ValueError("单次最多 10 万条")
        return v
    
class PersonalDataUpdate(BaseModel):
    skill: str
    resource: str
    wish: str
    user_id: str