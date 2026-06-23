"""Runtime settings for the SanJuan AI API.

The API intentionally uses environment variables instead of a larger settings
framework for the MVP. This keeps deployment simple while still giving production
hosts control over CORS and security-related behavior.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_DEV_CORS_ORIGINS = (
    "http://localhost:3000",
    "http://127.0.0.1:3000",
)


@dataclass(frozen=True)
class ApiSettings:
    """Runtime configuration for the FastAPI service."""

    environment: str
    cors_origins: tuple[str, ...]
    allow_credentials: bool
    api_version: str

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"


def parse_csv_env(value: str | None) -> tuple[str, ...]:
    """Parse a comma-separated environment variable into clean values."""
    if not value:
        return ()
    return tuple(item.strip() for item in value.split(",") if item.strip())


def load_api_settings() -> ApiSettings:
    """Load API settings from environment variables."""
    environment = os.getenv("SANJUAN_ENV", "development").strip() or "development"
    configured_origins = parse_csv_env(os.getenv("SANJUAN_CORS_ORIGINS"))

    if configured_origins:
        cors_origins = configured_origins
    elif environment.lower() == "production":
        # Production should explicitly configure the deployed web origin. Keeping
        # the default empty avoids accidentally allowing every origin.
        cors_origins = ()
    else:
        cors_origins = DEFAULT_DEV_CORS_ORIGINS

    allow_credentials = os.getenv("SANJUAN_CORS_ALLOW_CREDENTIALS", "false").lower() == "true"
    api_version = os.getenv("SANJUAN_API_VERSION", "0.5.0")

    return ApiSettings(
        environment=environment,
        cors_origins=cors_origins,
        allow_credentials=allow_credentials,
        api_version=api_version,
    )
