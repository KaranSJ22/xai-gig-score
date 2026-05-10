from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class LenderProfile(Base):
    __tablename__ = "lender_profiles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    institution_name = Column(String(150), nullable=False)
    institution_type = Column(String(50), nullable=False)
    license_number = Column(String(100), nullable=True)
    official_email_domain = Column(String(100), nullable=True)

    # pending / approved / rejected
    verification_status = Column(String(30), nullable=False, default="pending")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = relationship("User", back_populates="lender_profile")