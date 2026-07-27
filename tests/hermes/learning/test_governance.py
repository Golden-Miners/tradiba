from tradiba.hermes.learning.governance.learning_governance import LearningGovernance

def test_learning_governance():
    gov = LearningGovernance()
    
    res1 = gov.evaluate_promotion({"status": "SUPERSEDED"})
    assert res1 == "REJECTED_SUPERSEDED"
    
    res2 = gov.evaluate_promotion({"status": "DRAFT", "confidence": 0.8})
    assert res2 == "PENDING_HUMAN_REVIEW"
    
    res3 = gov.evaluate_promotion({"status": "HUMAN_APPROVED", "confidence": 0.8})
    assert res3 == "PROMOTED"
    
    res4 = gov.evaluate_promotion({"status": "DRAFT", "confidence": 0.95})
    assert res4 == "PROMOTED"
