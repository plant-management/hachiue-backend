from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel


class PlantBase(BaseModel):
    plant_name: str
    plant_type: str
    plant_label_color: str


class PlantCreate(PlantBase):
    pass


class PlantCreateResponse(PlantCreate):
    user_id: str
    plant_id: str
    weather_icon: Optional[str]
    temp: Optional[float]
    humidity: Optional[int]
    comment: str
    satisfaction: Optional[int]
    days: timedelta

    class Config:
        orm_mode = True


class Plant(PlantBase):
    user_id: str
    plant_id: str
    created_at: datetime

    class Config:
        orm_mode = True
