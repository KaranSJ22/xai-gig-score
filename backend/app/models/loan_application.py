from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class LoanApplication(Base):
    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True, index=True)

    borrower_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    lender_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    scheme_id = Column(
        Integer,
        ForeignKey("loan_schemes.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    prediction_id = Column(
        Integer,
        ForeignKey("predictions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    requested_amount = Column(Float, nullable=False)
    purpose = Column(String(255), nullable=True)

    # Pending / Under Review / Approved / Rejected / Need More Info
    status = Column(String(50), nullable=False, default="Pending")

    decision_reason = Column(Text, nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    borrower = relationship(
        "User",
        foreign_keys=[borrower_id],
        back_populates="borrower_applications",
    )

    lender = relationship(
        "User",
        foreign_keys=[lender_id],
        back_populates="lender_applications",
    )

    scheme = relationship(
        "LoanScheme",
        back_populates="applications",
    )

    prediction = relationship(
        "Prediction",
        back_populates="loan_applications",
    )