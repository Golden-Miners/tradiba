from decimal import Decimal
import uuid
from tradiba.strategy.models import TradingSignal
from .models import TradePlan, PortfolioSnapshot, RiskDecision
from .sizing import PositionSizer
from .exposure import ExposureManager
from .validator import RiskRule
from .limits import RiskLimits

class RiskManager:
    def __init__(
        self,
        sizer: PositionSizer,
        exposure: ExposureManager,
        rules: list[RiskRule],
        limits: RiskLimits
    ):
        self.sizer = sizer
        self.exposure = exposure
        self.rules = rules
        self.limits = limits

    def evaluate(
        self,
        signal: TradingSignal,
        account_state: PortfolioSnapshot,
        pip_value: Decimal = Decimal('10.0')
    ) -> TradePlan:
        
        # 1. Hard Limits Check (Max positions)
        if account_state.open_positions >= self.limits.max_open_positions:
            return TradePlan(
                signal_id=str(uuid.uuid4()),
                symbol=signal.symbol,
                side=signal.side.name,
                entry=Decimal(str(signal.entry)),
                stop_loss=Decimal(str(signal.stop_loss)),
                take_profit=Decimal(str(signal.take_profit)),
                position_size=Decimal('0'),
                risk_amount=Decimal('0'),
                decision=RiskDecision.REJECTED,
                reason="Max open positions reached"
            )

        # 2. Daily Loss Budget
        risk_percent = self.limits.account_risk_percent
        decision = RiskDecision.APPROVED
        reason = None
        
        if account_state.daily_pnl < 0:
            loss_percent = abs(account_state.daily_pnl) / account_state.balance
            available_risk = self.limits.daily_loss_percent - loss_percent
            if available_risk <= 0:
                return TradePlan(
                    signal_id=str(uuid.uuid4()),
                    symbol=signal.symbol,
                    side=signal.side.name,
                    entry=Decimal(str(signal.entry)),
                    stop_loss=Decimal(str(signal.stop_loss)),
                    take_profit=Decimal(str(signal.take_profit)),
                    position_size=Decimal('0'),
                    risk_amount=Decimal('0'),
                    decision=RiskDecision.REJECTED,
                    reason="Max daily loss reached"
                )
            if risk_percent > available_risk:
                risk_percent = available_risk
                decision = RiskDecision.REDUCED
                reason = "Reduced due to daily loss budget"

        # 3. Pipeline: Rules
        for rule in self.rules:
            is_valid = rule.evaluate(signal, account_state, self.exposure)
            if not is_valid:
                return TradePlan(
                    signal_id=str(uuid.uuid4()),
                    symbol=signal.symbol,
                    side=signal.side.name,
                    entry=Decimal(str(signal.entry)),
                    stop_loss=Decimal(str(signal.stop_loss)),
                    take_profit=Decimal(str(signal.take_profit)),
                    position_size=Decimal('0'),
                    risk_amount=Decimal('0'),
                    decision=RiskDecision.REJECTED,
                    reason=f"Rejected by {rule.__class__.__name__}"
                )

        # 4. Exposure Check
        if not self.exposure.can_open(signal):
            return TradePlan(
                signal_id=str(uuid.uuid4()),
                symbol=signal.symbol,
                side=signal.side.name,
                entry=Decimal(str(signal.entry)),
                stop_loss=Decimal(str(signal.stop_loss)),
                take_profit=Decimal(str(signal.take_profit)),
                position_size=Decimal('0'),
                risk_amount=Decimal('0'),
                decision=RiskDecision.REJECTED,
                reason="Exposure limit reached"
            )

        # 5. Sizing
        entry = Decimal(str(signal.entry))
        sl = Decimal(str(signal.stop_loss))
        stop_distance = abs(entry - sl)

        if stop_distance <= 0:
            return TradePlan(
                signal_id=str(uuid.uuid4()),
                symbol=signal.symbol,
                side=signal.side.name,
                entry=entry,
                stop_loss=sl,
                take_profit=Decimal(str(signal.take_profit)),
                position_size=Decimal('0'),
                risk_amount=Decimal('0'),
                decision=RiskDecision.REJECTED,
                reason="Zero stop distance"
            )

        try:
            lots = self.sizer.calculate(
                equity=account_state.equity,
                risk_percent=risk_percent,
                stop_distance=stop_distance,
                pip_value=pip_value
            )
        except ValueError as e:
            return TradePlan(
                signal_id=str(uuid.uuid4()),
                symbol=signal.symbol,
                side=signal.side.name,
                entry=entry,
                stop_loss=sl,
                take_profit=Decimal(str(signal.take_profit)),
                position_size=Decimal('0'),
                risk_amount=Decimal('0'),
                decision=RiskDecision.REJECTED,
                reason=str(e)
            )

        risk_amount = account_state.equity * risk_percent

        return TradePlan(
            signal_id=str(uuid.uuid4()),
            symbol=signal.symbol,
            side=signal.side.name,
            entry=entry,
            stop_loss=sl,
            take_profit=Decimal(str(signal.take_profit)),
            position_size=lots,
            risk_amount=risk_amount,
            decision=decision,
            reason=reason
        )
