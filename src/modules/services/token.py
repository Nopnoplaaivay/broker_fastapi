import os
import jwt
from typing import Dict
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = os.getenv("SECRET_KEY")
security = HTTPBearer()

class TokenService:
    @staticmethod
    def generate_token(user_data: Dict):
        payload = {
            "user_id": user_data["id"],
            "type_user": user_data["type_user"],
            "exp": datetime.now() + timedelta(days=1)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    @staticmethod
    async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
        try:
            payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            type_user = payload.get("type_user")
            return {"user_id": user_id, "type_user": type_user}
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")