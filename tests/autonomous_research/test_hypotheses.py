import uuid
from tradiba.autonomous_research.hypotheses import ResearchHypothesis

def test_hypothesis_immutability():
    hyp_id = uuid.uuid4()
    hyp = ResearchHypothesis(
        hypothesis_id=hyp_id,
        title="Test",
        description="Test description",
        assumptions=[],
        expected_outcome="Positive",
        confidence=0.8
    )
    
    import dataclasses
    import pytest
    with pytest.raises(dataclasses.FrozenInstanceError):
        hyp.confidence = 0.9  # type: ignore
