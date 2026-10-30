from typing import Optional, Dict, Any
from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid


class AppSettings(SQLModel, table=True):
    __tablename__ = "app_settings"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    key: str = Field(index=True, unique=True)
    value: Optional[Dict[str, Any]] = Field(default=None, sa_column_kwargs={"nullable": True})
    updated_at: datetime = Field(default_factory=datetime.utcnow)
