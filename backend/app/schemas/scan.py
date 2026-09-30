from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ScanRequest(BaseModel):
    type: str
    target: str


class ScanResponse(BaseModel):
    id: str
    type: str
    target: str
    result: str
    score: float
    details: Optional[dict] = None
    created_at: datetime
    class Config:
        from_attributes = True
