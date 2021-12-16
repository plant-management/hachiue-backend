import random
import uuid

import app.cruds.character as character_cruds
import app.cruds.plant as plant_cruds

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
    # 最新のデータを取得する
    data_id = str(uuid.uuid4())
    weather_icon = "sunny"
    temp = 24.8
    humidity = 34
    sunlight = 100.3
    moisture = 87
    satisfaction = 50  # 完全ダミーデータ
    comment_list = ("おなかすいたよ", "のどがかわいたよ", "あそんでよ～", "ねむたいよ～", "うれしいｗ")
    comment = random.choice(comment_list)

    await plant_cruds.create_data(
        db,
        user_id=user_id,
        plant_id=plant_id,
        data_id=data_id,
        weather_icon=weather_icon,
        temp=temp,
        humidity=humidity,
        sunlight=sunlight,
        moisture=moisture,
        satisfaction=satisfaction,
        comment=comment,
    )

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


@router.get("/character_tap_comment/{user_id}")
async def character_tap(
    user_id: str, plant_id: str, db: AsyncSession = Depends(get_db)
):
    comment1 = await character_cruds.get_character_comment(
        db, user_id=user_id, plant_id=plant_id
    )
    comment_list = ("遊んでくれてありがとう!!", "えへへｗ嬉しいな", "いい天気だね", comment1)
    comment = random.choice(comment_list)
    return comment
