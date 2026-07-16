"""
Shared declarative base and reusable mixins for every Galaeros ORM model.

Every table in the system composes these mixins so that the conventions
defined in the engineering skill are enforced structurally instead of by
convention alone:

    - UUID primary keys (internal integer IDs are never exposed over the API)
    - `created_at` / `updated_at` on every table
    - Soft deletes via `deleted_at` (important data is never hard-deleted)

Import `Base` from here in every model module so they all share one
`MetaData` / registry, which Alembic needs to autogenerate migrations
correctly.
"""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Declarative base shared by every ORM model in the backend."""


class UUIDPrimaryKeyMixin:
    """
    Gives a model a UUID primary key.

    UUIDs are generated client-side (Python's `uuid4`) rather than relying on
    a Postgres extension like `pgcrypto`, so IDs are available immediately
    after `Model(...)` is constructed and before the row is flushed -- useful
    when the API needs to return the new ID or reference it in a related
    object within the same request.
    """

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )


class TimestampMixin:
    """Adds `created_at` / `updated_at`, both maintained by the database."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class SoftDeleteMixin:
    """
    Adds `deleted_at` for soft deletes.

    Repositories should filter `deleted_at IS NULL` by default rather than
    issuing `DELETE` statements, per the "never permanently delete important
    data" rule. A dedicated hard-delete admin operation can bypass this when
    legally required (e.g. GDPR-style erasure requests).
    """

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
