from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
import sys

import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import sessionmaker


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = REPO_ROOT / "backend"
TEST_DB_PATH = REPO_ROOT / "tests" / "test.db"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

TEST_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("DATABASE_URL", f"sqlite:///{TEST_DB_PATH.as_posix()}")
os.environ.setdefault("DISABLE_DB_INIT", "1")

from app.database import Base  # noqa: E402
from app.deps import get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.services.feature_engineering import build_features  # noqa: E402
from sqlalchemy.dialects.postgresql import JSONB  # noqa: E402


@compiles(JSONB, "sqlite")
def _compile_jsonb_sqlite(_element, _compiler, **_kw):
    return "JSON"


_TEST_ENGINE = create_engine(
    os.environ["DATABASE_URL"],
    connect_args={"check_same_thread": False},
)
_TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_TEST_ENGINE)


@pytest.fixture(scope="session", autouse=True)
def _create_test_schema():
    """Create all tables once for the test session."""
    Base.metadata.create_all(bind=_TEST_ENGINE)
    yield
    Base.metadata.drop_all(bind=_TEST_ENGINE)


def _override_get_db():
    db = _TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def api_client():
    """FastAPI client with DB dependency override for tests."""
    app.dependency_overrides[get_db] = _override_get_db
    from fastapi.testclient import TestClient

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@dataclass
class PlatformDataStub:
    active_days_30d: float
    online_hours_30d: float
    avg_hours_per_active_day: float
    acceptance_rate: float
    cancellation_rate: float
    peak_hour_share: float
    avg_rating: float
    rating_count: int
    rating_std: float
    complaints_30d: int
    gross_earnings_30d: float
    net_payout_30d: float
    weekly_earnings_std: float
    incentive_share: float
    login_days_30d: int
    avg_session_length: float
    inactivity_gap_days_max: int
    kyc_verified: bool
    account_suspensions_12m: int
    policy_violations_12m: int
    fraud_flag: bool
    activity_stability: float
    earnings_per_hour: float
    volatility_ratio: float
    reliability_score: float
    discipline_score: float


@pytest.fixture()
def sample_platforms() -> list[PlatformDataStub]:
    """Provide mock platform data for feature engineering tests."""
    return [
        PlatformDataStub(
            active_days_30d=26,
            online_hours_30d=180,
            avg_hours_per_active_day=6.9,
            acceptance_rate=0.9,
            cancellation_rate=0.05,
            peak_hour_share=0.6,
            avg_rating=4.8,
            rating_count=320,
            rating_std=0.2,
            complaints_30d=0,
            gross_earnings_30d=42000,
            net_payout_30d=36000,
            weekly_earnings_std=1200,
            incentive_share=0.35,
            login_days_30d=27,
            avg_session_length=5.5,
            inactivity_gap_days_max=1,
            kyc_verified=True,
            account_suspensions_12m=0,
            policy_violations_12m=0,
            fraud_flag=False,
            activity_stability=0.85,
            earnings_per_hour=210,
            volatility_ratio=0.4,
            reliability_score=0.88,
            discipline_score=0.9,
        ),
        PlatformDataStub(
            active_days_30d=22,
            online_hours_30d=120,
            avg_hours_per_active_day=5.4,
            acceptance_rate=0.78,
            cancellation_rate=0.12,
            peak_hour_share=0.45,
            avg_rating=4.2,
            rating_count=180,
            rating_std=0.5,
            complaints_30d=2,
            gross_earnings_30d=30000,
            net_payout_30d=25500,
            weekly_earnings_std=2200,
            incentive_share=0.2,
            login_days_30d=22,
            avg_session_length=4.8,
            inactivity_gap_days_max=2,
            kyc_verified=True,
            account_suspensions_12m=0,
            policy_violations_12m=0,
            fraud_flag=False,
            activity_stability=0.72,
            earnings_per_hour=170,
            volatility_ratio=0.85,
            reliability_score=0.72,
            discipline_score=0.7,
        ),
    ]


@pytest.fixture()
def sample_features(sample_platforms: list[PlatformDataStub]) -> dict[str, float]:
    """Provide engineered features derived from mock platform data."""
    return build_features(sample_platforms)
