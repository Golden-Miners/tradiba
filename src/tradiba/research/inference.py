from typing import Any
import logging
from tradiba.research.pipelines.inference_pipeline import InferencePipeline

logger = logging.getLogger(__name__)

class InferenceService:
    """
    Exposes a stable inference interface for the rest of the application
    (strategies, etc.) so they don't depend on model specifics.
    """
    def __init__(self, active_pipeline: InferencePipeline):
        self.active_pipeline = active_pipeline

    def predict(self, data: Any) -> Any:
        """
        Generates a prediction using the currently active production model.
        """
        try:
            return self.active_pipeline.predict(data)
        except Exception as e:
            logger.error(f"Inference service failed: {e}")
            raise
