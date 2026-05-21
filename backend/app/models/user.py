from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    # borrower / lender / admin
    role = Column(String(20), nullable=False, default="borrower", index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # -------------------------
    # Borrower relationships
    # -------------------------
    pan_details = relationship(
        "PanDetails",
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )

    platforms = relationship(
        "PlatformData",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    predictions = relationship(
        "Prediction",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    borrower_applications = relationship(
        "LoanApplication",
        foreign_keys="LoanApplication.borrower_id",
        back_populates="borrower",
        cascade="all, delete-orphan",
    )

    # -------------------------
    # Lender relationships
    # -------------------------
    lender_profile = relationship(
        "LenderProfile",
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )

    loan_schemes = relationship(
        "LoanScheme",
        back_populates="lender",
        cascade="all, delete-orphan",
    )


    lender_applications = relationship(
        "LoanApplication",
        foreign_keys="LoanApplication.lender_id",
        back_populates="lender",
    )