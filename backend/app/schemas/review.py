from pydantic import BaseModel


class ReviewIssue(BaseModel):
    severity: str
    title: str
    explanation: str
    suggestion: str


class CodeReviewResponse(BaseModel):
    summary: str
    issues: list[ReviewIssue]
    overall_suggestions: list[str]