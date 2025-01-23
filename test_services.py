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
    {"id": 1, "account": "mai_van_hiep", "data": "demo data user4"},
    {"id": 2, "account": "mai_van_hiep", "data": "demo data user4"},
    {"id": 3, "account": "mai_van_hiep", "data": "demo data user4"},
    {"id": 4, "account": "mai_van_hiep", "data": "demo data user4"},
    {"id": 5, "account": "trang_doan", "data": "demo data user5"},
    {"id": 6, "account": "trang_doan", "data": "demo data user5"},
    {"id": 7, "account": "trang_doan", "data": "demo data user5"},
    {"id": 8, "account": "trang_doan", "data": "demo data user5"},
    {"id": 9, "account": "cao_thai", "data": "demo data user6"},
    {"id": 10, "account": "cao_thai", "data": "demo data user6"},
    {"id": 11, "account": "cao_thai", "data": "demo data user6"},
    {"id": 12, "account": "cao_thai", "data": "demo data user6"},
    {"id": 13, "account": "duong_huyen_trang", "data": "demo data user7"},
    {"id": 14, "account": "duong_huyen_trang", "data": "demo data user7"},
    {"id": 15, "account": "duong_huyen_trang", "data": "demo data user7"},
    {"id": 16, "account": "duong_huyen_trang", "data": "demo data user7"},
]

from src.modules.services import UserService, FakeDataService

async def create_users():
    await UserService.repo.insert_many(users_data)
    await FakeDataService.repo.insert_many(fake_data)

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_users())