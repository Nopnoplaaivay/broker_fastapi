import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

users_data = [
    {"id": 1, "account": "vu_khanh", "type_user": "admin", "password": "asd123456"},
    {"id": 2, "account": "vinh_khang", "type_user": "broker", "type_broker": "broker_2", "password": "asd123456"},
    {"id": 3, "account": "hanh_nguyen", "type_user": "broker", "type_broker": "broker_1", "password": "asd123456"},
    {"id": 4, "account": "mai_van_hiep", "type_user": "client", "type_client": "broker_1", "password": "asd123456"},
    {"id": 5, "account": "trang_doan", "type_user": "client", "type_client": "broker_1", "password": "asd123456"},
    {"id": 6, "account": "cao_thai", "type_user": "client", "type_client": "broker_2", "password": "asd123456"},
    {"id": 7, "account": "duong_huyen_trang", "type_user": "client", "type_client": "broker_2", "password": "asd123456"},
]

fake_data = [
    {"id": 1, "account": "mai_van_hiep", "data": "demo data mai_van_hiep"},
    {"id": 2, "account": "mai_van_hiep", "data": "demo data mai_van_hiep"},
    {"id": 3, "account": "mai_van_hiep", "data": "demo data mai_van_hiep"},
    {"id": 4, "account": "mai_van_hiep", "data": "demo data mai_van_hiep"},
    {"id": 5, "account": "trang_doan", "data": "demo data trang_doan"},
    {"id": 6, "account": "trang_doan", "data": "demo data trang_doan"},
    {"id": 7, "account": "trang_doan", "data": "demo data trang_doan"},
    {"id": 8, "account": "trang_doan", "data": "demo data trang_doan"},
    {"id": 9, "account": "cao_thai", "data": "demo data cao_thai"},
    {"id": 10, "account": "cao_thai", "data": "demo data cao_thai"},
    {"id": 11, "account": "cao_thai", "data": "demo data cao_thai"},
    {"id": 12, "account": "cao_thai", "data": "demo data cao_thai"},
    {"id": 13, "account": "duong_huyen_trang", "data": "demo data duong_huyen_trang"},
    {"id": 14, "account": "duong_huyen_trang", "data": "demo data duong_huyen_trang"},
    {"id": 15, "account": "duong_huyen_trang", "data": "demo data duong_huyen_trang"},
    {"id": 16, "account": "duong_huyen_trang", "data": "demo data duong_huyen_trang"},
    {"id": 17, "account": "vu_khanh", "data": "demo data vu_khanh"},
    {"id": 18, "account": "vu_khanh", "data": "demo data vu_khanh"},
    {"id": 19, "account": "vinh_khang", "data": "demo data vinh_khang"},
    {"id": 20, "account": "vinh_khang", "data": "demo data vinh_khang"},
]

from src.modules.services import UserService, FakeDataService

async def create_users():
    # await UserService.repo.insert_many(users_data)
    await FakeDataService.repo.insert_many(fake_data)

    # update user
    # user = await UserService.update_password({
    #     "account": "vu_khanh",
    #     "old_password": "asd123456",
    #     "new_password": "asd12345678"
    # })
    # print("Successfully updated")
    # print(user.__dict__)

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_users())