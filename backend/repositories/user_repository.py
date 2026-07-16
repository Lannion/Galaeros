"""
`User` repository -- the only place that writes SQLAlchemy queries against
the `users` table. Services call these functions; they never build queries
themselves, per skills.md's schemas/services/repositories separation.
"""
from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.user import User


async def get_by_id(db: AsyncSession, *, user_id: uuid.UUID) -> User | None:
    result = await db.execute(
        select(User).where(User.id == user_id, User.deleted_at.is_(None))
    )
    return result.scalar_one_or_none()


async def get_by_firebase_uid(db: AsyncSession, *, firebase_uid: str) -> User | None:
    result = await db.execute(
        select(User).where(User.firebase_uid == firebase_uid, User.deleted_at.is_(None))
    )
    return result.scalar_one_or_none()


async def create(db: AsyncSession, *, user: User) -> User:
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


async def save(db: AsyncSession, *, user: User) -> User:
    """Persist changes made to an already-tracked `User` instance."""
    await db.flush()
    await db.refresh(user)
    return user
