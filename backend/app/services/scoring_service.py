from typing import Dict

from sqlalchemy.orm import Session

from ..models.platform import PlatformData
from ..models.prediction import Prediction
from ..models.user import User
from .explain_service import explain_prediction
from .feature_engineering import build_features
from .model_service import get_model_metadata, predict_default_probability


def probability_to_credit_score(probability: float) -> float:
    probability = max(0.0, min(1.0, float(probability)))
    # New logic: Range 350 - 850
    return round(850 - (probability * 500), 2)


def credit_score_to_risk_level(score: float) -> str:
    if score >= 750:
        return "Low"
    if score >= 600:
        return "Medium"
    return "High"


def generate_prediction_for_user(db: Session, user: User) -> Dict:
    platforms = (
        db.query(PlatformData)
        .filter(PlatformData.user_id == user.id)
        .all()
    )

    if not platforms:
        raise ValueError("No connected platform data found for this user.")

    features = build_features(platforms)

    default_probability, _ = predict_default_probability(features)
    credit_score = probability_to_credit_score(default_probability)
    risk_level = credit_score_to_risk_level(credit_score)

    risk_increasing_factors, risk_reducing_factors, shap_values = explain_prediction(features)

    model_metadata = get_model_metadata()
    
    # Calculate confidence score based on data density (num platforms)
    confidence_score = min(0.98, 0.88 + (len(platforms) * 0.025))

    prediction = Prediction(
        user_id=user.id,
        credit_score=credit_score,
        default_probability=default_probability,
        risk_level=risk_level,
        risk_increasing_factors=risk_increasing_factors,
        risk_reducing_factors=risk_reducing_factors,
        shap_values=shap_values,
        model_name=model_metadata["model_name"],
        model_version=model_metadata["model_version"],
        confidence_score=confidence_score,
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return {
        "id": prediction.id,
        "user_id": prediction.user_id,
        "credit_score": prediction.credit_score,
        "default_probability": prediction.default_probability,
        "risk_level": prediction.risk_level,
        "risk_increasing_factors": prediction.risk_increasing_factors,
        "risk_reducing_factors": prediction.risk_reducing_factors,
        "shap_values": prediction.shap_values,
        "model_name": prediction.model_name,
        "model_version": prediction.model_version,
        "confidence_score": prediction.confidence_score,
        "created_at": prediction.created_at,
    }