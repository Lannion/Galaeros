"""
Firebase Admin SDK initialization.

`backend.api.deps` calls `firebase_admin.auth.verify_id_token(...)` directly,
which requires the SDK to already be initialized -- `init_firebase()` does
that, and must run once before the first request is handled (see
`main.py`'s startup hook).
"""
from __future__ import annotations

import firebase_admin
from firebase_admin import credentials

from backend.core.config import settings


def init_firebase() -> None:
    """
    Initialize the Firebase Admin app if it hasn't been already.

    Guarded by `firebase_admin._apps` so this is safe to call more than
    once -- useful under a multi-worker server (e.g. Uvicorn with
    `--workers`) or in tests that import `main` multiple times.
    """
    if firebase_admin._apps:
        return

    if settings.FIREBASE_CREDENTIALS_PATH:
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
    else:
        # Falls back to Application Default Credentials -- appropriate for
        # environments like Cloud Run where the service account is attached
        # to the runtime rather than shipped as a JSON key file.
        cred = credentials.ApplicationDefault()

    options = {"projectId": settings.FIREBASE_PROJECT_ID} if settings.FIREBASE_PROJECT_ID else None
    firebase_admin.initialize_app(cred, options)
