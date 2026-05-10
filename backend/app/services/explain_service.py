# from pathlib import Path
# from typing import Dict, List, Tuple

# import joblib
# import pandas as pd

# BASE_DIR = Path(__file__).resolve().parent.parent
# ML_DIR = BASE_DIR / "ml"

# EXPLAINER_PATH = ML_DIR / "explainer.pkl"
# FEATURES_PATH = ML_DIR / "features.pkl"

# _explainer = None
# _features = None


# FEATURE_LABELS = {
#     "age": "Age",
#     "platform_tenure": "Platform tenure",
#     "avg_active_days": "Active working days",
#     "avg_hours": "Average working hours",
#     "task_completion_rate": "Task completion rate",
#     "avg_rating": "Customer rating",
#     "activity_stability": "Activity stability",
#     "wallet_txn_freq": "Wallet transaction frequency",
#     "inward_txn_freq": "Incoming transaction frequency",
#     "avg_income": "Average income",
#     "income_volatility": "Income volatility",
#     "income_growth": "Income growth",
#     "savings_ratio": "Savings ratio",
#     "avg_balance": "Average balance",
#     "has_insurance": "Insurance coverage",
#     "emergency_buffer": "Emergency buffer",
#     "loan_utilization": "Loan utilization",
#     "fixed_emi_burden_ratio": "Fixed EMI burden ratio",
#     "credit_inquiries": "Credit inquiries",
#     "delay_score": "Payment delay score",
#     "recent_payment_delays_90": "Recent payment delays (90 days)",
#     "utility_delay_score": "Utility delay score",
#     "recent_missed_rent_3m": "Recent missed rent (3 months)",
#     "rent_consistency_ratio": "Rent consistency ratio",
# }


# def load_explainer_artifacts():
#     global _explainer, _features

#     if _explainer is None:
#         _explainer = joblib.load(EXPLAINER_PATH)

#     if _features is None:
#         _features = joblib.load(FEATURES_PATH)

#     return _explainer, _features


# def explain_prediction(features_dict: Dict[str, float], top_k: int = 3) -> Tuple[List[str], List[str]]:
#     explainer, feature_order = load_explainer_artifacts()

#     row = {feature: float(features_dict.get(feature, 0.0)) for feature in feature_order}
#     X = pd.DataFrame([row], columns=feature_order)

#     explanation = explainer(X)
#     values = explanation.values[0]

#     contributions = list(zip(feature_order, values))

#     positive = sorted([item for item in contributions if item[1] > 0], key=lambda x: x[1], reverse=True)
#     negative = sorted([item for item in contributions if item[1] < 0], key=lambda x: x[1])

#     positive_factors = [
#         f"{FEATURE_LABELS.get(feature, feature)} increased the predicted risk"
#         for feature, _ in positive[:top_k]
#     ]
#     negative_factors = [
#         f"{FEATURE_LABELS.get(feature, feature)} reduced the predicted risk"
#         for feature, _ in negative[:top_k]
#     ]

#     return positive_factors, negative_factors

# from pathlib import Path
# from typing import Dict, List, Tuple

# import joblib
# import pandas as pd

# BASE_DIR = Path(__file__).resolve().parent.parent
# ML_DIR = BASE_DIR / "ml"

# EXPLAINER_PATH = ML_DIR / "explainer.pkl"
# FEATURES_PATH = ML_DIR / "features.pkl"

# _explainer = None
# _features = None


# FEATURE_LABELS = {
#     "age": "Age",
#     "platform_tenure": "Platform tenure",
#     "avg_active_days": "Active working days",
#     "avg_hours": "Average working hours",
#     "task_completion_rate": "Task completion rate",
#     "avg_rating": "Customer rating",
#     "activity_stability": "Activity stability",
#     "wallet_txn_freq": "Wallet transaction frequency",
#     "inward_txn_freq": "Incoming transaction frequency",
#     "avg_income": "Average income",
#     "income_volatility": "Income volatility",
#     "income_growth": "Income growth",
#     "savings_ratio": "Savings ratio",
#     "avg_balance": "Average balance",
#     "has_insurance": "Insurance coverage",
#     "emergency_buffer": "Emergency buffer",
#     "loan_utilization": "Loan utilization",
#     "fixed_emi_burden_ratio": "Fixed EMI burden ratio",
#     "credit_inquiries": "Credit inquiries",
#     "delay_score": "Payment delay score",
#     "recent_payment_delays_90": "Recent payment delays (90 days)",
#     "utility_delay_score": "Utility delay score",
#     "recent_missed_rent_3m": "Recent missed rent (3 months)",
#     "rent_consistency_ratio": "Rent consistency ratio",
# }


