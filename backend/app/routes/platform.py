from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from ..deps import get_db, require_borrower
from ..models.platform import PlatformData
from ..models.user import User
from ..schemas.platform import PlatformConnectRequest, PlatformResponse
from ..services.mock_data import generate_mock_platform_features


router = APIRouter(prefix="/platforms", tags=["platforms"])


@router.post("/connect", response_model=PlatformResponse, status_code=status.HTTP_201_CREATED)
def connect_platform(
    payload: PlatformConnectRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_borrower),
) -> PlatformResponse:
    platform_name = payload.platform_name.strip().lower()

    existing_platform = (
        db.query(PlatformData)
        .filter(
            PlatformData.user_id == current_user.id,
            PlatformData.platform_name == platform_name,
        )
        .first()
    )

    generated = generate_mock_platform_features(platform_name)

    if existing_platform:
        for key, value in generated.items():
            setattr(existing_platform, key, value)

        db.commit()
        db.refresh(existing_platform)

        return existing_platform

    platform_record = PlatformData(
        user_id=current_user.id,
        platform_name=platform_name,
        **generated,
    )

    db.add(platform_record)
    db.commit()
    db.refresh(platform_record)

    return platform_record


@router.post("/disconnect", status_code=status.HTTP_204_NO_CONTENT)
def disconnect_platform(
    payload: PlatformConnectRequest, # Reuse schema for name
    db: Session = Depends(get_db),
    current_user: User = Depends(require_borrower),
):
    platform_name = payload.platform_name.strip().lower()
    
    platform = (
        db.query(PlatformData)
        .filter(
            PlatformData.user_id == current_user.id,
            PlatformData.platform_name == platform_name,
        )
        .first()
    )

    if platform:
        db.delete(platform)
        db.commit()
    
    return None


@router.get("/", response_model=list[PlatformResponse])
def list_connected_platforms(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_borrower),
) -> list[PlatformResponse]:
    platforms = (
        db.query(PlatformData)
        .filter(PlatformData.user_id == current_user.id)
        .order_by(PlatformData.created_at.desc())
        .all()
    )

    return platforms