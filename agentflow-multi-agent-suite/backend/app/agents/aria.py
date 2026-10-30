from .base import BaseAgent


class AriaAgent(BaseAgent):
    def __init__(self):
        super().__init__(internal_id="aria", display_name="Aria • COS")

    async def oversee(self, run_id: str, state: dict):
        prompt = f"Oversee run {run_id}. Current state: {state}. Decide next action. Be decisive."
        return await self.think(run_id, prompt, state)

aria = AriaAgent()
