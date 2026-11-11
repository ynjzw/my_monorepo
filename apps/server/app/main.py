from fastapi import FastAPI,Depends,UploadFile,File,HTTPException,Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import logging,uvicorn
from routes import ai_api,upload_api,simple_api,spider_api,parse_api,scheduled
from routes.scheduled import register_jobs,scheduler
from contextlib import asynccontextmanager

logger=logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    register_jobs()   # 注册任务
    scheduler.start() # 启动调度器
    yield
    scheduler.shutdown() # 关闭调度器

app = FastAPI(lifespan=lifespan)

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

app.include_router(ai_api.app, prefix="/routes/ai_api")
app.include_router(simple_api.app, prefix="/routes/simple_api")
app.include_router(upload_api.app, prefix="/routes/upload_api")
app.include_router(spider_api.app, prefix="/routes/spider_api")
app.include_router(parse_api.app, prefix="/routes/parse_api")
app.include_router(scheduled.app, prefix="/routes/dailyTask_api")

@app.get('/')
def hello():
    return {'hello':'world'}

if __name__=='__main__':
    uvicorn.run('main:app',host='0.0.0.0',port=8000,reload=True)