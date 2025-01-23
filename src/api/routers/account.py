from fastapi import APIRouter, HTTPException, Depends

from src.api.schemas import AccountCreate, AccountUpdatePassword
from src.modules.services import UserService, TokenService

router = APIRouter(prefix="/api/account")

@router.post("/create", response_model=AccountCreate)
async def create_account(account: AccountCreate):
    db_user = await UserService.get_user_by_account(account.account)
    if db_user:
        raise HTTPException(status_code=400, detail="Account already registered")
    user = await UserService.create_user(data=account.model_dump())
    return user

@router.patch("/password", response_model=AccountUpdatePassword)
async def update_password(account: AccountUpdatePassword, user_data: dict = Depends(TokenService.verify_token)):
    # user = await UserService.update_password(data=account.model_dump())
    print(user_data)
    return account
    # if not user:
    #     raise HTTPException(status_code=404, detail="Account not exists or password is incorrect")
    # return user