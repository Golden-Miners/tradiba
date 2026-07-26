from tradiba.decision.models.decision import Decision, DecisionStatus

class DecisionEngine:
    """Core engine for orchestrating decision evaluation and transition."""
    
    def process_decision(self, decision: Decision) -> Decision:
        """
        Mock process: checks if confidence is high enough to auto-approve.
        """
        if decision.confidence > 0.90:
            import dataclasses
            return dataclasses.replace(decision, status=DecisionStatus.APPROVED)
        return decision
