from pathlib import Path
from typing import Any, Dict, List, Tuple

import joblib
import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
ML_DIR = BASE_DIR / "ml"

EXPLAINER_PATH = ML_DIR / "explainer.pkl"
FEATURES_PATH = ML_DIR / "features.pkl"

_explainer = None
_features = None


FEATURE_METADATA = {
    "active_days_30d": {
        "label": "Active Days",
        "category": "Activity",
        "risk_increasing": "Your {val} active days in the last month is below the optimal threshold, increasing predicted risk.",
        "risk_reducing": "Consistent engagement with {val} active days in the last month improved your reliability profile.",
    },
    "online_hours_30d": {
        "label": "Online Hours",
        "category": "Activity",
        "risk_increasing": "Total online time of {val} hours suggests limited earning capacity, affecting your score.",
        "risk_reducing": "High platform commitment with {val} online hours indicates strong earning potential.",
    },
    "avg_hours_per_active_day": {
        "label": "Daily Work Intensity",
        "category": "Activity",
        "risk_increasing": "Your average of {val} hours per day indicates irregular work patterns.",
        "risk_reducing": "Steady daily intensity of {val} hours demonstrates professional performance stability.",
    },
    "acceptance_rate": {
        "label": "Job Acceptance Rate",
        "category": "Reliability",
        "risk_increasing": "An acceptance rate of {val}% is lower than required, suggesting operational risk.",
        "risk_reducing": "Strong reliability demonstrated by a {val}% job acceptance rate.",
    },
    "cancellation_rate": {
        "label": "Order Cancellation Rate",
        "category": "Reliability",
        "risk_increasing": "Frequent cancellations ({val}%) weakened your platform trust signals.",
        "risk_reducing": "Excellent professional reliability with a low cancellation rate of {val}%.",
    },
    "peak_hour_share": {
        "label": "Peak Hour Performance",
        "category": "Activity",
        "risk_increasing": "Limited participation ({val}%) during peak hours reduced your efficiency score.",
        "risk_reducing": "Optimal time management with {val}% share of work during peak demand hours.",
    },
    "avg_rating": {
        "label": "Platform Rating",
        "category": "Performance",
        "risk_increasing": "Your average rating of {val}/5.0 is below the elite threshold, increasing risk.",
        "risk_reducing": "Outstanding service quality reflected in your {val}/5.0 average rating.",
    },
    "rating_count": {
        "label": "Total Feedback",
        "category": "Performance",
        "risk_increasing": "Limited feedback history ({val} ratings) reduces statistical confidence in your score.",
        "risk_reducing": "High volume of {val} ratings indicates an established and trusted performance history.",
    },
    "rating_std": {
        "label": "Rating Consistency",
        "category": "Performance",
        "risk_increasing": "High variance ({val}) in customer ratings suggests inconsistent service quality.",
        "risk_reducing": "Low rating variance of {val} demonstrates highly predictable and stable performance.",
    },
    "complaints_30d": {
        "label": "Customer Complaints",
        "category": "Performance",
        "risk_increasing": "Recent customer complaints ({val} in 30 days) significantly increased behavioral risk.",
        "risk_reducing": "Clean behavioral record with {val} complaints improved your credit standing.",
    },
    "gross_earnings_30d": {
        "label": "Gross Earnings",
        "category": "Earnings",
        "risk_increasing": "Gross earnings of ₹{val} in the last month suggest limited repayment capacity.",
        "risk_reducing": "Healthy financial resilience shown by ₹{val} in monthly gross earnings.",
    },
    "net_payout_30d": {
        "label": "Net Payout",
        "category": "Earnings",
        "risk_increasing": "Net payout of ₹{val} after deductions impacted your disposable income score.",
        "risk_reducing": "Stable net payout of ₹{val} improves predicted monthly cash flow.",
    },
    "weekly_earnings_std": {
        "label": "Income Variance",
        "category": "Earnings",
        "risk_increasing": "High weekly income fluctuation (₹{val}) increased your predicted risk.",
        "risk_reducing": "Low income variance of ₹{val} demonstrates high cash flow predictability.",
    },
    "incentive_share": {
        "label": "Incentive Dependency",
        "category": "Earnings",
        "risk_increasing": "High dependency on incentives ({val}%) suggests unstable core base pay.",
        "risk_reducing": "Stable core earnings with only {val}% dependency on platform incentives.",
    },
    "login_days_30d": {
        "label": "System Login Frequency",
        "category": "Consistency",
        "risk_increasing": "Infrequent system logins ({val} days) suggest lower platform engagement.",
        "risk_reducing": "Regular system logins for {val} days indicate high operational discipline.",
    },
    "avg_session_length": {
        "label": "Work Session Duration",
        "category": "Consistency",
        "risk_increasing": "Shorter work sessions ({val} hrs avg) indicates fragmented and unstable activity.",
        "risk_reducing": "Steady work sessions of {val} hours improved your consistency score.",
    },
    "inactivity_gap_days_max": {
        "label": "Max Work Gap",
        "category": "Consistency",
        "risk_increasing": "Longest gap of {val} days between working sessions increased your risk profile.",
        "risk_reducing": "High stability shown by a minimal maximum work gap of {val} days.",
    },
    "kyc_verified": {
        "label": "Identity Verification",
        "category": "Risk",
        "risk_increasing": "Non-verified identity status significantly increased identity-related risk.",
        "risk_reducing": "Verified KYC status improved overall trust and regulatory compliance.",
    },
    "account_suspensions_12m": {
        "label": "Account Suspensions",
        "category": "Risk",
        "risk_increasing": "Previous account suspensions ({val}) significantly increased your risk profile.",
        "risk_reducing": "Clean suspension record ({val}) improved your reliability and trust profile.",
    },
    "policy_violations_12m": {
        "label": "Policy Violations",
        "category": "Risk",
        "risk_increasing": "History of {val} policy violations increased predicted behavioral risk.",
        "risk_reducing": "Zero policy violations ({val}) demonstrated high professional compliance.",
    },
    "fraud_flag": {
        "label": "Fraud Indicators",
        "category": "Risk",
        "risk_increasing": "Detected fraud indicators significantly increased your risk level.",
        "risk_reducing": "No fraud indicators found, maintaining your standard risk profile.",
    },
    "activity_stability": {
        "label": "Operational Stability",
        "category": "Derived",
        "risk_increasing": "Lower stability score of {val} increased your predicted repayment risk.",
        "risk_reducing": "High operational stability ({val}) improved work history confidence.",
    },
    "earnings_per_hour": {
        "label": "Hourly Efficiency",
        "category": "Derived",
        "risk_increasing": "Lower hourly efficiency of ₹{val} suggests reduced earning potential.",
        "risk_reducing": "High hourly efficiency of ₹{val} improved your financial resilience score.",
    },
    "volatility_ratio": {
        "label": "Earnings Volatility",
        "category": "Derived",
        "risk_increasing": "High earnings volatility ({val}) increased your predicted repayment risk.",
        "risk_reducing": "Stable earnings pattern (volatility: {val}) reduced your predicted risk.",
    },
    "reliability_score": {
        "label": "Behavioral Reliability",
        "category": "Derived",
        "risk_increasing": "Lower reliability score ({val}) increased your predicted behavioral risk.",
        "risk_reducing": "Strong behavioral reliability ({val}) improved your overall creditworthiness.",
    },
    "discipline_score": {
        "label": "Workplace Discipline",
        "category": "Derived",
        "risk_increasing": "Lower discipline score of {val} increased your predicted behavioral risk.",
        "risk_reducing": "High workplace discipline score ({val}) improved repayment confidence.",
    },
    "financial_stress_ratio": {
        "label": "Financial Stress Indicator",
        "category": "Derived",
        "risk_increasing": "High financial stress ratio of {val} increased your predicted risk.",
        "risk_reducing": "Lower financial stress ratio ({val}) improved your overall risk profile.",
    },
    "earnings_consistency": {
        "label": "Earnings Predictability",
        "category": "Derived",
        "risk_increasing": "Lower earnings predictability ({val}) increased your predicted risk.",
        "risk_reducing": "Consistent earnings predictability ({val}) improved repayment confidence.",
    },
}


