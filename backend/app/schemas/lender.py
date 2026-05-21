from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict


class LenderProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int

    institution_name: str
    institution_type: str
    license_number: Optional[str] = None
    official_email_domain: Optional[str] = None

    verification_status: str

    created_at: datetime
    updated_at: datetime



class LenderVerificationUpdateRequest(BaseModel):
    verification_status: Literal["pending", "approved", "rejected"]