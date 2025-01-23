from src.modules.repositories import UserRepo
from src.utils.logger import LOGGER


async def test_find_by_account():
    users = await UserRepo.get_all()
    user = await UserRepo.find_by_account("ltduong")
    LOGGER.info(user.__dict__)
    for u in users:
        LOGGER.info(u.__dict__)

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_find_by_account())