
class EngineeringKnowledgeGraph:
    """
    Tracks historical relationships between modules, APIs, and changes.
    """
    def __init__(self):
        self.nodes = {}
        self.edges = []
        
    def add_node(self, node_id: str, node_type: str):
        self.nodes[node_id] = {"type": node_type}
        
    def add_edge(self, source: str, target: str, relationship: str):
        self.edges.append({"source": source, "target": target, "rel": relationship})
