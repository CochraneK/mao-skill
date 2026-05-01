# -*- coding: utf-8 -*-
"""RAG 知识库模块"""

from pathlib import Path
from typing import List, Optional
import os


class KnowledgeBase:
    """知识库基类"""

    def __init__(self, config):
        self.config = config
        self.vectorstore = None
        self.initialized = False

    def build(self, force: bool = False):
        """构建向量库"""
        raise NotImplementedError

    def retrieve(self, query: str, top_k: int = None) -> str:
        """检索相关知识"""
        raise NotImplementedError


class ChromaKB(KnowledgeBase):
    """基于 ChromaDB 的知识库"""

    def __init__(self, config):
        super().__init__(config)
        self.persist_dir = config.vectorstore_dir

    def build(self, force: bool = False):
        """构建向量库"""
        # 检查是否已存在
        if not force and self.persist_dir.exists() and any(self.persist_dir.iterdir()):
            print(f"[INFO] 加载已有向量库: {self.persist_dir}")
            self._load()
            return

        print("[INFO] 开始构建向量库...")

        try:
            from langchain_community.document_loaders import DirectoryLoader
            from langchain_community.embeddings import HuggingFaceEmbeddings
            from langchain.text_splitter import MarkdownHeaderTextSplitter
            from langchain_community.vectorstores import Chroma
        except ImportError as e:
            print(f"[ERROR] 缺少依赖: {e}")
            print("[INFO] 安装: pip install langchain langchain-community chromadb")
            return

        # 1. 加载文档
        knowledge_dir = self.config.knowledge_dir
        if not knowledge_dir.exists():
            print(f"[WARN] 知识库目录不存在: {knowledge_dir}")
            return

        # 支持的格式
        loader = DirectoryLoader(
            str(knowledge_dir),
            glob="**/*.md",
            show_progress=True
        )

        try:
            docs = loader.load()
        except Exception as e:
            print(f"[ERROR] 加载文档失败: {e}")
            return

        if not docs:
            print("[WARN] 未找到文档")
            return

        print(f"[INFO] 已加载 {len(docs)} 个文档")

        # 2. 分割文本
        splitter = MarkdownHeaderTextSplitter()
        splits = splitter.split_documents(docs)
        print(f"[INFO] 分割为 {len(splits)} 个片段")

        # 3. 向量化
        embeddings = HuggingFaceEmbeddings(
            model_name=self.config.embedding_model,
            model_kwargs={'device': 'cpu'}
        )

        # 4. 创建向量库
        self.vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory=str(self.persist_dir)
        )

        print(f"[OK] 向量库已保存: {self.persist_dir}")
        self.initialized = True

    def _load(self):
        """加载已有向量库"""
        try:
            from langchain_community.embeddings import HuggingFaceEmbeddings
            from langchain_community.vectorstores import Chroma

            embeddings = HuggingFaceEmbeddings(
                model_name=self.config.embedding_model,
                model_kwargs={'device': 'cpu'}
            )

            self.vectorstore = Chroma(
                persist_directory=str(self.persist_dir),
                embedding_function=embeddings
            )
            self.initialized = True
            print("[OK] 向量库加载成功")

        except Exception as e:
            print(f"[ERROR] 加载向量库失败: {e}")

    def retrieve(self, query: str, top_k: int = None) -> str:
        """检索相关知识"""
        if not self.initialized or not self.vectorstore:
            print("[WARN] 向量库未初始化，返回空")
            return ""

        if top_k is None:
            top_k = self.config.top_k

        try:
            docs = self.vectorstore.similarity_search(query, k=top_k)
            context = "\n\n".join([
                f"【{d.metadata.get('source', 'unknown')}】\n{d.page_content}"
                for d in docs
            ])
            return context

        except Exception as e:
            print(f"[ERROR] 检索失败: {e}")
            return ""


# 便捷函数
def build_knowledge_base(force: bool = False):
    """快速构建知识库"""
    from .config import Config
    config = Config()
    kb = ChromaKB(config)
    kb.build(force=force)
    return kb


def retrieve(query: str, top_k: int = 3) -> str:
    """快速检索"""
    from .config import Config
    config = Config()
    kb = ChromaKB(config)
    kb.build(force=False)
    return kb.retrieve(query, top_k)


if __name__ == "__main__":
    # 构建知识库
    kb = build_knowledge_base(force=True)

    # 测试检索
    if kb.initialized:
        result = retrieve("毛泽东的实践论是什么")
        print("\n检索结果:")
        print(result[:500])
    else:
        print("[ERROR] 知识库构建失败")