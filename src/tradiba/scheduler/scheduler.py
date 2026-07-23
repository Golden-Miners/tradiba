"""
Production scheduler.
"""

from __future__ import annotations

from threading import Thread
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
        self._thread: Thread | None = None

    def add_task(self, task: Task) -> None:
        self._tasks.append(task)

    def remove_task(self, name: str) -> None:
        self._tasks = [t for t in self._tasks if t.name != name]

    def stop(self) -> None:
        self._running = False
        if self._thread is not None:
            self._thread.join(timeout=2.0)
            self._thread = None

    def start(self) -> None:
        """Start the scheduler loop on a background daemon thread."""
        self._thread = Thread(target=self.run, daemon=True)
        self._thread.start()

    @property
    def is_running(self) -> bool:
        return self._running

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