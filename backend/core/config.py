from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Galaeros API"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"  # "development" | "staging" | "production"
    DEBUG: bool = False

    # Database Settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "galaeros"

    # Firebase Authentication
    # Path to a service-account JSON file. If unset, falls back to
    # Application Default Credentials (e.g. Cloud Run's attached identity).
    FIREBASE_CREDENTIALS_PATH: str | None = None
    FIREBASE_PROJECT_ID: str | None = None

    # CORS -- comma-separated in the environment, e.g.
    # CORS_ALLOW_ORIGINS=https://app.galaeros.ph,https://galaeros.ph
    CORS_ALLOW_ORIGINS: list[str] = ["*"]

    @property
    def DATABASE_URL(self) -> str:
        # We will use asyncpg for asynchronous operations
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def SYNC_DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")


settings = Settings()
