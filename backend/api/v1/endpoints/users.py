"""
`/api/v1/users` -- account onboarding and profile management.

Routers stay thin: they parse/validate input (via Pydantic + FastAPI),
enforce auth, and delegate to `backend.services.user_service`. No SQLAlchemy
queries appear in this file -- that belongs to the repository layer that
the service calls, per skills.md > FastAPI ("Separate schemas / models /
services / repositories / routers").
"""
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.deps import get_current_active_user, get_db, get_firebase_claims
from backend.models.user import User
from backend.schemas.user import UserCreate, UserOnboardingRequest, UserPrivateRead, UserRead, UserUpdate
from backend.services import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserPrivateRead)
async def read_my_profile(current_user: User = Depends(get_current_active_user)) -> User:
    """Return the authenticated user's full profile, including contact info."""
    return current_user


@router.patch("/me", response_model=UserPrivateRead)
async def update_my_profile(
    payload: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Update editable profile fields for the authenticated user.

    Delegates to `user_service.update_profile`, which is responsible for
    persisting the change and returning the refreshed `User`.
    """
    return await user_service.update_profile(db, user=current_user, payload=payload)


@router.post(
    "",
    response_model=UserPrivateRead,
    status_code=status.HTTP_201_CREATED,
)
async def complete_onboarding(
    payload: UserOnboardingRequest,
    claims: dict = Depends(get_firebase_claims),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Create the Galaeros profile for an already-Firebase-authenticated caller.

    Identity fields (`firebase_uid`, `email`) come from the
    verified token, never from `payload` -- see `UserOnboardingRequest`'s
    docstring for why.
    """
    existing = await user_service.get_by_firebase_uid(db, firebase_uid=claims["uid"])
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A profile already exists for this account.",
        )

    email = claims.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "This Firebase account has no verified email. `email` is "
                "required on User; phone-only sign-in isn't supported yet."
            ),
        )

    data = UserCreate(
        firebase_uid=claims["uid"],
        email=email,
        display_name=payload.display_name,
        avatar_url=payload.avatar_url,
    )
    return await user_service.create_profile(db, data=data)


@router.get("/{user_id}", response_model=UserRead)
async def read_user_profile(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> User:
    """Return another user's public profile (no contact info)."""
    user = await user_service.get_by_id(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user
