from tradiba.knowledge.graph.enterprise_graph import EnterpriseKnowledgeGraph

def test_graph():
    graph = EnterpriseKnowledgeGraph()
    graph.add_node("n1", {})
    graph.add_node("n2", {})
    graph.add_edge("n1", "n2", "RelatedTo")
    assert "n2" in graph.get_related("n1")
