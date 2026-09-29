from app.services.code_analyzer import analyze_python_code


code = """
def calculate_average(numbers):
    if not numbers:
        return None

    total = 0

    for number in numbers:
        total += number

    return total / len(numbers)
"""


results = analyze_python_code(code)

for result in results:
    print(result)