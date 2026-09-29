from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.parser import parse_python_code
from app.services.prompt_builder import build_rag_prompt
from app.services.providers.groq import GroqService
from app.services.debug_prompt import build_debug_prompt


class RAGEngine:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = None
        self.indexed = False
        self.llm = GroqService()

    def index_code(self, code: str):
        chunks = parse_python_code(code)

        if not chunks:
            return {
                "chunk_count": 0,
                "message": "No code chunks found"
            }

        texts = [chunk["code"] for chunk in chunks]

        embeddings = self.embedding_service.generate_embeddings(texts)

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

    def search(
        self,
        query: str,
        top_k: int = 3,
        score_threshold: float = 0.5
    ):
        if not self.indexed:
            raise ValueError("No code has been indexed yet")

        query_embedding = (
            self.embedding_service
            .generate_embedding(query)
        )

        return self.vector_store.search(
            query_embedding,
            top_k,
            score_threshold
        )

    def build_prompt(self, question: str, top_k: int = 3):
        results = self.search(question, top_k)

        prompt = build_rag_prompt(
            question,
            results
        )

        return {
            "question": question,
            "results": results,
            "prompt": prompt
        }

    def ask(self, question: str, top_k: int = 3):
        results = self.search(question, top_k)

        prompt = build_rag_prompt(
            question,
            results
        )

        answer = self.llm.generate(prompt)

        sources = []

        for result in results:
            document = result["document"]

            sources.append({
                "name": document.get("name"),
                "type": document.get("type"),
                "start_line": document.get("start_line"),
                "end_line": document.get("end_line"),
                "score": result["score"]
            })

        return {
            "question": question,
            "answer": answer,
            "sources": sources
        }


    def debug(self, question: str, top_k: int = 3):
        results = self.search(question, top_k)

        prompt = build_debug_prompt(
            question,
            results
        )

        answer = self.llm.debug(prompt)

        sources = []

        for result in results:
            document = result["document"]

            sources.append({
                "name": document.get("name"),
                "type": document.get("type"),
                "start_line": document.get("start_line"),
                "end_line": document.get("end_line"),
                "score": result["score"]
            })

        return {
            "question": question,
            "answer": answer.model_dump(),
            "sources": sources
        }