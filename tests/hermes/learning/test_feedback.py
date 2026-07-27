from tradiba.hermes.learning.feedback.human_feedback import HumanFeedbackManager

def test_human_feedback():
    manager = HumanFeedbackManager()
    
    manager.submit_feedback("ctx_123", "TRADER", "Good entry, bad exit", 3)
    
    feedback = manager.get_feedback_for_context("ctx_123")
    assert len(feedback) == 1
    assert feedback[0]["rating"] == 3
