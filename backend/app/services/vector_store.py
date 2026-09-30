import json
import os

import faiss
import numpy as np


class VectorStore:

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.documents = []

    def add(self, embeddings, documents):
        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        self.index.add(embeddings)
        self.documents.extend(documents)

    def search(
        self,
        query_embedding,
        top_k=3,
        score_threshold=0.5
    ):
        query_embedding = np.asarray(
            [query_embedding],
            dtype="float32"
        )

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0]
        ):
            if index == -1:
                continue

            if score < score_threshold:
                continue

            results.append({
                "score": float(score),
                "document": self.documents[index]
            })

        return results

    def save(self, directory: str):
        os.makedirs(
            directory,
            exist_ok=True
        )

        index_path = os.path.join(
            directory,
            "index.faiss"
        )

        documents_path = os.path.join(
            directory,
            "documents.json"
        )

        faiss.write_index(
            self.index,
            index_path
        )

        with open(
            documents_path,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                self.documents,
                file,
                indent=2,
                ensure_ascii=False
            )
    
    def reset(self):
        self.index = faiss.IndexFlatIP(self.dimension)
        self.documents = []

    @classmethod
    def load(cls, directory: str):

        index_path = os.path.join(
            directory,
            "index.faiss"
        )

        documents_path = os.path.join(
            directory,
            "documents.json"
        )

        index = faiss.read_index(
            index_path
        )

        with open(
            documents_path,
            "r",
            encoding="utf-8"
        ) as file:
            documents = json.load(file)

        store = cls(index.d)
        store.index = index
        store.documents = documents

        return store