from typing import Optional
from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    account: str
    type_user: str
    type_broker: Optional[str] = None
    type_client: Optional[str] = None