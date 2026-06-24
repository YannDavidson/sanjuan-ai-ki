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


def parse_bool_env(value: str | None, default: bool = False) -> bool:
    """Parse a boolean environment variable."""
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def parse_int_env(value: str | None, default: int, minimum: int | None = None) -> int:
    """Parse an integer environment variable with a safe fallback."""
    try:
        parsed = int(value) if value is not None else default
    except ValueError:
        parsed = default

    if minimum is not None:
        return max(minimum, parsed)
    return parsed


@dataclass(frozen=True)
class ApiSettings:
    """Runtime configuration for the FastAPI service."""

    environment: str
    cors_origins: tuple[str, ...]
    allow_credentials: bool
    api_version: str
    rate_limit_enabled: bool
    ask_rate_limit_per_minute: int

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

    allow_credentials = parse_bool_env(os.getenv("SANJUAN_CORS_ALLOW_CREDENTIALS"), default=False)
    api_version = os.getenv("SANJUAN_API_VERSION", "0.6.0")
    rate_limit_enabled = parse_bool_env(os.getenv("SANJUAN_RATE_LIMIT_ENABLED"), default=True)
    ask_rate_limit_per_minute = parse_int_env(
        os.getenv("SANJUAN_ASK_RATE_LIMIT_PER_MINUTE"),
        default=30,
        minimum=1,
    )

    return ApiSettings(
        environment=environment,
        cors_origins=cors_origins,
        allow_credentials=allow_credentials,
        api_version=api_version,
        rate_limit_enabled=rate_limit_enabled,
        ask_rate_limit_per_minute=ask_rate_limit_per_minute,
    )
