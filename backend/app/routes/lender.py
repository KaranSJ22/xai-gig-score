from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..deps import get_db, require_lender
from ..models.loan_application import LoanApplication
from ..models.prediction import Prediction
from ..models.user import User
from ..schemas.loan_application import (
    LoanApplicationDecisionRequest,
    LoanApplicationDetailResponse,
    LoanApplicationResponse,
)


router = APIRouter(prefix="/lender", tags=["lender"])


@router.get("/dashboard")
def get_lender_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lender),
):
    applications = (
        db.query(LoanApplication)
        .filter(LoanApplication.lender_id == current_user.id)
        .all()
    )

    total_applications = len(applications)
    pending_applications = sum(1 for app in applications if app.status == "Pending")
    under_review_applications = sum(1 for app in applications if app.status == "Under Review")
    approved_applications = sum(1 for app in applications if app.status == "Approved")
    rejected_applications = sum(1 for app in applications if app.status == "Rejected")

    scores = [
        app.prediction.credit_score
        for app in applications
        if app.prediction is not None
    ]

    average_gigscore = round(sum(scores) / len(scores), 2) if scores else 0.0

    high_risk_applications = sum(
        1
        for app in applications
        if app.prediction is not None and app.prediction.risk_level == "High"
    )

    recent_applications = sorted(
        applications,
        key=lambda app: app.created_at,
        reverse=True,
    )[:5]

    return {
        "total_applications": total_applications,
        "pending_applications": pending_applications,
        "under_review_applications": under_review_applications,
        "approved_applications": approved_applications,
        "rejected_applications": rejected_applications,
        "average_gigscore": average_gigscore,
        "high_risk_applications": high_risk_applications,
        "recent_applications": [
            {
                "id": app.id,
                "borrower_name": app.borrower.name if app.borrower else None,
                "scheme_name": app.scheme.scheme_name if app.scheme else None,
                "requested_amount": app.requested_amount,
                "status": app.status,
                "credit_score": app.prediction.credit_score if app.prediction else None,
                "risk_level": app.prediction.risk_level if app.prediction else None,
                "created_at": app.created_at,
            }
            for app in recent_applications
        ],
    }


@router.get("/applications", response_model=list[LoanApplicationResponse])
def list_lender_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lender),
) -> list[LoanApplicationResponse]:
    applications = (
        db.query(LoanApplication)
        .filter(LoanApplication.lender_id == current_user.id)
        .order_by(LoanApplication.created_at.desc())
        .all()
    )

    return applications


@router.get("/applications/{application_id}", response_model=LoanApplicationDetailResponse)
def get_lender_application_detail(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lender),
) -> LoanApplicationDetailResponse:
    application = (
        db.query(LoanApplication)
        .filter(
            LoanApplication.id == application_id,
            LoanApplication.lender_id == current_user.id,
        )
        .first()
    )

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan application not found",
        )

    borrower = application.borrower
    prediction = application.prediction
    scheme = application.scheme

    pan_verified = (
        borrower.pan_details.is_verified
        if borrower and borrower.pan_details
        else False
    )

    return {
        "id": application.id,
        "borrower_id": application.borrower_id,
        "borrower_name": borrower.name if borrower else "",
        "borrower_email": borrower.email if borrower else "",
        "pan_verified": pan_verified,
        "lender_id": application.lender_id,
        "lender_name": application.lender.name if application.lender else None,
        "scheme_id": application.scheme_id,
        "scheme_name": scheme.scheme_name if scheme else None,
        "requested_amount": application.requested_amount,
        "purpose": application.purpose,
        "status": application.status,
        "decision_reason": application.decision_reason,
        "credit_score": prediction.credit_score if prediction else None,
        "default_probability": prediction.default_probability if prediction else None,
        "risk_level": prediction.risk_level if prediction else None,
        "risk_increasing_factors": prediction.risk_increasing_factors if prediction else None,
        "risk_reducing_factors": prediction.risk_reducing_factors if prediction else None,
        "shap_values": prediction.shap_values if prediction else None,
        "confidence_score": prediction.confidence_score if prediction else None,
        "reviewed_at": application.reviewed_at,
        "created_at": application.created_at,
        "updated_at": application.updated_at,
    }


@router.patch("/applications/{application_id}/decision", response_model=LoanApplicationResponse)
def update_application_decision(
    application_id: int,
    payload: LoanApplicationDecisionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lender),
) -> LoanApplicationResponse:
    application = (
        db.query(LoanApplication)
        .filter(
            LoanApplication.id == application_id,
            LoanApplication.lender_id == current_user.id,
        )
        .first()
    )

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan application not found",
        )

    application.status = payload.status
    application.decision_reason = payload.decision_reason
    application.reviewed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(application)

    return application