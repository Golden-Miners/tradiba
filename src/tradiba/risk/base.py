from __future__ import annotations

from abc import ABC, abstractmethod

from tradiba.risk.models import TradePlan


class RiskRule(ABC):

    @abstractmethod
    def validate(
        self,
        signal: Signal,
    ) -> TradePlan:
        ...
