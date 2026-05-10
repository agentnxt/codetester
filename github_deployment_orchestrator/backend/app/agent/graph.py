from __future__ import annotations

import json
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

from app.agent.state import OrchestratorState
from app.config import settings
from app.tools.github_tools import GitHubTools
from app.services.project_tracker import ProjectTracker

SYSTEM = """You are a GitHub Deployment Orchestrator Assistant.
You are NOT a coding agent.
Your job is repo analysis, deployment planning, clarification, project tracking, and controlled GitHub operations.
When scope is unclear, identify it as clarification_needed.
Highlight assumptions, risks, and blockers separately.
Never claim a merge or deployment happened unless a tool result confirms it.
"""


def _llm():
    return ChatOpenAI(model=settings.model_name, temperature=0.2)


def intake(state: OrchestratorState) -> OrchestratorState:
    return state


def scan_repo(state: OrchestratorState) -> OrchestratorState:
    gh = GitHubTools()
    state["repo_state"] = gh.scan_repo(state.get("repo"))
    return state


def analyze(state: OrchestratorState) -> OrchestratorState:
    prompt = f"Analyze repository and generate deployment readiness. Repo: {json.dumps(state.get('repo_state', {}))[:12000]}"
    msg = _llm().invoke(prompt)
    state["analysis"] = {
        "current_state": msg.content,
        "deployment_readiness": "draft",
        "suggested_next_states": ["review ci/cd", "validate secrets", "create release checklist"],
        "highlights": [],
    }
    return state


def plan_deployment(state: OrchestratorState) -> OrchestratorState:
    state["plan"] = {
        "summary": "Initial deployment readiness plan",
        "milestones": ["repo scan", "ci validation", "staging deploy", "production release"],
        "tasks": [],
        "test_plan": ["run integration tests"],
        "release_plan": ["deploy to staging then production"],
        "rollback_plan": ["rollback previous stable image"],
    }
    return state


async def sync_project(state: OrchestratorState) -> OrchestratorState:
    tracker = ProjectTracker()
    state["project_sync"] = await tracker.sync_plan(state.get("plan", {}), state.get("preferences", {}))
    return state


def respond(state: OrchestratorState) -> OrchestratorState:
    state["answer"] = "Deployment analysis completed"
    return state


def build_graph():
    graph = StateGraph(OrchestratorState)
    graph.add_node("intake", intake)
    graph.add_node("scan_repo", scan_repo)
    graph.add_node("analyze", analyze)
    graph.add_node("plan_deployment", plan_deployment)
    graph.add_node("sync_project", sync_project)
    graph.add_node("respond", respond)

    graph.set_entry_point("intake")
    graph.add_edge("intake", "scan_repo")
    graph.add_edge("scan_repo", "analyze")
    graph.add_edge("analyze", "plan_deployment")
    graph.add_edge("plan_deployment", "sync_project")
    graph.add_edge("sync_project", "respond")
    graph.add_edge("respond", END)
    return graph.compile()
