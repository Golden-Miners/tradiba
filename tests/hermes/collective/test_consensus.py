from tradiba.hermes.collective.consensus.engine import ConsensusEngine

def test_consensus_majority():
    engine = ConsensusEngine(policy="majority")
    
    votes = [
        {"agent_id": "1", "vote": "APPROVE"},
        {"agent_id": "2", "vote": "APPROVE"},
        {"agent_id": "3", "vote": "REJECT"}
    ]
    
    result = engine.evaluate_votes("goal_1", votes)
    assert result["status"] == "APPROVED"
    assert result["reason"] == "MAJORITY_APPROVAL"

def test_consensus_unanimous():
    engine = ConsensusEngine(policy="unanimous")
    
    votes = [
        {"agent_id": "1", "vote": "APPROVE"},
        {"agent_id": "2", "vote": "APPROVE"},
        {"agent_id": "3", "vote": "REJECT"}
    ]
    
    result = engine.evaluate_votes("goal_1", votes)
    assert result["status"] == "REJECTED"
    assert result["reason"] == "NOT_UNANIMOUS"
