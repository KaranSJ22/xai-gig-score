from datetime import datetime

from pydantic import BaseModel, Field


class PlatformConnectRequest(BaseModel):
    platform_name: str = Field(..., min_length=2, max_length=50)


class PlatformResponse(BaseModel):
    id: int
    user_id: int
    platform_name: str

    # Work & Activity Profile
    active_days_30d: float
    online_hours_30d: float
    avg_hours_per_active_day: float
    acceptance_rate: float
    cancellation_rate: float
    peak_hour_share: float

    # Performance Profile
    avg_rating: float
    rating_count: int
    rating_std: float
    complaints_30d: int

    # Earnings Profile
    gross_earnings_30d: float
    net_payout_30d: float
    weekly_earnings_std: float
    incentive_share: float

    # Consistency Profile
    login_days_30d: int
    avg_session_length: float
    inactivity_gap_days_max: int

    # Risk & Compliance Profile
    kyc_verified: bool
    account_suspensions_12m: int
    policy_violations_12m: int
    fraud_flag: bool

    # Derived Features
    activity_stability: float
    earnings_per_hour: float
    volatility_ratio: float
    reliability_score: float
    discipline_score: float

    # Data quality signal
    data_completeness_score: float

    created_at: datetime

    class Config:
        from_attributes = True