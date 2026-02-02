from __future__ import annotations

import os
from typing import List

from app.superpower.skills_context import build_context
from app.superpower.skills_loader import SkillsLoader
from app.superpower.skills_retriever import SkillsRetriever
from app.superpower.chroma_store import ChromaStore
from app.superpower.embeddings import EmbeddingService
from app.superpower.hybrid_retriever import HybridRetriever


class ContextServer:
    def __init__(self):
        self.documents = []
        self.skills_loader = SkillsLoader()
        self.skills_loader.reload()
        self.skills_retriever = SkillsRetriever(self.skills_loader)
        self.hybrid_retriever: HybridRetriever | None = None
        if os.environ.get("ENABLE_VECTOR_SEARCH") == "1":
            self.hybrid_retriever = HybridRetriever(
                self.skills_retriever,
                ChromaStore(collection_name="skills"),
                EmbeddingService(),
            )
            self.hybrid_retriever.index_skills(self.skills_loader.list_skills())

    def index_document(self, doc_id: str, content: str):
        """Index a document for retrieval."""
        self.documents.append({"id": doc_id, "content": content})

    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        """Retrieve relevant context for a query."""
        skills = self.skills_retriever.retrieve(query, top_k=top_k)
        return [item[0].content for item in skills]

    def retrieve_skills(self, query: str, tags: list[str] | None = None, top_k: int = 5):
        if self.hybrid_retriever and not tags:
            return self.hybrid_retriever.retrieve(query, top_k=top_k)
        return self.skills_retriever.retrieve(query, tags=tags, top_k=top_k)

    def build_skills_context(
        self,
        query: str,
        tags: list[str] | None = None,
        top_k: int = 5,
        max_tokens: int = 2000,
        model_name: str | None = None,
    ) -> tuple[str, list[str]]:
        skills_with_scores = self.retrieve_skills(query, tags=tags, top_k=top_k)
        context = build_context(skills_with_scores, max_tokens=max_tokens, model_name=model_name)
        skill_names = [skill.name for skill, _ in skills_with_scores]
        return context, skill_names


context_server = ContextServer()
