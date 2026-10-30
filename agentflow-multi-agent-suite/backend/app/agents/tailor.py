from .base import BaseAgent

class TailorAgent(BaseAgent):
    def __init__(self):
        super().__init__(internal_id="tailor", display_name="Tailor")
    async def craft(self, run_id: str, state: dict):
        prompt = f"Tailor answers for each field: {state}. Keep natural, fit limits."
        return await self.think(run_id, prompt)

tailor = TailorAgent()
