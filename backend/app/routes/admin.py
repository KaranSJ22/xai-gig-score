from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..deps import get_db, require_admin
from ..models.lender import LenderProfile
from ..models.user import User
from ..schemas.lender import (
    LenderProfileResponse,
    LenderVerificationUpdateRequest,
)


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/lenders/pending", response_model=list[LenderProfileResponse])
def list_pending_lenders(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> list[LenderProfileResponse]:
    pending_lenders = (
        db.query(LenderProfile)
        .filter(LenderProfile.verification_status == "pending")
        .order_by(LenderProfile.created_at.desc())
        .all()
    )

    return pending_lenders


@router.get("/lenders", response_model=list[LenderProfileResponse])
def list_all_lenders(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> list[LenderProfileResponse]:
    lenders = (
        db.query(LenderProfile)
        .order_by(LenderProfile.created_at.desc())
        .all()
    )

    return lenders


@router.patch("/lenders/{lender_profile_id}/verification", response_model=LenderProfileResponse)
def update_lender_verification(
    lender_profile_id: int,
    payload: LenderVerificationUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> LenderProfileResponse:
    lender_profile = (
        db.query(LenderProfile)
        .filter(LenderProfile.id == lender_profile_id)
        .first()
    )

    if not lender_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lender profile not found",
        )

    lender_profile.verification_status = payload.verification_status

    db.commit()
    db.refresh(lender_profile)

    return lender_profile