from .base import BaseAgent

class ExecutorAgent(BaseAgent):
    def __init__(self):
        super().__init__(internal_id="executor", display_name="Executor")
    async def act(self, run_id: str, action: dict):
        prompt = f"Execute ONLY Aria-approved action: {action}. Be precise."
        return await self.think(run_id, prompt)

executor = ExecutorAgent()
