from __future__ import annotations

from app.services.feature_engineering import build_features
from app.services.model_service import predict_default_probability
from app.services.scoring_service import (
    credit_score_to_risk_level,
    probability_to_credit_score,
)


def test_end_to_end_pipeline(sample_platforms):
    """Validate the full scoring pipeline output ranges."""
    features = build_features(sample_platforms)
    probability, _ = predict_default_probability(features)

    credit_score = probability_to_credit_score(probability)
    risk_level = credit_score_to_risk_level(credit_score)

    assert 350.0 <= credit_score <= 850.0
    assert risk_level in {"Low", "Medium", "High"}
