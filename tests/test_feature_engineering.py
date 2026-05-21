from __future__ import annotations

import math

import pytest

from app.services.feature_engineering import FEATURE_COLUMNS, build_features


def test_build_features_empty_platforms_raises():
    """Raise a clear error when no platform data exists."""
    with pytest.raises(ValueError, match="No platform data"):
        build_features([])


def test_build_features_contains_all_columns(sample_platforms):
    """Ensure feature engineering outputs the full feature set."""
    features = build_features(sample_platforms)

    assert set(features.keys()) == set(FEATURE_COLUMNS)


def test_build_features_handles_zero_values():
    """Avoid NaN/inf when inputs are all zeros."""
    platforms = [
        type(
            "Stub",
            (),
            {
                "active_days_30d": 0.0,
                "online_hours_30d": 0.0,
                "avg_hours_per_active_day": 0.0,
                "acceptance_rate": 0.0,
                "cancellation_rate": 0.0,
                "peak_hour_share": 0.0,
                "avg_rating": 1.0,
                "rating_count": 0,
                "rating_std": 0.0,
                "complaints_30d": 0,
                "gross_earnings_30d": 0.0,
                "net_payout_30d": 0.0,
                "weekly_earnings_std": 0.0,
                "incentive_share": 0.0,
                "login_days_30d": 0,
                "avg_session_length": 0.0,
                "inactivity_gap_days_max": 0,
                "kyc_verified": False,
                "account_suspensions_12m": 0,
                "policy_violations_12m": 0,
                "fraud_flag": False,
                "activity_stability": 0.0,
                "earnings_per_hour": 0.0,
                "volatility_ratio": 0.0,
                "reliability_score": 0.0,
                "discipline_score": 0.0,
            },
        )()
    ]

    features = build_features(platforms)

    assert math.isfinite(features["financial_stress_ratio"])
    assert math.isfinite(features["earnings_consistency"])
    assert features["financial_stress_ratio"] == pytest.approx(0.0)
    assert features["earnings_consistency"] == pytest.approx(0.0)
