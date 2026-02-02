from __future__ import annotations

from .chroma_store import ChromaStore
from .embeddings import EmbeddingService
from .models import Skill
from .skills_retriever import SkillsRetriever


class HybridRetriever:
    def __init__(self, skills_retriever: SkillsRetriever, vector_store: ChromaStore, embedder: EmbeddingService):
        self.skills_retriever = skills_retriever
        self.vector_store = vector_store
        self.embedder = embedder
        self._indexed = False

    def index_skills(self, skills: list[Skill]) -> None:
        if self._indexed or not skills:
            return
        ids: list[str] = []
        documents: list[str] = []
        embeddings: list[list[float]] = []
        for skill in skills:
            ids.append(f"{skill.name}:{skill.file_path}")
            documents.append(skill.content)
            embeddings.append(self.embedder.embed_text(skill.content).vector)
        if ids:
            self.vector_store.add_documents(ids=ids, documents=documents, embeddings=embeddings)
            self._indexed = True

    def retrieve(self, query: str, top_k: int = 5) -> list[tuple[Skill, float]]:
        skills_results = self.skills_retriever.retrieve(query, top_k=top_k)
        self.index_skills([skill for skill, _score in skills_results])
        embedding = self.embedder.embed_text(query)
        vector_results = self.vector_store.query(embedding.vector, top_k=top_k)
        combined = {skill.name: (skill, score) for skill, score in skills_results}
        for doc, distance in zip(vector_results.documents, vector_results.distances):
            for skill, _score in skills_results:
                if doc.strip() and doc in skill.content:
                    combined[skill.name] = (skill, max(_score, 1 / (1 + distance)))
        return sorted(combined.values(), key=lambda item: item[1], reverse=True)
