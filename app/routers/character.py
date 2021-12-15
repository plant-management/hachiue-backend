import app.cruds.character as character_cruds

# import app.schemas.character as character_schema
from app.db import get_db
from app.func.img_func import calc_progress_day, png_to_base64
from fastapi import APIRouter, Depends  # ,HTTPException,status
from sqlalchemy.ext.asyncio.session import AsyncSession

router = APIRouter()


# ホーム → character画面遷移で必要なdataを送信
@router.get(
    "/character/{user_id}"
)  # , response_model=character_schema.CharacterCreateResponse
async def character_infomation(
    user_id: str, plant_id: str, db: AsyncSession = Depends(get_db)
):
    plant_data = await character_cruds.get_character_plant(
        db, user_id=user_id, plant_id=plant_id
    )
    character_img = await character_cruds.get_one_character_image(
        db, user_id=user_id, plant_id=plant_id
    )
    data = await character_cruds.get_character_data(
        db, user_id=user_id, plant_id=plant_id
    )
    for i in plant_data:
        plant_name = i["plant_name"]
        plant_type = i["plant_type"]
        time1 = i["created_at"]
    days = calc_progress_day(time1)
    character_image_base64 = png_to_base64(character_img[0]["character_image_path"])
    for i in data:
        weather_icon = i["weather_icon"]
        temp = i["temp"]
        humidity = i["humidity"]
        satisfaction = i["satisfaction"]
        comment = i["comment"]

    return {
        "plant_name": plant_name,
        "plant_type": plant_type,
        "day": days,
        "weather_icon": weather_icon,
        "temp": temp,
        "humidity": humidity,
        "satisfaction": satisfaction,
        "comment": comment,
        "character_image": character_image_base64,
    }
