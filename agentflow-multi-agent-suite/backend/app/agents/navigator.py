from .base import BaseAgent

class NavigatorAgent(BaseAgent):
    def __init__(self):
        super().__init__(internal_id="navigator", display_name="Navigator")
    async def navigate_flow(self, run_id: str, state: dict):
        prompt = f"Handle multi-step flow: {state}. Plan next safe step."
        return await self.think(run_id, prompt)

navigator = NavigatorAgent()