def load_explainer_artifacts():
    global _explainer, _features

    if _explainer is None:
        _explainer = joblib.load(EXPLAINER_PATH)

    if _features is None:
        _features = joblib.load(FEATURES_PATH)

    return _explainer, _features


def _extract_1d_shap_values(shap_values) -> np.ndarray:
    """
    Normalize SHAP output to a 1D array of length n_features.
    Handles different SHAP versions and model output formats.
    """
    arr = np.array(shap_values)

    # Case: list output from older TreeExplainer for classifiers:
    # [class_0_values, class_1_values]
    if isinstance(shap_values, list):
        arr = np.array(shap_values[1])

    # Case: (1, n_features)
    if arr.ndim == 2 and arr.shape[0] == 1:
        return arr[0]

    # Case: (1, n_features, 2) or similar, choose class 1
    if arr.ndim == 3:
        if arr.shape[0] == 1 and arr.shape[2] == 2:
            return arr[0, :, 1]

        if arr.shape[0] == 1 and arr.shape[1] == 2:
            return arr[0, 1, :]

    return arr.flatten()


def _build_factor(
    feature: str,
    feature_value: float,
    shap_value: float,
    direction: str,
) -> dict[str, Any]:
    metadata = FEATURE_METADATA.get(
        feature,
        {
            "label": feature,
            "category": "Other",
            "risk_increasing": "{val} increased predicted repayment risk.",
            "risk_reducing": "{val} reduced predicted repayment risk.",
        },
    )

    explanation_key = (
        "risk_increasing"
        if direction == "risk_increasing"
        else "risk_reducing"
    )
    
    # Format the explanation with the real value
    raw_explanation = metadata[explanation_key]
    
    # Handle percentage conversion for rates
    display_val = feature_value
    
    integer_features = [
        "active_days_30d", "online_hours_30d", "rating_count", 
        "complaints_30d", "login_days_30d", "inactivity_gap_days_max",
        "account_suspensions_12m", "policy_violations_12m"
    ]
    
    if feature in integer_features:
        display_val = int(round(display_val))
    elif "rate" in feature or "share" in feature or "ratio" in feature:
        if display_val <= 1.0:
            display_val = round(display_val * 100, 1)
        else:
            display_val = round(display_val, 2)
    elif "earnings" in feature or "payout" in feature:
        display_val = f"{int(display_val):,}"
    else:
        display_val = round(display_val, 2) if isinstance(display_val, float) else display_val

    try:
        explanation = raw_explanation.format(val=display_val)
    except (KeyError, ValueError):
        explanation = raw_explanation

    return {
        "feature_key": feature,
        "label": metadata["label"],
        "category": metadata["category"],
        "value": float(feature_value),
        "impact": round(float(shap_value), 6),
        "explanation": explanation,
    }


