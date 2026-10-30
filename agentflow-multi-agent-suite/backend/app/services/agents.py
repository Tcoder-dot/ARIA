from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.agent_definition import AgentDefinition

AGENT_SEED = [
    {
        "internal_id": "aria",
        "default_name": "Aria • COS",
        "color_hex": "#a78bfa",
        "mascot_key": "aria",
        "role": "Chief of Staff",
        "description": "Oversees everything, delegates, approves, handles handoffs",
        "sort_order": 0,
    },
    {
        "internal_id": "scout",
        "default_name": "Scout",
        "color_hex": "#22d3ee",
        "mascot_key": "scout",
        "role": "Site Recon",
        "description": "Maps page, detects auth/CAPTCHA/platform",
        "sort_order": 1,
    },
    {
        "internal_id": "profiler",
        "default_name": "Profiler",
        "color_hex": "#60a5fa",
        "mascot_key": "profiler",
        "role": "Profile Mapper",
        "description": "Builds field map from resume vault",
        "sort_order": 2,
    },
    {
        "internal_id": "tailor",
        "default_name": "Tailor",
        "color_hex": "#fb923c",
        "mascot_key": "tailor",
        "role": "Content Crafter",
        "description": "Tailors answers per field",
        "sort_order": 3,
    },
    {
        "internal_id": "navigator",
        "default_name": "Navigator",
        "color_hex": "#2dd4bf",
        "mascot_key": "navigator",
        "role": "Flow Handler",
        "description": "Handles multi-step forms/flows",
        "sort_order": 4,
    },
    {
        "internal_id": "verifier",
        "default_name": "Verifier",
        "color_hex": "#a3e635",
        "mascot_key": "verifier",
        "role": "QA & Guardrail",
        "description": "Blocks bad fills, enforces checks",
        "sort_order": 5,
    },
    {
        "internal_id": "executor",
        "default_name": "Executor",
        "color_hex": "#f472b6",
        "mascot_key": "executor",
        "role": "Precise Actor",
        "description": "Executes Aria-approved actions only",
        "sort_order": 6,
    },
]


async def seed_agents(session: AsyncSession):
    for seed in AGENT_SEED:
        result = await session.execute(select(AgentDefinition).where(AgentDefinition.internal_id == seed["internal_id"]))
        existing = result.scalar_one_or_none()
        if not existing:
            agent = AgentDefinition(**seed)
            session.add(agent)
    await session.commit()
