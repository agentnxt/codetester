import httpx
from app.config import settings


class A2AClient:
    async def delegate_task(self, payload: dict):
        if not settings.a2a_coding_agent_url:
            return {"status": "missing_a2a_endpoint"}

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                settings.a2a_coding_agent_url,
                json=payload,
            )
            return response.json()
