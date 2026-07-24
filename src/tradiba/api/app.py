from fastapi import FastAPI, Depends, Request
from tradiba.config.loader import load_settings
from tradiba.persistence.database import Database
from tradiba.api.schemas.responses import HealthResponse, PortfolioResponse
from tradiba.persistence.repositories.trade_repository import TradeRepository
from tradiba.persistence.repositories.snapshot_repository import SnapshotRepository

app = FastAPI(title="Tradiba API", version="0.1.0")

settings = load_settings()
database = Database(settings.database.url)

def get_db():
    session_gen = database.get_session()
    session = next(session_gen)
    try:
        yield session
    finally:
        session.close()

@app.get("/health", response_model=HealthResponse)
def health_check(request: Request):
    container = getattr(request.app.state, "container", None)
    services_status = {}
    
    if container:
        from tradiba.events import EventBus
        from tradiba.scheduler import Scheduler
        from tradiba.persistence.database import Database
        from tradiba.mt5.connection import MT5ConnectionManager
        
        # Check basic resolution (if it resolves, we count it as "registered")
        # For MT5, we can check if it's connected
        mt5 = container.resolve(MT5ConnectionManager)
        services_status["mt5"] = "connected" if (mt5 and mt5._connected) else "disconnected"
        
        db = container.resolve(Database)
        services_status["database"] = "registered" if db else "missing"
        
        bus = container.resolve(EventBus)
        services_status["event_bus"] = "registered" if bus else "missing"
        
        scheduler = container.resolve(Scheduler)
        services_status["scheduler"] = "registered" if scheduler else "missing"
    
    return HealthResponse(
        status="ok", 
        version="0.1.0",
        services=services_status
    )

@app.get("/portfolio")
def get_portfolio(db=Depends(get_db)):
    repo = SnapshotRepository(db)
    snapshots = repo.all()
    if not snapshots:
        return {"message": "No portfolio data available"}
    latest = snapshots[-1]
    return PortfolioResponse(
        equity=latest.equity,
        balance=latest.balance,
        margin=latest.margin,
        profit=latest.profit,
        free_margin=latest.free_margin
    )

@app.get("/positions")
def get_positions():
    return {"message": "Active positions from ExecutionService"}

@app.get("/orders")
def get_orders():
    return {"message": "Active orders from ExecutionService"}

@app.get("/trades")
def get_trades(db=Depends(get_db)):
    repo = TradeRepository(db)
    trades = repo.all()
    return [{"ticket": t.ticket, "symbol": t.symbol, "profit": t.profit} for t in trades]

@app.get("/statistics")
def get_statistics(db=Depends(get_db)):
    repo = TradeRepository(db)
    trades = repo.all()
    from tradiba.analytics.performance import calculate_net_profit, calculate_win_rate
    return {
        "net_profit": calculate_net_profit(trades),
        "win_rate": calculate_win_rate(trades)
    }

@app.get("/signals")
def get_signals():
    return {"message": "Latest strategy signals"}
