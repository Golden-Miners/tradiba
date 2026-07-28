from typing import Dict, Any

class ExecutionContext:
    """
    Runtime sandboxing specifically for executing automation steps, secret injection, and checkpointing.
    """
    def __init__(self):
        self.context: Dict[str, Any] = {}

    def inject_secrets(self, secrets: Dict[str, str]) -> None:
        self.context["secrets"] = secrets

    def save_checkpoint(self, state: Dict[str, Any]) -> None:
        self.context["checkpoint"] = state
