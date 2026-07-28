from tradiba.hermes.multimodal.fusion.cross_modal import CrossModalFusion
from tradiba.hermes.multimodal.reasoning.multimodal_reasoner import MultimodalReasoner

def test_reasoning():
    fusion = CrossModalFusion()
    fusion.fuse([{"type": "chart", "trend": "up"}])
    
    reasoner = MultimodalReasoner(fusion)
    rec = reasoner.generate_recommendation()
    
    assert rec["recommendation"] == "BUY"
    assert rec["confidence"] == 0.85
