"""
LangChain Version: v1.0+
Documentation Reference:
  - https://docs.langchain.com/oss/python/langchain/tools
  - https://docs.langchain.com/oss/python/langchain/retrieval
Last Verified: 2025-10-30
"""

from typing import List
import logging

from langchain_core.tools import tool

from app.retrieval.retriever import similarity_search


@tool
def search_documents(query: str, k: int = 3) -> str:
    """Search the knowledge base for relevant passages. Always call this before answering."""
    logger = logging.getLogger("app.tools.search_documents")
    try:
        docs = similarity_search(query, k=k)
    except Exception as exc:
        logger.exception("search_documents tool failed")
        raise
    if not docs:
        return ""
    # Return a compact string; agents will ground answers with this context
    lines: List[str] = []
    for i, d in enumerate(docs, start=1):
        meta = d.metadata or {}
        src = meta.get("source", "unknown")
        lines.append(f"[{i}] source={src} | {d.page_content}")
    return "\n\n".join(lines)


