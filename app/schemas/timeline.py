from datetime import datetime

from pydantic import BaseModel

# from typing import Optional


# タイムライン画面
class TimelineCreateResponse(BaseModel):
    plant_id: str
    plant_name: str
    # character_image: bytes
    comment: str
    created_at: datetime

    class Config:
        orm_mode = True


class Timeline(TimelineCreateResponse):
    class Config:
        orm_mode = True
