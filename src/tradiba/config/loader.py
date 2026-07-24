"""
Configuration loader.
"""

from __future__ import annotations

from pathlib import Path
import tomllib

from .settings import (
    APISettings,
    DatabaseSettings,
    MT5Settings,
    Settings,
)

DEFAULT_CONFIG = (
    Path(__file__)
    .with_name("settings.toml")
)

def load_settings() -> Settings:
    """Load application settings from the TOML file."""
    with DEFAULT_CONFIG.open("rb") as fp:
        data = tomllib.load(fp)

    return Settings(
        mt5=MT5Settings(**data.get("mt5", {})),
        database=DatabaseSettings(**data.get("database", {})),
        api=APISettings(**data.get("api", {})),
        strategies=data.get("strategies", {}),
        risk=data.get("risk", {}),
    )