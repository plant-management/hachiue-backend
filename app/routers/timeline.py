import app.cruds.timeline as timeline_cruds
from app.db import get_db
from app.func.img_func import png_to_base64
from fastapi import APIRouter, Depends  # ,HTTPException,status
from sqlalchemy.ext.asyncio.session import AsyncSession

router = APIRouter()


# [タイムライン用]ユーザーのデータを１０件分返す
@router.get("/timeline/{user_id}")
async def send_timeline(user_id: str, db: AsyncSession = Depends(get_db)):
    # img = await timeline_cruds.get_ten_character_image(db, user_id=user_id)
    data = await timeline_cruds.get_timeline_deta(db, user_id=user_id)
    timeline_data = []
    # 画像のbase64 とその他のデータを辞書型で結合したい。もっといい書き方はありそう。
    for i in data:
        character_image = png_to_base64(i["character_image_path"])
        plant_id = i["plant_id"]
        plant_name = i["plant_name"]
        comment = i["comment"]
        created_at = i["created_at"]
        timeline_data.append(
            {
                "plant_id": plant_id,
                "character_image": character_image,
                "plant_name": plant_name,
                "comment": comment,
                "created_at": created_at,
            }
        )
    return timeline_data
