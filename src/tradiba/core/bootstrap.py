"""
Application bootstrap.
"""

from __future__ import annotations

from dataclasses import dataclass

from tradiba.events import EventBus
from tradiba.mt5 import MT5Service
from tradiba.scheduler import Scheduler

from .container import Container
from .lifecycle import Lifecycle


@dataclass(slots=True)
class BootstrapResult:
    event_bus: EventBus
    scheduler: Scheduler
    mt5: MT5Service


def bootstrap(
    container: Container,
    lifecycle: Lifecycle,
) -> BootstrapResult:
    event_bus = EventBus()
    scheduler = Scheduler()
    mt5 = MT5Service()

    container.register_singleton(EventBus, event_bus)
    container.register_singleton(Scheduler, scheduler)
    container.register_singleton(MT5Service, mt5)

    lifecycle.add(mt5)

    return BootstrapResult(
        event_bus=event_bus,
        scheduler=scheduler,
        mt5=mt5,
    )