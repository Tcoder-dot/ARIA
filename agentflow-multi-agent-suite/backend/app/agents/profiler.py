from .base import BaseAgent

class ProfilerAgent(BaseAgent):
    def __init__(self):
        super().__init__(internal_id="profiler", display_name="Profiler")
    async def map(self, run_id: str, state: dict):
        prompt = f"Map resume fields to form: {state}. Build field map."
        return await self.think(run_id, prompt)

profiler = ProfilerAgent()
