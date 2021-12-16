from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    user_name: str
    post_code: str = Field(...,example = "7550092")
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
