import itertools
from typing import Dict, Iterator

from .base import SearchAlgorithm


class GridSearch(SearchAlgorithm):
    """Systematically evaluates all parameter combinations."""

    def generate(self) -> Iterator[Dict[str, float]]:
        param_names = [p.name for p in self.parameters]
        param_ranges = []

        for p in self.parameters:
            values = []
            val = p.minimum
            while val <= p.maximum:
                values.append(val)
                val += p.step
                val = round(val, 10)  # Handle floating point inaccuracies
            param_ranges.append(values)

        for combo in itertools.product(*param_ranges):
            yield dict(zip(param_names, combo))
