from tradiba.autonomous_research.promotion import PromotionEngine

def test_promotion_engine():
    engine = PromotionEngine()
    
    rec = engine.recommend_promotion("cand-1", True)
    assert rec is not None
    assert rec.target_stage == "VALIDATED"
    
    rec_fail = engine.recommend_promotion("cand-2", False)
    assert rec_fail is None
