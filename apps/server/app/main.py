from fastapi import FastAPI,Depends,UploadFile,File,HTTPException,Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import logging,uvicorn
from routes import ai_api,upload_api,simple_api,spider_api

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

app.include_router(ai_api.app, prefix="/routes/ai_api")

@app.get('/')
def hello():
    return {'hello':'world'}

if __name__=='__main__':
    uvicorn.run('main:app',host='0.0.0.0',port=8000,reload=True)