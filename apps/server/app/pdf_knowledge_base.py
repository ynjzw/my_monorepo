# pdf_knowledge_base.py
# -*- coding: utf-8 -*-
"""
PDF 知识库系统 - Python 3.9 兼容版本
使用本地模型，完全离线运行
"""

import os
import pickle
import numpy as np
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader

class PDFKnowledgeBase:
    """基于 PDF 的本地知识库"""
    
    def __init__(self, pdf_path: str, model_name: str = "paraphrase-MiniLM-L3-v2"):
        """
        初始化知识库
        
        Args:
            pdf_path: PDF 文件路径
            model_name: 嵌入模型名称（可选：paraphrase-MiniLM-L3-v2, all-MiniLM-L6-v2）
        """
        self.pdf_path = pdf_path
        self.chunks = []
        self.embeddings = None
        self.embedding_model = SentenceTransformer(model_name)
        print(f"✅ 初始化完成，使用模型: {model_name}")
    
    def extract_text_from_pdf(self) -> str:
        """从 PDF 提取文本"""
        text = ""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                total_pages = len(pdf_reader.pages)
                print(f"📄 PDF 共 {total_pages} 页")
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n[第{page_num}页]\n{page_text}\n"
                    # 显示进度
                    if page_num % 10 == 0:
                        print(f"   已提取 {page_num}/{total_pages} 页")
        except Exception as e:
            print(f"❌ 读取 PDF 失败: {e}")
            raise
        
        print(f"✅ 文本提取完成，共 {len(text)} 字符")
        return text
    
    def smart_chunking(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        智能分割文本
        
        Args:
            text: 原始文本
            chunk_size: 每块大小（字符数）
            overlap: 重叠大小
        """
        # 按段落分割
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = []
        current_length = 0
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
                
            para_length = len(para)
            
            # 如果当前块加上新段落会超限
            if current_length + para_length > chunk_size and current_chunk:
                # 保存当前块
                chunks.append('\n\n'.join(current_chunk))
                # 保留重叠部分
                overlap_text = current_chunk[-overlap:] if overlap > 0 else []
                current_chunk = overlap_text.copy()
                current_length = sum(len(p) for p in current_chunk)
            
            current_chunk.append(para)
            current_length += para_length
        
        # 添加最后一块
        if current_chunk:
            chunks.append('\n\n'.join(current_chunk))
        
        print(f"✂️  文本已分割为 {len(chunks)} 个块")
        return chunks
    
    def build_knowledge_base(self, save_path: str = "knowledge_base.pkl"):
        """构建知识库"""
        print("\n🔄 开始构建知识库...")
        
        # 1. 提取文本
        full_text = self.extract_text_from_pdf()
        
        # 2. 分割文本
        self.chunks = self.smart_chunking(full_text)
        
        # 3. 生成嵌入向量
        print("🔢 正在生成向量嵌入...")
        self.embeddings = self.embedding_model.encode(
            self.chunks,
            show_progress_bar=True,
            batch_size=32
        )
        
        # 4. 保存到文件
        knowledge_data = {
            'chunks': self.chunks,
            'embeddings': self.embeddings,
            'model_name': self.embedding_model._modules.keys()
        }
        
        with open(save_path, 'wb') as f:
            pickle.dump(knowledge_data, f)
        
        print(f"✅ 知识库已保存至: {save_path}")
        print(f"   - 文本块数: {len(self.chunks)}")
        print(f"   - 向量维度: {self.embeddings.shape[1] if len(self.embeddings.shape) > 1 else '?'}")
    
    def load_knowledge_base(self, load_path: str = "knowledge_base.pkl"):
        """加载已存在的知识库"""
        print(f"\n📂 加载知识库: {load_path}")
        
        with open(load_path, 'rb') as f:
            data = pickle.load(f)
            self.chunks = data['chunks']
            self.embeddings = data['embeddings']
        
        print(f"✅ 加载完成，共 {len(self.chunks)} 个文本块")
        return True
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        搜索相关内容
        
        Args:
            query: 查询文本
            top_k: 返回最相关的前 k 个结果
        """
        if not self.chunks or self.embeddings is None:
            raise ValueError("知识库未加载，请先调用 build_knowledge_base() 或 load_knowledge_base()")
        
        # 生成查询向量
        query_embedding = self.embedding_model.encode([query])
        
        # 计算余弦相似度
        from sklearn.metrics.pairwise import cosine_similarity
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # 获取 top_k 索引
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        # 构建结果
        results = []
        for idx in top_indices:
            results.append({
                'content': self.chunks[idx],
                'similarity': float(similarities[idx]),
                'index': int(idx),
                'preview': self.chunks[idx][:200] + '...' if len(self.chunks[idx]) > 200 else self.chunks[idx]
            })
        
        return results
    
    def answer(self, question: str, top_k: int = 3) -> Dict[str, Any]:
        """
        回答问题（纯检索模式，不需要 LLM）
        
        Args:
            question: 问题
            top_k: 返回最相关的前 k 个段落
        """
        print(f"\n{'='*60}")
        print(f"❓ 问题: {question}")
        print(f"{'='*60}")
        
        # 搜索相关段落
        results = self.search(question, top_k)
        
        if not results:
            print("⚠️  未找到相关内容")
            return {'answer': None, 'sources': []}
        
        # 显示结果
        print(f"\n📚 找到 {len(results)} 个相关段落:\n")
        
        for i, result in enumerate(results, 1):
            print(f"{'─'*50}")
            print(f"[段落 {i}] 相关度: {result['similarity']:.3f}")
            print(f"{'─'*50}")
            print(f"{result['preview']}\n")
        
        # 提取最相关的段落作为答案
        best_content = results[0]['content']
        answer = self._extract_relevant_answer(question, best_content)
        
        print(f"{'='*60}")
        print(f"💡 最佳答案:")
        print(f"{'─'*60}")
        print(answer[:500])
        if len(answer) > 500:
            print("...(内容过长，已截断)")
        print(f"{'='*60}\n")
        
        return {
            'answer': answer,
            'sources': results,
            'best_match': results[0] if results else None
        }
    
    def _extract_relevant_answer(self, question: str, context: str) -> str:
        """从上下文中提取相关答案"""
        # 将问题和上下文转换为小写进行比较
        question_lower = question.lower()
        question_words = set(question_lower.split())
        
        # 按句子分割
        sentences = context.replace('。', '。\n').replace('！', '！\n').replace('？', '？\n').split('\n')
        
        # 找出包含问题关键词的句子
        relevant_sentences = []
        for sentence in sentences:
            if len(sentence.strip()) < 5:
                continue
            
            sentence_lower = sentence.lower()
            keyword_count = sum(1 for word in question_words if word in sentence_lower)
            
            if keyword_count > 0:
                relevant_sentences.append((keyword_count, sentence.strip()))
        
        # 按相关度排序
        relevant_sentences.sort(key=lambda x: x[0], reverse=True)
        
        if relevant_sentences:
            # 返回最相关的 2-3 句话
            answer = '。'.join([sent for _, sent in relevant_sentences[:3]])
            return answer
        else:
            # 没有找到相关句子，返回上下文的前 300 个字符
            return context[:300] + "..." if len(context) > 300 else context


class AdvancedPDFKnowledgeBase(PDFKnowledgeBase):
    """高级版本：支持使用本地 Ollama 模型的完整 RAG"""
    
    def __init__(self, pdf_path: str, use_ollama: bool = True):
        super().__init__(pdf_path)
        self.use_ollama = use_ollama
        self.ollama_available = False
        
        if use_ollama:
            self._check_ollama()
    
    def _check_ollama(self):
        """检查 Ollama 是否可用"""
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                self.ollama_available = True
                print("✅ 检测到 Ollama 服务，将使用 LLM 生成答案")
            else:
                print("⚠️  Ollama 服务未运行，将使用检索模式")
        except:
            print("⚠️  未检测到 Ollama，使用检索模式")
    
    def answer_with_llm(self, question: str, top_k: int = 3, model: str = "llama3.2:3b") -> str:
        """使用 LLM 生成答案"""
        if not self.ollama_available:
            print("❌ Ollama 不可用，回退到检索模式")
            result = self.answer(question, top_k)
            return result['answer'] if result['answer'] else "未找到相关信息"
        
        # 搜索相关内容
        search_results = self.search(question, top_k)
        
        if not search_results:
            return "未在 PDF 中找到相关内容"
        
        # 构建上下文
        context = "\n\n".join([r['content'] for r in search_results])
        
        # 构建 prompt
        prompt = f"""基于以下文档内容回答问题。如果文档中没有相关信息，请如实告知。

相关文档内容：
{context}

问题：{question}

请基于上述文档内容给出准确、简洁的回答："""
        
        # 调用 Ollama API
        try:
            import requests
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.1
                }
            )
            
            if response.status_code == 200:
                answer = response.json()['response']
                
                # 显示结果
                print(f"\n{'='*60}")
                print(f"❓ 问题: {question}")
                print(f"{'='*60}")
                print(f"\n💡 LLM 回答:\n{answer}\n")
                print(f"📖 参考了 {len(search_results)} 个文档片段\n")
                
                return answer
            else:
                return f"Ollama API 错误: {response.status_code}"
        except Exception as e:
            return f"调用 Ollama 失败: {e}"


