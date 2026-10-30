from .base import BaseAgent


class ScoutAgent(BaseAgent):
    def __init__(self):
        super().__init__(internal_id="scout", display_name="Scout")

    async def recon(self, run_id: str, url: str):
        prompt = f"Recon target: {url}. Identify forms, auth needs, CAPTCHA indicators. Return concise findings."
        return await self.think(run_id, prompt)

scout = ScoutAgent()
