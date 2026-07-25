from fastapi import APIRouter
from tradiba.api.schemas import LoginRequest, TokenResponse
from tradiba.api.exceptions import APIError
from .jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    # Dummy authentication logic
    if credentials.username == "admin" and credentials.password == "admin":
        roles = ["Admin"]
    elif credentials.username == "trader" and credentials.password == "trader":
        roles = ["Trader"]
    elif credentials.username == "viewer" and credentials.password == "viewer":
        roles = ["Viewer"]
    else:
        raise APIError("INVALID_CREDENTIALS", "Incorrect username or password.", 401)
        
    token = create_access_token({"sub": credentials.username, "roles": roles})
    return TokenResponse(access_token=token)
