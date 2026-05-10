from typing import Any
from pydantic import BaseModel


class Highlight(BaseModel):
    type: str
    message: str


class DeploymentPlan(BaseModel):
    summary: str
    milestones: list[str] = []
    tasks: list[dict[str, Any]] = []
    test_plan: list[str] = []
    release_plan: list[str] = []
    rollback_plan: list[str] = []


class ChatRequest(BaseModel):
    repo: str
    message: str
    user_preferences: dict[str, Any] = {}


class ChatResponse(BaseModel):
    answer: str
    highlights: list[Highlight] = []
    plan: DeploymentPlan | None = None
    raw_state: dict[str, Any] = {}
