import app.cruds.home as home_cruds
from app.db import get_db
from app.func.img_func import calc_progress_day, png_to_base64
from fastapi import APIRouter, Depends  # ,HTTPException,status
from sqlalchemy.ext.asyncio.session import AsyncSession

router = APIRouter()


# ホーム画面に必要な、ユーザーのすべての植物の情報を返す
@router.get("/home/{user_id}")
async def send_home_infomation(user_id: str, db: AsyncSession = Depends(get_db)):
    home_data = await home_cruds.get_home_plant(db, user_id=user_id)
    character_img = await home_cruds.get_home_character_image(db, user_id=user_id)
    all_plant = []
    counter = 0
    for i in character_img:
        base64_character_image = png_to_base64(i["character_image_path"])
        time1 = home_data[counter]["created_at"]
        days = calc_progress_day(time1)
        plant_id = home_data[counter]["plant_id"]
        plant_name = home_data[counter]["plant_name"]
        plant_type = home_data[counter]["plant_type"]
        plant_label_color = home_data[counter]["plant_label_color"]
        all_plant.append(
            {
                "plant_id": plant_id,
                "plant_name": plant_name,
                "plant_type": plant_type,
                "plant_label_color": plant_label_color,
                "day": days,
                "character_image": base64_character_image,
            }
        )
        counter += 1
    return all_plant
