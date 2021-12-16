import os
import random
import uuid

import app.cruds.plant as plant_cruds
import app.schemas.plant as plant_schama
from app.db import get_db
from app.func.data_func import get_sunlight_value, location, select_comment, weather
from app.func.get_ftp_data import get_ftp
from app.func.img_func import b64_to_png, calc_progress_day, png_to_base64
from fastapi import APIRouter, Depends  # ,HTTPException,status
from sqlalchemy.ext.asyncio.session import AsyncSession

router = APIRouter()


# 植物新規登録の処理(dataのみ)
@router.post(
    "/new_plant_data/{user_id}", response_model=plant_schama.PlantCreateResponse
)
async def create_new_plant_character(
    user_id: str,
    b64_image: str,
    plant_create: plant_schama.PlantCreate,
    db: AsyncSession = Depends(get_db),
):
    # plant情報の登録
    plant_id = str(uuid.uuid4())
    data_id = str(uuid.uuid4())
    image_id = str(uuid.uuid4())
    await plant_cruds.create_plant(
        db, plant_create=plant_create, user_id=user_id, plant_id=plant_id
    )
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

    # ユーザー用の植物データ保存用ディレクトリの新規作成
    UPLOAD_PLANT_FOLDER = "./picture/" + str(user_id) + "/plant_image/"
    os.makedirs(UPLOAD_PLANT_FOLDER, exist_ok=True)
    plant_image_path = b64_to_png(b64_image, UPLOAD_PLANT_FOLDER)

    # growth,healthの推定：綾部君
    growth = 2
    health = 2
    # 表情に関するパラメーターの算出
    satisfaction = int(
        (health * sunlight * moisture) / 200
    )  # 母数はmax値 moistureは0-100 or 1-3 迷い中 health 1-3

    # 美少女画像の生成：一氏君
    # UPLOAD_CHARACTER_FOLDER = "./picture/" + str(user_id) + "/character_image/"
    os.makedirs(UPLOAD_PLANT_FOLDER, exist_ok=True)
    character_image_path = "test1.png"  # ダミーデータ
    character_image_base64 = png_to_base64(character_image_path)
    # 植物画像は、pngの場合：plant_image_path, b64の場合：b64_imageです。
    # 保存場所は、character_image_path = UPLOAD_CHARACTER_FOLDER + str(uuid.uuid4()) + ".png"
    # 可能であれば、リサイズした状態で保存してほしいです。

    await plant_cruds.create_image(
        db,
        user_id=user_id,
        plant_id=plant_id,
        image_id=image_id,
        plant_image_path=plant_image_path,
        character_image_path=character_image_path,
        growth=growth,
        health=health,
    )
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
    return {
        "user_id": user_id,
        "plant_id": plant_id,
        **plant_create.dict(),
        "weather_icon": weather_icon,
        "temp": temp,
        "humidity": humidity,
        "comment": comment,
        "satisfaction": satisfaction,
        "days": days,
        "character_image": character_image_base64,
    }
