from fastapi import APIRouter,HTTPException
from langchain_community.embeddings import HuggingFaceEmbeddings
from vosk import Model, KaldiRecognizer
from ollama import chat,ChatResponse
from pathlib import Path
from schemas import FilterRule,FilePathInput,QuestionInput,TripleResponse,TextInput
from . import parse_api 
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import json
import os,logging,queue,json,pyttsx3
import sounddevice as sd

app=APIRouter()
CHROMA_DB_PATH = "./chroma_db"
logger=logging.getLogger(__name__)
def apply_rule(rule: str, comment: str) -> bool:
    """
    简单规则解析：
    - 包含关键词xxx
    - 长度大于N
    - 长度小于N
    后续可扩展
    """
    rule = rule.strip()
    # 检测无意义文字
    meaningless_words = ["哈哈哈", "啦啦啦", "啊啊啊", "123456", "abcdef"]
    if rule == "无意义文字":
        # 1. 检查是否为常见无意义词
        for w in meaningless_words:
            if w in comment:
                return False
        # 2. 检查是否为单一字符重复
        if len(set(comment)) == 1 and len(comment) > 3:
            return False
        # 3. 检查是否为同一词语重复
        import re
        match = re.match(r"^(\w+)(\\1){2,}$", comment)
        if match:
            return False
        return True
    elif rule == "重复文字":
        # 检查是否为同一词语重复
        import re
        match = re.match(r"^(\w+)(\\1){2,}$", comment)
        if match:
            return False
        # 检查是否为单一字符重复
        if len(set(comment)) == 1 and len(comment) > 3:
            return False
        return True
    elif rule.startswith('包含关键词'):
        keyword = rule.replace('包含关键词', '').strip()
        return keyword in comment
    elif rule.startswith('长度大于'):
        try:
            n = int(rule.replace('长度大于', '').strip())
            return len(comment) > n
        except:
            return False
    elif rule.startswith('长度小于'):
        try:
            n = int(rule.replace('长度小于', '').strip())
            return len(comment) < n
        except:
            return False
    else:
        # 默认通过
        return True

@app.post('/filter_comment')
def filter_comment(rule_data: FilterRule):
    """
    根据规则描述过滤评论，返回是否通过筛选
    """
    result = apply_rule(rule_data.rule, rule_data.comment)
    return {"passed": result}

# AI评论筛选接口
@app.post('/ai_filter_comment')
def ai_filter_comment(rule_data: FilterRule):
    """
    使用AI模型，根据规则过滤评论，返回是否通过筛选
    """
    prompt = f"你是一个评论审核助手。请根据以下规则判断评论是否通过筛选。\n规则：{rule_data.rule}\n评论：{rule_data.comment}\n只回答True或False，不要解释。"
    try:
        response: ChatResponse = chat(messages=[{"role": "user", "content": prompt}])
        ai_result = response.message.content.strip()
        passed = ai_result.lower() == "true"
    except Exception as e:
        return {"error": str(e), "passed": False}
    return {"passed": passed}


@app.get("/speechtotext")
def speech_to_text():
    # 加载离线模型（确保模型路径正确）
    model_path = "../model/vosk-model-small-cn-0.22"  # 替换为你的模型文件夹路径
    
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)  # 设置采样率为 16kHz
    audio_queue = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            logger.info(f"状态错误: {status}")
        audio_queue.put(bytes(indata))

    print("请开始说话...")
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16",
                           channels=1, callback=callback):
        while True:
            data = audio_queue.get()
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                result=json.loads(result)['text']
                result=result.replace(' ', '')
                return result
                break

@app.post("/chat")
def chat_with_ollama(text: str):
    engine=pyttsx3.init()
    print("欢迎使用 Ollama AI 对话功能！输入 '退出' 退出对话。")
    model = "deepseek-r1:1.5b"  # 使用的模型名称（确保已通过 Ollama 下载）
    # url = f"http://localhost:11434/api/chat"  # Ollama 本地 API 地址
    conversation = []  # 用于存储对话上下文

    while True:
        # 用户输入
        user_input=text
        if user_input.startswith("退出") :
            print("对话结束，再见！")
            engine.say("对话结束，再见！")
            engine.runAndWait()
            break
        else:
            print("你: ", user_input)

        # 添加用户消息到上下文
        
        conversation.append({"role": "user", "content": user_input})

        # 发送请求到 Ollama API
        response: ChatResponse = chat(model=model, stream=True, messages=[
            {"role": "system", "content": "你是一个友好的 AI 助手，随时准备回答用户的问题。"},
            {"role": "user", "content": user_input}
        ])

        # 实时输出 AI 回复
        print("AI: ", end="", flush=True)
        ai_response = ""
        for chunk in response:
            if chunk.message and chunk.message.content:
                data = chunk.message.content                     
                print(data, end="", flush=True)
                ai_response += data
        engine.say(ai_response)
        engine.runAndWait()
        print()
        
        # 将 AI 回复添加到上下文
        conversation.append({"role": "assistant", "content": ai_response})
        engine.stop()

