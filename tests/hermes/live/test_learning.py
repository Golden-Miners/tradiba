from tradiba.hermes.live.monitoring.live_learning import LiveLearningFeedback

def test_live_learning_feedback():
    feedback = LiveLearningFeedback()
    
    feedback.record_trade({"slippage": 0.02})
    feedback.record_trade({"slippage": 0.04})
    feedback.record_violation({"reason": "Size too large"})
    
    analysis = feedback.analyze_feedback()
    assert analysis["trades_analyzed"] == 2
    assert analysis["average_slippage"] == 0.03
    assert analysis["total_violations"] == 1
