from .base import BaseAgent

class VerifierAgent(BaseAgent):
    def __init__(self):
        super().__init__(internal_id="verifier", display_name="Verifier")
    async def verify(self, run_id: str, state: dict):
        prompt = f"QA check before actions: {state}. Block if risky. Return pass/fail + issues."
        return await self.think(run_id, prompt)

verifier = VerifierAgent()
