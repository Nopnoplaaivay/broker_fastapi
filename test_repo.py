users_data = [
    {
        "id": 1,
        "account": "client_alex",
        "type_user": "client", 
        "type_client": "financial",
        "password": "client_secure_pass444"
    },
    {
        "id": 2,
        "account": "client_rachel",
        "type_user": "client", 
        "type_client": "real_estate",
        "password": "client_secure_pass555"
    },
    {
        "id": 3,
        "account": "broker_tom",
        "type_user": "broker", 
        "type_broker": "insurance",
        "password": "broker_secure_pass666"
    },
    {
        "id": 4,
        "account": "client_james",
        "type_user": "client", 
        "type_client": "insurance",
        "password": "client_secure_pass777"
    }
]

from src.modules.services.user import UserService

async def create_users():
    await UserService.repo.insert_many(users_data)

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_users())