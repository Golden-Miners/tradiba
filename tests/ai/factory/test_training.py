from tradiba.ai.factory.training.pipeline import FineTuningPipeline

def test_training():
    pipeline = FineTuningPipeline()
    assert pipeline.start_training("job_1", "v1.0", {}) == "RUNNING"
    assert pipeline.complete_training("job_1") == "COMPLETED"
