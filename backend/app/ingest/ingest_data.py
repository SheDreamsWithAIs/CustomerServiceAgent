"""
LangChain Version: v1.0+
Documentation Reference:
  - https://docs.langchain.com/oss/python/langchain/knowledge-base
  - https://docs.langchain.com/oss/python/langchain/retrieval
Last Verified: 2025-10-30

Purpose: Load documents, split text, embed chunks, and persist to ChromaDB.

CLI usage:
  python -m app.ingest.ingest_data --source <path-to-docs>
  # Default source is repo_root/AI_docs
"""

import argparse
import os
from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


def _repo_root() -> Path:
    # backend/app/ingest/ingest_data.py → project root is parents[3]
    return Path(__file__).resolve().parents[3]


def _default_source_dir() -> Path:
    return _repo_root() / "AI_docs"


def _persist_dir() -> Path:
    raw = os.getenv("CHROMA_PERSIST_DIRECTORY", ".chroma")
    p = Path(raw)
    if not p.is_absolute():
        p = _repo_root() / raw
    return p


def _collection_name() -> str:
    return os.getenv("CHROMA_COLLECTION", "office_lifeline_kb")


def load_documents(source_dir: Path) -> List:
    docs = []
    for path in source_dir.rglob("*"):
        if not path.is_file():
            continue
        ext = path.suffix.lower()
        try:
            if ext == ".pdf":
                loader = PyPDFLoader(str(path))
                docs.extend(loader.load())
            elif ext in {".md", ".txt"}:
                loader = TextLoader(str(path), encoding="utf-8")
                docs.extend(loader.load())
        except Exception:
            # Skip unreadable files; detailed logging can be added later
            continue
    return docs


def split_documents(documents: List) -> List:
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(documents)


def build_vectorstore(chunks: List) -> Chroma:
    embeddings = OpenAIEmbeddings(model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"))
    vs = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(_persist_dir()),
        collection_name=_collection_name(),
    )
    vs.persist()
    return vs


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest documents into ChromaDB")
    parser.add_argument("--source", type=str, default=str(_default_source_dir()), help="Directory containing documents")
    args = parser.parse_args()

    source_dir = Path(args.source)
    if not source_dir.exists():
        raise SystemExit(f"Source directory not found: {source_dir}")

    documents = load_documents(source_dir)
    if not documents:
        print("No documents loaded. Nothing to ingest.")
        return

    chunks = split_documents(documents)
    print(f"Loaded {len(documents)} docs → {len(chunks)} chunks. Building vectorstore...")
    vs = build_vectorstore(chunks)
    count = vs._collection.count() if hasattr(vs, "_collection") else "unknown"
    print(f"Chroma persisted at: {str(_persist_dir())}")
    print(f"Collection: {_collection_name()} | Records: {count}")


if __name__ == "__main__":
    main()


