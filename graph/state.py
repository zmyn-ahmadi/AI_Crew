from typing import TypedDict
from pydantic import BaseModel, Field


class DraftState(TypedDict, total=False):
    topic: str
    outline: str
    research: str
    draft: str
    score: int
    feedback: str
    revisions: int
    path: str


class Review(BaseModel):
    feedback: str
    score: int = Field(ge=1, le=10)
