from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class PlatformData(Base):
    __tablename__ = "platform_data"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    platform_name = Column(String(50), nullable=False)

    # Work & Activity Profile
    active_days_30d = Column(Float, nullable=False)
    online_hours_30d = Column(Float, nullable=False)
    avg_hours_per_active_day = Column(Float, nullable=False)
    acceptance_rate = Column(Float, nullable=False)
    cancellation_rate = Column(Float, nullable=False)
    peak_hour_share = Column(Float, nullable=False)

    # Performance Profile
    avg_rating = Column(Float, nullable=False)
    rating_count = Column(Integer, nullable=False)
    rating_std = Column(Float, nullable=False)
    complaints_30d = Column(Integer, nullable=False)

    # Earnings Profile
    gross_earnings_30d = Column(Float, nullable=False)
    net_payout_30d = Column(Float, nullable=False)
    weekly_earnings_std = Column(Float, nullable=False)
    incentive_share = Column(Float, nullable=False)

    # Consistency Profile
    login_days_30d = Column(Integer, nullable=False)
    avg_session_length = Column(Float, nullable=False)
    inactivity_gap_days_max = Column(Integer, nullable=False)

    # Risk & Compliance Profile
    kyc_verified = Column(Boolean, nullable=False, default=True)
    account_suspensions_12m = Column(Integer, nullable=False, default=0)
    policy_violations_12m = Column(Integer, nullable=False, default=0)
    fraud_flag = Column(Boolean, nullable=False, default=False)

    # Derived Features
    activity_stability = Column(Float, nullable=False)
    earnings_per_hour = Column(Float, nullable=False)
    volatility_ratio = Column(Float, nullable=False)
    reliability_score = Column(Float, nullable=False)
    discipline_score = Column(Float, nullable=False)

    # Data quality signal
    data_completeness_score = Column(Float, nullable=False, default=1.0)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="platforms")