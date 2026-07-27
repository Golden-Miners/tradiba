from tradiba.ai.factory.pipelines.cicd import AICICDPipeline

def test_cicd_pipeline():
    pipeline = AICICDPipeline()
    assert pipeline.run_pipeline("p1") == "PASSED"