# def load_explainer_artifacts():
#     global _explainer, _features

#     if _explainer is None:
#         _explainer = joblib.load(EXPLAINER_PATH)

#     if _features is None:
#         _features = joblib.load(FEATURES_PATH)

#     return _explainer, _features


# def explain_prediction(features_dict: Dict[str, float], top_k: int = 3) -> Tuple[List[str], List[str]]:
#     explainer, feature_order = load_explainer_artifacts()

#     row = {feature: float(features_dict.get(feature, 0.0)) for feature in feature_order}
#     X = pd.DataFrame([row], columns=feature_order)

#     shap_values = explainer.shap_values(X)

#     # For binary classification, TreeExplainer may return a list of 2 arrays
#     if isinstance(shap_values, list):
#         values = shap_values[1][0]
#     else:
#         values = shap_values[0]

#     contributions = list(zip(feature_order, values))

#     positive = sorted(
#         [(feature, value) for feature, value in contributions if value > 0],
#         key=lambda x: x[1],
#         reverse=True,
#     )
#     negative = sorted(
#         [(feature, value) for feature, value in contributions if value < 0],
#         key=lambda x: x[1],
#     )

#     positive_factors = [
#         f"{FEATURE_LABELS.get(feature, feature)} increased the predicted risk"
#         for feature, _ in positive[:top_k]
#     ]
#     negative_factors = [
#         f"{FEATURE_LABELS.get(feature, feature)} reduced the predicted risk"
#         for feature, _ in negative[:top_k]
#     ]

#     return positive_factors, negative_factors


# from pathlib import Path
# from typing import Dict, List, Tuple

# import joblib
# import numpy as np
# import pandas as pd

# BASE_DIR = Path(__file__).resolve().parent.parent
# ML_DIR = BASE_DIR / "ml"

# EXPLAINER_PATH = ML_DIR / "explainer.pkl"
# FEATURES_PATH = ML_DIR / "features.pkl"

# _explainer = None
# _features = None


# FEATURE_LABELS = {
#     "age": "Age",
#     "platform_tenure": "Platform tenure",
#     "avg_active_days": "Active working days",
#     "avg_hours": "Average working hours",
#     "task_completion_rate": "Task completion rate",
#     "avg_rating": "Customer rating",
#     "activity_stability": "Activity stability",
#     "wallet_txn_freq": "Wallet transaction frequency",
#     "inward_txn_freq": "Incoming transaction frequency",
#     "avg_income": "Average income",
#     "income_volatility": "Income volatility",
#     "income_growth": "Income growth",
#     "savings_ratio": "Savings ratio",
#     "avg_balance": "Average balance",
#     "has_insurance": "Insurance coverage",
#     "emergency_buffer": "Emergency buffer",
#     "loan_utilization": "Loan utilization",
#     "fixed_emi_burden_ratio": "Fixed EMI burden ratio",
#     "credit_inquiries": "Credit inquiries",
#     "delay_score": "Payment delay score",
#     "recent_payment_delays_90": "Recent payment delays (90 days)",
#     "utility_delay_score": "Utility delay score",
#     "recent_missed_rent_3m": "Recent missed rent (3 months)",
#     "rent_consistency_ratio": "Rent consistency ratio",
# }


# def load_explainer_artifacts():
#     global _explainer, _features

#     if _explainer is None:
#         _explainer = joblib.load(EXPLAINER_PATH)

#     if _features is None:
#         _features = joblib.load(FEATURES_PATH)

#     return _explainer, _features


# def _extract_1d_shap_values(shap_values) -> np.ndarray:
#     """
#     Normalize SHAP output to a 1D array of length n_features.
#     Handles different SHAP versions / model output formats.
#     """
#     arr = np.array(shap_values)

#     # Common cases:
#     # (1, n_features)
#     if arr.ndim == 2 and arr.shape[0] == 1:
#         return arr[0]

