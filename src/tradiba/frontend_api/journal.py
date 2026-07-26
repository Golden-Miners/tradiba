from typing import Dict, Any, List

class TradeJournalService:
    """Automatically captures entries, exits, screenshots, and AI explanations."""
    
    def __init__(self) -> None:
        self._entries: List[Dict[str, Any]] = []
        
    def add_entry(self, entry: Dict[str, Any]) -> None:
        self._entries.append(entry)
        
    def get_entries(self) -> List[Dict[str, Any]]:
        return self._entries
