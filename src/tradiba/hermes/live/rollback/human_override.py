from enum import Enum
from typing import Dict, Any, List
import datetime

class OverrideState(Enum):
    NORMAL = 0
    PAUSED = 1
    MANUAL_ONLY = 2

class HumanOverrideManager:
    """
    Provides operators with capabilities to:
    - Pause Hermes
    - Resume Hermes
    - Force manual mode
    - Reject specific proposals
    - Review decision history
    """

    def __init__(self):
        self._state = OverrideState.NORMAL
        self._history = []

    def pause_hermes(self, reason: str):
        self._state = OverrideState.PAUSED
        self._log_override("PAUSE", reason)

    def resume_hermes(self, reason: str):
        self._state = OverrideState.NORMAL
        self._log_override("RESUME", reason)

    def force_manual_mode(self, reason: str):
        self._state = OverrideState.MANUAL_ONLY
        self._log_override("MANUAL_MODE", reason)

    def is_paused(self) -> bool:
        return self._state == OverrideState.PAUSED

    def is_manual_only(self) -> bool:
        return self._state == OverrideState.MANUAL_ONLY

    def reject_proposal(self, proposal_id: str, reason: str):
        self._log_override(f"REJECT_PROPOSAL:{proposal_id}", reason)

    def _log_override(self, action: str, reason: str):
        self._history.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "action": action,
            "reason": reason
        })

    def get_history(self) -> List[Dict[str, Any]]:
        return self._history
