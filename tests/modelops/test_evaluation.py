from tradiba.modelops.evaluation.framework import EvaluationFramework

def test_evaluation():
    eva = EvaluationFramework()
    assert eva.evaluate("m1")["accuracy"] == 0.95
