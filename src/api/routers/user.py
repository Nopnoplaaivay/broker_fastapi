from fastapi import APIRouter, HTTPException

from src.api.schemas import User
from src.modules.services import UserService


router = APIRouter(prefix="/api/user")

@router.get("/{account}", response_model=User)
async def get_user_by_account(account: str):
    user = await UserService.get_user_by_account(account)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
