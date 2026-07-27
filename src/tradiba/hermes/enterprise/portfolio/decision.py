
class DecisionPortfolio:
    """
    Tracks organizational decisions with justification and evidence.
    """
    def __init__(self):
        self.decisions = {}
        
    def record_decision(self, decision_id: str, justification: str):
        self.decisions[decision_id] = {"justification": justification, "approved": False}
        
    def approve(self, decision_id: str):
        if decision_id in self.decisions:
            self.decisions[decision_id]["approved"] = True
