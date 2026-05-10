class ProjectTracker:
    async def sync_plan(self, plan: dict, preferences: dict):
        return {
            "tool": preferences.get("tool", "github_projects"),
            "status": "synced",
            "tracked_items": len(plan.get("tasks", [])),
        }
