import app.models.model as production_model
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession


# [ホーム画面用]plantテーブルからデータを取得
async def get_home_plant(db: AsyncSession, user_id: str):
    result: Result = await (
        db.execute(
            select(
                production_model.Plant.plant_id,
                production_model.Plant.plant_name,
                production_model.Plant.plant_type,
                production_model.Plant.created_at,
                production_model.Plant.plant_label_color,
            ).filter(production_model.Plant.user_id == user_id)
        )
    )
    return result.all()


# [ホーム]imageテーブルからcharacter_image_pathを取得
async def get_home_character_image(db: AsyncSession, user_id: str):
    result: Result = await (
        db.execute(
            select(production_model.Image.character_image_path).filter(
                production_model.Image.user_id == user_id
            )
        )
    )
    return result.all()
