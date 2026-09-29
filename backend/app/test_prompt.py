from app.services.prompt_builder import build_rag_prompt


question = "Where do we calculate the average?"

results = [
    {
        "score": 0.91,
        "document": {
            "type": "function",
            "name": "calculate_average",
            "start_line": 10,
            "end_line": 11,
            "code": """def calculate_average(numbers):
    return sum(numbers) / len(numbers)"""
        }
    }
]


prompt = build_rag_prompt(question, results)

print(prompt)