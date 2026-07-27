from fastapi.testclient import TestClient
from fastapi import FastAPI
from tradiba.api.routers.mobile import router

app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_mobile_dashboard():
    response = client.get("/mobile/dashboard")
    assert response.status_code == 200
    assert response.json()["status"] == "active"
    assert "portfolio_value" in response.json()

def test_mobile_notifications():
    response = client.get("/mobile/notifications")
    assert response.status_code == 200
    assert len(response.json()) > 0
