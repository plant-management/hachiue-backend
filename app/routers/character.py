import random
import uuid

import app.cruds.character as character_cruds
import app.cruds.plant as plant_cruds

# import app.schemas.character as character_schema
from app.db import get_db
from app.func.data_func import (
    get_sunlight_value,
    location,
    satisfact,
    select_comment,
    weather,
)
from app.func.get_ftp_data import get_ftp
from app.func.img_func import b64_to_png, calc_progress_day, png_to_base64
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
    # キャラクターの最新のimage_idを取得する
    image_id = await character_cruds.get_image_id(
        db, user_id=user_id, plant_id=plant_id
    )
    # 最新のデータを取得する
    data_id = str(uuid.uuid4())
    post_code = await plant_cruds.get_post_code(db, user_id=user_id)
    lat, lon = location(post_code)  # 緯度経度を取得
    get_ftp()
    sunlight = get_sunlight_value(lat, lon)  # 日照度を取得する
    wth = weather(lat, lon)
    weather_icon = wth[0]  # 天気
    temp = wth[1]  # 気温
    humidity = wth[2]  # 湿度
    moisture = random.randrange(1, 100)
    comment = select_comment(moisture, sunlight)
    satisfaction = random.randrange(1, 9)  # 完全ダミーデータ

    await plant_cruds.create_data(
        db,
        user_id=user_id,
        plant_id=plant_id,
        image_id=image_id,
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


@router.post("/take_picture/{user_id}")
async def take_picture(
    user_id: str, plant_id: str, b64_image: str, db: AsyncSession = Depends(get_db)
):
    image_id = str(uuid.uuid4())
    # データの取得
    post_code = await plant_cruds.get_post_code(db, user_id=user_id)
    lat, lon = location(post_code)  # 緯度経度を取得
    get_ftp()
    sunlight = get_sunlight_value(lat, lon)  # 日照度を取得する
    wth = weather(lat, lon)
    weather_icon = wth[0]  # 天気
    temp = wth[1]  # 気温
    humidity = wth[2]  # 湿度
    moisture = random.randrange(1, 100)
    comment = select_comment(moisture, sunlight)

    time1 = await plant_cruds.get_plant_create_time(
        db, user_id=user_id, plant_id=plant_id
    )
    days = calc_progress_day(time1)

    # UPLOAD_PLANT_FOLDER = "./picture/" + str(user_id) + "/plant_image/"
    # plant_image_path = b64_to_png(b64_image, UPLOAD_PLANT_FOLDER)

    # growth,healthの推定：綾部君
    growth = 2
    health = 2
    # 表情に関するパラメーターの算出
    satisfaction = satisfact(sunlight, moisture, health)

    # 美少女画像の生成：一氏君
    # UPLOAD_CHARACTER_FOLDER = "./picture/" + str(user_id) + "/character_image/"
    character_image_path = "test1.png"  # ダミーデータ
    character_image_base64 = png_to_base64(character_image_path)
    # 植物画像は、pngの場合：plant_image_path, b64の場合：b64_imageです。
    # 保存場所は、character_image_path = UPLOAD_CHARACTER_FOLDER + str(uuid.uuid4()) + ".png"
    # 可能であれば、リサイズした状態で保存してほしいです。

    # Image dbに画像データを登録 本来は登録するが、今回はpass await plant_cruds.create_image
    # plant_name,plant_typeを取得
    plant_name, plant_type = await plant_cruds.get_plant_name_and_type(
        db, user_id=user_id, plant_id=plant_id
    )

    satisfaction = int(satisfaction * 100)

    return {
        "plant_id": plant_id,
        "plant_name": plant_name,
        "plant_type": plant_type,
        "weather_icon": weather_icon,
        "temp": temp,
        "humidity": humidity,
        "comment": comment,
        "satisfaction": satisfaction,
        "days": days,
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
