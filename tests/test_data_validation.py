from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.schemas.platform import PlatformConnectRequest
from app.services.mock_data import generate_mock_platform_features


def test_platform_connect_request_requires_min_length():
    """Reject platform names shorter than the minimum length."""
    with pytest.raises(ValidationError):
        PlatformConnectRequest(platform_name="a")


def test_generate_mock_platform_features_rejects_unknown_platform():
    """Reject unsupported platform identifiers."""
    with pytest.raises(ValueError, match="Unsupported platform"):
        generate_mock_platform_features("unknown-app")


def test_generate_mock_platform_features_ranges():
    """Validate generated mock data stays in expected ranges."""
    features = generate_mock_platform_features("uber")

    assert 0.0 <= features["acceptance_rate"] <= 1.0
    assert 0.0 <= features["cancellation_rate"] <= 1.0
    assert 0.0 <= features["peak_hour_share"] <= 1.0
    assert 1.0 <= features["avg_rating"] <= 5.0
    assert features["net_payout_30d"] >= 0
    assert features["gross_earnings_30d"] >= 0
    assert features["rating_count"] >= 0
    assert features["complaints_30d"] >= 0
