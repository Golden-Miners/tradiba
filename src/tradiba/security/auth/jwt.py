import jwt
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

class JWTService:
    def __init__(self, secret_key: str, algorithm: str = "HS256", access_token_expire_minutes: int = 30):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes

    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
            
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
        
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.PyJWTError:
            return None
