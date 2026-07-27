from typing import Dict, Any

class PolicyEngine:
    """
    Evaluates constraints such as:
    - Allowed instruments
    - Trading sessions
    - Maximum position size
    - Daily loss limits
    - Maximum exposure
    - Maximum leverage
    - Approved strategies
    - Confidence thresholds
    - Maximum concurrent trades
    """

    def __init__(self, policies: Dict[str, Any]):
        self.policies = policies

    def evaluate_proposal(self, proposal: Dict[str, Any], current_state: Dict[str, Any]) -> bool:
        """
        Validates a trade proposal against all configured policies.
        Returns True if the proposal is compliant, False otherwise.
        """
        if not proposal:
            return False

        symbol = proposal.get("symbol")
        strategy = proposal.get("strategy")
        size = proposal.get("size", 0.0)
        confidence = proposal.get("confidence", 0.0)

        # Instrument Check
        allowed_instruments = self.policies.get("allowed_instruments", [])
        if allowed_instruments and symbol not in allowed_instruments:
            return False

        # Strategy Check
        approved_strategies = self.policies.get("approved_strategies", [])
        if approved_strategies and strategy not in approved_strategies:
            return False

        # Confidence Threshold Check
        min_confidence = self.policies.get("min_confidence", 0.0)
        if confidence < min_confidence:
            return False

        # Position Size Check
        max_position_size = self.policies.get("max_position_size", float('inf'))
        if size > max_position_size:
            return False

        # Concurrent Trades Check
        max_concurrent = self.policies.get("max_concurrent_trades", float('inf'))
        current_trades = current_state.get("active_trades_count", 0)
        if current_trades >= max_concurrent:
            return False

        # Daily Loss Check
        daily_loss = current_state.get("daily_loss", 0.0)
        max_daily_loss = self.policies.get("max_daily_loss", float('inf'))
        if daily_loss >= max_daily_loss:
            return False

        return True
