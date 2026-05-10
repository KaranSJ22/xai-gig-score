from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class LoanScheme(Base):
    __tablename__ = "loan_schemes"

    id = Column(Integer, primary_key=True, index=True)

    lender_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    scheme_name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)

    min_amount = Column(Float, nullable=False)
    max_amount = Column(Float, nullable=False)

    interest_rate = Column(Float, nullable=False)
    tenure_months = Column(Integer, nullable=False)

    min_score_required = Column(Float, nullable=False, default=0)
    eligible_risk_level = Column(String(50), nullable=False, default="Any")

    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    lender = relationship("User", back_populates="loan_schemes")

    applications = relationship(
        "LoanApplication",
        back_populates="scheme",
    )