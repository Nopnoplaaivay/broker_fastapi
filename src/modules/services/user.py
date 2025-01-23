from typing import Dict, Optional

from src.modules.entities import User
from src.modules.repositories import UserRepo

class UserService:
    repo = UserRepo

    @classmethod
    async def get_user_by_account(cls, account: str) -> Optional[User]:
        user = await cls.repo.find_by_account(account)
        if not user:
            return None
        return user

    @classmethod
    async def create_user(cls, data: Dict) ->  Optional[User]:
        result = await cls.repo.insert(data=data)
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

    @classmethod
    async def update_password(cls, data: Dict) -> Optional[User]:
        account = data['account']
        old_password = data['old_password']
        new_password = data['new_password']
        user = await cls.repo.find_by_account(account)
        print(user)
        if not user:
            return None
        if user.password != old_password:
            return None
        user.password = new_password

        result = await cls.repo.update(data=user.__dict__)
        return result