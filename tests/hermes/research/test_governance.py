from tradiba.hermes.research.workflows.approval import ResearchWorkflowEngine, ResearchRecommendation

def test_research_approval_workflow():
    engine = ResearchWorkflowEngine()
    rec = ResearchRecommendation(id="rec1", hypothesis_id="hyp1", evidence={"sharpe": 2.1})
    
    engine.submit_for_review(rec)
    assert len(engine.pending_research) == 1
    
    success = engine.promote_to_digital_twin("rec1")
    assert success is True
    assert len(engine.pending_research) == 0
    assert rec.approved is True
