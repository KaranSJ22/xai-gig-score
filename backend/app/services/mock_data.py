import random


SUPPORTED_PLATFORMS = {
    "uber",
    "zomato",
    "swiggy",
    "rapido",
    "freelance",
    "delivery",
    "ride-hailing",
    "ola",
    "upwork",
}


def generate_mock_platform_features(platform_name: str) -> dict:
    platform = platform_name.strip().lower()

    if platform not in SUPPORTED_PLATFORMS:
        raise ValueError(f"Unsupported platform: {platform_name}")

    # Platform-specific tendencies
    if platform in {"uber", "rapido", "ola", "ride-hailing"}:
        income_base = (18000, 42000)
        active_days_range = (18, 29)
        avg_hours_range = (5.0, 11.0)
        rating_range = (3.6, 5.0)

    elif platform in {"zomato", "swiggy", "delivery"}:
        income_base = (15000, 35000)
        active_days_range = (20, 30)
        avg_hours_range = (5.0, 12.0)
        rating_range = (3.5, 5.0)

    else:  # freelance / upwork
        income_base = (12000, 50000)
        active_days_range = (10, 26)
        avg_hours_range = (3.0, 10.0)
        rating_range = (3.8, 5.0)

    avg_income = random.uniform(*income_base)
    income_volatility = random.uniform(0.05, 0.90)
    income_growth = random.uniform(-0.30, 0.80)

    savings_ratio = random.uniform(0.05, 0.45)
    avg_balance = avg_income * random.uniform(0.10, 0.60)

    # Higher volatility means lower consistency.
    income_consistency_score = max(0.0, min(1.0, 1.0 - income_volatility))

    # Encoded trend:
    # -1 = decreasing income trend
    #  0 = stable income trend
    #  1 = increasing income trend
    if income_growth > 0.10:
        monthly_income_trend = 1.0
    elif income_growth < -0.10:
        monthly_income_trend = -1.0
    else:
        monthly_income_trend = 0.0

    utility_delay_score = random.uniform(0, 5)
    recent_missed_rent_3m = random.uniform(0, 3)
    rent_consistency_ratio = random.uniform(0.30, 1.00)

    # Non-credit delay score is based on utility/rent behavior,
    # not loan or credit-card repayment behavior.
    non_credit_payment_delay_score = (
        (utility_delay_score / 5.0) * 0.6
        + (recent_missed_rent_3m / 3.0) * 0.4
    ) * 5.0

    # Mock completeness represents how complete this platform's data is.
    data_completeness_score = random.uniform(0.70, 1.00)

    return {
        # Basic borrower / platform context
        "age": float(random.randint(21, 50)),
        "platform_tenure": float(random.randint(1, 60)),

        # This row represents one connected platform.
        # During aggregation, platform_count should be recomputed as len(platforms).
        "platform_count": 1.0,

        # Work activity signals
        "avg_active_days": round(random.uniform(*active_days_range), 2),
        "avg_hours": round(random.uniform(*avg_hours_range), 2),
        "task_completion_rate": round(random.uniform(0.70, 0.99), 3),
        "avg_rating": round(random.uniform(*rating_range), 2),
        "activity_stability": round(random.uniform(0.20, 1.00), 3),

        # Income and cash-flow signals
        "wallet_txn_freq": round(random.uniform(5, 100), 2),
        "inward_txn_freq": round(random.uniform(5, 60), 2),
        "avg_income": round(avg_income, 2),
        "income_volatility": round(income_volatility, 3),
        "income_growth": round(income_growth, 3),
        "income_consistency_score": round(income_consistency_score, 3),
        "monthly_income_trend": monthly_income_trend,

        # Financial discipline / resilience signals
        "savings_ratio": round(savings_ratio, 3),
        "avg_balance": round(avg_balance, 2),
        "has_insurance": random.choice([True, False]),
        "emergency_buffer": random.choice([True, False]),

        # Non-credit payment behavior signals
        "utility_delay_score": round(utility_delay_score, 3),
        "recent_missed_rent_3m": round(recent_missed_rent_3m, 2),
        "rent_consistency_ratio": round(rent_consistency_ratio, 3),
        "non_credit_payment_delay_score": round(non_credit_payment_delay_score, 3),

        # Data quality signal
        "data_completeness_score": round(data_completeness_score, 3),
    }