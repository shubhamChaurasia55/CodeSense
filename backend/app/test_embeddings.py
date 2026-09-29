from services.embeddings import EmbeddingService


service = EmbeddingService()

texts = [
    "calculate average of numbers",
    "find the mean of a list",
    "JWT authentication middleware"
]

embeddings = service.generate_embeddings(texts)

print("Number of embeddings:", len(embeddings))
print("Embedding dimension:", len(embeddings[0]))
print("First embedding:")
print(embeddings[0])