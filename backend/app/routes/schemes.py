from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..deps import get_db, require_borrower, require_lender
from ..models.loan_scheme import LoanScheme
from ..models.user import User
from ..schemas.loan_scheme import (
    LoanSchemeCreateRequest,
    LoanSchemeResponse,
    LoanSchemeUpdateRequest,
)


router = APIRouter(prefix="/schemes", tags=["schemes"])


@router.post(
    "/",
    response_model=LoanSchemeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_scheme(
    payload: LoanSchemeCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lender),
) -> LoanSchemeResponse:
    if payload.min_amount > payload.max_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Minimum amount cannot be greater than maximum amount",
        )

    scheme = LoanScheme(
        lender_id=current_user.id,
        scheme_name=payload.scheme_name.strip(),
        description=payload.description,
        min_amount=payload.min_amount,
        max_amount=payload.max_amount,
        interest_rate=payload.interest_rate,
        tenure_months=payload.tenure_months,
        min_score_required=payload.min_score_required,
        eligible_risk_level=payload.eligible_risk_level,
        is_active=payload.is_active,
    )

    db.add(scheme)
    db.commit()
    db.refresh(scheme)

    return scheme


@router.get("/my", response_model=list[LoanSchemeResponse])
def list_my_schemes(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lender),
) -> list[LoanSchemeResponse]:
    schemes = (
        db.query(LoanScheme)
        .filter(LoanScheme.lender_id == current_user.id)
        .order_by(LoanScheme.created_at.desc())
        .all()
    )

    return schemes


@router.get("/public", response_model=list[LoanSchemeResponse])
def list_public_schemes(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_borrower),
) -> list[LoanSchemeResponse]:
    schemes = (
        db.query(LoanScheme)
        .filter(LoanScheme.is_active == True)
        .order_by(LoanScheme.created_at.desc())
        .all()
    )

    return schemes


@router.patch("/{scheme_id}", response_model=LoanSchemeResponse)
def update_scheme(
    scheme_id: int,
    payload: LoanSchemeUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lender),
) -> LoanSchemeResponse:
    scheme = (
        db.query(LoanScheme)
        .filter(
            LoanScheme.id == scheme_id,
            LoanScheme.lender_id == current_user.id,
        )
        .first()
    )

    if not scheme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan scheme not found",
        )

    update_data = payload.model_dump(exclude_unset=True)

    if "scheme_name" in update_data and update_data["scheme_name"] is not None:
        update_data["scheme_name"] = update_data["scheme_name"].strip()

    for key, value in update_data.items():
        setattr(scheme, key, value)

    if scheme.min_amount > scheme.max_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Minimum amount cannot be greater than maximum amount",
        )

    db.commit()
    db.refresh(scheme)

    return scheme


@router.delete("/{scheme_id}")
def delete_scheme(
    scheme_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lender),
):
    scheme = (
        db.query(LoanScheme)
        .filter(
            LoanScheme.id == scheme_id,
            LoanScheme.lender_id == current_user.id,
        )
        .first()
    )

    if not scheme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan scheme not found",
        )

    # Soft delete by deactivating scheme
    scheme.is_active = False

    db.commit()

    return {"message": "Loan scheme deactivated successfully"}