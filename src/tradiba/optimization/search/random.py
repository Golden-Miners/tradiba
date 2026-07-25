import random
from typing import Dict, Iterator, List

from .base import SearchAlgorithm
from ..configuration import Parameter


class RandomSearch(SearchAlgorithm):
    """Evaluates random parameter combinations within bounds."""

    def __init__(self, parameters: List[Parameter], seed: int, max_iterations: int):
        super().__init__(parameters)
        self.max_iterations = max_iterations
        self.rng = random.Random(seed)

    def generate(self) -> Iterator[Dict[str, float]]:
        for _ in range(self.max_iterations):
            params = {}
            for p in self.parameters:
                # Randomly pick a value aligned with 'step'
                steps = int((p.maximum - p.minimum) / p.step)
                chosen_step = self.rng.randint(0, steps)
                val = p.minimum + (chosen_step * p.step)
                params[p.name] = round(val, 10)
            yield params
