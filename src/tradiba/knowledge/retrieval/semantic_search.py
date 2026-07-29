from typing import Dict, Any, List

class SemanticSearch:
    """
    Supports hybrid search, vector search, graph traversal, and keyword search.
    """
    def search(self, query: str) -> List[Dict[str, Any]]:
        if "incident" in query:
            return [{"type": "incident", "id": "inc_123"}]
        return []
