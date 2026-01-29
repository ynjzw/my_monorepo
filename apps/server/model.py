
from sqlalchemy import Column, String, Integer,JSON
from sqlalchemy.orm import declarative_base,Session

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
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
