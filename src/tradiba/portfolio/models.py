from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Portfolio:
    equity: float
    balance: float
    margin: float
    free_margin: float
    profit: float
    open_positions: int
