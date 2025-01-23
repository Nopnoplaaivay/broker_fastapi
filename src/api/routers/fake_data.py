from typing import Dict, List
from fastapi import APIRouter, HTTPException, Depends

from src.api.schemas import FakeData
from src.modules.services import TokenService, FakeDataService


router = APIRouter(prefix="/api/data")

@router.get("/", response_model=Dict[str, List[FakeData]])
async def get_data(request_user: dict = Depends(TokenService.verify_token)):
    data = await FakeDataService.get_fake_data(request_user=request_user)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return {"data": data}
