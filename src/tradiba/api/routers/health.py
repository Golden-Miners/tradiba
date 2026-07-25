from fastapi import APIRouter
from fastapi.responses import JSONResponse
# Depending on setup, we might pull health manager from app.state or a global module
# Since Observability HealthManager is likely a global/singleton in the app, we can use a dummy for now 
# or inject it. Let's assume we inject it via app.state.

router = APIRouter(tags=["health"])

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.get("/live")
async def liveness():
    # In a real setup: if not request.app.state.health_manager.is_alive(): return 503
    return JSONResponse(status_code=200, content={"status": "alive"})

@router.get("/ready")
async def readiness():
    # In a real setup: if not request.app.state.health_manager.is_ready(): return 503
    return JSONResponse(status_code=200, content={"status": "ready"})
