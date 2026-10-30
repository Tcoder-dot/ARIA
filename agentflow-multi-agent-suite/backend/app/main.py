from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.core.config import settings
from app.db.session import init_db
from app.db.session import async_session_maker
from app.services.agents import seed_agents
from app.api.v1 import runs

app = FastAPI(
    title=settings.APP_NAME,
    description="Autonomous multi-agent AI career and form-filling platform with live browser view",
    version="0.1.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

app.include_router(runs.router, prefix="/api/v1/runs", tags=["runs"])


# CORS
if isinstance(settings.BACKEND_CORS_ORIGINS, list):
    origins = []
    for o in settings.BACKEND_CORS_ORIGINS:
        origins.append(str(o))
else:
    origins = [str(settings.BACKEND_CORS_ORIGINS)]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.ENVIRONMENT}


@app.get("/")
async def root():
    return {"message": "AgentFlow Multi-Agent Suite API", "docs": "/docs"}


@app.websocket("/ws/{run_id}")
async def websocket_endpoint(websocket: WebSocket, run_id: str):
    await websocket.accept()
    try:
        await websocket.send_json({"type": "connected", "run_id": run_id, "message": "AgentFlow live stream connected"})
        from app.browser.manager import browser_manager
        import asyncio
        while True:
            frame = await browser_manager.get_frame(run_id, timeout=0.5)
            if frame:
                await websocket.send_json({"type": "frame", "run_id": run_id, "data": frame})
            else:
                await asyncio.sleep(0.01)
    except Exception as e:
        logger.warning(f"WS disconnected: {e}")



@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.APP_NAME} in {settings.ENVIRONMENT} mode")
    try:
        await init_db()
        logger.info("Database initialized")
        async with async_session_maker() as session:
            await seed_agents(session)
        logger.info("Agent definitions seeded (Aria + 6)")
    except Exception as e:
        logger.error(f"Startup init failed: {e}")
    logger.info("Aria • COS + 6 agents ready")



@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.APP_NAME}")
