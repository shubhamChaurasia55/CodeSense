def build_grounded_review_prompt(
    question: str,
    code: str,
    analysis: list[dict],
    results: list[dict]
) -> str:

    context_parts = []

    for index, result in enumerate(results, start=1):
        document = result["document"]

        context_parts.append(
            f"""
Source {index}
Name: {document.get("name")}
Type: {document.get("type")}
Lines: {document.get("start_line")}-{document.get("end_line")}
Retrieval score: {result["score"]}

Code:
{document.get("code")}
"""
        )

    context = "\n".join(context_parts)

    return f"""
You are CodeSense, an AI code intelligence assistant.

User question:
{question}

Complete source code:
{code}

Static analysis:
{analysis}

Retrieved relevant code:
{context}

Instructions:

1. Use the source code as the primary source of truth.
2. Use static analysis values exactly as provided.
3. Use retrieved code to identify the most relevant functions.
4. Do not invent functions, bugs, metrics, or behavior.
5. Do not claim code was executed.
6. Distinguish actual bugs from optional improvements.
7. If the available information is insufficient, explicitly say so.
8. Keep the response technically accurate and concise.

Provide a structured code review.
"""