import asyncio
import time
from sqlalchemy import text
from src.modules.repositories import UserRepo
from src.db.sessions import backend_session_scope


async def main():

    async with backend_session_scope() as session:
        print(asyncio.iscoroutinefunction(session.commit))  # Should return True
        print(asyncio.iscoroutinefunction(session.rollback))

    start_time = time.time()

    task_1 = UserRepo.find_by_account("vu_khanh", delay=5, id=1)
    task_2 = UserRepo.find_by_account("vinh_khang", delay=2, id=2)
    task_3 = UserRepo.find_by_account("hanh_nguyen", delay=3, id=3)
    task_4 = UserRepo.find_by_account("cao_thai", delay=4, id=4)
    task_5 = UserRepo.find_by_account("trang_doan", delay=1, id=5)
    task_6 = UserRepo.find_by_account("mai_van_hiep", delay=2, id=6)

    async_task_1 = asyncio.create_task(task_1)
    async_task_2 = asyncio.create_task(task_2)
    async_task_3 = asyncio.create_task(task_3)
    async_task_4 = asyncio.create_task(task_4)
    async_task_5 = asyncio.create_task(task_5)
    async_task_6 = asyncio.create_task(task_6)

    await asyncio.gather(
        async_task_1,
        async_task_2,
        async_task_3,
        async_task_4,
        async_task_5,
        async_task_6,
    )
    end_time = time.time()

    print(f"\nTotal Time: {end_time - start_time:.3f}s")


if __name__ == "__main__":
    asyncio.run(main())
