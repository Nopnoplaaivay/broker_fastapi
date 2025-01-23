from fastapi import APIRouter, HTTPException

from src.api.schemas import Token, AccountLogin
from src.modules.services import UserService, TokenService


router = APIRouter(prefix="/api/auth")

@router.post("/access_token", response_model=Token)
async def get_access_token(account: AccountLogin):
    user = await UserService.login_user(data=account.model_dump())
    if not user:
        raise HTTPException(status_code=404, detail="Account not exists or password is incorrect")

    token = TokenService.generate_token(user_data=user.__dict__)
    return Token(access_token=token)