from typing import List

class ContextServer:
    def __init__(self):
        self.documents = []  # In Phase 2, this will be ChromaDB connection

    def index_document(self, doc_id: str, content: str):
        """Index a document for retrieval."""
        self.documents.append({"id": doc_id, "content": content})
        print(f"Indexed document: {doc_id}")

    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        """Retrieve relevant context for a query."""
        # Mock retrieval: return all docs for now
        return [doc["content"] for doc in self.documents[:top_k]]

context_server = ContextServer()
