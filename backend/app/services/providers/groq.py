import os

from dotenv import load_dotenv
from groq import Groq

from app.services.llm_service import LLMService
from app.schemas.debug import DebugAIResponse


load_dotenv()


class GroqService(LLMService):

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY is not set")

        self.client = Groq(api_key=api_key)

        self.model = "openai/gpt-oss-20b"

    def generate(self, prompt: str) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are CodeSense, an AI code "
                        "intelligence and debugging assistant."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            reasoning_effort="low"
        )

        return response.choices[0].message.content

    def debug(self, prompt: str) -> DebugAIResponse:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are CodeSense, an AI code "
                        "debugging assistant."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "debug_response",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "problem": {
                                "type": "string"
                            },
                            "why": {
                                "type": "string"
                            },
                            "fix": {
                                "type": "string"
                            },
                            "explanation": {
                                "type": "string"
                            }
                        },
                        "required": [
                            "problem",
                            "why",
                            "fix",
                            "explanation"
                        ],
                        "additionalProperties": False
                    }
                }
            },
            reasoning_effort="low"
        )

        content = response.choices[0].message.content

        return DebugAIResponse.model_validate_json(content)