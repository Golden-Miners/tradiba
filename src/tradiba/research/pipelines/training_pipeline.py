from typing import Any
from uuid import uuid4
from tradiba.research.trainer import TrainingPipeline
from tradiba.research.datasets import DatasetRegistry
from tradiba.research.registry import ModelRegistry, RegisteredModel
from tradiba.research.experiments import ExperimentEngine, Experiment

class DefaultTrainingPipeline(TrainingPipeline):
    """
    Standard training pipeline implementation connecting dataset,
    model fitting, evaluation, and registry.
    """
    def __init__(self, dataset_registry: DatasetRegistry, experiment_engine: ExperimentEngine, model_registry: ModelRegistry):
        self.dataset_registry = dataset_registry
        self.experiment_engine = experiment_engine
        self.model_registry = model_registry

    def prepare_dataset(self, dataset_id: Any) -> Any:
        dataset = self.dataset_registry.get(dataset_id)
        if not dataset:
            raise ValueError(f"Dataset {dataset_id} not found")
        # Stub: Return dummy data
        return {"features": [1, 2, 3], "labels": [1, 0, 1]}

    def train(self, data: Any, parameters: dict[str, Any]) -> Any:
        from tradiba.research.models.classification import BinaryClassifierModel
        model = BinaryClassifierModel()
        model.fit(data["features"], data["labels"])
        return model

    def evaluate(self, model: Any, data: Any) -> dict[str, float]:
        from tradiba.research.metrics import calculate_accuracy
        # Dummy evaluation
        predictions = [model.predict(f) for f in data["features"]]
        acc = calculate_accuracy(predictions, data["labels"])
        return {"accuracy": acc}

    def register(self, experiment_id: Any, model: Any, metrics: dict[str, float]) -> None:
        # Create experiment record
        exp = Experiment(
            experiment_id=experiment_id,
            dataset_id=uuid4(), # Stub for now
            model_type=model.__class__.__name__,
            parameters={},
            metrics=metrics
        )
        self.experiment_engine.log(exp)

        # Register model
        reg_model = RegisteredModel(
            model_id=uuid4(),
            experiment_id=experiment_id,
            artifact_path="/tmp/dummy"
        )
        self.model_registry.register(reg_model)
