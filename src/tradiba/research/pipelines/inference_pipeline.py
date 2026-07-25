from typing import Any
from tradiba.research.models.base import QuantitativeModel
from tradiba.research.pipelines.feature_pipeline import FeaturePipeline

class InferencePipeline:
    """
    Coordinates real-time or batch inference by chaining 
    a FeaturePipeline with a trained QuantitativeModel.
    """
    def __init__(self, feature_pipeline: FeaturePipeline, model: QuantitativeModel):
        self.feature_pipeline = feature_pipeline
        self.model = model

    def predict(self, raw_data: Any) -> Any:
        """
        Extracts features and passes them to the model for prediction.
        """
        features = self.feature_pipeline.process(raw_data)
        # Often models expect a specific format (e.g., array), we'd adapt it here.
        # Stub logic: pass the raw dict
        prediction = self.model.predict(features)
        return prediction
