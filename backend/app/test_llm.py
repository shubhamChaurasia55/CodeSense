from app.services.llm import stream_answer


prompt = """
You are CodeSense, an AI code assistant.

Explain this Python function in simple terms:

def calculate_average(numbers):
    return sum(numbers) / len(numbers)
"""

print("\nAI Answer:\n")

answer = stream_answer(prompt)

print("\n")