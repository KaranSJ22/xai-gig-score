from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..deps import get_db, require_borrower
from ..models.loan_application import LoanApplication
from ..models.loan_scheme import LoanScheme
from ..models.prediction import Prediction
from ..models.user import User
from ..schemas.loan_application import (
    LoanApplicationCreateRequest,
    LoanApplicationResponse,
)


router = APIRouter(prefix="/applications", tags=["applications"])


@router.post(
    "/",
    response_model=LoanApplicationResponse,
    status_code=status.HTTP_201_CREATED,
)
def apply_for_loan_scheme(
    payload: LoanApplicationCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_borrower),
) -> LoanApplicationResponse:
    scheme = (
        db.query(LoanScheme)
        .filter(
            LoanScheme.id == payload.scheme_id,
            LoanScheme.is_active == True,
        )
        .first()
    )

    if not scheme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan scheme not found or inactive",
        )

    if payload.requested_amount < scheme.min_amount or payload.requested_amount > scheme.max_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Requested amount must be between {scheme.min_amount} and {scheme.max_amount}",
        )

    latest_prediction = (
        db.query(Prediction)
        .filter(Prediction.user_id == current_user.id)
        .order_by(Prediction.created_at.desc())
        .first()
    )

    if not latest_prediction:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please generate GigScore before applying for a loan",
        )

    if latest_prediction.credit_score < scheme.min_score_required:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your GigScore does not meet the minimum score requirement for this scheme",
        )

    existing_pending_application = (
        db.query(LoanApplication)
        .filter(
            LoanApplication.borrower_id == current_user.id,
            LoanApplication.scheme_id == scheme.id,
            LoanApplication.status.in_(["Pending", "Under Review", "Need More Info"]),
        )
        .first()
    )

    if existing_pending_application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have an active application for this scheme",
        )

    application = LoanApplication(
        borrower_id=current_user.id,
        lender_id=scheme.lender_id,
        scheme_id=scheme.id,
        prediction_id=latest_prediction.id,
        requested_amount=payload.requested_amount,
        purpose=payload.purpose,
        status="Pending",
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


@router.get("/my", response_model=list[LoanApplicationResponse])
def list_my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_borrower),
) -> list[LoanApplicationResponse]:
    applications = (
        db.query(LoanApplication)
        .filter(LoanApplication.borrower_id == current_user.id)
        .order_by(LoanApplication.created_at.desc())
        .all()
    )

    return applications