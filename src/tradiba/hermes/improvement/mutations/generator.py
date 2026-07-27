"""Strategy Mutation module."""

from typing import Dict, Any

class MutationGenerator:
    """Generates mutations for strategy improvement.
    
    Supports safe modifications like parameter tuning, entry condition refinement,
    exit rule refinement, position sizing experiments, and feature selection.
    Structural changes require explicit approval.
    """

    def __init__(self) -> None:
        pass

    def tune_parameters(self, strategy: Dict[str, Any], bounds: Dict[str, Any]) -> Dict[str, Any]:
        """Tunes parameters within defined bounds."""
        mutated = strategy.copy()
        mutated["parameters_tuned"] = True
        return mutated

    def refine_entry_conditions(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Refines entry rules."""
        mutated = strategy.copy()
        mutated["entry_refined"] = True
        return mutated

    def refine_exit_conditions(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Refines exit rules."""
        mutated = strategy.copy()
        mutated["exit_refined"] = True
        return mutated

    def propose_structural_change(self, strategy: Dict[str, Any], change: str) -> Dict[str, Any]:
        """Proposes a structural change that requires approval."""
        return {"strategy": strategy, "change": change, "approved": False}
