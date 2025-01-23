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
            "account": user_data.get("account"),
            "type_user": user_data.get("type_user"),
            "type_broker": user_data.get("type_broker"),
            "type_client": user_data.get("type_client"),
            "exp": datetime.now() + timedelta(days=1)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    @staticmethod
    async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
        try:
            payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
            account = payload.get("account")
            type_user = payload.get("type_user")
            type_broker = payload.get("type_broker")
            type_client = payload.get("type_client")
            return {"account": account, "type_user": type_user, "type_broker": type_broker, "type_client": type_client}
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")