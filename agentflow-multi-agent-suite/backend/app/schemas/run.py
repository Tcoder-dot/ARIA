from pydantic import BaseModel
from typing import Optional


class RunStartRequest(BaseModel):
    target_url: str
    user_id: Optional[str] = None


class RunControlRequest(BaseModel):
    action: str  # take_control | hand_back | pause | resume
    reason: Optional[str] = None
