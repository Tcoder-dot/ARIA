from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import get_session
from app.schemas.run import RunStartRequest, RunControlRequest
from app.models.run import Run
from app.models.browser_session import BrowserSession
from app.orchestrator.swarm import swarm
from app.browser.manager import browser_manager
import uuid

router = APIRouter()


@router.post("/start")
async def start_run(req: RunStartRequest, session: AsyncSession = Depends(get_session)):
    run = Run(target_url=req.target_url, user_id=req.user_id, status="running")
    session.add(run)
    await session.commit()
    await session.refresh(run)

    bs = BrowserSession(run_id=run.id)
    session.add(bs)
    await session.commit()
    await session.refresh(bs)

    # Start browser session
    try:
        await browser_manager.create_session(run.id, req.target_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Browser start failed: {e}")

    # Start swarm
    try:
        await swarm.start_run(run.id, req.target_url)
    except Exception as e:
        pass

    return {"ok": True, "run_id": run.id, "browser_session_id": bs.id}


@router.post("/{run_id}/control")
async def control_run(run_id: str, req: RunControlRequest, session: AsyncSession = Depends(get_session)):
    from sqlmodel import select
    from app.models.run import Run

    result = await session.execute(select(Run).where(Run.id == run_id))
    run = result.scalar_one_or_none()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    if req.action == "take_control":
        run.user_in_control = True
        run.status = "waiting_user"
    elif req.action == "hand_back":
        run.user_in_control = False
        run.status = "running"
    elif req.action == "pause":
        run.status = "paused"
    elif req.action == "resume":
        run.status = "running"

    session.add(run)
    await session.commit()
    await session.refresh(run)
    return {"ok": True, "run_id": run_id, "action": req.action, "status": run.status, "user_in_control": run.user_in_control}

