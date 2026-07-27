import uuid
from typing import Dict, Any, Optional
from tradiba.hermes.hcos.context.state import UnifiedCognitiveState

class CognitiveKernel:
    """
    The orchestrating kernel for Hermes Cognitive OS.
    Manages sessions, global state, task routing, and error recovery.
    """
    def __init__(self):
        self.active_sessions: Dict[str, UnifiedCognitiveState] = {}
        
    def start_session(self) -> str:
        session_id = str(uuid.uuid4())
        state = UnifiedCognitiveState(session_id=session_id)
        self.active_sessions[session_id] = state
        return session_id
        
    def get_state(self, session_id: str) -> Optional[UnifiedCognitiveState]:
        return self.active_sessions.get(session_id)
        
    def route_task(self, session_id: str, task: Dict[str, Any]) -> str:
        state = self.get_state(session_id)
        if not state:
            raise ValueError(f"Session {session_id} not found.")
        
        # Route to appropriate skill or subsystem
        state.running_tasks.append(task)
        return "TASK_ROUTED"

    def recover_session(self, session_id: str, snapshot: Dict[str, Any]) -> bool:
        """Recovers a session from a saved snapshot."""
        state = UnifiedCognitiveState(
            session_id=session_id,
            active_goals=snapshot.get("active_goals", []),
            running_tasks=snapshot.get("running_tasks", []),
            market_context=snapshot.get("market_context", {}),
            portfolio_context=snapshot.get("portfolio_context", {}),
            system_health="RECOVERED"
        )
        self.active_sessions[session_id] = state
        return True
