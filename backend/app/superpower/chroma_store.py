from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Any, cast


@dataclass
class ChromaResult:
    ids: list[str]
    documents: list[str]
    distances: list[float]


class ChromaStore:
    def __init__(self, collection_name: str = "skills", persist_dir: str | None = None):
        try:
            import chromadb  # type: ignore
        except Exception as exc:
            raise RuntimeError("chromadb package is required for vector search") from exc
        if persist_dir:
            client = chromadb.PersistentClient(path=persist_dir)
        else:
            client = chromadb.Client()
        self.collection = client.get_or_create_collection(collection_name)

    def add_documents(self, ids: list[str], documents: list[str], embeddings: list[list[float]]):
        try:
            embeddings_payload = cast(Any, embeddings)
            self.collection.add(ids=ids, documents=documents, embeddings=embeddings_payload)
            logging.getLogger(__name__).info(
                "Vector documents added",
                extra={"count": len(ids), "collection": getattr(self.collection, "name", None)},
            )
        except Exception as exc:
            logging.getLogger(__name__).error(
                "Vector add failed",
                extra={"count": len(ids), "collection": getattr(self.collection, "name", None)},
                exc_info=exc,
            )
            raise

    def query(self, embedding: list[float], top_k: int = 5) -> ChromaResult:
        try:
            result: Any = self.collection.query(query_embeddings=[embedding], n_results=top_k) or {}
            logging.getLogger(__name__).debug(
                "Vector query completed",
                extra={"count": top_k, "collection": getattr(self.collection, "name", None)},
            )
            ids = result.get("ids") or [[]]
            documents = result.get("documents") or [[]]
            distances = result.get("distances") or [[]]
            return ChromaResult(
                ids=ids[0],
                documents=documents[0],
                distances=distances[0],
            )
        except Exception as exc:
            logging.getLogger(__name__).error(
                "Vector query failed",
                extra={"count": top_k, "collection": getattr(self.collection, "name", None)},
                exc_info=exc,
            )
            raise
