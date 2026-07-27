from typing import List, Set, Tuple

class KnowledgeGraph:
    """Lightweight in-memory representation of domain relationships."""
    
    def __init__(self):
        self._edges: Set[Tuple[str, str, str]] = set()  # (source, relation, target)
        
    def add_relationship(self, source: str, relation: str, target: str):
        """Add a relationship to the graph."""
        self._edges.add((source, relation, target))
        
    def get_related(self, source: str, relation: str) -> List[str]:
        """Find all targets connected to source by the given relation."""
        return [target for s, r, target in self._edges if s == source and r == relation]
