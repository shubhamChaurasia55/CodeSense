def build_rag_prompt(question: str, results: list[dict]) -> str:
    context_parts = []

    for index, result in enumerate(results, start=1):
        document = result["document"]

        context_parts.append(
            f"""
Source {index}
Type: {document.get("type")}
Name: {document.get("name")}
Lines: {document.get("start_line")}-{document.get("end_line")}

Code:
{document.get("code")}
"""
        )

    context = "\n".join(context_parts)

    prompt = f"""
You are CodeSense, an AI code intelligence and debugging assistant.

Your task is to answer the user's question using the provided code context.

Rules:
1. Use the provided code as the primary source.
2. Do not invent code that is not present in the context.
3. If the context does not contain enough information, clearly say so.
4. Mention the relevant function, class, or source when possible.
5. When referring to code, include the source line numbers.

User question:
{question}

Relevant code context:
{context}

Provide a clear and concise answer.
"""

    return prompt