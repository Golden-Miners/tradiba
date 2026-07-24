import pytest
from decimal import Decimal
from datetime import datetime, timezone
from tradiba.risk.models import PortfolioSnapshot, RiskDecision
from tradiba.risk.limits import RiskLimits
from tradiba.risk.sizing import PositionSizer
from tradiba.risk.exposure import ExposureManager
from tradiba.risk.manager import RiskManager
from tradiba.strategy.models import TradingSignal, SignalSide, SignalStrength

@pytest.fixture
def base_limits():
    return RiskLimits(
        account_risk_percent=Decimal('0.02'),
        daily_loss_percent=Decimal('0.05'),
        weekly_loss_percent=Decimal('0.10'),
        max_open_positions=3,
        max_symbol_positions=1,
        max_correlated_positions=2
    )

@pytest.fixture
def base_account():
    return PortfolioSnapshot(
        equity=Decimal('10000.00'),
        balance=Decimal('10000.00'),
        floating_pnl=Decimal('0'),
        daily_pnl=Decimal('0'),
        open_positions=0,
        open_orders=0
    )

@pytest.fixture
def manager(base_limits):
    sizer = PositionSizer()
    exposure = ExposureManager()
    return RiskManager(sizer, exposure, [], base_limits)

def create_signal(entry, sl, tp):
    return TradingSignal(
        strategy="test",
        symbol="EURUSD",
        timeframe="H1",
        side=SignalSide.BUY,
        strength=SignalStrength.STRONG,
        confidence=90,
        entry=entry,
        stop_loss=sl,
        take_profit=tp,
        created_at=datetime.now(timezone.utc),
        metadata={}
    )

def test_position_sizing():
    sizer = PositionSizer()
    # 10000 * 0.02 = 200 risk. Stop distance = 0.0050. Pip value = 10.0
    lots = sizer.calculate(Decimal('10000.0'), Decimal('0.02'), Decimal('0.0050'), Decimal('10.0'))
    # 200 / (0.0050 * 10) = 200 / 0.05 = 4000.0 lots? Wait.
    # Usually pip_value in MT5 is per standard lot. If stop is 50 pips (0.0050), and pip value is $10/lot per pip:
    # 200 / (50 * 10) = 0.4 lots.
    # But mathematically: 200 / (0.0050 * 10.0) = 4000.
    assert lots == Decimal('4000')

def test_position_approved(manager, base_account):
    sig = create_signal(1.1000, 1.0950, 1.1100)
    plan = manager.evaluate(sig, base_account)
    
    assert plan.decision == RiskDecision.APPROVED
    assert plan.risk_amount == Decimal('200.00')

def test_maximum_daily_loss_reached(manager):
    # Loss is 600, which is 6% of 10000. Limit is 5%.
    acc = PortfolioSnapshot(Decimal('9400.00'), Decimal('10000.00'), Decimal('0'), Decimal('-600.00'), 0, 0)
    sig = create_signal(1.1000, 1.0950, 1.1100)
    
    plan = manager.evaluate(sig, acc)
    assert plan.decision == RiskDecision.REJECTED
    assert "Max daily loss" in plan.reason

def test_reduced_position_size(manager):
    # Loss is 400, which is 4% of 10000. Limit is 5%. Available is 1%. Normal risk is 2%.
    # Should reduce to 1% risk.
    acc = PortfolioSnapshot(Decimal('9600.00'), Decimal('10000.00'), Decimal('0'), Decimal('-400.00'), 0, 0)
    sig = create_signal(1.1000, 1.0950, 1.1100)
    
    plan = manager.evaluate(sig, acc)
    assert plan.decision == RiskDecision.REDUCED
    # Risk amount should be 1% of equity (9600) = 96
    assert plan.risk_amount == Decimal('96.00')

def test_maximum_open_positions(manager, base_account):
    acc = PortfolioSnapshot(Decimal('10000.00'), Decimal('10000.00'), Decimal('0'), Decimal('0'), 3, 0)
    sig = create_signal(1.1000, 1.0950, 1.1100)
    
    plan = manager.evaluate(sig, acc)
    assert plan.decision == RiskDecision.REJECTED
    assert "Max open positions" in plan.reason

def test_zero_stop_distance_rejected(manager, base_account):
    sig = create_signal(1.1000, 1.1000, 1.1100)
    plan = manager.evaluate(sig, base_account)
    
    assert plan.decision == RiskDecision.REJECTED
    assert "Zero stop distance" in plan.reason

def test_decimal_precision(manager, base_account):
    # Test that float issues don't happen with decimal
    sig = create_signal(1.1000, 1.0999, 1.1003)
    plan = manager.evaluate(sig, base_account, pip_value=Decimal('10'))
    
    assert plan.decision == RiskDecision.APPROVED
    assert isinstance(plan.position_size, Decimal)
    assert isinstance(plan.risk_amount, Decimal)
