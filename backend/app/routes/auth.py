from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..deps import get_db, get_current_user
from ..models.user import User
from ..models.lender import LenderProfile
from ..schemas.user import (
    LenderRegisterRequest,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from ..utils.security import (
    create_access_token,
    hash_password,
    verify_password,
)


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    payload: UserRegisterRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    existing_user = (
        db.query(User)
        .filter(User.email == payload.email.lower().strip())
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = User(
        name=payload.name.strip(),
        email=payload.email.lower().strip(),
        password_hash=hash_password(payload.password),
        role="borrower",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "role": user.role,
        }
    )

    return TokenResponse(access_token=access_token)


@router.post(
    "/lender-register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_lender(
    payload: LenderRegisterRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    existing_user = (
        db.query(User)
        .filter(User.email == payload.email.lower().strip())
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    email = payload.email.lower().strip()
    email_domain = email.split("@")[-1] if "@" in email else None

    user = User(
        name=payload.name.strip(),
        email=email,
        password_hash=hash_password(payload.password),
        role="lender",
    )

    db.add(user)
    db.flush()

    lender_profile = LenderProfile(
        user_id=user.id,
        institution_name=payload.institution_name.strip(),
        institution_type=payload.institution_type,
        license_number=payload.license_number.strip(),
        official_email_domain=email_domain,
        verification_status="pending",
    )

    db.add(lender_profile)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "role": user.role,
        }
    )

    return TokenResponse(access_token=access_token)


@router.post("/login", response_model=TokenResponse)
def login_user(
    payload: UserLoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    user = (
        db.query(User)
        .filter(User.email == payload.email.lower().strip())
        .first()
    )

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "role": user.role,
        }
    )

    return TokenResponse(access_token=access_token)


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    return current_user