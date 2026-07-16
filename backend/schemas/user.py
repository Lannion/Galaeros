"""
Pydantic schemas for the `User` resource.

Matches `backend.models.user.User` exactly -- no `phone_number`,
`is_active`, or `last_seen_at` fields exist on that model (unlike an
earlier draft of this schema), and `email` is required there, not optional.
"""
from __future__ import annotations

import uuid

from pydantic import BaseModel, EmailStr, Field

from backend.models.enums import ContributorRank, UserRole
from backend.schemas.common import ORMBaseModel


class UserOnboardingRequest(BaseModel):
    """
    Client-supplied fields for `POST /api/v1/users` (onboarding).

    Deliberately excludes `firebase_uid` and `email`: those come from the
    verified Firebase token server-side (see
    `backend.api.deps.get_firebase_claims`), never from client JSON --
    otherwise a caller could claim someone else's verified email.
    """

    display_name: str = Field(..., min_length=1, max_length=80)
    avatar_url: str | None = Field(default=None, max_length=512)


class UserCreate(BaseModel):
    """Internal payload the onboarding service uses to construct a `User`."""

    firebase_uid: str = Field(..., min_length=1, max_length=128)
    email: EmailStr
    display_name: str = Field(..., min_length=1, max_length=80)
    avatar_url: str | None = Field(default=None, max_length=512)


class UserUpdate(BaseModel):
    """Partial update payload; every field is optional (PATCH semantics)."""

    display_name: str | None = Field(default=None, min_length=1, max_length=80)
    avatar_url: str | None = Field(default=None, max_length=512)


class UserRead(ORMBaseModel):
    """Public-facing user profile."""

    id: uuid.UUID
    display_name: str
    avatar_url: str | None
    role: UserRole
    rank: ContributorRank
    experience_points: int
    trust_score: int


class UserPrivateRead(UserRead):
    """
    Extended profile returned only for `GET /api/v1/users/me` -- includes
    the contact field that should never be visible on someone else's
    profile.
    """

    email: EmailStr
