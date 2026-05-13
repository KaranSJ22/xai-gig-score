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

    # Risk segment distribution for mock generation
    # Low: 45%, Medium: 33%, High: 22%
    risk_seg = random.choices(['Low', 'Medium', 'High'], weights=[0.45, 0.33, 0.22])[0]
    
    # Behavioral segment distribution based on risk
    if risk_seg == 'Low':
        beh_seg = random.choices(['High Performer', 'Average', 'Unstable'], weights=[0.40, 0.55, 0.05])[0]
    elif risk_seg == 'Medium':
        beh_seg = random.choices(['High Performer', 'Average', 'Unstable'], weights=[0.05, 0.65, 0.30])[0]
    else:
        beh_seg = random.choices(['High Performer', 'Average', 'Unstable'], weights=[0.01, 0.19, 0.80])[0]

    # Active Days
    if beh_seg == 'High Performer': active_days = random.randint(26, 30)
    elif beh_seg == 'Average': active_days = random.randint(22, 28)
    else: active_days = random.randint(18, 24)

    # Online Hours
    if beh_seg == 'High Performer':
        online_hours = random.randint(max(200, active_days * 2), min(300, active_days * 10))
    elif beh_seg == 'Average':
        online_hours = random.randint(max(120, active_days * 2), min(220, active_days * 10))
    else:
        online_hours = random.randint(max(60, active_days * 2), min(140, active_days * 10))

    avg_hours_per_active_day = round(online_hours / active_days, 2)

    # Acceptance/Cancellation
    if beh_seg == 'High Performer':
        acceptance_rate = random.uniform(0.85, 1.0)
        cancellation_rate = random.uniform(0.0, 0.05)
        avg_rating = random.uniform(4.6, 5.0)
        rating_std = random.uniform(0.05, 0.3)
        complaints = random.choices([0, 1], weights=[0.9, 0.1])[0]
    elif beh_seg == 'Average':
        acceptance_rate = random.uniform(0.70, 0.90)
        cancellation_rate = random.uniform(0.05, 0.15)
        avg_rating = random.uniform(4.0, 4.7)
        rating_std = random.uniform(0.2, 0.7)
        complaints = random.choices([0, 1, 2, 3], weights=[0.5, 0.3, 0.15, 0.05])[0]
    else:
        acceptance_rate = random.uniform(0.50, 0.75)
        cancellation_rate = random.uniform(0.15, 0.40)
        avg_rating = random.uniform(3.5, 4.2)
        rating_std = random.uniform(0.5, 1.2)
        complaints = random.choices([1, 2, 3, 4, 5, 6], weights=[0.1, 0.2, 0.3, 0.2, 0.1, 0.1])[0]

    peak_hour_share = random.uniform(0.4, 0.7) if beh_seg == 'High Performer' else random.uniform(0.1, 0.9)
    rating_count = max(50, min(1500, int(online_hours * random.uniform(1.0, 4.5))))

    # Earnings
    hourly_rate = random.gauss(120, 25)
    if beh_seg == 'High Performer': hourly_rate += 20
    elif beh_seg == 'Unstable': hourly_rate -= 20
    hourly_rate = max(60, min(200, hourly_rate))
    
    gross_earnings = int(online_hours * hourly_rate)
    gross_earnings = max(8000, min(60000, gross_earnings))
    net_payout = int(gross_earnings * random.uniform(0.8, 0.95))
    
    if beh_seg == 'High Performer': weekly_earnings_std = random.randint(500, 1500)
    elif beh_seg == 'Average': weekly_earnings_std = random.randint(1000, 3000)
    else: weekly_earnings_std = random.randint(2000, 6000)
    
    incentive_share = random.uniform(0.2, 0.6) if beh_seg == 'High Performer' else (random.uniform(0.1, 0.4) if beh_seg == 'Average' else random.uniform(0.0, 0.2))

    # Consistency
    login_days = min(30, active_days + random.randint(0, 2))
    avg_session_length = max(1.0, min(12.0, random.gauss(5, 1.5)))
    
    if beh_seg == 'High Performer': inactivity_gap = random.randint(0, 1)
    elif beh_seg == 'Average': inactivity_gap = random.randint(1, 3)
    else: inactivity_gap = random.randint(2, 6)

    # Risk Profile
    if beh_seg == 'High Performer': kyc = random.random() < 0.99
    elif beh_seg == 'Average': kyc = random.random() < 0.95
    else: kyc = random.random() < 0.80
    
    if beh_seg == 'High Performer': suspensions = 0
    elif beh_seg == 'Average': suspensions = 1 if random.random() < 0.1 else 0
    else: suspensions = random.choices([0, 1, 2, 3], weights=[0.6, 0.2, 0.15, 0.05])[0]

    # Derived
    activity_stability = round(max(0.1, min(0.99, (1 - inactivity_gap/7.0) - (weekly_earnings_std/10000)*0.2)), 2)
    earnings_per_hour = round(gross_earnings / online_hours, 1)
    volatility_ratio = round(max(0.0, min(3.0, weekly_earnings_std / (gross_earnings / 4 + 1))), 2)
    
    reliability_score = round(max(0.1, min(1.0, ((acceptance_rate + (1 - cancellation_rate*2.5) + (avg_rating/5.0) - (complaints * 0.10)) / 3.0) + random.gauss(0, 0.1))), 2)
    
    discipline_score = round(max(0.1, min(1.0, ((login_days/30.0) * 0.4 + 
                                               (1 - min(1.0, inactivity_gap/7.0)) * 0.3 +
                                               (1 - min(1.0, complaints/4.0)) * 0.2 + 
                                               (1 - min(1.0, 0/3.0)) * 0.1) + random.gauss(0, 0.15))), 2)

    return {
        "active_days_30d": float(active_days),
        "online_hours_30d": float(online_hours),
        "avg_hours_per_active_day": float(avg_hours_per_active_day),
        "acceptance_rate": round(float(acceptance_rate), 2),
        "cancellation_rate": round(float(cancellation_rate), 2),
        "peak_hour_share": round(float(peak_hour_share), 2),
        "avg_rating": round(float(avg_rating), 1),
        "rating_count": int(rating_count),
        "rating_std": round(float(rating_std), 2),
        "complaints_30d": int(complaints),
        "gross_earnings_30d": float(gross_earnings),
        "net_payout_30d": float(net_payout),
        "weekly_earnings_std": float(weekly_earnings_std),
        "incentive_share": round(float(incentive_share), 2),
        "login_days_30d": int(login_days),
        "avg_session_length": round(float(avg_session_length), 1),
        "inactivity_gap_days_max": int(inactivity_gap),
        "kyc_verified": bool(kyc),
        "account_suspensions_12m": int(suspensions),
        "policy_violations_12m": 0, # Defaulting to 0 for mock
        "fraud_flag": False,
        "activity_stability": float(activity_stability),
        "earnings_per_hour": float(earnings_per_hour),
        "volatility_ratio": float(volatility_ratio),
        "reliability_score": float(reliability_score),
        "discipline_score": float(discipline_score),
        "data_completeness_score": round(random.uniform(0.70, 1.00), 3)
    }