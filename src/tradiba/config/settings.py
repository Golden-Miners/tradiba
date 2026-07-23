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


@dataclass(slots=True)
class DatabaseSettings:
    path: str


@dataclass(slots=True)
class DashboardSettings:
    host: str
    port: int


@dataclass(slots=True)
class Settings:
    mt5: MT5Settings
    database: DatabaseSettings
    dashboard: DashboardSettings