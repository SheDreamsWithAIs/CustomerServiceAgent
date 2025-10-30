"""
LangChain Version: v1.0+
Documentation Reference:
  - https://docs.langchain.com/oss/python/langchain/retrieval
Last Verified: 2025-10-30

Helpers for loading a persisted Chroma vector store and running searches.
"""

import os
from pathlib import Path
from typing import List

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _persist_dir() -> Path:
    raw = os.getenv("CHROMA_PERSIST_DIRECTORY", ".chroma")
    p = Path(raw)
    if not p.is_absolute():
        p = _repo_root() / raw
    return p


def _collection_name() -> str:
    return os.getenv("CHROMA_COLLECTION", "office_lifeline_kb")


def get_vectorstore() -> Chroma:
    embeddings = OpenAIEmbeddings(model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"))
    return Chroma(
        embedding_function=embeddings,
        persist_directory=str(_persist_dir()),
        collection_name=_collection_name(),
    )


def similarity_search(query: str, k: int = 3) -> List[Document]:
    vs = get_vectorstore()
    return vs.similarity_search(query, k=k)


def mmr_search(query: str, k: int = 3, fetch_k: int = 20, lambda_mult: float = 0.5) -> List[Document]:
    vs = get_vectorstore()
    return vs.max_marginal_relevance_search(query, k=k, fetch_k=fetch_k, lambda_mult=lambda_mult)


