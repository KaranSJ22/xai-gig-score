from __future__ import annotations

import pytest

from app.services.model_service import get_model_metadata, predict_default_probability


def test_predict_default_probability_valid_range(sample_features):
    """Return a bounded probability and a binary class."""
    probability, predicted_class = predict_default_probability(sample_features)

    assert 0.0 <= probability <= 1.0
    assert predicted_class in (0.0, 1.0)


def test_predict_default_probability_missing_feature_raises(sample_features):
    """Raise when a required feature is missing."""
    sample_features.pop(next(iter(sample_features)))

    with pytest.raises(ValueError, match="Missing required model features"):
        predict_default_probability(sample_features)


def test_get_model_metadata_returns_name_and_version():
    """Expose model metadata for UI and audit trails."""
    metadata = get_model_metadata()

    assert metadata["model_name"]
    assert metadata["model_version"]
