from uuid import uuid4
from datetime import datetime
from tradiba.research.datasets import DatasetRegistry, Dataset
from tradiba.research.registry import ModelRegistry
from tradiba.research.experiments import ExperimentEngine
from tradiba.research.pipelines.training_pipeline import DefaultTrainingPipeline
from tradiba.research.models.classification import BinaryClassifierModel

def test_training_pipeline_flow():
    datasets = DatasetRegistry()
    models = ModelRegistry()
    experiments = ExperimentEngine()
    
    ds_id = uuid4()
    datasets.register(Dataset(ds_id, "BTC", "1h", datetime.now(), datetime.now(), "v1", "v1"))
    
    pipeline = DefaultTrainingPipeline(datasets, experiments, models)
    
    # 1. Prepare
    data = pipeline.prepare_dataset(ds_id)
    assert "features" in data
    
    # 2. Train
    model = pipeline.train(data, {})
    assert isinstance(model, BinaryClassifierModel)
    assert model.is_fitted
    
    # 3. Evaluate
    metrics = pipeline.evaluate(model, data)
    assert "accuracy" in metrics
    
    # 4. Register
    exp_id = uuid4()
    pipeline.register(exp_id, model, metrics)
    
    exp = experiments.get(exp_id)
    assert exp is not None
    assert exp.metrics == metrics
