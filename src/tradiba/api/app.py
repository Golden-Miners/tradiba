from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
import secure
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

secure_headers = secure.Secure()
limiter = Limiter(key_func=get_remote_address, default_limits=["200/minute"])

from tradiba.api.routers import (
    health,
    metrics,
    portfolio,
    strategies,
    narrative,
    backtest,
    optimization,
    operations
)
from tradiba.api.auth import routes as auth_routes
from tradiba.api.exceptions import APIError, api_error_handler, global_exception_handler
from tradiba.api import websocket as ws_module


def create_app() -> FastAPI:
    app = FastAPI(
        title="Tradiba API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Rate Limiting
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler) # type: ignore
    app.add_middleware(SlowAPIMiddleware)

    # Security Headers Middleware
    @app.middleware("http")
    async def set_secure_headers(request: Request, call_next):
        response = await call_next(request)
        secure_headers.set_headers(response)
        return response
        
    # Exception Handlers
    app.add_exception_handler(APIError, api_error_handler) # type: ignore
    app.add_exception_handler(Exception, global_exception_handler) # type: ignore

    # Routers
    app.include_router(auth_routes.router)
    app.include_router(health.router)
    app.include_router(metrics.router)
    app.include_router(portfolio.router)
    app.include_router(strategies.router)
    app.include_router(narrative.router)
    app.include_router(backtest.router)
    app.include_router(optimization.router)
    app.include_router(operations.router)

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        if not ws_module.ws_manager:
            await websocket.close()
            return
            
        await ws_module.ws_manager.connect(websocket)
        try:
            while True:
                # Wait for subscription message
                data = await websocket.receive_json()
                # Process subscription if necessary
        except WebSocketDisconnect:
            ws_module.ws_manager.disconnect(websocket)
            
    return app

# Main entry point for uvicorn etc
app = create_app()
