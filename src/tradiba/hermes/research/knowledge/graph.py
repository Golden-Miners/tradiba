import json
import os
from typing import Dict, List, Any

class KnowledgeGraph:
    """Lightweight in-memory/JSON-backed Graph structure for v4.2."""
    
    def __init__(self, storage_path: str = ".data/hermes/knowledge_graph.json"):
        self.storage_path = storage_path
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r") as f:
                data = json.load(f)
                self.nodes = data.get("nodes", {})
                self.edges = data.get("edges", [])

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w") as f:
            json.dump({"nodes": self.nodes, "edges": self.edges}, f, indent=2)

    def add_node(self, node_id: str, label: str, properties: Dict[str, Any]):
        self.nodes[node_id] = {"label": label, "properties": properties}
        self._save()

    def add_edge(self, source_id: str, target_id: str, relationship: str, properties: Dict[str, Any] | None = None):
        self.edges.append({
            "source": source_id,
            "target": target_id,
            "relationship": relationship,
            "properties": properties or {}
        })
        self._save()
