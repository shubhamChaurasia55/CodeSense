from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStore


embedding_service = EmbeddingService()


documents = [
    {
        "name": "calculate_sum",
        "code": "def calculate_sum(a, b): return a + b"
    },
    {
        "name": "calculate_average",
        "code": "def calculate_average(numbers): return sum(numbers) / len(numbers)"
    },
    {
        "name": "authenticate_user",
        "code": "def authenticate_user(token): return verify_jwt(token)"
    }
]


texts = [
    document["code"]
    for document in documents
]


embeddings = embedding_service.generate_embeddings(texts)


dimension = len(embeddings[0])

vector_store = VectorStore(dimension)

vector_store.add(
    embeddings,
    documents
)


query = "How do we find the mean of a list?"

query_embedding = embedding_service.generate_embedding(query)

results = vector_store.search(
    query_embedding,
    top_k=2
)


for result in results:

    print("\nScore:", result["score"])

    print(
        "Document:",
        result["document"]["name"]
    )

    print(
        "Code:",
        result["document"]["code"]
    )