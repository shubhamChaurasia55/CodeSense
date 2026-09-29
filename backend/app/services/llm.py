import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.8-flash"


def generate_answer(prompt: str) -> str:
    response = client.interactions.create(
        model=MODEL_NAME,
        input=prompt,
        generation_config={
            "thinking_level": "low"
        }
    )

    return response.output_text


def stream_answer(prompt: str):
    stream = client.interactions.create(
        model=MODEL_NAME,
        input=prompt,
        generation_config={
            "thinking_level": "low"
        },
        stream=True
    )

    full_response = ""

    for event in stream:

        if event.event_type == "error":
            raise RuntimeError(
                f"Gemini API error: {event.error.message}"
            )

        if event.event_type == "step.delta":
            if event.delta.type == "text":
                text = event.delta.text
                full_response += text
                print(text, end="", flush=True)

    return full_response