from fastapi import FastAPI,APIRouter
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
import requests
from bs4 import BeautifulSoup
import time
import random
from typing import Dict, List, Optional
import os

app=APIRouter()
CHROMA_DB_PATH = "./chroma_db"

@app.post("/fetch_page")
def fetch_page(self, url: str, method: str = 'GET', params: Optional[Dict] = None, 
                data: Optional[Dict] = None, retry: int = 3) -> Optional[str]:
    """
    获取网页内容
    
    Args:
        url: 目标URL
        method: 请求方法，'GET' 或 'POST'
        params: GET请求参数
        data: POST请求数据
        retry: 重试次数
    
    Returns:
        网页HTML内容，失败返回None
    """
    for attempt in range(retry):
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params, timeout=10)
            else:
                response = self.session.post(url, params=params, data=data, timeout=10)
            
            response.raise_for_status()
            response.encoding = response.apparent_encoding  # 自动检测编码
            
            return BeautifulSoup(response.text, 'html.parser')
            
        except requests.RequestException as e:
            print(f"请求失败 (尝试 {attempt + 1}/{retry}): {e}")
            if attempt < retry - 1:
                time.sleep(random.uniform(1, 3))  # 随机等待
            else:
                print(f"所有重试都失败: {url}")
                return None

# @app.post("/extract_text")
# def extract_text(self, soup: BeautifulSoup, selector: str, attr: Optional[str] = None) -> List[str]:
#     """
#     从BeautifulSoup对象中提取文本
    
#     Args:
#         soup: BeautifulSoup对象
#         selector: CSS选择器
#         attr: 属性名，如果指定则提取属性值，否则提取文本
    
#     Returns:
#         提取的文本列表
#     """
#     elements = soup.select(selector)
#     if attr:
#         return [elem.get(attr, '').strip() for elem in elements]
#     else:
#         return [elem.get_text(strip=True) for elem in elements]

# @app.post("/extract_table")
# def extract_table(self, soup: BeautifulSoup, table_selector: str = 'table') -> List[List[str]]:
#     """
#     提取表格数据
    
#     Args:
#         soup: BeautifulSoup对象
#         table_selector: 表格选择器
    
#     Returns:
#         二维列表形式的表格数据
#     """
#     table = soup.select_one(table_selector)
#     if not table:
#         return []
    
#     data = []
#     rows = table.find_all('tr')
    
#     for row in rows:
#         row_data = []
#         cells = row.find_all(['td', 'th'])
#         for cell in cells:
#             row_data.append(cell.get_text(strip=True))
#         if row_data:
#             data.append(row_data)
    
#     return data

# @app.post("/extract_links")
# def extract_links(self, soup: BeautifulSoup, base_url: str = '') -> List[Dict[str, str]]:
    """
    提取页面中的所有链接
    
    Args:
        soup: BeautifulSoup对象
        base_url: 基础URL，用于构建完整链接
    
    Returns:
        链接字典列表，包含href和text
    """
    links = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        text = a_tag.get_text(strip=True)
        
        # 构建完整URL
        if base_url and href.startswith('/'):
            href = base_url.rstrip('/') + href
        
        links.append({'url': href, 'text': text})
    
    return links

@app.post("/save_to_chroma")
def save_to_chroma(self, content: str) -> bool:
    """
    保存内容到知识库
    
    Args:
        content: 要保存的内容
    
    Returns:
        是否保存成功
    """
    try:
        # 检查内容是否为空
        if not content or not content.strip():
            return {
                "success": False,
                "message": "内容为空，无法保存",
                "chunks_count": 0,
                "total_characters": 0
            }
        # 提取所有段落文本
        words = content.split()
        # 如果没有足够的内容
        if len(words) < 50:
            return {
                "success": False,
                "message": "内容过少，至少需要50个词",
                "chunks_count": 0,
                "total_characters": len(content)
            }
        chunks = []
        chunk_size = 500
        overlap = 50  # 添加重叠避免上下文丢失

        # 修复1：正确处理分块逻辑
        i = 0
        while i < len(words):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk.strip():  # 只添加非空块
                chunks.append(chunk)
            i += chunk_size - overlap
        
        
        documents = [
            Document(page_content=chunk,metadata={"chunk_id": idx})
            for idx,chunk in enumerate(chunks)
        ]
        
        # 修复3：检查是否有文档需要保存
        if not documents:
            return {
                "success": False,
                "message": "没有生成有效的文档块",
                "chunks_count": 0,
                "total_characters": len(content)
            }
        
        # 创建向量存储
        embeddings = OllamaEmbeddings(
            model="qwen2.5:7b",
            base_url="http://localhost:11434"
        )
        
        os.makedirs(CHROMA_DB_PATH, exist_ok=True)

        vector_store = Chroma.from_documents(
            documents,
            embeddings,
            persist_directory=CHROMA_DB_PATH
        )
        
        return {
            "success": True,
            "message": f"知识库创建完成",
            "chunks_count": len(chunks),
            "total_characters": len(content),
            "persist_directory": CHROMA_DB_PATH
        }
    except ImportError as e:
        print(f"导入模块失败: {e}")
        return {
            "success": False,
            "message": f"缺少必要的库: {e}",
            "chunks_count": 0,
            "total_characters": 0
        }
    except Exception as e:
        print(f"保存到知识库失败: {e}")
        return {
            "success": False,
            "message": f"保存失败: {str(e)}",
            "chunks_count": 0,
            "total_characters": len(content) if 'content' in locals() else 0
        }
