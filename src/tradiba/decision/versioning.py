from tradiba.decision.models.decision import Decision
from tradiba.decision.repository import DecisionRepository

class DecisionVersioning:
    """Ensures decisions are append-only and revisions are fully traceable."""
    
    def __init__(self, repo: DecisionRepository) -> None:
        self.repo = repo
        
    def commit_revision(self, new_revision: Decision) -> None:
        """
        Saves a new revision of the decision without overwriting past state.
        """
        self.repo.save(new_revision)
