from dataclasses import dataclass
from typing import Callable

@dataclass
class RunbookStep:
    name: str
    action: Callable[[], bool]
    is_automated: bool = True

class RunbookExecutor:
    """Executes operational procedures (runbooks)."""
    
    def __init__(self) -> None:
        self._runbooks: dict[str, list[RunbookStep]] = {}

    def register_runbook(self, name: str, steps: list[RunbookStep]) -> None:
        self._runbooks[name] = steps

    def execute(self, name: str) -> bool:
        """Executes a runbook, returning True if all steps succeed."""
        if name not in self._runbooks:
            raise ValueError(f"Runbook {name} not found.")

        steps = self._runbooks[name]
        for step in steps:
            if step.is_automated:
                success = step.action()
                if not success:
                    return False
            # Manual steps would pause here in a real system
        return True
