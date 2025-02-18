from typing import Dict

from src.modules.entities import FakeData
from src.modules.repositories import FakeDataRepo

class FakeDataService:
    repo = FakeDataRepo

    @classmethod
    async def get_fake_data(cls, request_user: Dict) -> FakeData:
        account = request_user["account"]
        type_user = request_user["type_user"]
        data = None
        if type_user == "admin":
            data = await cls.repo.get_all()
        else:
            data = await cls.repo.get_data_by_account(account=account)

        return  [item.__dict__ for item in data]