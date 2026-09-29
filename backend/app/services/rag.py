from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.parser import parse_python_code


class RAGEngine:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = None
        self.indexed = False

    def index_code(self, code: str):

        chunks = parse_python_code(code)

        if not chunks:
            return {
                "chunk_count": 0,
                "message": "No code chunks found"
            }

        texts = [
            chunk["code"]
            for chunk in chunks
        ]

        embeddings = self.embedding_service.generate_embeddings(
            texts
        )

        dimension = len(embeddings[0])

        self.vector_store = VectorStore(dimension)

        self.vector_store.add(
            embeddings,
            chunks
        )

        self.indexed = True

        return {
            "chunk_count": len(chunks),
            "message": "Code indexed successfully"
        }

    def search(self, query: str, top_k: int = 3):

        if not self.indexed:
            raise ValueError(
                "No code has been indexed yet"
            )

        query_embedding = (
            self.embedding_service.generate_embedding(query)
        )

        results = self.vector_store.search(
            query_embedding,
            top_k=top_k
        )

        return results