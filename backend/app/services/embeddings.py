from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)

    def generate_embedding(self, text: str):
        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )

        return embedding

    def generate_embeddings(self, texts: list[str]):
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True
        )

        return embeddings
