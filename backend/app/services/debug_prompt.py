def build_debug_prompt(question: str, results: list[dict]) -> str:
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
You are CodeSense, an AI code debugging assistant.

Analyze the provided code and answer the user's debugging question.

User question:
{question}

Relevant code:
{context}

Return your answer using EXACTLY this structure:

Problem:
<describe the problem>

Why:
<explain why the problem happens>

Fix:
<provide corrected code or a concrete fix>

Explanation:
<explain why the fix works>

Rules:
1. Base the answer primarily on the provided code.
2. Do not invent code that is not present in the context.
3. If the context is insufficient, say so.
4. Do not claim that code was executed.
5. Keep the explanation technically accurate and concise.
"""

    return prompt