#     # (1, n_features, 2) or (1, 2, n_features)
#     if arr.ndim == 3:
#         # Case: (1, n_features, 2) -> choose class 1
#         if arr.shape[0] == 1 and arr.shape[2] == 2:
#             return arr[0, :, 1]

#         # Case: (1, 2, n_features) -> choose class 1
#         if arr.shape[0] == 1 and arr.shape[1] == 2:
#             return arr[0, 1, :]

#     # Fallback
#     return arr.flatten()


# def explain_prediction(features_dict: Dict[str, float], top_k: int = 3) -> Tuple[List[str], List[str]]:
#     explainer, feature_order = load_explainer_artifacts()

#     row = {feature: float(features_dict.get(feature, 0.0)) for feature in feature_order}
#     X = pd.DataFrame([row], columns=feature_order)

#     shap_values = explainer.shap_values(X)
#     values = _extract_1d_shap_values(shap_values)

#     contributions = list(zip(feature_order, values.tolist()))

#     positive = sorted(
#         [(feature, float(value)) for feature, value in contributions if float(value) > 0],
#         key=lambda x: x[1],
#         reverse=True,
#     )
#     negative = sorted(
#         [(feature, float(value)) for feature, value in contributions if float(value) < 0],
#         key=lambda x: x[1],
#     )

#     positive_factors = [
#         f"{FEATURE_LABELS.get(feature, feature)} increased the predicted risk"
#         for feature, _ in positive[:top_k]
#     ]
#     negative_factors = [
#         f"{FEATURE_LABELS.get(feature, feature)} reduced the predicted risk"
#         for feature, _ in negative[:top_k]
#     ]

