from tradiba.hermes.research.knowledge.graph import KnowledgeGraph
import os

def test_knowledge_graph_nodes_and_edges(tmp_path):
    storage = tmp_path / "graph.json"
    kg = KnowledgeGraph(storage_path=str(storage))
    
    kg.add_node("strat1", "Strategy", {"name": "ICT Trend"})
    kg.add_node("feat1", "Feature", {"name": "FVG"})
    kg.add_edge("strat1", "feat1", "USES", {"weight": 1.0})
    
    assert "strat1" in kg.nodes
    assert "feat1" in kg.nodes
    assert len(kg.edges) == 1
    assert kg.edges[0]["relationship"] == "USES"
