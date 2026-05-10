from typing import TypedDict, Any


class OrchestratorState(TypedDict, total=False):
    repo: str
    message: str
    preferences: dict[str, Any]
    repo_state: dict[str, Any]
    analysis: dict[str, Any]
    plan: dict[str, Any]
    project_sync: dict[str, Any]
    answer: str