def explain_prediction(
    features_dict: Dict[str, float],
    top_k: int = 3,
) -> Tuple[List[dict[str, Any]], List[dict[str, Any]], Dict[str, float]]:
    explainer, feature_order = load_explainer_artifacts()

    missing_features = [feature for feature in feature_order if feature not in features_dict]

    if missing_features:
        raise ValueError(f"Missing required SHAP features: {missing_features}")

    row = {
        feature: float(features_dict[feature])
        for feature in feature_order
    }

    X = pd.DataFrame([row], columns=feature_order)

    shap_values = explainer.shap_values(X)
    values = _extract_1d_shap_values(shap_values)

    if len(values) != len(feature_order):
        raise ValueError(
            f"SHAP values length mismatch. Expected {len(feature_order)}, got {len(values)}."
        )

    contributions = [
        (feature, float(row[feature]), float(shap_value))
        for feature, shap_value in zip(feature_order, values.tolist())
    ]

    # Since model predicts default probability:
    # positive SHAP value = risk increasing
    # negative SHAP value = risk reducing
    risk_increasing = sorted(
        [
            (feature, feature_value, shap_value)
            for feature, feature_value, shap_value in contributions
            if shap_value > 0
        ],
        key=lambda x: x[2],
        reverse=True,
    )

    risk_reducing = sorted(
        [
            (feature, feature_value, shap_value)
            for feature, feature_value, shap_value in contributions
            if shap_value < 0
        ],
        key=lambda x: x[2],
    )

    risk_increasing_factors = [
        _build_factor(
            feature=feature,
            feature_value=feature_value,
            shap_value=shap_value,
            direction="risk_increasing",
        )
        for feature, feature_value, shap_value in risk_increasing[:top_k]
    ]

    risk_reducing_factors = [
        _build_factor(
            feature=feature,
            feature_value=feature_value,
            shap_value=shap_value,
            direction="risk_reducing",
        )
        for feature, feature_value, shap_value in risk_reducing[:top_k]
    ]

    shap_values_dict = {
        feature: round(float(shap_value), 6)
        for feature, _, shap_value in contributions
    }

    return risk_increasing_factors, risk_reducing_factors, shap_values_dict