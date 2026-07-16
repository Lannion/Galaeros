"""
`User` service -- business logic for account onboarding and profile
management. Routers call these functions and never touch the repository or
ORM directly.
"""
from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.user import User
from backend.repositories import user_repository
from backend.schemas.user import UserCreate, UserUpdate


async def get_by_id(db: AsyncSession, *, user_id: uuid.UUID) -> User | None:
    return await user_repository.get_by_id(db, user_id=user_id)


async def get_by_firebase_uid(db: AsyncSession, *, firebase_uid: str) -> User | None:
    return await user_repository.get_by_firebase_uid(db, firebase_uid=firebase_uid)


async def create_profile(db: AsyncSession, *, data: UserCreate) -> User:
    """
    Create a new `User` row for a verified Firebase account.

    Callers (the onboarding endpoint) are responsible for first checking
    `get_by_firebase_uid` to avoid a duplicate-profile race turning into an
    unhandled integrity error here.
    """
    user = User(
        firebase_uid=data.firebase_uid,
        email=data.email,
        display_name=data.display_name,
        avatar_url=data.avatar_url,
    )
    return await user_repository.create(db, user=user)


async def update_profile(db: AsyncSession, *, user: User, payload: UserUpdate) -> User:
    """Apply only the fields the client actually sent (PATCH semantics)."""
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    return await user_repository.save(db, user=user)
