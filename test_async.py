import asyncio
import time

from src.modules.repositories import UserRepo

async def main():

    start_time = time.time()

    task_1 = UserRepo.find_by_account("vu_khanh", delay=5, id=1)
    task_2 = UserRepo.find_by_account("vinh_khang", delay=2, id=2)

    async_task_1 = asyncio.create_task(task_1)
    async_task_2 = asyncio.create_task(task_2)

    await asyncio.gather(async_task_1, async_task_2)
    end_time = time.time()

    print(f"\nTotal Time: {end_time - start_time:.3f}s")

if __name__ == "__main__":
    asyncio.run(main())