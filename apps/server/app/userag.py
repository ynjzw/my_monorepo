from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. 加载向量库
embeddings = OllamaEmbeddings(
    model="qwen2.5:7b",
    base_url="http://localhost:11434"
)

vector_store = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

# 2. 创建检索器
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# 3. 设置LLM
llm = ChatOllama(
    model="qwen2.5:7b",
    base_url="http://localhost:11434"
)
# all_metadata = vector_store.get(include=["metadatas"])
# print(f"metadata示例: {all_metadata['metadatas']}")
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
question = "胸口疼有几种情况？"
answer = rag_chain.invoke(question)
print(answer)
