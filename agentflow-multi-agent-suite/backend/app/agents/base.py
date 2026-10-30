from typing import Dict, Any, Optional
from app.llm.openrouter import openrouter
from app.models.agent_step import AgentStep
from app.db.session import async_session_maker


class BaseAgent:
    def __init__(self, internal_id: str, display_name: str = None):
        self.internal_id = internal_id
        self.display_name = display_name or internal_id

    async def log_step(self, run_id: str, step_type: str, content: str, data: Dict[str, Any] = None, model_used: str = None):
        try:
            async with async_session_maker() as session:
                step = AgentStep(
                    run_id=run_id,
                    agent_internal_id=self.internal_id,
                    agent_display_name=self.display_name,
                    step_type=step_type,
                    content=content,
                    data=data,
                    model_used=model_used,
                )
                session.add(step)
                await session.commit()
        except Exception:
            pass

    async def think(self, run_id: str, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        messages = [
            {"role": "system", "content": f"You are {self.display_name}, an agent in AgentFlow swarm. Be concise, practical, action-oriented."},
            {"role": "user", "content": prompt},
        ]
        res = await openrouter.chat_completion(messages, agent_id=self.internal_id)
        if res.get("ok"):
            try:
                content = res["data"]["choices"][0]["message"]["content"]
                await self.log_step(run_id, "thought", content, {"prompt": prompt[:200]}, res.get("model"))
                return {"ok": True, "content": content, "model": res.get("model")}
            except Exception as e:
                return {"ok": False, "error": str(e)}
        await self.log_step(run_id, "thought", f"Thinking... (model routing in progress)")
        return res
