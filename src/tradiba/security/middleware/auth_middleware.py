from fastapi import Request, status
from fastapi.security import HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from tradiba.security.auth.jwt import JWTService
from tradiba.security.auth.sessions import SessionManager

security = HTTPBearer()

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, jwt_service: JWTService, session_manager: SessionManager, public_paths: list = None):
        super().__init__(app)
        self.jwt = jwt_service
        self.sessions = session_manager
        self.public_paths = public_paths or ["/api/auth/login", "/api/health"]

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.public_paths:
            return await call_next(request)
            
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                content={"detail": "Missing or invalid authorization header"}
            )
            
        token = auth_header.split(" ")[1]
        payload = self.jwt.verify_token(token)
        
        if not payload:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                content={"detail": "Invalid token"}
            )
            
        session_id = payload.get("session_id")
        if not session_id or not self.sessions.get_session(session_id):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                content={"detail": "Session revoked or expired"}
            )
            
        # Attach user info to request state
        request.state.user = {
            "id": payload.get("sub"),
            "username": payload.get("username"),
            "roles": payload.get("roles", []),
            "session_id": session_id
        }
        
        return await call_next(request)
