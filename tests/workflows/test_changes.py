from tradiba.workflows.changes import ChangeManager
from tradiba.workflows.models.change import ChangeRecord, ChangeStatus

def test_change_lifecycle():
    manager = ChangeManager()
    change = ChangeRecord(
        id="CHG-01",
        description="test change",
        justification="test",
        approvers=[],
        implementation_plan="none",
        rollback_plan="none",
        verification_checklist=[],
        status=ChangeStatus.PROPOSED
    )
    
    manager.propose_change(change)
    manager.approve_change("CHG-01")
    assert change.status == ChangeStatus.APPROVED
    
    manager.implement_change("CHG-01")
    assert change.status == ChangeStatus.IMPLEMENTED
    
    manager.rollback_change("CHG-01")
    assert change.status == ChangeStatus.ROLLED_BACK
