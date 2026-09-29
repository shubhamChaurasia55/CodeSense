from pydantic import BaseModel


class DebugAIResponse(BaseModel):
    problem: str
    why: str
    fix: str
    explanation: str