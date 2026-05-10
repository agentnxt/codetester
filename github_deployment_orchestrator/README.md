# GitHub Deployment Orchestrator Assistant

A LangGraph-based chat assistant that scans a GitHub repository, summarizes current state, asks clarification questions, creates deployment project plans, tracks tasks, and coordinates with a separate coding agent over A2A.

## Scope

This assistant is a project/deployment orchestrator. It does **not** write implementation code. Coding work is delegated to a coding agent through A2A.

## MVP features

- FastAPI chat backend
- LangGraph workflow
- GitHub repo scan tools
- Deployment readiness analysis
- Clarification highlighting
- Project plan generation
- GitHub Projects placeholder adapter
- GitHub operations tools for PR/test/deploy workflows
- A2A coding-agent client stub
- Next.js chat UI scaffold

## Quick start

```bash
cd backend
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

## Required environment

```bash
OPENAI_API_KEY=
GITHUB_TOKEN=
GITHUB_OWNER=
GITHUB_REPO=
A2A_CODING_AGENT_URL=
PROJECT_TOOL=github_projects
```

## Safety

Merge, deploy, production config edits, dependency upgrades, and branch deletion should require explicit human approval.
