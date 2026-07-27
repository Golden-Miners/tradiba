from tradiba.ai.factory.evaluations.evaluator import AIEvaluationFramework

def test_evaluator():
    evaluator = AIEvaluationFramework()
    res = evaluator.evaluate({"out": "yes"}, {"truth": "yes"})
    assert res["accuracy"] > 0.9
    assert res["hallucination"] < 0.1
