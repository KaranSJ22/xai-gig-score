from datetime import datetime
from typing import Any, Optional, Literal

from pydantic import BaseModel, Field


class LoanApplicationCreateRequest(BaseModel):
    scheme_id: int
    requested_amount: float = Field(..., gt=0)
    purpose: Optional[str] = Field(default=None, max_length=255)


class LoanApplicationDecisionRequest(BaseModel):
    status: Literal["Pending", "Under Review", "Approved", "Rejected", "Need More Info"]
    decision_reason: Optional[str] = Field(default=None, max_length=1000)


class LoanApplicationResponse(BaseModel):
    id: int

    borrower_id: int
    lender_id: int
    scheme_id: Optional[int] = None
    prediction_id: Optional[int] = None

    requested_amount: float
    purpose: Optional[str] = None

    status: str
    decision_reason: Optional[str] = None

    reviewed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LoanApplicationDetailResponse(BaseModel):
    id: int

    borrower_id: int
    borrower_name: str
    borrower_email: str
    pan_verified: bool

    lender_id: int
    lender_name: Optional[str] = None

    scheme_id: Optional[int] = None
    scheme_name: Optional[str] = None

    requested_amount: float
    purpose: Optional[str] = None

    status: str
    decision_reason: Optional[str] = None

    credit_score: Optional[float] = None
    default_probability: Optional[float] = None
    risk_level: Optional[str] = None

    risk_increasing_factors: Optional[list[dict[str, Any]]] = None
    risk_reducing_factors: Optional[list[dict[str, Any]]] = None
    shap_values: Optional[dict[str, float]] = None

    reviewed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True