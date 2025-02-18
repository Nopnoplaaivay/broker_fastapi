from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class AuthReqDto(BaseModel):
    email: EmailStr
    password: constr(min_length=8)  # Password must be at least 8 characters

class AuthResDto(BaseModel):
    access_token: str
    refresh_token: str

class LoginResDto(AuthResDto):
    pass

class RefreshResDto(BaseModel):
    access_token: str