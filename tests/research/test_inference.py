from tradiba.research.inference import InferenceService
from tradiba.research.pipelines.inference_pipeline import InferencePipeline
from tradiba.research.pipelines.feature_pipeline import FeaturePipeline
from tradiba.research.features import Feature
from tradiba.research.models.regression import LinearRegressionModel

class DummyFeature(Feature):
    @property
    def name(self): return "f1"
    def compute(self, data): return 1

def test_inference_service():
    model = LinearRegressionModel()
    model.fit([1], [1])
    
    fp = FeaturePipeline([DummyFeature()])
    ip = InferencePipeline(fp, model)
    
    service = InferenceService(ip)
    
    prediction = service.predict({"raw": "data"})
    assert prediction == 0.005
