from typing import Optional, Dict, Any
from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid


class LogEntry(SQLModel, table=True):
    __tablename__ = "logs"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    run_id: Optional[str] = Field(default=None, index=True)
    level: str = Field(default="info")
    source: str = Field(default="system")
    message: str
    meta: Optional[Dict[str, Any]] = Field(default=None, sa_column_kwargs={"nullable": True})
    created_at: datetime = Field(default_factory=datetime.utcnow)
