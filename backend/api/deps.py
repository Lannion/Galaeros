"""
Shared FastAPI dependencies for the `api/` layer.

Per skills.md > FASTAPI, dependency injection here is done with plain
`Depends()` -- no service-locator pattern, no globals. Every endpoint
declares exactly what it needs (a DB session, the current user, a required
role) and FastAPI wires it up per-request.

ASSUMPTION: `backend/core/database.py` exposes an async session provider
(`get_db`) -- this is where the SQLAlchemy async engine/sessionmaker from
your already-working Alembic + PostGIS setup lives, per the `core/` folder
in the project structure.
"""
from __future__ import annotations

import uuid

from fastapi import Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth as firebase_auth
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db as _get_db_session
from backend.models.enums import UserRole
from backend.models.user import User

_bearer_scheme = HTTPBearer(auto_error=False)


async def get_db(session: AsyncSession = Depends(_get_db_session)) -> AsyncSession:
    """
    Thin pass-through so endpoints depend on `backend.api.deps.get_db`
    rather than importing `core.database` directly -- keeps the session
    provider swappable without touching every router.
    """
    return session


async def get_firebase_claims(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
) -> dict:
    """
    Verify the Firebase ID token and return its decoded claims.

    This is deliberately separate from `get_current_user` below: onboarding
    (`POST /api/v1/users`) needs a verified identity *before* a Galaeros
    `User` row exists, so it can't depend on something that 404s in exactly
    that situation.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        return firebase_auth.verify_id_token(credentials.credentials)
    except Exception as exc:  # firebase_admin raises several distinct exception types
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


async def get_current_user(
    claims: dict = Depends(get_firebase_claims),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Resolve a verified Firebase token to a Galaeros `User` row.

    Raises 404 if the token is valid but no profile has been created yet --
    the client should treat that as "call `POST /api/v1/users` to finish
    onboarding," not as an error.
    """
    firebase_uid: str = claims["uid"]

    result = await db.execute(
        select(User).where(User.firebase_uid == firebase_uid, User.deleted_at.is_(None))
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Authenticated, but no Galaeros profile exists yet for this account.",
        )

    return user


async def get_current_active_user(user: User = Depends(get_current_user)) -> User:
    """
    Alias for `get_current_user`.

    NOTE: your `User` model has no `is_active`/deactivation field, so this
    currently does nothing extra. Kept as a separate dependency (rather
    than having every endpoint depend on `get_current_user` directly) so
    that adding account deactivation later is a one-line change here
    instead of touching every router.
    """
    return user


def require_role(*allowed_roles: UserRole):
    """
    Dependency factory for role-gated endpoints, e.g.:

        @router.delete("/stops/{stop_id}")
        async def delete_stop(user: User = Depends(require_role(UserRole.MODERATOR, UserRole.ADMINISTRATOR))):
            ...
    """

    async def _check_role(user: User = Depends(get_current_active_user)) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This action requires one of these roles: {[r.value for r in allowed_roles]}.",
            )
        return user

    return _check_role


class PaginationParams:
    """
    Common `?page=&page_size=` query params, per skills.md > API STYLE
    ("Always support pagination, sorting, filtering, search").
    """

    def __init__(
        self,
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=20, ge=1, le=100),
    ) -> None:
        self.page = page
        self.page_size = page_size

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


def parse_uuid_path_param(value: str, *, param_name: str = "id") -> uuid.UUID:
    """
    Explicit UUID parsing with a clean 422 instead of FastAPI's default
    error shape -- used where a path param needs validation beyond what
    `UUID` type coercion gives for free.
    """
    try:
        return uuid.UUID(value)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"'{value}' is not a valid {param_name}.",
        ) from exc
