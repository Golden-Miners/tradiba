from tradiba.ai.factory.prompts.pipeline import PromptEngineeringPipeline

def test_prompts():
    pipeline = PromptEngineeringPipeline()
    assert pipeline.validate_prompt("sys_prompt", "v2.0")
