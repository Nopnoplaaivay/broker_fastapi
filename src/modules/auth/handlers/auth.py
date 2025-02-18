from fastapi import APIRouter, Body, Depends
from typing import Optional
from .decorators import JwtPayload, RefreshToken
from .dtos import AuthReqDto, LoginResDto, RefreshResDto
from .services import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", summary="Register a new account")
async def register(dto: AuthReqDto, service: AuthService = Depends()):
    await service.register(dto)

@router.post("/login", summary="Login", response_model=LoginResDto)
async def login(dto: AuthReqDto, service: AuthService = Depends()) -> LoginResDto:
    return await service.login(dto)

@router.post("/logout", summary="Logout")
async def logout(payload: dict = Depends(JwtPayload), service: AuthService = Depends()):
    await service.logout(payload)

@router.post("/refresh-token", summary="Get new access token", response_model=RefreshResDto)
@RefreshToken()
async def refresh_token(
    payload: dict = Depends(JwtPayload), service: AuthService = Depends()
) -> RefreshResDto:
    return await service.refresh_token(payload)

# TODO: Implement forgot password, verify email, etc.
@router.post("/forgot-password", include_in_schema=False)
async def forgot_password():
    return {"message": "forgot-password"}

@router.post("/verify/forgot-password", include_in_schema=False)
async def verify_forgot_password():
    return {"message": "verify-forgot-password"}

@router.get("/verify/email", include_in_schema=False)
async def verify_email():
    return {"message": "verify-email"}

@router.post("/verify/email/resend", include_in_schema=False)
async def resend_verify_email():
    return {"message": "resend-verify-email"}