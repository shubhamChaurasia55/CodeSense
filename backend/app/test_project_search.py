from app.services.dependencies import rag_engine


query = "Which files contain functions that process numbers?"

results = rag_engine.search(
    query,
    top_k=5,
    score_threshold=0.0
)

print("\nQuery:", query)
print("\nResults:")

for result in results:
    document = result["document"]

    print("\n--------------------")
    print("Score:", result["score"])
    print("Filename:", document.get("filename"))
    print("Name:", document.get("name"))
    print("Type:", document.get("type"))
    print("Class:", document.get("class_name"))
    print("Code:")
    print(document.get("code"))