from tradiba.workflows.models.change import ChangeRecord, ChangeStatus

class ChangeManager:
    """Tracks operational changes."""
    def __init__(self) -> None:
        self._changes: dict[str, ChangeRecord] = {}
        
    def propose_change(self, change: ChangeRecord) -> None:
        self._changes[change.id] = change
        
    def approve_change(self, change_id: str) -> None:
        change = self._changes.get(change_id)
        if change and change.status == ChangeStatus.PROPOSED:
            change.status = ChangeStatus.APPROVED
            
    def implement_change(self, change_id: str) -> None:
        change = self._changes.get(change_id)
        if change and change.status == ChangeStatus.APPROVED:
            change.status = ChangeStatus.IMPLEMENTED

    def rollback_change(self, change_id: str) -> None:
        change = self._changes.get(change_id)
        if change and change.status == ChangeStatus.IMPLEMENTED:
            change.status = ChangeStatus.ROLLED_BACK
