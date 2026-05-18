import PyPDF2
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

text=''
pdf_path='诊断学(第10版).pdf'
with open(pdf_path, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    for page in pdf_reader.pages:
        text += page.extract_text()
# 分割文本

words = text.split()
chunks = []

for i in range(0, len(words), 500):
    chunk = ' '.join(words[i:i+500])
    chunks.append(chunk)

documents = [
    Document(page_content=chunk, metadata={"source": pdf_path, "chunk_id": i})
    for i, chunk in enumerate(chunks)
]
embeddings = OllamaEmbeddings(
        model="qwen2.5:7b",  # 千问也支持嵌入
        base_url="http://localhost:11434"
    )

# 创建向量存储
vector_store = Chroma.from_documents(
    documents, 
    embeddings,
    persist_directory="./chroma_db"  # 持久化存储
)

print(f"知识库创建完成，共 {len(chunks)} 个文本块")
