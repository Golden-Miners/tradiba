from decimal import Decimal

class PositionSizer:

    def calculate(
        self,
        equity: Decimal,
        risk_percent: Decimal,
        stop_distance: Decimal,
        pip_value: Decimal,
    ) -> Decimal:
        
        if stop_distance <= 0:
            raise ValueError("Stop distance must be strictly positive")
        if pip_value <= 0:
            raise ValueError("Pip value must be strictly positive")

        risk_amount = equity * risk_percent

        lots = (
            risk_amount
            / (stop_distance * pip_value)
        )

        return lots