#     return positive_factors, negative_factors



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
    "age": {
        "label": "Age",
        "category": "Profile",
        "risk_increasing": "Age profile slightly increased predicted repayment risk.",
        "risk_reducing": "Age profile slightly reduced predicted repayment risk.",
    },
    "platform_tenure": {
        "label": "Platform Tenure",
        "category": "Work Stability",
        "risk_increasing": "Shorter platform tenure increased predicted repayment risk.",
        "risk_reducing": "Longer platform tenure improved work stability and reduced predicted risk.",
    },
    "platform_count": {
        "label": "Connected Platforms",
        "category": "Work Diversity",
        "risk_increasing": "Limited platform diversity increased predicted risk.",
        "risk_reducing": "Multiple connected platforms improved income source diversity and reduced predicted risk.",
    },
    "avg_active_days": {
        "label": "Active Working Days",
        "category": "Work Activity",
        "risk_increasing": "Lower active working days reduced income reliability.",
        "risk_reducing": "Consistent active working days improved income reliability.",
    },
    "avg_hours": {
        "label": "Average Working Hours",
        "category": "Work Activity",
        "risk_increasing": "Lower average working hours reduced earning consistency.",
        "risk_reducing": "Consistent working hours improved earning stability.",
    },
    "task_completion_rate": {
        "label": "Task Completion Rate",
        "category": "Work Reliability",
        "risk_increasing": "Lower task completion rate reduced platform reliability.",
        "risk_reducing": "High task completion rate improved work reliability and reduced predicted risk.",
    },
    "avg_rating": {
        "label": "Platform Rating",
        "category": "Work Reliability",
        "risk_increasing": "Lower platform rating increased predicted risk.",
        "risk_reducing": "Good platform rating improved trust and reduced predicted risk.",
    },
    "activity_stability": {
        "label": "Activity Stability",
        "category": "Work Stability",
        "risk_increasing": "Unstable work activity increased predicted repayment risk.",
        "risk_reducing": "Stable work activity reduced predicted repayment risk.",
    },
    "wallet_txn_freq": {
        "label": "Wallet Transaction Frequency",
        "category": "Cash Flow",
        "risk_increasing": "Lower wallet transaction activity weakened cash-flow confidence.",
        "risk_reducing": "Regular wallet transaction activity improved cash-flow confidence.",
    },
    "inward_txn_freq": {
        "label": "Incoming Transaction Frequency",
        "category": "Cash Flow",
        "risk_increasing": "Lower incoming transaction frequency increased predicted risk.",
        "risk_reducing": "Frequent incoming transactions indicated stable cash flow.",
    },
    "avg_income": {
        "label": "Average Monthly Income",
        "category": "Income",
        "risk_increasing": "Lower average monthly income increased predicted repayment risk.",
        "risk_reducing": "Higher average monthly income reduced predicted repayment risk.",
    },
    "income_volatility": {
        "label": "Income Volatility",
        "category": "Income Stability",
        "risk_increasing": "High income fluctuation increased predicted repayment risk.",
        "risk_reducing": "Lower income fluctuation improved income stability and reduced predicted risk.",
    },
    "income_growth": {
        "label": "Income Growth",
        "category": "Income Stability",
        "risk_increasing": "Weak or declining income growth increased predicted risk.",
        "risk_reducing": "Positive income growth reduced predicted repayment risk.",
    },
    "income_consistency_score": {
        "label": "Income Consistency",
        "category": "Income Stability",
        "risk_increasing": "Lower income consistency increased predicted repayment risk.",
        "risk_reducing": "Consistent income pattern reduced predicted repayment risk.",
    },
    "monthly_income_trend": {
        "label": "Monthly Income Trend",
        "category": "Income Stability",
        "risk_increasing": "Declining or unstable income trend increased predicted risk.",
        "risk_reducing": "Stable or improving income trend reduced predicted risk.",
    },
    "savings_ratio": {
        "label": "Savings Ratio",
        "category": "Financial Discipline",
        "risk_increasing": "Low savings ratio indicated weaker financial buffer.",
        "risk_reducing": "Healthy savings ratio indicated better financial discipline.",
    },
    "avg_balance": {
        "label": "Average Balance",
        "category": "Financial Resilience",
        "risk_increasing": "Lower average balance indicated weaker liquidity.",
        "risk_reducing": "Higher average balance indicated better liquidity and reduced predicted risk.",
    },
    "has_insurance": {
        "label": "Insurance Coverage",
        "category": "Risk Protection",
        "risk_increasing": "Lack of insurance coverage increased financial vulnerability.",
        "risk_reducing": "Insurance coverage reduced financial vulnerability.",
    },
    "emergency_buffer": {
        "label": "Emergency Buffer",
        "category": "Financial Resilience",
        "risk_increasing": "Lack of emergency buffer increased predicted repayment risk.",
        "risk_reducing": "Emergency buffer improved financial resilience and reduced predicted risk.",
    },
    "utility_delay_score": {
        "label": "Utility Payment Delay",
        "category": "Non-credit Payment Behavior",
        "risk_increasing": "Utility payment delays increased predicted repayment risk.",
        "risk_reducing": "Consistent utility payments reduced predicted repayment risk.",
    },
    "recent_missed_rent_3m": {
        "label": "Recent Missed Rent",
        "category": "Non-credit Payment Behavior",
        "risk_increasing": "Recent missed rent payments increased predicted repayment risk.",
        "risk_reducing": "No recent missed rent payments improved repayment confidence.",
    },
    "rent_consistency_ratio": {
        "label": "Rent Consistency",
        "category": "Non-credit Payment Behavior",
        "risk_increasing": "Irregular rent payment behavior increased predicted risk.",
        "risk_reducing": "Consistent rent payment behavior reduced predicted risk.",
    },
    "non_credit_payment_delay_score": {
        "label": "Non-credit Payment Delay Score",
        "category": "Non-credit Payment Behavior",
        "risk_increasing": "Delays in non-credit payments increased predicted repayment risk.",
        "risk_reducing": "Timely non-credit payments reduced predicted repayment risk.",
    },
    "data_completeness_score": {
        "label": "Data Completeness",
        "category": "Data Quality",
        "risk_increasing": "Incomplete platform data reduced confidence and increased predicted risk.",
        "risk_reducing": "More complete platform data improved confidence in the assessment.",
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
            "risk_increasing": f"{feature} increased predicted repayment risk.",
            "risk_reducing": f"{feature} reduced predicted repayment risk.",
        },
    )

    explanation_key = (
        "risk_increasing"
        if direction == "risk_increasing"
        else "risk_reducing"
    )

    return {
        "feature_key": feature,
        "label": metadata["label"],
        "category": metadata["category"],
        "value": round(float(feature_value), 4),
        "impact": round(float(shap_value), 6),
        "explanation": metadata[explanation_key],
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