from pathlib import Path
from pydantic_settings import BaseSettings
import os


class Config(BaseSettings):
    """Application configuration.

    For this assignment we mainly use BASE_DIR and MEDIA_DIR for file uploads.
    """

    SECRET_KEY: str = "default_secret_key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Project root (here: fastapi_assignment)
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    MEDIA_DIR: str = os.path.join(BASE_DIR, "media")


def get_config() -> Config:
    return Config()


config = get_config()
