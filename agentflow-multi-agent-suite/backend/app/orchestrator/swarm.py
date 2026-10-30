import asyncio
from typing import Dict, Any
from loguru import logger

from app.agents.aria import aria
from app.agents.scout import scout
from app.agents.profiler import profiler
from app.agents.tailor import tailor
from app.agents.navigator import navigator
from app.agents.verifier import verifier
from app.agents.executor import executor


class SwarmOrchestrator:
    def __init__(self):
        self.aria = aria
        self.scout = scout
        self.profiler = profiler
        self.tailor = tailor
        self.navigator = navigator
        self.verifier = verifier
        self.executor = executor

    async def start_run(self, run_id: str, target_url: str, state: Dict[str, Any] = None):
        state = state or {}
        await self.aria.log_step(run_id, "delegation", f"Aria initiating run for {target_url}")
        # Start recon
        await self.scout.recon(run_id, target_url)
        # Aria oversees
        await self.aria.oversee(run_id, {"url": target_url, "phase": "recon"})
        return {"ok": True, "run_id": run_id}


swarm = SwarmOrchestrator()
