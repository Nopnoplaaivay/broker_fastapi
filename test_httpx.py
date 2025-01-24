import asyncio
import httpx
import time

API_URL = "http://127.0.0.1:8000/api/user/vu_khanh"

async def send_request(client: httpx.AsyncClient, request_id: int):
    try:
        start_time = time.time()
        response = await client.get(API_URL, timeout=5.0)
        end_time = time.time()
        print(f"Request {request_id} - Status: {response.status_code}, Time: {end_time - start_time:.2f}s")
        return response.status_code
    except httpx.RequestError as e:
        print(f"Request {request_id} failed: {e}")
        return None

async def main():
    num_requests = 500
    async with httpx.AsyncClient() as client:
        tasks = [send_request(client, i) for i in range(num_requests)]

        start_time = time.time()
        responses = await asyncio.gather(*tasks)
        end_time = time.time()

        print(f"\nTotal Time for {num_requests} requests: {end_time - start_time:.3f}s")
        print(f"Successful Responses: {responses.count(200)}")

if __name__ == "__main__":
    asyncio.run(main())
