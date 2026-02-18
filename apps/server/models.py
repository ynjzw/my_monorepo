from sqlalchemy import Column, Integer, String, DateTime, Text, Float, BigInteger, JSON
from sqlalchemy.sql import func
from database import Base
import uuid
from sqlalchemy.orm import declarative_base,Session

# 创建对象的基类:
Base = declarative_base()

class UploadFileRecord(Base):
    """上传文件记录表"""
    __tablename__ = "upload_file_records"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String(255), nullable=False, comment="文件名")
    original_filename = Column(String(255), nullable=False, comment="原始文件名")
    file_size = Column(Integer, nullable=False, comment="文件大小(字节)")
    file_type = Column(String(50), nullable=False, comment="文件类型")
    file_path = Column(String(500), nullable=False, comment="存储路径")
    
    status = Column(String(20), default="pending", comment="状态: pending, processing, completed, failed")
    message = Column(Text, comment="处理信息")
    
    total_rows = Column(Integer, default=0, comment="总行数")
    imported_rows = Column(Integer, default=0, comment="导入行数")
    
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    
    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.original_filename,
            "file_size": self.file_size,
            "file_size_format": self.format_size(self.file_size),
            "file_type": self.file_type,
            "status": self.status,
            "message": self.message,
            "total_rows": self.total_rows,
            "imported_rows": self.imported_rows,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        }
    
    @staticmethod
    def format_size(size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"

class ImportedData(Base):
    """导入数据表"""
    __tablename__ = "imported_data"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(String(36), nullable=False, index=True, comment="文件ID")
    row_index = Column(Integer, nullable=False, comment="行号")
    
    # 使用JSON字段存储所有数据，灵活适配不同格式的文件
    data = Column(JSON, nullable=False, comment="数据内容")
    
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    
    def to_dict(self):
        return {
            "id": self.id,
            "file_id": self.file_id,
            "row_index": self.row_index,
            "data": self.data,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        }
    

class Links(Base):
    # 表的名字:
    __tablename__ = 'links'
    # 表的结构:    
    source = Column(String(255),primary_key=True)
    target = Column(String(255))
    value = Column(String(255))
    symbol=Column(String(255))

class world(Base):
    # 表的名字:
    __tablename__ = 'world'
    # 表的结构:    
    name = Column(String(255),primary_key=True)
    value = Column(String(255))
    x=Column(Integer)
    y=Column(Integer)
    symbol=Column(String(255))
    symbol_size=Column(Integer)
    itemStyle=Column(JSON)

class family(Base):
    # 表的名字:
    __tablename__ = 'family'
    # 表的结构:    
    name = Column(String(255),primary_key=True)
    value = Column(String(255))
    x=Column(Integer)
    y=Column(Integer)
    symbol=Column(String(255))
    symbol_size=Column(Integer)
    itemStyle=Column(JSON)
