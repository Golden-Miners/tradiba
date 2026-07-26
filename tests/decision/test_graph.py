import uuid
from tradiba.decision.graph import DecisionGraph

def test_decision_graph():
    graph = DecisionGraph()
    
    d_id = uuid.uuid4()
    e_id = uuid.uuid4()
    
    graph.add_relationship(d_id, e_id, "supported_by")
    
    evs = graph.get_supporting_evidence(d_id)
    assert len(evs) == 1
    assert evs[0] == e_id
