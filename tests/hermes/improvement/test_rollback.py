"""Tests for Hermes Rollback Manager."""

from tradiba.hermes.improvement.rollback.manager import RollbackManager

def test_rollback_manager():
    manager = RollbackManager()
    
    manager.tag_deployment("v1.0", {"date": "2026-07-27"})
    manager.tag_deployment("v1.1", {"date": "2026-07-28"})
    
    assert manager.rollback("v1.0") is True
    assert manager.rollback("v2.0") is False
    
    diff = manager.compare_history("v1.0", "v1.1")
    assert "diff" in diff
