from uuid import uuid4
from tradiba.research.shadow import ShadowDeployment
from tradiba.research.pipelines.inference_pipeline import InferencePipeline
from tradiba.research.pipelines.feature_pipeline import FeaturePipeline
from tradiba.research.features import Feature
from tradiba.research.models.classification import BinaryClassifierModel

class DummyFeature(Feature):
    @property
    def name(self): return "f1"
    def compute(self, data): return 1

def test_shadow_deployment():
    model = BinaryClassifierModel()
    model.fit([1], [1])
    
    fp = FeaturePipeline([DummyFeature()])
    ip = InferencePipeline(fp, model)
    
    shadow = ShadowDeployment(uuid4(), ip)
    
    # Should not raise exception
    shadow.process_event({"raw": "data"})
