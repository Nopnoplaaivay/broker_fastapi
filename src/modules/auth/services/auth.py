import argon2
from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import jwt
from typing import Dict, Optional
from .config import AuthConfig
from .entities import UserEntity, SessionEntity

class AuthService:
    def __init__(self, config: AuthConfig, cache_manager):
        self.config = config
        self.cache_manager = cache_manager
        self.logger = None  # Replace with a proper logger

    async def register(self, dto: AuthReqDto):
        email = dto.email
        if await UserEntity.exists_by({"email": email}):
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = await self._hash_password(dto.password)
        await UserEntity.save(
            UserEntity(email=email, password=hashed_password, role="USER")
        )

    async def login(self, dto: AuthReqDto) -> Dict[str, str]:
        user = await UserEntity.find_one({"email": dto.email})
        if not user or not await self._verify_password(user.password, dto.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        refresh_token_ttl = self.config.get("AUTH_REFRESH_TOKEN_EXPIRES_IN")
        signature = self._create_signature()
        session = await SessionEntity.save(
            SessionEntity(
                signature=signature,
                user=user,
                expires_at=datetime.utcnow() + timedelta(seconds=refresh_token_ttl),
            )
        )

        payload = {
            "user_id": user.id,
            "session_id": session.id,
            "role": user.role,
        }
        access_token = await self._create_access_token(payload)
        refresh_token = await self._create_refresh_token({**payload, "signature": signature})
        return {"access_token": access_token, "refresh_token": refresh_token}

    async def logout(self, payload: Dict[str, str]):
        session_id = payload["session_id"]
        user_id = payload["user_id"]
        exp = payload["exp"]

        key = f"SESSION_BLACKLIST:{user_id}:{session_id}"
        await self._add_to_blacklist(key, exp)

        session = await SessionEntity.find_one({"id": session_id})
        if session:
            await SessionEntity.delete(session)

    async def refresh_token(self, payload: Dict[str, str]) -> Dict[str, str]:
        session_id = payload["session_id"]
        signature = payload["signature"]

        session = await SessionEntity.find_one({"id": session_id}, relations={"user": True})
        if not session or session.signature != signature:
            raise HTTPException(status_code=401, detail="Invalid session")

        new_signature = self._create_signature()
        payload = {
            "user_id": session.user.id,
            "session_id": session.id,
            "role": session.user.role,
        }

        await SessionEntity.update(session.id, {"signature": new_signature})

        access_token = await self._create_access_token(payload)
        refresh_token = await self._create_refresh_token({**payload, "signature": new_signature})
        return {"access_token": access_token, "refresh_token": refresh_token}

    async def _create_access_token(self, payload: Dict[str, str]) -> str:
        return jwt.encode(
            payload,
            self.config.get("AUTH_JWT_SECRET"),
            algorithm="HS256",
            expires_delta=timedelta(seconds=self.config.get("AUTH_JWT_TOKEN_EXPIRES_IN")),
        )

    async def _create_refresh_token(self, payload: Dict[str, str]) -> str:
        return jwt.encode(
            payload,
            self.config.get("AUTH_REFRESH_SECRET"),
            algorithm="HS256",
            expires_delta=timedelta(seconds=self.config.get("AUTH_REFRESH_TOKEN_EXPIRES_IN")),
        )

    async def _verify_password(self, hashed: str, plain: str) -> bool:
        try:
            return argon2.verify(hashed, plain)
        except Exception:
            return False

    async def _hash_password(self, plain: str) -> str:
        return argon2.hash(plain)

    def _create_signature(self) -> str:
        import secrets
        return secrets.token_hex(16)

    async def _add_to_blacklist(self, key: str, exp: int):
        ttl = exp * 1000 - int(datetime.utcnow().timestamp() * 1000)
        await self.cache_manager.set(key, True, ttl)

    async def _check_blacklist(self, user_id: int, key: str):
        is_blacklisted = await self.cache_manager.get(key)
        if is_blacklisted:
            sessions = await SessionEntity.find({"user_id": user_id})
            await SessionEntity.delete_many(sessions)
            raise HTTPException(status_code=401, detail="Session revoked")