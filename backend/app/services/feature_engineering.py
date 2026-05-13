from typing import Dict, List

from ..models.platform import PlatformData


FEATURE_COLUMNS = [
    "active_days_30d",
    "online_hours_30d",
    "avg_hours_per_active_day",
    "acceptance_rate",
    "cancellation_rate",
    "peak_hour_share",
    "avg_rating",
    "rating_count",
    "rating_std",
    "complaints_30d",
    "gross_earnings_30d",
    "net_payout_30d",
    "weekly_earnings_std",
    "incentive_share",
    "login_days_30d",
    "avg_session_length",
    "inactivity_gap_days_max",
    "kyc_verified",
    "account_suspensions_12m",
    "policy_violations_12m",
    "fraud_flag",
    "activity_stability",
    "earnings_per_hour",
    "volatility_ratio",
    "reliability_score",
    "discipline_score",
    "financial_stress_ratio",
    "earnings_consistency",
]


def _bool_to_float(value: bool) -> float:
    return 1.0 if value else 0.0


def build_features(platforms: List[PlatformData]) -> Dict[str, float]:
    if not platforms:
        raise ValueError("No platform data available to build features.")

    count = len(platforms)

    def avg(attr: str) -> float:
        return float(sum(float(getattr(p, attr)) for p in platforms) / count)

    def avg_bool(attr: str) -> float:
        return float(sum(_bool_to_float(bool(getattr(p, attr))) for p in platforms) / count)

    def any_bool(attr: str) -> float:
        return 1.0 if any(bool(getattr(p, attr)) for p in platforms) else 0.0

    # Basic averages
    features = {
        "active_days_30d": avg("active_days_30d"),
        "online_hours_30d": avg("online_hours_30d"),
        "avg_hours_per_active_day": avg("avg_hours_per_active_day"),
        "acceptance_rate": avg("acceptance_rate"),
        "cancellation_rate": avg("cancellation_rate"),
        "peak_hour_share": avg("peak_hour_share"),
        "avg_rating": avg("avg_rating"),
        "rating_count": int(avg("rating_count")),
        "rating_std": avg("rating_std"),
        "complaints_30d": int(avg("complaints_30d")),
        "gross_earnings_30d": avg("gross_earnings_30d"),
        "net_payout_30d": avg("net_payout_30d"),
        "weekly_earnings_std": avg("weekly_earnings_std"),
        "incentive_share": avg("incentive_share"),
        "login_days_30d": int(avg("login_days_30d")),
        "avg_session_length": avg("avg_session_length"),
        "inactivity_gap_days_max": int(avg("inactivity_gap_days_max")),
        "kyc_verified": avg_bool("kyc_verified"),
        "account_suspensions_12m": int(avg("account_suspensions_12m")),
        "policy_violations_12m": int(avg("policy_violations_12m")),
        "fraud_flag": any_bool("fraud_flag"),
        "activity_stability": avg("activity_stability"),
        "earnings_per_hour": avg("earnings_per_hour"),
        "volatility_ratio": avg("volatility_ratio"),
        "reliability_score": avg("reliability_score"),
        "discipline_score": avg("discipline_score"),
    }

    # Add derived features required by the new model
    features["financial_stress_ratio"] = features["volatility_ratio"] / (features["net_payout_30d"] / 1000 + 1)
    features["earnings_consistency"] = features["active_days_30d"] * (1 / (features["volatility_ratio"] + 1))

    return features