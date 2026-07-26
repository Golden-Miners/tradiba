from typing import Dict, Any

class WorkspaceEngine:
    """Manages and synchronizes user layouts, open charts, and preferences."""
    
    def __init__(self) -> None:
        self._workspaces: Dict[str, Dict[str, Any]] = {}
        
    def save_layout(self, user_id: str, layout: Dict[str, Any]) -> None:
        self._workspaces[user_id] = layout
        
    def get_layout(self, user_id: str) -> Dict[str, Any]:
        return self._workspaces.get(user_id, {})
