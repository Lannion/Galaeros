from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.v1.api import api_router
from backend.core.config import settings
from backend.core.firebase import init_firebase

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.on_event("startup")
async def on_startup() -> None:
    """
    Initialize things that must happen exactly once, before the first
    request is handled.

    `init_firebase()` sets up the Firebase Admin SDK that
    `backend.api.deps.get_firebase_claims` relies on to verify bearer
    tokens -- without this, every authenticated endpoint would fail on its
    first call.
    """
    init_firebase()


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Basic health check endpoint to verify the service is running.
    """
    return {"status": "ok", "service": settings.PROJECT_NAME}


app.include_router(api_router, prefix=settings.API_V1_STR)
