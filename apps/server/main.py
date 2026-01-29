
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from model import Links,family,world
import uvicorn

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://jack@localhost:3406/graph')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

def get_db():    
    session=DBSession()
    try:
        yield session
    finally:
        session.close()

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


@app.get('/')
def hello():
    return {'hello':'world'}

@app.get('/links')
def get_links(db:Session=Depends(get_db)):
    links = db.query(Links).all()
    return links

@app.get('/family')
def get_links(db:Session=Depends(get_db)):
    links = db.query(family).all()
    return links

@app.get('/world')
def get_world(db:Session=Depends(get_db)):
    data = db.query(world).all()
    return data

if __name__=='__main__':
    uvicorn.run('main:app',host='127.0.0.1',port=8000,reload=True)