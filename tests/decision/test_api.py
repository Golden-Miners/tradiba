from fastapi.testclient import TestClient
from tradiba.decision.api import router
from fastapi import FastAPI
import uuid

app = FastAPI()
app.include_router(router)

def test_decision_api():
    client = TestClient(app)
    
    resp = client.get("/decisions/")
    assert resp.status_code == 200
    
    d_id = uuid.uuid4()
    resp2 = client.post(f"/decisions/{d_id}/approve")
    assert resp2.status_code == 200
    assert resp2.json()["status"] == "approved"
