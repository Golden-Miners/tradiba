from tradiba.modelops.training.orchestrator import TrainingOrchestrator

def test_training():
    orchestrator = TrainingOrchestrator()
    assert orchestrator.run_pipeline("p1")
