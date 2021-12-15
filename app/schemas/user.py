from datetime import date
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    user_name: str
    post_code: str
    wifi_ssid: Optional[str]
    wifi_pass: Optional[str]
    birthday: date


class UserCreateResponse(UserBase):
    user_id: str

    class Config:
        orm_mode = True


class User(UserCreate):
    user_id: str

    class Config:
        orm_mode = True
