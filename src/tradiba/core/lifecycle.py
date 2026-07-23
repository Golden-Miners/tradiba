"""
Application lifecycle manager.
"""

from __future__ import annotations

from .service import Service


class Lifecycle:

    def __init__(self) -> None:
        self._services: list[Service] = []

    def add(self, service: Service) -> None:
        self._services.append(service)

    def start(self) -> None:
        for service in self._services:
            service.start()

    def stop(self) -> None:
        for service in reversed(self._services):
            service.stop()