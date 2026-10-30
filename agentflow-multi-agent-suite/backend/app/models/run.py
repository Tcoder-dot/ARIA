from typing import Optional, Dict, Any
from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid


class Run(SQLModel, table=True):
    __tablename__ = "runs"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: Optional[str] = Field(default=None, index=True)
    target_url: str
    status: str = Field(default="created")  # created|running|paused|waiting_user|completed|failed
    current_agent: Optional[str] = None
    browser_session_id: Optional[str] = None
    post_login_detected: bool = False
    captcha_detected: bool = False
    user_in_control: bool = False
    run_meta: Optional[Dict[str, Any]] = Field(default=None, sa_column_kwargs={"nullable": True})
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