def main():
    """主函数 - 使用示例"""
    
    # 配置
    PDF_PATH = "your_5mb_file.pdf"  # 请修改为您的 PDF 路径
    
    # 检查文件是否存在
    if not os.path.exists(PDF_PATH):
        print(f"❌ 错误: 找不到文件 '{PDF_PATH}'")
        print("请将 PDF 文件放在当前目录，或修改 PDF_PATH 变量")
        return
    
    # 创建知识库实例
    kb = PDFKnowledgeBase(PDF_PATH)
    
    # 检查是否已有保存的知识库
    if os.path.exists("knowledge_base.pkl"):
        print("\n发现已存在的知识库，是否加载？(y/n)")
        choice = input().lower()
        if choice == 'y':
            kb.load_knowledge_base()
        else:
            kb.build_knowledge_base()
    else:
        kb.build_knowledge_base()
    
    # 交互式问答
    print("\n" + "="*60)
    print("🎉 知识库就绪！输入问题开始查询，输入 'quit' 退出")
    print("="*60 + "\n")
    
    while True:
        question = input("👤 您: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("👋 再见！")
            break
        
        if not question:
            continue
        
        # 回答问题
        kb.answer(question, top_k=3)


def advanced_mode():
    """高级模式 - 使用 Ollama LLM"""
    PDF_PATH = "your_5mb_file.pdf"
    
    if not os.path.exists(PDF_PATH):
        print(f"❌ 错误: 找不到文件 '{PDF_PATH}'")
        return
    
    # 使用高级版本
    kb = AdvancedPDFKnowledgeBase(PDF_PATH, use_ollama=True)
    
    # 构建或加载知识库
    if os.path.exists("knowledge_base.pkl"):
        kb.load_knowledge_base()
    else:
        kb.build_knowledge_base()
    
    # 交互式问答
    print("\n" + "="*60)
    print("🎉 高级知识库就绪（支持 AI 生成答案）")
    print("输入问题开始查询，输入 'quit' 退出")
    print("="*60 + "\n")
    
    while True:
        question = input("👤 您: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("👋 再见！")
            break
        
        if not question:
            continue
        
        # 使用 LLM 回答
        kb.answer_with_llm(question)


if __name__ == "__main__":
    print("请选择运行模式:")
    print("1. 基础模式（纯检索，无需额外服务）")
    print("2. 高级模式（需要 Ollama 服务）")
    
    choice = input("请输入 1 或 2: ").strip()
    
    if choice == "2":
        advanced_mode()
    else:
        main()