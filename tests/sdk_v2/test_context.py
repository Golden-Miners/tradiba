from tradiba.sdk_v2.context import StrategyContext, PortfolioContext, RiskContext, MarketContext

def test_strategy_context_initialization():
    ctx = StrategyContext()
    assert isinstance(ctx.portfolio, PortfolioContext)
    assert isinstance(ctx.risk, RiskContext)
    assert isinstance(ctx.market, MarketContext)
    
    assert ctx.portfolio.cash == 0.0
    assert ctx.portfolio.equity == 0.0
