from datetime import timedelta
from typing import Optional

from pydantic import BaseModel


# キャラクター画面
class CharacterCreateResponse(BaseModel):
    plant_name: str
    plant_type: str
    days: timedelta
    wether_icon: Optional[str]
    temp: Optional[float]
    humidity: Optional[int]
    satisfaction: Optional[int]
    comment: str
    character_image: str

    class Config:
        orm_mode = True


class Character(CharacterCreateResponse):
    class Config:
        orm_mode = True
