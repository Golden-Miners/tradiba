from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from tradiba.api.exceptions import APIError
from .jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    payload = decode_access_token(token)
    if not payload:
        raise APIError("UNAUTHORIZED", "Invalid or expired token.", 401)
    
    # Normally we'd query the DB for the user here. 
    # For now, trust the payload.
    return payload


def requires_role(required_role: str):
    def role_checker(user: dict = Depends(get_current_user)):
        roles = user.get("roles", [])
        if required_role not in roles and "Admin" not in roles:
            raise APIError(
                "FORBIDDEN", 
                f"Insufficient permissions. Required role: {required_role}", 
                403
            )
        return user
    return role_checker
