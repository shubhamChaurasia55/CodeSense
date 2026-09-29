import os

from dotenv import load_dotenv
from google import genai

from app.services.llm_service import LLMService


load_dotenv()


class GeminiService(LLMService):

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set")

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.8-flash"

    def generate(self, prompt: str) -> str:

        response = self.client.interactions.create(
            model=self.model,
            input=prompt,
            generation_config={
                "thinking_level": "low"
            }
        )

        return response.output_text