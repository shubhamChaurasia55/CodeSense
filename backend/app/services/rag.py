from huggingface_hub.inference._generated.types import zero_shot_image_classification
from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.parser import parse_python_code
from app.services.prompt_builder import build_rag_prompt
from app.services.providers.groq import GroqService
from app.services.debug_prompt import build_debug_prompt
from app.services.review_prompt import build_review_prompt
from app.services.code_analyzer import analyze_python_code
from app.models.project import Project

import os

VECTOR_STORE_PATH = "data"

class RAGEngine:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.indexed = False
        self.llm = GroqService()
        self.project = Project(name="default")
        self.vector_store = None

        index_path = os.path.join(
            VECTOR_STORE_PATH,
            "index.faiss"
        )

        documents_path = os.path.join(
            VECTOR_STORE_PATH,
            "documents.json"
        )

        if os.path.exists(index_path) and os.path.exists(documents_path):
            self.vector_store = VectorStore.load(
                VECTOR_STORE_PATH
            )

            self.indexed = True
        else:
            self.indexed = False

    def index_code(self, code: str, filename: str = "unknown.py"):
        chunks = parse_python_code(
            code,
            filename
        )

        self.project.add_file(filename)

        if not chunks:
            return {
                "chunk_count": 0,
                "message": "No code chunks found"
            }

        texts = [
            f"""
        File: {chunk.get("filename")}
        Type: {chunk.get("type")}
        Class: {chunk.get("class_name")}
        Name: {chunk.get("name")}

        Code:
        {chunk.get("code")}
        """
            for chunk in chunks
        ]

        embeddings = self.embedding_service.generate_embeddings(texts)

        # Create the vector store only for the first indexed file.
        if self.vector_store is None:
            dimension = len(embeddings[0])
            self.vector_store = VectorStore(dimension)

        # Add new chunks to the existing index.
        self.vector_store.add(
            embeddings,
            chunks
        )

        self.vector_store.save(
            VECTOR_STORE_PATH
        )

        self.indexed = True

        return {
            "filename": filename,
            "chunk_count": len(chunks),
            "project": self.project.name,
            "indexed_files": len(self.project.files),
            "message": "Code indexed successfully"
        }

    def search(self, query, top_k=3, score_threshold=0.5):
        if not self.indexed:
            raise ValueError("No code has been indexed yet")

        query_embedding = self.embedding_service.generate_embedding(query)

        results = self.vector_store.search(
            query_embedding,
            top_k=top_k,
            score_threshold=score_threshold
        )

        unique_results = []
        seen = set()

        for result in results:
            document = result["document"]

            key = (
                document.get("filename"),
                document.get("type"),
                document.get("name"),
                document.get("class_name"),
                document.get("start_line"),
                document.get("end_line"),
            )

            if key in seen:
                continue

            seen.add(key)
            unique_results.append(result)

        return unique_results

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

    def ask(self, question: str, top_k: int = 5):
        results = self.search(
            question,
            top_k=top_k,
            score_threshold=0.35
        )

        prompt = build_rag_prompt(
            question,
            results
        )

        answer = self.llm.generate(prompt)

        sources = []

        for result in results:
            document = result["document"]

            sources.append({
                "filename": document.get("filename"),
                "name": document.get("name"),
                "type": document.get("type"),
                "class_name": document.get("class_name"),
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
                "filename": document.get("filename"),
                "name": document.get("name"),
                "type": document.get("type"),
                "class_name": document.get("class_name"),
                "start_line": document.get("start_line"),
                "end_line": document.get("end_line"),
                "score": result["score"]
            })

        return {
            "question": question,
            "answer": answer.model_dump(),
            "sources": sources
        }

    def review(self, code: str):
        from app.services.code_analyzer import analyze_python_code

        analysis = analyze_python_code(code)

        prompt = build_review_prompt(
            code,
            analysis
        )

        result = self.llm.review(prompt)

        return {
            "analysis": analysis,
            "review": result.model_dump()
        }

    def grounded_review(self, code: str, question: str):
        analysis = analyze_python_code(code)

        results = self.search(
            question,
            top_k=3
        )

        context = []

        for result in results:
            context.append({
                "score": result["score"],
                "document": result["document"]
            })

        prompt = build_grounded_review_prompt(
            question=question,
            code=code,
            analysis=analysis,
            results=results
        )

        review = self.llm.review(prompt)

        return {
            "question": question,
            "analysis": analysis,
            "retrieved_sources": [
                {
                    "name": result["document"].get("name"),
                    "type": result["document"].get("type"),
                    "start_line": result["document"].get("start_line"),
                    "end_line": result["document"].get("end_line"),
                    "score": result["score"]
                }
                for result in results
            ],
            "review": review.model_dump()
        }

    def reset_project(self):
        self.vector_store = None
        self.indexed = False

        self.project = Project(
            name="default"
        )

        index_path = os.path.join(
            VECTOR_STORE_PATH,
            "index.faiss"
        )

        documents_path = os.path.join(
            VECTOR_STORE_PATH,
            "documents.json"
        )

        if os.path.exists(index_path):
            os.remove(index_path)

        if os.path.exists(documents_path):
            os.remove(documents_path)

        return {
            "message": "Project reset successfully"
        }