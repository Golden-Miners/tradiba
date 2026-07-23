"""
Dependency injection container.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any
from typing import TypeVar

T = TypeVar("T")


class Container:
    """
    Lightweight dependency injection container.

    Supports:

    - singleton registration
    - factory registration
    - type-safe resolution
    """

    def __init__(self) -> None:
        self._singletons: dict[type[Any], Any] = {}
        self._factories: dict[type[Any], Callable[[], Any]] = {}

    def register_singleton(
        self,
        interface: type[T],
        instance: T,
    ) -> None:
        if interface in self._singletons:
            raise ValueError(
                f"{interface.__name__} already registered."
            )

        self._singletons[interface] = instance

    def register_factory(
        self,
        interface: type[T],
        factory: Callable[[], T],
    ) -> None:
        if interface in self._factories:
            raise ValueError(
                f"{interface.__name__} already registered."
            )

        self._factories[interface] = factory

    def resolve(
        self,
        interface: type[T],
    ) -> T:

        if interface in self._singletons:
            return self._singletons[interface]

        if interface in self._factories:
            return self._factories[interface]()

        raise LookupError(
            f"No registration found for "
            f"{interface.__name__}."
        )

    def contains(
        self,
        interface: type[Any],
    ) -> bool:
        return (
            interface in self._singletons
            or interface in self._factories
        )

    def clear(self) -> None:
        self._singletons.clear()
        self._factories.clear()