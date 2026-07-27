from typing import Dict, Any, List

class WorkflowSynthesizer:
    """
    Composes versioned workflows as DAGs.
    """
    def __init__(self):
        pass
        
    def synthesize(self, nodes: List[str]) -> Dict[str, Any]:
        edges = []
        for i in range(len(nodes) - 1):
            edges.append(f"{nodes[i]} -> {nodes[i+1]}")
            
        return {
            "version": "1.0",
            "nodes": nodes,
            "edges": edges
        }
