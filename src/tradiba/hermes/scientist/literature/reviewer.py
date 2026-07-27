
class KnowledgeReviewer:
    """
    Reviews internal knowledge sources to prevent duplicate research.
    """
    def __init__(self):
        self.knowledge_base = ["past_exp_1", "past_exp_2"]
        
    def review(self, topic: str) -> bool:
        return topic not in self.knowledge_base
