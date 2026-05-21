from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class LoanSchemeCreateRequest(BaseModel):
    scheme_name: str = Field(..., min_length=2, max_length=150)
    description: Optional[str] = None

    min_amount: float = Field(..., gt=0)
    max_amount: float = Field(..., gt=0)

    interest_rate: float = Field(..., ge=0)
    tenure_months: int = Field(..., gt=0)

    min_score_required: float = Field(default=0, ge=0)
    eligible_risk_level: Literal["Any", "Low", "Medium", "High"] = "Any"

    is_active: bool = True


class LoanSchemeUpdateRequest(BaseModel):
    scheme_name: Optional[str] = None
    description: Optional[str] = None

    min_amount: Optional[float] = Field(default=None, gt=0)
    max_amount: Optional[float] = Field(default=None, gt=0)

    interest_rate: Optional[float] = Field(default=None, ge=0)
    tenure_months: Optional[int] = Field(default=None, gt=0)

    min_score_required: Optional[float] = Field(default=None, ge=0)
    eligible_risk_level: Optional[Literal["Any", "Low", "Medium", "High"]] = None

    is_active: Optional[bool] = None


class LoanSchemeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    lender_id: int

    scheme_name: str
    description: Optional[str] = None

    min_amount: float
    max_amount: float

    interest_rate: float
    tenure_months: int

    min_score_required: float
    eligible_risk_level: str
    is_active: bool

    created_at: datetime
    updated_at: datetime

