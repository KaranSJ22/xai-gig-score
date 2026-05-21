from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class PredictionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int

    credit_score: float
    default_probability: float
    risk_level: str

    risk_increasing_factors: Optional[list[dict[str, Any]]] = None
    risk_reducing_factors: Optional[list[dict[str, Any]]] = None
    shap_values: Optional[dict[str, float]] = None

    model_name: Optional[str] = None
    model_version: Optional[str] = None

    created_at: datetime



class PredictionResultResponse(BaseModel):
    credit_score: float
    default_probability: float
    risk_level: str

    risk_increasing_factors: Optional[list[dict[str, Any]]] = None
    risk_reducing_factors: Optional[list[dict[str, Any]]] = None
    shap_values: Optional[dict[str, float]] = None

    model_name: Optional[str] = None
    model_version: Optional[str] = None