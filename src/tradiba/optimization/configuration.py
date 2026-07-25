from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class OptimizationConfig:
    workers: int
    max_iterations: int
    random_seed: int
    objective: str
    walk_forward_windows: int


@dataclass(slots=True, frozen=True)
class Parameter:
    name: str
    minimum: float
    maximum: float
    step: float
