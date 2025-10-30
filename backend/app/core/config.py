import os
from typing import List


class Settings:
    """
    Minimal settings loader. Uses environment variables with safe defaults.

    For development, copy `.env.example` to `.env` and load via python-dotenv in your runner.
    """

    project_name: str = os.getenv("PROJECT_NAME", "OfficeLifeline")
    api_v1_prefix: str = os.getenv("API_V1_PREFIX", "/api/v1")
    allowed_origins: List[str] = (
        os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
        .split(",")
        if os.getenv("ALLOWED_ORIGINS") is not None
        else ["http://localhost:3000", "http://127.0.0.1:3000"]
    )

    # Vector store settings
    chroma_persist_directory: str = os.getenv("CHROMA_PERSIST_DIRECTORY", ".chroma")
    chroma_collection: str = os.getenv("CHROMA_COLLECTION", "office_lifeline_kb")

    # Debugging
    debug: bool = os.getenv("DEBUG", "false").lower() in {"1", "true", "yes"}


def get_settings() -> Settings:
    return Settings()


