from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid


class AgentDefinition(SQLModel, table=True):
    __tablename__ = "agent_definitions"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    internal_id: str = Field(index=True, unique=True)  # aria, scout, profiler, tailor, navigator, verifier, executor
    default_name: str
    custom_name: Optional[str] = None
    color_hex: str
    mascot_key: str
    role: str
    description: Optional[str] = None
    enabled: bool = True
    sort_order: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
