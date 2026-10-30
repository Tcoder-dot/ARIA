from typing import Optional, Dict, Any
from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid


class BrowserSession(SQLModel, table=True):
    __tablename__ = "browser_sessions"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    run_id: str = Field(index=True)
    playwright_context_id: Optional[str] = None
    current_url: Optional[str] = None
    is_logged_in: bool = False
    has_captcha: bool = False
    user_in_control: bool = False
    state: Optional[Dict[str, Any]] = Field(default=None, sa_column_kwargs={"nullable": True})
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
