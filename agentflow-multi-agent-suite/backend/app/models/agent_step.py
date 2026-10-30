from typing import Optional, Dict, Any
from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid


class AgentStep(SQLModel, table=True):
    __tablename__ = "agent_steps"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    run_id: str = Field(index=True)
    agent_internal_id: str
    agent_display_name: str
    step_type: str  # thought|action|delegation|approval|handoff|warning
    content: str
    data: Optional[Dict[str, Any]] = Field(default=None, sa_column_kwargs={"nullable": True})
    model_used: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
