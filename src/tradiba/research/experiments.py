from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
from typing import Any, Dict

@dataclass
class Experiment:
    """
    Metadata for a single training run.
    """
    experiment_id: UUID
    dataset_id: UUID
    model_type: str
    parameters: Dict[str, Any]
    metrics: Dict[str, float] = field(default_factory=dict)
    git_commit: str = ""
    created_at: datetime = field(default_factory=datetime.now)

class ExperimentEngine:
    """
    Engine to track and retrieve experiments.
    """
    def __init__(self):
        self._experiments: dict[UUID, Experiment] = {}

    def log(self, experiment: Experiment) -> None:
        self._experiments[experiment.experiment_id] = experiment

    def get(self, experiment_id: UUID) -> Experiment | None:
        return self._experiments.get(experiment_id)
