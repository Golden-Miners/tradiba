"""
Configuration loader.
"""

from __future__ import annotations

from pathlib import Path
import tomllib

from .settings import (
    DashboardSettings,
    DatabaseSettings,
    MT5Settings,
    Settings,
)


DEFAULT_CONFIG = (
    Path(__file__)
    .with_name("defaults.toml")
)


def load_settings() -> Settings:
    """Load application settings from the default TOML file."""

    with DEFAULT_CONFIG.open("rb") as fp:
        data = tomllib.load(fp)

    return Settings(
        mt5=MT5Settings(**data["mt5"]),
        database=DatabaseSettings(**data["database"]),
        dashboard=DashboardSettings(**data["dashboard"]),
    )