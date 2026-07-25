from typing import Any
from tradiba.research.features import Feature
from tradiba.research.pipelines.feature_pipeline import FeaturePipeline

class DummyFeature(Feature):
    @property
    def name(self) -> str:
        return "dummy_feat"
        
    def compute(self, data: Any) -> Any:
        return data.get("value", 0) * 2

def test_feature_pipeline():
    feat = DummyFeature()
    pipeline = FeaturePipeline([feat])
    
    data = {"value": 5}
    result = pipeline.process(data)
    
    assert "dummy_feat" in result
    assert result["dummy_feat"] == 10
