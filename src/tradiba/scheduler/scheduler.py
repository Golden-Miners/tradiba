"""
Production scheduler.
"""

from __future__ import annotations

from time import monotonic
from time import sleep

from tradiba.logging import get_logger

from .task import Task

logger = get_logger(__name__)


class Scheduler:
    """
    Cooperative scheduler.
    """

    def __init__(self) -> None:
        self._tasks: list[Task] = []
        self._running = False

    def add_task(self, task: Task) -> None:
        self._tasks.append(task)

    def remove_task(self, name: str) -> None:
        self._tasks = [t for t in self._tasks if t.name != name]

    def stop(self) -> None:
        self._running = False

    def run(self) -> None:
        self._running = True

        previous = monotonic()

        while self._running:

            now = monotonic()
            delta = now - previous
            previous = now

            for task in self._tasks:

                if not task.enabled:
                    continue

                if task.running:
                    continue

                task.elapsed += delta

                if task.elapsed < task.interval:
                    continue

                task.elapsed = 0.0
                task.running = True

                try:
                    task.action()

                except Exception:
                    logger.exception(
                        "Scheduled task '%s' failed.",
                        task.name,
                    )

                finally:
                    task.running = False

            sleep(0.05)