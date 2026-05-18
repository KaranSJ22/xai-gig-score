from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PanSubmitRequest(BaseModel):
    pan_number: str = Field(..., min_length=10, max_length=10)


class PanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    pan_number: str
    is_verified: bool
    created_at: datetime

