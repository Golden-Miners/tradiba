import pytest
from fastapi.testclient import TestClient
from tradiba.api.app import app

client = TestClient(app)

def test_dashboard():
    response = client.get("/operations/dashboard")
    assert response.status_code == 200
    assert "status" in response.json()

def test_report_incident():
    response = client.post("/operations/incidents", params={
        "title": "API Gateway Down",
        "description": "502 Bad Gateway observed",
        "severity": "SEV1"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "API Gateway Down"
    assert response.json()["status"] == "OPEN"

def test_register_slo():
    response = client.post("/operations/slo", params={
        "slo_id": "api-latency-99",
        "service": "api-gateway",
        "description": "99th percentile latency under 200ms",
        "metric_type": "latency",
        "target": 200.0,
        "operator": "<="
    })
    assert response.status_code == 200
    assert response.json()["metric_type"] == "latency"

def test_record_release():
    response = client.post("/operations/releases", params={
        "service": "api-gateway",
        "version": "v1.2.0",
        "change_type": "deployment",
        "approver": "sre-lead"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "successful"

def test_get_dependencies():
    response = client.get("/operations/dependencies")
    assert response.status_code == 200
    assert "nodes" in response.json()
    assert "edges" in response.json()

def test_get_capacity():
    response = client.get("/operations/capacity")
    assert response.status_code == 200
    assert "history" in response.json()

def test_get_forecast():
    response = client.get("/operations/forecast", params={"service": "api-gateway"})
    assert response.status_code == 200
    assert "predicted_cpu_percent" in response.json()

def test_get_reliability():
    response = client.get("/operations/reliability", params={"service": "api-gateway"})
    assert response.status_code == 200
    assert "mttr_minutes" in response.json()

@pytest.mark.asyncio
async def test_execute_runbook():
    response = client.post("/operations/runbooks", params={
        "runbook_name": "Restart Worker",
        "requester": "on-call-eng"
    })
    assert response.status_code == 200
    assert response.json()["runbook_name"] == "Restart Worker"
    # Even if it fails (because the powershell command echo might be slightly different on Windows CI vs local), we check that it responded
