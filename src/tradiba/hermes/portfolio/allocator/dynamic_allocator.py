from typing import Dict, Any, List

class DynamicAllocator:
    """
    Allocates capital using configurable objectives:
    - Maximum Sharpe
    - Risk parity
    - Volatility targeting
    - Kelly-inspired sizing (bounded)
    - Fixed allocation
    - Regime-aware allocation
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def allocate(self, strategies: List[Dict[str, Any]], regime: str) -> Dict[str, float]:
        """
        Returns a dictionary mapping strategy ID to allocation fraction (0.0 to 1.0).
        """
        if not strategies:
            return {}

        allocation_type = self.config.get("allocation_type", "fixed")
        
        if allocation_type == "regime-aware":
            return self._allocate_regime_aware(strategies, regime)
        elif allocation_type == "kelly":
            return self._allocate_kelly(strategies)
        elif allocation_type == "risk-parity":
            return self._allocate_risk_parity(strategies)
        elif allocation_type == "max-sharpe":
            return self._allocate_max_sharpe(strategies)
        elif allocation_type == "volatility-targeting":
            return self._allocate_volatility_targeting(strategies)
        else:
            return self._allocate_fixed(strategies)

    def _allocate_fixed(self, strategies: List[Dict[str, Any]]) -> Dict[str, float]:
        fraction = 1.0 / len(strategies)
        return {s["id"]: fraction for s in strategies}

    def _allocate_kelly(self, strategies: List[Dict[str, Any]]) -> Dict[str, float]:
        """Half-Kelly implementation."""
        allocations = {}
        total = 0.0
        for s in strategies:
            win_rate = s.get("win_rate", 0.5)
            win_loss_ratio = s.get("win_loss_ratio", 1.0)
            
            # Kelly formula: K = W - ((1 - W) / R)
            if win_loss_ratio > 0:
                kelly_fraction = win_rate - ((1.0 - win_rate) / win_loss_ratio)
            else:
                kelly_fraction = 0.0
                
            # Half-Kelly and bounded
            fraction = max(0.0, min(0.5, kelly_fraction * 0.5))
            allocations[s["id"]] = fraction
            total += fraction
            
        # Normalize if total > 1.0
        if total > 1.0:
            allocations = {k: v / total for k, v in allocations.items()}
            
        return allocations

    def _allocate_risk_parity(self, strategies: List[Dict[str, Any]]) -> Dict[str, float]:
        # Inverse volatility allocation
        inv_vols = {}
        total_inv_vol = 0.0
        for s in strategies:
            vol = s.get("volatility", 1.0)
            if vol <= 0:
                vol = 0.0001
            inv_vol = 1.0 / vol
            inv_vols[s["id"]] = inv_vol
            total_inv_vol += inv_vol
            
        return {k: v / total_inv_vol for k, v in inv_vols.items()}
        
    def _allocate_max_sharpe(self, strategies: List[Dict[str, Any]]) -> Dict[str, float]:
        # Simplified max sharpe heuristic
        scores = {}
        total = 0.0
        for s in strategies:
            sharpe = s.get("sharpe", 0.0)
            score = max(0.0, sharpe)
            scores[s["id"]] = score
            total += score
            
        if total == 0.0:
            return self._allocate_fixed(strategies)
            
        return {k: v / total for k, v in scores.items()}

    def _allocate_volatility_targeting(self, strategies: List[Dict[str, Any]]) -> Dict[str, float]:
        target_vol = self.config.get("target_volatility", 0.1)
        allocations = {}
        for s in strategies:
            vol = s.get("volatility", 1.0)
            if vol <= 0:
                vol = 0.0001
            fraction = target_vol / vol
            # Cap at 1.0
            allocations[s["id"]] = min(1.0, fraction)
            
        # Normalize to 1.0 if exceeded
        total = sum(allocations.values())
        if total > 1.0:
            allocations = {k: v / total for k, v in allocations.items()}
            
        return allocations

    def _allocate_regime_aware(self, strategies: List[Dict[str, Any]], regime: str) -> Dict[str, float]:
        # Adjust allocation based on regime
        allocations = {}
        total = 0.0
        for s in strategies:
            regime_scores = s.get("regime_scores", {})
            score = regime_scores.get(regime, 1.0)
            allocations[s["id"]] = max(0.0, score)
            total += allocations[s["id"]]
            
        if total == 0.0:
            return self._allocate_fixed(strategies)
            
        return {k: v / total for k, v in allocations.items()}
