
class Indicator:
    """Base class for built-in SDK indicators."""
    def update(self, value: float) -> None:
        pass
        
    def value(self) -> float:
        return 0.0

class SMA(Indicator):
    """Simple Moving Average."""
    def __init__(self, window: int) -> None:
        self.window = window
        self._values: list[float] = []
        
    def update(self, value: float) -> None:
        self._values.append(value)
        if len(self._values) > self.window:
            self._values.pop(0)
            
    def value(self) -> float:
        if not self._values:
            return 0.0
        return sum(self._values) / len(self._values)

class EMA(Indicator):
    """Exponential Moving Average."""
    def __init__(self, window: int) -> None:
        self.window = window
        self._ema = 0.0
        self._count = 0
        self._alpha = 2.0 / (window + 1.0)
        
    def update(self, value: float) -> None:
        if self._count == 0:
            self._ema = value
        else:
            self._ema = (value - self._ema) * self._alpha + self._ema
        self._count += 1
            
    def value(self) -> float:
        return self._ema

class RSI(Indicator):
    """Relative Strength Index."""
    def __init__(self, window: int) -> None:
        self.window = window
        self._gains: list[float] = []
        self._losses: list[float] = []
        self._last_val: float | None = None
        
    def update(self, value: float) -> None:
        if self._last_val is not None:
            change = value - self._last_val
            self._gains.append(max(change, 0))
            self._losses.append(max(-change, 0))
            if len(self._gains) > self.window:
                self._gains.pop(0)
                self._losses.pop(0)
        self._last_val = value
        
    def value(self) -> float:
        if len(self._gains) < self.window:
            return 50.0
        avg_gain = sum(self._gains) / self.window
        avg_loss = sum(self._losses) / self.window
        if avg_loss == 0:
            return 100.0
        rs = avg_gain / avg_loss
        return 100.0 - (100.0 / (1.0 + rs))
