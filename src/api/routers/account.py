from fastapi import APIRouter, HTTPException, Depends

from src.api.schemas import AccountCreate, AccountUpdatePassword
from src.modules.services import UserService, TokenService
from src.utils.permissions import Permissions
from src.utils.logger import LOGGER

router = APIRouter(prefix="/api/account")

@router.post("/create", response_model=AccountCreate)
async def create_account(account: AccountCreate):
    db_user = await UserService.get_user_by_account(account.account)
    if db_user:
        raise HTTPException(status_code=400, detail="Account already registered")
    user = await UserService.create_user(data=account.model_dump())
    return user

@router.patch("/password", response_model=AccountUpdatePassword)
async def update_password(account_data: AccountUpdatePassword, request_user: dict = Depends(TokenService.verify_token)):
    target_user = await UserService.get_user_by_account(account_data.account)
    if not target_user:
        raise HTTPException(status_code=404, detail="Account not exists or password is incorrect")
    target_user = target_user.__dict__
    print(target_user)
    print(request_user)

    if not Permissions.verify(action="update_password", request_user=request_user, target_user=target_user):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    # Update password logic
    user = await UserService.update_password(account_data=account_data.model_dump())
    if not user:
        raise HTTPException(status_code=404, detail="Account not exists or password is incorrect")

    LOGGER.info(f"Successfully updated: {user.__dict__}")
    LOGGER.info(f"Request User: {request_user}")
    return account_data