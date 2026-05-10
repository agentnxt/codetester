from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.agent.graph import build_graph
from app.models.schemas import ChatRequest, ChatResponse, DeploymentPlan, Highlight

app = FastAPI(title="GitHub Deployment Orchestrator Assistant")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = build_graph()


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        result = await graph.ainvoke({
            "message": req.message,
            "repo": req.repo,
            "preferences": req.user_preferences,
        })
        return ChatResponse(
            answer=result.get("answer", ""),
            highlights=[Highlight(**h) for h in result.get("highlights", [])],
            plan=DeploymentPlan(**result["plan"]) if result.get("plan") else None,
            raw_state={
                "analysis": result.get("analysis"),
                "project_sync": result.get("project_sync"),
            },
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
