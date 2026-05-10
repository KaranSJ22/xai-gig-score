# from typing import Dict, List

# from ..models.platform import PlatformData


# FEATURE_COLUMNS = [
#     "age",
#     "platform_tenure",
#     "avg_active_days",
#     "avg_hours",
#     "task_completion_rate",
#     "avg_rating",
#     "activity_stability",
#     "wallet_txn_freq",
#     "inward_txn_freq",
#     "avg_income",
#     "income_volatility",
#     "income_growth",
#     "savings_ratio",
#     "avg_balance",
#     "has_insurance",
#     "emergency_buffer",
#     "loan_utilization",
#     "fixed_emi_burden_ratio",
#     "credit_inquiries",
#     "delay_score",
#     "recent_payment_delays_90",
#     "utility_delay_score",
#     "recent_missed_rent_3m",
#     "rent_consistency_ratio",
# ]


# def _bool_to_float(value: bool) -> float:
#     return 1.0 if value else 0.0


# def build_features(platforms: List[PlatformData]) -> Dict[str, float]:
#     if not platforms:
#         raise ValueError("No platform data available to build features.")

#     count = len(platforms)

#     def avg(attr: str) -> float:
#         return float(sum(getattr(p, attr) for p in platforms) / count)

#     features = {
#         "age": avg("age"),
#         "platform_tenure": avg("platform_tenure"),
#         "avg_active_days": avg("avg_active_days"),
#         "avg_hours": avg("avg_hours"),
#         "task_completion_rate": avg("task_completion_rate"),
#         "avg_rating": avg("avg_rating"),
#         "activity_stability": avg("activity_stability"),
#         "wallet_txn_freq": avg("wallet_txn_freq"),
#         "inward_txn_freq": avg("inward_txn_freq"),
#         "avg_income": avg("avg_income"),
#         "income_volatility": avg("income_volatility"),
#         "income_growth": avg("income_growth"),
#         "savings_ratio": avg("savings_ratio"),
#         "avg_balance": avg("avg_balance"),
#         "has_insurance": avg("_has_insurance_numeric"),
#         "emergency_buffer": avg("_emergency_buffer_numeric"),
#         "loan_utilization": avg("loan_utilization"),
#         "fixed_emi_burden_ratio": avg("fixed_emi_burden_ratio"),
#         "credit_inquiries": avg("credit_inquiries"),
#         "delay_score": avg("delay_score"),
#         "recent_payment_delays_90": avg("recent_payment_delays_90"),
#         "utility_delay_score": avg("utility_delay_score"),
#         "recent_missed_rent_3m": avg("recent_missed_rent_3m"),
#         "rent_consistency_ratio": avg("rent_consistency_ratio"),
#     }

#     return features


# def attach_numeric_flags(platform: PlatformData) -> None:
#     platform._has_insurance_numeric = _bool_to_float(platform.has_insurance)
#     platform._emergency_buffer_numeric = _bool_to_float(platform.emergency_buffer)



from typing import Dict, List

from ..models.platform import PlatformData


FEATURE_COLUMNS = [
    "age",
    "platform_tenure",
    "platform_count",
    "avg_active_days",
    "avg_hours",
    "task_completion_rate",
    "avg_rating",
    "activity_stability",
    "wallet_txn_freq",
    "inward_txn_freq",
    "avg_income",
    "income_volatility",
    "income_growth",
    "income_consistency_score",
    "monthly_income_trend",
    "savings_ratio",
    "avg_balance",
    "has_insurance",
    "emergency_buffer",
    "utility_delay_score",
    "recent_missed_rent_3m",
    "rent_consistency_ratio",
    "non_credit_payment_delay_score",
    "data_completeness_score",
]


def _bool_to_float(value: bool) -> float:
    return 1.0 if value else 0.0


def _weighted_income_aggregation(incomes: list[float]) -> float:
    """
    Prevents unrealistic income inflation when a user connects multiple mock platforms.

    Highest income platform is treated as primary.
    Additional platforms contribute with diminishing weights.
    """
    if not incomes:
        return 0.0

    base_weights = [1.0, 0.45, 0.25, 0.15, 0.10, 0.05]
    sorted_incomes = sorted(incomes, reverse=True)

    weighted_income = 0.0

    for index, income in enumerate(sorted_incomes):
        weight = base_weights[index] if index < len(base_weights) else 0.05
        weighted_income += float(income) * weight

    return round(weighted_income, 2)


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

    incomes = [float(p.avg_income) for p in platforms]

    features = {
        # Basic borrower / platform context
        "age": avg("age"),
        "platform_tenure": avg("platform_tenure"),
        "platform_count": float(count),

        # Work activity signals
        "avg_active_days": avg("avg_active_days"),
        "avg_hours": avg("avg_hours"),
        "task_completion_rate": avg("task_completion_rate"),
        "avg_rating": avg("avg_rating"),
        "activity_stability": avg("activity_stability"),

        # Income and cash-flow signals
        # Weighted aggregation avoids blindly summing full-time-like mock incomes.
        "wallet_txn_freq": avg("wallet_txn_freq"),
        "inward_txn_freq": avg("inward_txn_freq"),
        "avg_income": _weighted_income_aggregation(incomes),
        "income_volatility": avg("income_volatility"),
        "income_growth": avg("income_growth"),
        "income_consistency_score": avg("income_consistency_score"),
        "monthly_income_trend": avg("monthly_income_trend"),

        # Financial discipline / resilience signals
        "savings_ratio": avg("savings_ratio"),
        "avg_balance": avg("avg_balance"),

        # If user has insurance/emergency buffer in any connected platform record,
        # consider it available at user level.
        "has_insurance": any_bool("has_insurance"),
        "emergency_buffer": any_bool("emergency_buffer"),

        # Non-credit payment behavior signals
        "utility_delay_score": avg("utility_delay_score"),
        "recent_missed_rent_3m": avg("recent_missed_rent_3m"),
        "rent_consistency_ratio": avg("rent_consistency_ratio"),
        "non_credit_payment_delay_score": avg("non_credit_payment_delay_score"),

        # Data quality signal
        "data_completeness_score": avg("data_completeness_score"),
    }

    return features