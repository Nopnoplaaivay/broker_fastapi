from typing import List, Dict
from pydantic import BaseModel, ConfigDict

class FakeData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    account: str
    data: str