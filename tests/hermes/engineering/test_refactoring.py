from tradiba.hermes.engineering.refactoring.engine import RefactoringEngine

def test_refactoring():
    engine = RefactoringEngine()
    prop = engine.propose("module_a", "split")
    assert prop["target"] == "module_a"
    assert "rollback" in prop
