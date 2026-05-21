from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..deps import get_db, require_borrower
from ..models.loan_application import LoanApplication
from ..models.pan import PanDetails
from ..models.platform import PlatformData
from ..models.prediction import Prediction
from ..models.user import User


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_borrower),
):
    pan_record = (
        db.query(PanDetails)
        .filter(PanDetails.user_id == current_user.id)
        .first()
    )

    platforms = (
        db.query(PlatformData)
        .filter(PlatformData.user_id == current_user.id)
        .order_by(PlatformData.created_at.desc())
        .all()
    )

    latest_prediction = (
        db.query(Prediction)
        .filter(Prediction.user_id == current_user.id)
        .order_by(Prediction.created_at.desc())
        .first()
    )

    prediction_history = (
        db.query(Prediction)
        .filter(Prediction.user_id == current_user.id)
        .order_by(Prediction.created_at.desc())
        .limit(5)
        .all()
    )

    loan_applications = (
        db.query(LoanApplication)
        .filter(LoanApplication.borrower_id == current_user.id)
        .order_by(LoanApplication.created_at.desc())
        .all()
    )

    platform_summary = {
        "connected_count": len(platforms),
        "platform_names": [p.platform_name for p in platforms],
        "avg_income": (
            round(sum(p.gross_earnings_30d for p in platforms) / len(platforms), 2)
            if platforms
            else 0.0
        ),
        "avg_rating": (
            round(sum(p.avg_rating for p in platforms) / len(platforms), 2)
            if platforms
            else 0.0
        ),
        "avg_active_days": (
            round(sum(p.active_days_30d for p in platforms) / len(platforms), 2)
            if platforms
            else 0.0
        ),
        "data_completeness_score": (
            round(sum(p.data_completeness_score for p in platforms) / len(platforms), 3)
            if platforms
            else 0.0
        ),
    }

    return {
        "user": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "role": current_user.role,
        },
        "pan": {
            "submitted": pan_record is not None,
            "is_verified": pan_record.is_verified if pan_record else False,

            # For borrower dashboard this is okay.
            # For lender dashboard, never expose full PAN.
            "pan_number": pan_record.pan_number if pan_record else None,
        },
        "platform_summary": platform_summary,
        "latest_prediction": {
            "id": latest_prediction.id,
            "credit_score": latest_prediction.credit_score,
            "default_probability": latest_prediction.default_probability,
            "risk_level": latest_prediction.risk_level,
            "risk_increasing_factors": latest_prediction.risk_increasing_factors,
            "risk_reducing_factors": latest_prediction.risk_reducing_factors,
            "shap_values": latest_prediction.shap_values,
            "model_name": latest_prediction.model_name,
            "model_version": latest_prediction.model_version,
            "created_at": latest_prediction.created_at,
        } if latest_prediction else None,
        "prediction_history": [
            {
                "id": p.id,
                "credit_score": p.credit_score,
                "default_probability": p.default_probability,
                "risk_level": p.risk_level,
                "created_at": p.created_at,
            }
            for p in prediction_history
        ],
        "loan_applications": [
            {
                "id": application.id,
                "scheme_id": application.scheme_id,
                "scheme_name": application.scheme.scheme_name if application.scheme else None,
                "lender_id": application.lender_id,
                "lender_name": application.lender.name if application.lender else None,
                "requested_amount": application.requested_amount,
                "purpose": application.purpose,
                "status": application.status,
                "decision_reason": application.decision_reason,
                "reviewed_at": application.reviewed_at,
                "created_at": application.created_at,
            }
            for application in loan_applications
        ],
    }