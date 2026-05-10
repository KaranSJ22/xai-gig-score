from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel


class LenderProfileResponse(BaseModel):
    id: int
    user_id: int

    institution_name: str
    institution_type: str
    license_number: Optional[str] = None
    official_email_domain: Optional[str] = None

    verification_status: str

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LenderVerificationUpdateRequest(BaseModel):
    verification_status: Literal["pending", "approved", "rejected"]