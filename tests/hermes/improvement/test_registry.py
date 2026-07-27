"""Tests for Hermes Improvement Registry."""

from tradiba.hermes.improvement.registry.store import ImprovementRegistry

def test_registry_register_and_status():
    registry = ImprovementRegistry()
    registry.register_candidate("cand_1", "parent_1", {"type": "momentum"})
    
    lineage = registry.get_lineage("cand_1")
    assert len(lineage) == 1
    assert lineage[0]["parent_id"] == "parent_1"
    assert lineage[0]["status"] == "registered"
    
    registry.update_status("cand_1", "validating")
    
    lineage = registry.get_lineage("cand_1")
    assert lineage[0]["status"] == "validating"
    assert len(lineage[0]["history"]) == 1
    assert lineage[0]["history"][0]["status"] == "validating"
