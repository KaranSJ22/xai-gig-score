from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import os

from .database import Base, engine
from .models import (
    User,
    PanDetails,
    PlatformData,
    Prediction,
    LenderProfile,
    LoanScheme,
    LoanApplication,
)

from .routes.auth import router as auth_router
from .routes.pan import router as pan_router
from .routes.platform import router as platform_router
from .routes.predict import router as predict_router
from .routes.dashboard import router as dashboard_router

# New route files
from .routes.schemes import router as schemes_router
from .routes.applications import router as applications_router
from .routes.lender import router as lender_router
from .routes.admin import router as admin_router


# Create tables unless explicitly disabled (e.g., during tests)
if os.getenv("DISABLE_DB_INIT") != "1":
    Base.metadata.create_all(bind=engine)

app = FastAPI(title="GigScore Backend")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://127.0.0.1:3000", "http://127.0.0.1:3001", "http://127.0.0.1:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(pan_router)
app.include_router(platform_router)
app.include_router(predict_router)
app.include_router(dashboard_router)

# New routers
app.include_router(schemes_router)
app.include_router(applications_router)
app.include_router(lender_router)
app.include_router(admin_router)