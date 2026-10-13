import json
import logging
import secrets
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "AI Digital Bodyguard"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DATABASE_URL: str = "sqlite:///./bodyguard.db"
    # JWT signing key. Never ship a fixed default: anyone who reads this file could forge
    # tokens for a deployment that kept it. If unset, a random key is generated per process
    # (tokens then stop working on restart), and a warning is logged.
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    CORS_ORIGINS: str = '["http://localhost:3000","http://localhost:8080"]'
    MONITOR_INTERVAL: int = 30
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "bodyguard.log"

    @property
    def cors_origins_list(self) -> list[str]:
        try:
            return json.loads(self.CORS_ORIGINS)
        except Exception:
            return ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

if not settings.SECRET_KEY:
    settings.SECRET_KEY = secrets.token_urlsafe(32)
    logging.getLogger(__name__).warning(
        "SECRET_KEY is not set; using a random per-process key. Set SECRET_KEY so that "
        "issued tokens survive restarts and are shared across workers."
    )
