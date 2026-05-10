# from datetime import datetime
# from pydantic import BaseModel


# class PlatformConnectRequest(BaseModel):
#     platform_name: str


# class PlatformResponse(BaseModel):
#     id: int
#     user_id: int
#     platform_name: str

#     age: float
#     platform_tenure: float
#     avg_active_days: float
#     avg_hours: float
#     task_completion_rate: float
#     avg_rating: float
#     activity_stability: float
#     wallet_txn_freq: float
#     inward_txn_freq: float
#     avg_income: float
#     income_volatility: float
#     income_growth: float
#     savings_ratio: float
#     avg_balance: float
#     has_insurance: bool
#     emergency_buffer: bool
#     loan_utilization: float
#     fixed_emi_burden_ratio: float
#     credit_inquiries: float
#     delay_score: float
#     recent_payment_delays_90: float
#     utility_delay_score: float
#     recent_missed_rent_3m: float
#     rent_consistency_ratio: float

#     created_at: datetime

#     class Config:
#         from_attributes = True



from datetime import datetime

from pydantic import BaseModel, Field


class PlatformConnectRequest(BaseModel):
    platform_name: str = Field(..., min_length=2, max_length=50)


class PlatformResponse(BaseModel):
    id: int
    user_id: int
    platform_name: str

    # Basic borrower / platform context
    age: float
    platform_tenure: float
    platform_count: float

    # Work activity signals
    avg_active_days: float
    avg_hours: float
    task_completion_rate: float
    avg_rating: float
    activity_stability: float

    # Income and cash-flow signals
    wallet_txn_freq: float
    inward_txn_freq: float
    avg_income: float
    income_volatility: float
    income_growth: float
    income_consistency_score: float
    monthly_income_trend: float

    # Financial discipline / resilience signals
    savings_ratio: float
    avg_balance: float
    has_insurance: bool
    emergency_buffer: bool

    # Non-credit payment behavior signals
    utility_delay_score: float
    recent_missed_rent_3m: float
    rent_consistency_ratio: float
    non_credit_payment_delay_score: float

    # Data quality signal
    data_completeness_score: float

    created_at: datetime

    class Config:
        from_attributes = True