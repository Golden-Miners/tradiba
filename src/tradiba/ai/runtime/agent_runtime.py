from typing import Dict, Any

class AIRuntime:
    """
    Common runtime for all AI agents managing lifecycle, context, memory, and tools.
    """
    def __init__(self):
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        
    def start_session(self, session_id: str, agent_id: str):
        self.active_sessions[session_id] = {
            "agent_id": agent_id,
            "status": "RUNNING",
            "context": {},
            "history": []
        }
        
    def execute_turn(self, session_id: str, input_data: Any) -> Dict[str, Any]:
        if session_id not in self.active_sessions:
            raise ValueError("Session not found")
            
        session = self.active_sessions[session_id]
        session["history"].append(input_data)
        
        # Simulate execution
        response = {"output": f"Processed {input_data} by {session['agent_id']}"}
        session["history"].append(response)
        
        return response
