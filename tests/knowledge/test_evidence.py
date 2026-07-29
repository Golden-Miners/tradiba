from tradiba.knowledge.evidence.tracker import EvidenceTracker

def test_evidence():
    tracker = EvidenceTracker()
    tracker.link_evidence("k1", "e1")
    assert "e1" in tracker.evidence["k1"]
