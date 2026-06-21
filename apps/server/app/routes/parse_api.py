from fastapi import APIRouter,FastAPI,Depends,UploadFile,File,HTTPException,Query
from bs4 import BeautifulSoup
import os
import ebooklib
from ebooklib import epub
import os,logging,json
import pandas as pd

app=APIRouter()
logger=logging.getLogger(__name__)

@app.post("/extract_text_from_epub")
def extract_text_from_epub(epub_path: str) -> tuple[str, dict]:
    """从EPUB提取文本和元数据"""
    book = epub.read_epub(epub_path)
    
    # 提取元数据
    title = book.get_metadata('DC', 'title')
    author = book.get_metadata('DC', 'creator')
    title_str = title[0][0] if title else os.path.basename(epub_path)
    author_str = author[0][0] if author else "未知作者"
    
    # 提取所有文本
    all_text = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            text = soup.get_text()
            # 清理文本
            text = '\n'.join([line.strip() for line in text.splitlines() if line.strip()])
            if text:
                all_text.append(text)
    
    full_text = '\n\n'.join(all_text)
    metadata = {
        "title": title_str,
        "author": author_str,
        "source": epub_path,
        "type": "epub"
    }
    
    return full_text, metadata

@app.post("/extract_text_from_pdf")
def extract_text_from_pdf(pdf_path: str) -> tuple[str, dict]:
    """从PDF提取文本和元数据（你原有的逻辑）"""
    import PyPDF2
    
    text = ''
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    
    metadata = {
        "source": pdf_path,
        "type": "pdf"
    }
    return text, metadata

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

@app.post("/parse_json_file")
def parse_json_file(file_path) :
    """解析JSON文件"""

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return {"status": "success", "data": data}
    except FileNotFoundError:
        return {"status": "error", "message": f"文件不存在: {file_path}"}
    except json.JSONDecodeError as e:
        return {"status": "error", "message": f"JSON解析错误: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"服务器错误: {str(e)}"}
        
        # # 处理不同的JSON结构
        # if isinstance(data, list):
        #     data_list = data
        # elif isinstance(data, dict):
        #     # 如果JSON是对象，尝试找到包含数据的数组
        #     for key, value in data.items():
        #         if isinstance(value, list):
        #             data_list = value
        #             break
        #     else:
        #         data_list = [data]
        # else:
        #     data_list = [{"data": data}]

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
