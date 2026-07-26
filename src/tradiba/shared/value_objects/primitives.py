from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self):
        if not isinstance(self.amount, Decimal):
            raise TypeError("Amount must be a Decimal")

@dataclass(frozen=True)
class Price:
    value: Decimal

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Price cannot be negative")

@dataclass(frozen=True)
class Quantity:
    value: Decimal

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Quantity cannot be negative")
