import pytest
from fastapi.testclient import TestClient

from tradiba.api.app import app
from tradiba.events import EventBus
from tradiba.portfolio.service import PortfolioService
from tradiba.portfolio.models import Portfolio
from decimal import Decimal
from unittest.mock import MagicMock

client = TestClient(app)


@pytest.fixture
def mock_app_state():
    app.state.event_bus = MagicMock()
    app.state.portfolio_service = MagicMock()
    app.state.strategy_engine = MagicMock()
    app.state.narrative_builder = MagicMock()
    
    mock_portfolio = Portfolio(
        equity=10000.0,
        balance=10000.0,
        margin=0.0,
        free_margin=10000.0,
        profit=0.0,
        open_positions=0
    )
    app.state.portfolio_service.repository = MagicMock()
    app.state.portfolio_service.repository.load.return_value = mock_portfolio
    app.state.strategy_engine._strategies = {"test_strategy": MagicMock()}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def get_auth_token():
    response = client.post("/auth/login", json={"username": "trader", "password": "trader"})
    return response.json()["access_token"]


def test_auth_login():
    response = client.post("/auth/login", json={"username": "trader", "password": "trader"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_portfolio_unauthorized():
    response = client.get("/portfolio")
    assert response.status_code == 401


def test_portfolio_authorized(mock_app_state):
    token = get_auth_token()
    response = client.get(
        "/portfolio",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["balance"] == "10000.0"


def test_strategy_list_authorized(mock_app_state):
    viewer_res = client.post("/auth/login", json={"username": "viewer", "password": "viewer"})
    token = viewer_res.json()["access_token"]
    response = client.get(
        "/strategies",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "test_strategy"


def test_backtest_lifecycle(mock_app_state):
    # Only Admin can create backtest
    admin_res = client.post("/auth/login", json={"username": "admin", "password": "admin"})
    admin_token = admin_res.json()["access_token"]
    
    res = client.post(
        "/backtests",
        json={
            "strategy": "test",
            "symbol": "EURUSD",
            "timeframe": "M1",
            "start_date": "2026-01-01T00:00:00",
            "end_date": "2026-02-01T00:00:00"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res.status_code == 200
    job_id = res.json()["id"]
    
    # Viewer can read it
    viewer_res = client.post("/auth/login", json={"username": "viewer", "password": "viewer"})
    viewer_token = viewer_res.json()["access_token"]
    
    res2 = client.get(
        f"/backtests/{job_id}",
        headers={"Authorization": f"Bearer {viewer_token}"}
    )
    assert res2.status_code == 200
    assert res2.json()["status"] in ["QUEUED", "RUNNING", "COMPLETED"]
