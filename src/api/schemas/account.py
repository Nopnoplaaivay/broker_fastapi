from typing import Optional
from pydantic import BaseModel, ConfigDict

class AccountBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    account: str
    type_user: str
    type_broker: Optional[str] = None
    type_client: Optional[str] = None

class AccountLogin(BaseModel):
    account: str
    password: str

class AccountCreate(AccountBase):
    password: str

class AccountUpdatePassword(BaseModel):
    account: str
    old_password: str
    new_password: str