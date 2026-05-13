import pandas as pd
import numpy as np
import os

def generate_gig_dataset():
    np.random.seed(42)

    NUM_ROWS = 15000

    # 1. Assign Risk Segments
    # Low Risk (0): 45%, Medium Risk (1): 33%, High Risk (2): 22%
    risk_segments = np.random.choice(['Low', 'Medium', 'High'], size=NUM_ROWS, p=[0.45, 0.33, 0.22])

    # 2. Assign Behavioral Segments
    # High Performer (0), Average (1), Unstable (2)
    behavior_segments = []
    for r in risk_segments:
        if r == 'Low':
            behavior_segments.append(np.random.choice(['High Performer', 'Average', 'Unstable'], p=[0.40, 0.55, 0.05]))
        elif r == 'Medium':
            behavior_segments.append(np.random.choice(['High Performer', 'Average', 'Unstable'], p=[0.05, 0.65, 0.30]))
        else: # High
            behavior_segments.append(np.random.choice(['High Performer', 'Average', 'Unstable'], p=[0.01, 0.19, 0.80]))
            
    df = pd.DataFrame({'risk_segment': risk_segments, 'behavior_segment': behavior_segments})
    df['Worker ID'] = range(1000, 1000 + NUM_ROWS)

    # A. WORK & ACTIVITY PROFILE
    def generate_active_days(row):
        b = row['behavior_segment']
        if b == 'High Performer': return np.random.randint(26, 31)
        elif b == 'Average': return np.random.randint(22, 29)
        else: return np.random.randint(18, 25)

    df['active_days_30d'] = df.apply(generate_active_days, axis=1)

    def generate_online_hours(row):
        days = row['active_days_30d']
        b = row['behavior_segment']
        if b == 'High Performer': 
            min_hrs = max(200, days * 2)
            max_hrs = min(300, days * 10)
            if min_hrs >= max_hrs: return min_hrs
            return np.random.randint(min_hrs, max_hrs + 1)
        elif b == 'Average': 
            min_hrs = max(120, days * 2)
            max_hrs = min(220, days * 10)
            if min_hrs >= max_hrs: return min_hrs
            return np.random.randint(min_hrs, max_hrs + 1)
        else: 
            min_hrs = max(60, days * 2)
            max_hrs = min(140, days * 10)
            if min_hrs >= max_hrs: return min_hrs
            return np.random.randint(min_hrs, max_hrs + 1)

    df['online_hours_30d'] = df.apply(generate_online_hours, axis=1)
    df['avg_hours_per_active_day'] = round(df['online_hours_30d'] / df['active_days_30d'], 2)

    def generate_acceptance(row):
        b = row['behavior_segment']
        if b == 'High Performer': return np.random.uniform(0.85, 1.0)
        elif b == 'Average': return np.random.uniform(0.70, 0.90)
        else: return np.random.uniform(0.50, 0.75)

    df['acceptance_rate'] = df.apply(generate_acceptance, axis=1).round(2)

    def generate_cancellation(row):
        b = row['behavior_segment']
        if b == 'High Performer': return np.random.uniform(0.0, 0.05)
        elif b == 'Average': return np.random.uniform(0.05, 0.15)
        else: return np.random.uniform(0.15, 0.40)

    df['cancellation_rate'] = df.apply(generate_cancellation, axis=1).round(2)

    def generate_peak_share(row):
        b = row['behavior_segment']
        if b == 'High Performer': return np.random.uniform(0.4, 0.7)
        else: return np.random.uniform(0.1, 0.9)

    df['peak_hour_share'] = df.apply(generate_peak_share, axis=1).round(2)

    # B. PERFORMANCE PROFILE
    def generate_rating(row):
        b = row['behavior_segment']
        if b == 'High Performer': return np.random.uniform(4.6, 5.0)
        elif b == 'Average': return np.random.uniform(4.0, 4.7)
        else: return np.random.uniform(3.5, 4.2)

    df['avg_rating'] = df.apply(generate_rating, axis=1).round(1)

    df['rating_count'] = (df['online_hours_30d'] * np.random.uniform(1.0, 4.5, size=NUM_ROWS)).astype(int)
    df['rating_count'] = np.clip(df['rating_count'], 50, 1500)

    def generate_rating_std(row):
        b = row['behavior_segment']
        if b == 'High Performer': return np.random.uniform(0.05, 0.3)
        elif b == 'Average': return np.random.uniform(0.2, 0.7)
        else: return np.random.uniform(0.5, 1.2)

    df['rating_std'] = df.apply(generate_rating_std, axis=1).round(2)

    def generate_complaints(row):
        b = row['behavior_segment']
        if b == 'High Performer': return np.random.choice([0, 1], p=[0.9, 0.1])
        elif b == 'Average': return np.random.choice([0, 1, 2, 3], p=[0.5, 0.3, 0.15, 0.05])
        else: return np.random.choice([1, 2, 3, 4, 5, 6], p=[0.1, 0.2, 0.3, 0.2, 0.1, 0.1])

    df['complaints_30d'] = df.apply(generate_complaints, axis=1)

    # C. EARNINGS PROFILE
    def get_hourly_rate(row):
        b = row['behavior_segment']
        rate = np.random.normal(120, 25)
        if b == 'High Performer': rate += 20
        elif b == 'Unstable': rate -= 20
        return np.clip(rate, 60, 200)

    df['gross_earnings_30d'] = (df['online_hours_30d'] * df.apply(get_hourly_rate, axis=1)).astype(int)
    # Cap limits as requested: ₹8k – ₹60k roughly
    df['gross_earnings_30d'] = np.clip(df['gross_earnings_30d'], 8000, 60000)

    df['net_payout_30d'] = (df['gross_earnings_30d'] * np.random.uniform(0.8, 0.95, size=NUM_ROWS)).astype(int)
    df['net_payout_30d'] = np.clip(df['net_payout_30d'], 6000, 50000)

    def generate_weekly_std(row):
        b = row['behavior_segment']
        if b == 'High Performer': return np.random.randint(500, 1500)
        elif b == 'Average': return np.random.randint(1000, 3000)
        else: return np.random.randint(2000, 6000)

    df['weekly_earnings_std'] = df.apply(generate_weekly_std, axis=1)

    def generate_incentive(row):
        b = row['behavior_segment']
        if b == 'High Performer': return np.random.uniform(0.2, 0.6)
        elif b == 'Average': return np.random.uniform(0.1, 0.4)
        else: return np.random.uniform(0.0, 0.2)

    df['incentive_share'] = df.apply(generate_incentive, axis=1).round(2)

    # D. CONSISTENCY PROFILE
    df['login_days_30d'] = np.minimum(df['active_days_30d'] + np.random.randint(0, 2, size=NUM_ROWS), 30)

    df['avg_session_length'] = np.random.normal(5, 1.5, size=NUM_ROWS).round(1)
    df['avg_session_length'] = np.clip(df['avg_session_length'], 1.0, 12.0)

    def generate_gap(row):
        b = row['behavior_segment']
        if b == 'High Performer': return np.random.randint(0, 2)
        elif b == 'Average': return np.random.randint(1, 4)
        else: return np.random.randint(2, 7)

    df['inactivity_gap_days_max'] = df.apply(generate_gap, axis=1)

    # E. RISK & COMPLIANCE PROFILE
    def generate_kyc(row):
        b = row['behavior_segment']
        if b == 'High Performer': return np.random.choice([1, 0], p=[0.99, 0.01])
        elif b == 'Average': return np.random.choice([1, 0], p=[0.95, 0.05])
        else: return np.random.choice([1, 0], p=[0.80, 0.20])

    df['kyc_verified'] = df.apply(generate_kyc, axis=1)

    def generate_suspensions(row):
        b = row['behavior_segment']
        if b == 'High Performer': return 0
        elif b == 'Average': return np.random.choice([0, 1], p=[0.9, 0.1])
        else: return np.random.choice([0, 1, 2, 3], p=[0.6, 0.2, 0.15, 0.05])

    df['account_suspensions_12m'] = df.apply(generate_suspensions, axis=1)

    def generate_violations(row):
        b = row['behavior_segment']
        if b == 'High Performer': return np.random.choice([0, 1], p=[0.95, 0.05])
        elif b == 'Average': return np.random.choice([0, 1, 2], p=[0.8, 0.15, 0.05])
        else: return np.random.choice([1, 2, 3, 4, 5], p=[0.4, 0.3, 0.15, 0.1, 0.05])

    df['policy_violations_12m'] = df.apply(generate_violations, axis=1)

    def generate_fraud(row):
        b = row['behavior_segment']
        r = row['risk_segment']
        # rare ~2% overall
        if b == 'High Performer': return 0
        elif b == 'Average' and r == 'Low': return 0
        elif b == 'Average': return np.random.choice([0, 1], p=[0.995, 0.005])
        else: return np.random.choice([0, 1], p=[0.95, 0.05])

    df['fraud_flag'] = df.apply(generate_fraud, axis=1)

    # F. DERIVED FEATURES
    max_gap = df['inactivity_gap_days_max'].max()
    if max_gap == 0: max_gap = 1
    df['activity_stability'] = (1 - (df['inactivity_gap_days_max'] / max_gap)).round(2)
    df['activity_stability'] = np.clip(df['activity_stability'] - (df['weekly_earnings_std']/10000)*0.2, 0.1, 0.99).round(2)

    df['earnings_per_hour'] = (df['gross_earnings_30d'] / df['online_hours_30d']).round(1)
    
    # FIX: Cap volatility ratio
    df['volatility_ratio'] = (df['weekly_earnings_std'] / (df['gross_earnings_30d'] / 4 + 1)).round(2)
    df['volatility_ratio'] = np.clip(df['volatility_ratio'], 0, 3.0)

    # FIX: Reliability score spread
    df['reliability_score'] = ((df['acceptance_rate'] + (1 - df['cancellation_rate']*2.5) + (df['avg_rating']/5.0) - (df['complaints_30d'] * 0.10)) / 3.0)
    df['reliability_score'] += np.random.normal(0, 0.1, size=NUM_ROWS)
    df['reliability_score'] = np.clip(df['reliability_score'], 0.1, 1.0).round(2)

    # FIX: Discipline score spread and penalty
    df['discipline_score'] = ((df['login_days_30d']/30.0) * 0.4 + 
                              (1 - np.clip(df['inactivity_gap_days_max']/7.0, 0, 1)) * 0.3 +
                              (1 - np.clip(df['complaints_30d']/4.0, 0, 1)) * 0.2 + 
                              (1 - np.clip(df['policy_violations_12m']/3.0, 0, 1)) * 0.1)
    df['discipline_score'] += np.random.normal(0, 0.15, size=NUM_ROWS)
    df['discipline_score'] = np.clip(df['discipline_score'], 0.1, 1.0).round(2)

    # G. TARGET VARIABLES
    def generate_default_prob(row):
        r = row['risk_segment']
        if r == 'Low': return np.random.uniform(0.01, 0.15)
        elif r == 'Medium': return np.random.uniform(0.15, 0.45)
        else: return np.random.uniform(0.45, 0.90)

    df['default_prob'] = df.apply(generate_default_prob, axis=1).round(2)
    df['default'] = np.random.binomial(1, df['default_prob'])

    df['credit_score'] = (850 - (df['default_prob'] * 500) + np.random.normal(0, 20, size=NUM_ROWS)).astype(int)
    df['credit_score'] = np.clip(df['credit_score'], 300, 850)

    # Drop helper segments
    df_final = df.drop(columns=['risk_segment', 'behavior_segment'])

    # Reorder columns
    columns_order = [
        'Worker ID',
        'active_days_30d', 'online_hours_30d', 'avg_hours_per_active_day', 'acceptance_rate', 'cancellation_rate', 'peak_hour_share',
        'avg_rating', 'rating_count', 'rating_std', 'complaints_30d',
        'gross_earnings_30d', 'net_payout_30d', 'weekly_earnings_std', 'incentive_share',
        'login_days_30d', 'avg_session_length', 'inactivity_gap_days_max',
        'kyc_verified', 'account_suspensions_12m', 'policy_violations_12m', 'fraud_flag',
        'activity_stability', 'earnings_per_hour', 'volatility_ratio', 'reliability_score', 'discipline_score',
        'default_prob', 'default', 'credit_score'
    ]
    df_final = df_final[columns_order]

    output_path = os.path.join(os.path.dirname(__file__), 'realistic_gig_worker_dataset.csv')
    df_final.to_csv(output_path, index=False)
    print(f"Dataset generated successfully at: {output_path}")

if __name__ == "__main__":
    generate_gig_dataset()