@app.post("/extract_triples", response_model=TripleResponse)
def extract_triples(text_input: TextInput):
    """
    从文本中提取三元组（主语、谓语、宾语）
    """
    try:
        llm = ChatOllama(
            model="qwen2.5:7b",
            base_url="http://localhost:11434",
            temperature=0,
            num_predict=2048,
            top_k=40,
            top_p=0.9,
        )
        
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "你是信息抽取专家。从给定的文本中提取所有（主语、谓语、宾语）三元组，并以JSON数组格式输出，每个元素包含subject, predicate, object字段。"
            ),
            ("human", "文本：{input}"),
        ])
        
        chain = prompt | llm
        response = chain.invoke({
            "input": text_input.text,  # 使用传入的文本参数
        })
        
        # 解析响应内容
        content = response.content if hasattr(response, 'content') else str(response)
        
        # 尝试解析JSON，如果失败则返回原始内容
        try:
            # 提取JSON部分（如果响应中包含其他文本）
            if '```json' in content:
                json_str = content.split('```json')[1].split('```')[0]
            elif '```' in content:
                json_str = content.split('```')[1]
            else:
                json_str = content
            triples_data = json.loads(json_str)
            return {"triples": triples_data}
        except:
            # 如果解析失败，返回单个三元组格式
            return {"triples": [{"subject": "", "predicate": "", "object": content}]}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"提取三元组失败: {str(e)}")

@app.post('/create_knowledge_base')
def create_knowledge_base(file_path: FilePathInput):
    """
    从文件创建知识库
    """
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"文件不存在: {file_path}")
    
    
    try:
        
        ext = Path(file_path).suffix.lower()
        if ext == '.pdf':
            text ,metadata= parse_api.extract_text_from_pdf(file_path)
        if ext == '.epub':
            text ,metadata= parse_api.extract_text_from_epub(file_path)
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="文件无法提取任何文本内容")
        
        # 分割文本（改进的分割方式）
        words = text.split()
        chunks = []
        chunk_size = 500
        overlap = 50  # 添加重叠避免上下文丢失
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk:  # 只添加非空块
                chunks.append(chunk)
        
        documents = [
            Document(page_content=chunk, metadata=metadata)
            for i, chunk in enumerate(chunks)
        ]
        
        # 创建向量存储
        embeddings = OllamaEmbeddings(
            model="nomic-embed-text",
            base_url="http://localhost:11434"
        )
        # embeddings = HuggingFaceEmbeddings(
        #     model_name="paraphrase-multilingual-MiniLM-L12-v2",  # 多语言，约 470MB
        #     model_kwargs={'device': 'cpu'}
        # )
        # 如果已存在，先清理
        import shutil
        if os.path.exists(CHROMA_DB_PATH):
            shutil.rmtree(CHROMA_DB_PATH)
        
        vector_store = Chroma.from_documents(
            documents,
            embeddings,
            persist_directory=CHROMA_DB_PATH
        )
        
        return {
            "message": f"知识库创建完成",
            "chunks_count": len(chunks),
            "total_characters": len(text),
            "persist_directory": CHROMA_DB_PATH
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建知识库失败: {str(e)}")

@app.post('/insert_knowledge')
def insert_knowledge(file_path: FilePathInput):
        
    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"文件不存在: {file_path}")
    
    try:
        ext = Path(file_path).suffix.lower()
        if ext == '.pdf':
            text ,metadata= parse_api.extract_text_from_pdf(file_path)
        if ext == '.epub':
            text ,metadata= parse_api.extract_text_from_epub(file_path)
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="PDF文件无法提取任何文本内容")
        
        # 分割文本（改进的分割方式）
        words = text.split()
        chunks = []
        chunk_size = 500
        overlap = 50  # 添加重叠避免上下文丢失
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk:  # 只添加非空块
                chunks.append(chunk)
        
        documents = [
            Document(page_content=chunk, metadata=metadata)
            for i, chunk in enumerate(chunks)
        ]
        
        # 创建向量存储
        embeddings = OllamaEmbeddings(
            model="nomic-embed-text",
            base_url="http://localhost:11434"
        )
        # embeddings = HuggingFaceEmbeddings(
        #     model_name="paraphrase-multilingual-MiniLM-L12-v2",  # 多语言，约 470MB
        #     model_kwargs={'device': 'cpu'}
        # )
        
        vector_store = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=embeddings
        )
        vector_store.add_documents(documents)
        return {
            "message": f"知识引入完成",
            "chunks_count": len(chunks),
            "total_characters": len(text),
            "persist_directory": CHROMA_DB_PATH
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"引入知识失败: {str(e)}")

@app.post('/use_knowledge')
def use_knowledge(question_input: QuestionInput):
    """
    基于知识库回答问题
    """
    question = question_input.question
    
    # 检查向量库是否存在
    if not os.path.exists(CHROMA_DB_PATH):
        raise HTTPException(status_code=404, detail="知识库不存在，请先调用/create_knowledge_base接口创建知识库")
    
    try:
        # 1. 加载向量库
        embeddings = OllamaEmbeddings(
            model="qwen2.5:7b",
            base_url="http://localhost:11434"
        )
        
        vector_store = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=embeddings
        )
        
        # 检查是否有文档
        try:
            collection_size = vector_store._collection.count()
            if collection_size == 0:
                raise HTTPException(status_code=404, detail="知识库为空")
        except:
            pass
        
        # 2. 创建检索器
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        
        # 3. 设置LLM
        llm = ChatOllama(
            model="qwen2.5:7b",
            base_url="http://localhost:11434",
            temperature=0.7
        )
        
        # 4. 构建RAG链
        prompt = ChatPromptTemplate.from_template("""
        基于以下上下文信息，回答用户的问题。如果无法从上下文中找到答案，请如实说明。
        
        上下文信息：
        {context}
        
        用户问题：{question}
        
        请给出准确、专业的回答：
        """)
        
        def format_docs(docs):
            return "\n\n".join([doc.page_content for doc in docs])
        
        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        # 5. 提问
        answer = rag_chain.invoke(question)
        
        return {
            "question": question,
            "answer": answer,
            "status": "success"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询知识库失败: {str(e)}")

@app.get('/health')
def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "chroma_db_exists": os.path.exists(CHROMA_DB_PATH)
    }
