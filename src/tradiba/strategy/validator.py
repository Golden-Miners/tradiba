from .models import TradingSignal

class SignalValidator:

    def validate(
        self,
        signal: TradingSignal,
    ) -> bool:

        if signal.stop_loss <= 0:
            return False

        if signal.take_profit <= 0:
            return False

        if signal.entry <= 0:
            return False

        if signal.confidence < 50:
            return False

        return True
