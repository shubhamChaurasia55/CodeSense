from app.services.providers.groq import GroqService


service = GroqService()

prompt = """
Explain this Python function in simple terms:

def calculate_average(numbers):
    return sum(numbers) / len(numbers)
"""


answer = service.generate(prompt)

print("\nAI Answer:\n")
print(answer)