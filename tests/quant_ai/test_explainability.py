from tradiba.quant_ai.explainability.xai import ExplainableAI

def test_explainability():
    xai = ExplainableAI()
    res = xai.explain_prediction("m1", "p1")
    assert res["feature_importance"]["f1"] == 0.8
