from __future__ import annotations

from abc import ABC, abstractmethod

from tradiba.strategy.models import Signal
from .models.risk_result import RiskResult


class RiskRule(ABC):

    @abstractmethod
    def validate(
        self,
        signal: Signal,
    ) -> RiskResult:
        ...
