import app.models.model as production_model
from sqlalchemy import desc, select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession


# cruds操作を3つに分けずに1つにまとめてもいい気がします。outerjoin
# [キャラクター画面用]Plant_テーブルから必要なデータを取得
async def get_character_plant(db: AsyncSession, user_id: str, plant_id: str):
    result: Result = await (
        db.execute(
            select(
                production_model.Plant.plant_name,
                production_model.Plant.plant_type,
                production_model.Plant.created_at,
            )
            .filter(production_model.Plant.user_id == user_id)
            .filter(production_model.Plant.plant_id == plant_id)
            .limit(1)
        )
    )
    return result.all()


# [キャラクター画面]imageテーブルから最新のcharacter_image_pathを取得(1件)
async def get_one_character_image(db: AsyncSession, user_id: str, plant_id: str):
    result: Result = await (
        db.execute(
            select(production_model.Image.character_image_path)
            .order_by(desc(production_model.Image.created_at))
            .filter(production_model.Image.user_id == user_id)
            .filter(production_model.Image.plant_id == plant_id)
            .limit(1)
        )
    )
    return result.all()


# [キャラクター画面用]Data_テーブルメイン画面に必要なデータを取得
async def get_character_data(db: AsyncSession, user_id: str, plant_id: str):
    result: Result = await (
        db.execute(
            select(
                production_model.Data.weather_icon,
                production_model.Data.temp,
                production_model.Data.humidity,
                production_model.Data.satisfaction,
                production_model.Data.comment,
            )
            .order_by(desc(production_model.Data.created_at))
            .filter(production_model.Data.user_id == user_id)
            .filter(production_model.Data.plant_id == plant_id)
            .limit(1)
        )
    )
    return result.all()


# キャラクタータップ時にコメントを送信
async def get_character_comment(db: AsyncSession, user_id: str, plant_id: str):
    result: Result = await (
        db.execute(
            select(production_model.Data.comment)
            .order_by(desc(production_model.Data.created_at))
            .filter(production_model.Data.user_id == user_id)
            .filter(production_model.Data.plant_id == plant_id)
            .limit(1)
        )
    )
    comment = result.all()[0]["comment"]
    return comment
