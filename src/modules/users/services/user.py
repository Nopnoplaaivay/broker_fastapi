from typing import Dict, Optional

from src.modules.entities import User
from src.modules.repositories import UserRepo

class UserService:
    repo = UserRepo

    @classmethod
    async def update_password(cls, account_data: Dict) -> Optional[User]:
        account = account_data['account']
        old_password = account_data['old_password']
        new_password = account_data['new_password']
        user = await cls.repo.find_by_account(account)

        if not user:
            return None
        if user.password != old_password:
            return None
        user.password = new_password

        user = await cls.repo.upsert(entity=user)

        return user

    @classmethod
    async def get_user_by_account(cls, account: str) -> Optional[User]:
        user = await cls.repo.find_by_account(account)
        return user

    @classmethod
    async def create_user(cls, data: Dict) ->  Optional[User]:
        user = User(**data)
        result = await cls.repo.upsert(entity=user)
        return result

    @classmethod
    async def login_user(cls, data: Dict) -> Optional[User]:
        account = data['account']
        password = data['password']
        user = await cls.repo.find_by_account(account)
        if not user:
            return None
        if user.password != password:
            return None
        return user
