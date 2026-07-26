def test_recommendation_immutability():
    from tradiba.agents.recommendations import Recommendation
    
    rec = Recommendation(
        id="123",
        category="test",
        priority="HIGH",
        confidence=0.9,
        evidence="test evidence",
        affected_resources=[],
        recommended_action="HOLD",
        requires_approval=True
    )
    
    import dataclasses
    import pytest
    with pytest.raises(dataclasses.FrozenInstanceError):
        rec.confidence = 0.5  # type: ignore
