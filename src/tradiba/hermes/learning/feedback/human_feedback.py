from typing import Dict, Any, List

class HumanFeedbackManager:
    """
    Ingests trader and risk manager feedback as structured training data.
    """
    def __init__(self):
        self.feedback_store: List[Dict[str, Any]] = []
        
    def submit_feedback(self, context_id: str, feedback_type: str, comments: str, rating: int):
        """
        Feedback Type: 'TRADER', 'RISK', 'RESEARCH'
        Rating: 1 to 5
        """
        self.feedback_store.append({
            "context_id": context_id,
            "type": feedback_type,
            "comments": comments,
            "rating": rating
        })
        
    def get_feedback_for_context(self, context_id: str) -> List[Dict[str, Any]]:
        return [f for f in self.feedback_store if f["context_id"] == context_id]
