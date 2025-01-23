import uvicorn
from fastapi import FastAPI

from src.api.routers import user_router, token_router, account_router

app = FastAPI()
app.include_router(user_router)
app.include_router(account_router)
app.include_router(token_router)

def main():
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)

if __name__ == "__main__":
    main()
