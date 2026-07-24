"""
Application configuration models.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class MT5Settings:
    terminal_path: str
    login: int
    password: str
    server: str
    timeout: int = 60000


@dataclass(slots=True)
class DatabaseSettings:
    url: str


@dataclass(slots=True)
class APISettings:
    host: str
    port: int


@dataclass(slots=True)
class Settings:
    mt5: MT5Settings
    database: DatabaseSettings
    api: APISettings
    strategies: dict[str, dict] = __import__("dataclasses").field(default_factory=dict)
    risk: dict[str, float] = __import__("dataclasses").field(default_factory=dict)