import app.cruds.timeline as timeline_cruds
from app.db import get_db
from app.func.img_func import png_to_base64
from fastapi import APIRouter, Depends  # ,HTTPException,status
from sqlalchemy.ext.asyncio.session import AsyncSession

router = APIRouter()


# [タイムライン用]ユーザーのデータを１０件分返す
@router.get("/timeline/{user_id}")
async def send_timeline(user_id: str, db: AsyncSession = Depends(get_db)):
    img = await timeline_cruds.get_ten_character_image(db, user_id=user_id)
    data = await timeline_cruds.get_timeline_deta(db, user_id=user_id)
    timeline_data = []
    counter = 0
    # 画像のbase64 とその他のデータを辞書型で結合したい。もっといい書き方はありそう。
    for i in img:
        character_image = png_to_base64(i["character_image_path"])
        plant_name = data[counter]["plant_name"]
        comment = data[counter]["comment"]
        created_at = data[counter]["created_at"]
        timeline_data.append(
            {
                "character_image": character_image,
                "plant_name": plant_name,
                "comment": comment,
                "created_at": created_at,
            }
        )
        counter += 1
    return timeline_data
