"""
Application configuration settings.
"""

import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # API Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = os.getenv(
        "ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000"
    ).split(",")

    # File Upload Configuration
    MAX_FILE_SIZE: int = int(
        os.getenv("MAX_FILE_SIZE", 10 * 1024 * 1024)
    )  # 10MB default
    ALLOWED_MIME_TYPES: List[str] = ["application/pdf"]
    ALLOWED_EXTENSIONS: List[str] = [".pdf"]

    # LLM Configuration
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", 4000))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", 0))

    # RAG Configuration
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", 1000))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", 200))

    # Output Configuration
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "outputs")

    # Rate Limiting (optional)
    RATE_LIMIT_ENABLED: bool = (
        os.getenv("RATE_LIMIT_ENABLED", "false").lower() == "true"
    )
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", 10))

    def validate(self) -> None:
        """Validate required settings."""
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        if self.MAX_FILE_SIZE <= 0:
            raise ValueError("MAX_FILE_SIZE must be positive")

        if self.MAX_TOKENS <= 0:
            raise ValueError("MAX_TOKENS must be positive")


settings = Settings()
