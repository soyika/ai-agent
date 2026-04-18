from typing import Optional, list
import os
from loguru import logger
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from app.core.config import settings


KIWIFRUIT_KNOWLEDGE_BASE = """
# 猕猴桃种植基础知识

## 猕猴桃品种选择
常见品种：海沃德(Hayward)、徐香、华优、红阳、翠香等。
- 海沃德：晚熟，果大，耐储运，全球主栽品种
- 红阳：早熟，果肉红色，口感甜，不耐储
- 翠香：中早熟，香气浓郁，品质优良

## 猕猴桃生长周期
1. 休眠期：12月-次年2月，需低温积累需冷量
2. 伤流期：2月下旬-3月上旬，树液开始流动
3. 萌芽期：3月中下旬，芽膨大绽开
4. 展叶期：4月上中旬，叶片展开
5. 开花期：5月上中旬，花期7-10天
6. 果实膨大期：5月下旬-8月
7. 果实成熟期：8月下旬-10月

## 土壤要求
- 土层深厚，疏松肥沃
- 排水良好，保水保肥
- pH 5.5-6.5，微酸性
- 有机质含量>1.5%

## 施肥管理
- 萌芽肥(2-3月)：以氮肥为主
- 花前肥(4-5月)：氮磷钾配合
- 果实膨大肥(6-8月)：以钾肥为主
- 采后肥(9-10月)：有机肥+复合肥

## 水分管理
- 全年需水关键期：萌芽期、开花期、果实膨大期
- 灌溉方式：滴灌、微喷、渗灌
- 土壤相对含水量保持在60-80%

## 修剪技术
- 冬季修剪：12月至次年2月，短截、疏枝
- 夏季修剪：5-8月，抹芽、摘心、疏枝
- 架式：T型架、大棚架、篱架

## 病虫害防治
常见病害：褐斑病、炭疽病、根腐病、花叶病、软腐病
常见虫害：叶蝉、介壳虫、红蜘蛛、蚜虫、金龟子
防治原则：预防为主，综合防治

## 采收与储运
- 采收标准：可溶性固形物>6.5%，硬度>8kg/cm²
- 采收方法：分批采收，轻采轻放
- 储存温度：0°C，湿度90-95%
- 储存期：常温7-14天，冷藏3-6个月
"""


class RAGService:
    def __init__(self):
        self._vector_store = None
        self._initialized = False

    async def initialize(self):
        if not self._initialized:
            try:
                embeddings = OllamaEmbeddings(
                    model="nomic-embed-text",
                    base_url=settings.OLLAMA_BASE_URL,
                )
                self._vector_store = Chroma(
                    persist_directory="./chroma_db",
                    embedding_function=embeddings,
                )
                self._splitter = RecursiveCharacterTextSplitter(
                    chunk_size=500,
                    chunk_overlap=50,
                )
                await self._load_knowledge_base()
                self._initialized = True
                logger.info("RAG Service 初始化完成")
            except Exception as e:
                logger.warning(f"RAG Service 初始化失败，使用模拟模式: {e}")
                self._initialized = False

    async def _load_knowledge_base(self):
        if not self._vector_store:
            return

        try:
            docs = self._splitter.split_text(KIWIFRUIT_KNOWLEDGE_BASE)
            if docs:
                self._vector_store.add_texts(docs)
                logger.info(f"加载知识库: {len(docs)} 个文档块")
        except Exception as e:
            logger.warning(f"知识库加载失败: {e}")

    async def search(self, query: str, top_k: int = 3) -> list[str]:
        if not self._initialized or not self._vector_store:
            logger.info(f"使用模拟 RAG 搜索结果 for: {query[:50]}...")
            return [f"知识库检索结果（模拟）: {query}"]

        try:
            results = self._vector_store.similarity_search(query, k=top_k)
            return [doc.page_content for doc in results]
        except Exception as e:
            logger.error(f"RAG 搜索失败: {e}")
            return []

    async def add_document(self, content: str, metadata: Optional[dict] = None):
        if not self._vector_store:
            return

        try:
            docs = self._splitter.split_text(content)
            self._vector_store.add_texts(docs, metadatas=[metadata or {}] * len(docs))
            logger.info(f"添加文档到知识库: {len(docs)} 个文档块")
        except Exception as e:
            logger.error(f"添加文档失败: {e}")


# 全局 RAG 服务实例
rag_service = RAGService()
