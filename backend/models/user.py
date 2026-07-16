# backend/app/models/user.py
"""
User Domain Model (Firebase-linked, Gamification).

Authentication identity lives in Firebase Auth (see ARCHITECTURE.md >
Security); this model stores the local profile, permission role, and
gamification state Galaeros tracks on top of that identity.

Every account is a contributor from creation — see UserRole in enums.py.
There is no passive "viewer" tier; `role` is an escalating trust ladder
built on top of that shared contributor identity, and `rank` is a fully
independent progression track (earned experience, not permissions).
"""

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin
from .enums import ContributorRank, UserRole


class User(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """A Galaeros account, linked 1:1 to a Firebase Authentication user."""

    __tablename__ = "users"

    # --- Identity (Firebase-linked) ---
    firebase_uid: Mapped[str] = mapped_column(
        String(128), unique=True, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    display_name: Mapped[str] = mapped_column(String(80), nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(512), nullable=True)

    # --- Permissions (see ARCHITECTURE.md > Security > Authorization) ---
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(
            UserRole,
            name="user_role",
            native_enum=True,
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        default=UserRole.CONTRIBUTOR,
        server_default=UserRole.CONTRIBUTOR.value,
        nullable=False,
        index=True,
    )

    # --- Gamification (see README.md > Gamification) ---
    rank: Mapped[ContributorRank] = mapped_column(
        SQLEnum(
            ContributorRank,
            name="contributor_rank",
            native_enum=True,
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        default=ContributorRank.MORTAL_TRAVELER,
        server_default=ContributorRank.MORTAL_TRAVELER.value,
        nullable=False,
        index=True,
    )
    experience_points: Mapped[int] = mapped_column(
        Integer, default=0, server_default="0", nullable=False
    )

    # --- Reputation / Trust (see ARCHITECTURE.md > Reputation System) ---
    # Drives both contribution auto-approval speed and moderator eligibility.
    trust_score: Mapped[int] = mapped_column(
        Integer, default=0, server_default="0", nullable=False, index=True
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} display_name={self.display_name!r} role={self.role}>"