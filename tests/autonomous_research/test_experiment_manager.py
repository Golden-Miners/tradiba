import uuid
from tradiba.autonomous_research.experiment_manager import ExperimentManager

def test_experiment_reproducibility_metadata():
    manager = ExperimentManager()
    result = manager.run_experiment(uuid.uuid4(), {"seed": 123})
    
    assert result["status"] == "COMPLETED"
    assert result["metadata"]["random_seed"] == 123
