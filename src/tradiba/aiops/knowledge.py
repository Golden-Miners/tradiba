
class KnowledgeBase:
    """Maintains structured operational knowledge for AI references."""
    def __init__(self) -> None:
        self.runbooks: dict[str, str] = {}
        self.playbooks: dict[str, str] = {}
        
    def add_runbook(self, incident_type: str, content: str) -> None:
        self.runbooks[incident_type] = content
        
    def get_runbook(self, incident_type: str) -> str | None:
        return self.runbooks.get(incident_type)
