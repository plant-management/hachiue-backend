import app.models.model as production_model
from sqlalchemy import desc, select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession


# [timeline]に送るデータを10件分取得
async def get_timeline_deta(db: AsyncSession, user_id: str):
    result: Result = await (
        db.execute(
            select(
                production_model.Plant.plant_name,
                production_model.Data.comment,
                production_model.Data.created_at,
                production_model.Image.character_image_path,
            )
            .order_by(desc(production_model.Data.created_at))
            .filter(production_model.Data.user_id == user_id)
            .filter(production_model.Plant.user_id == user_id)
            .outerjoin(production_model.Plant)
            .outerjoin(production_model.Image.user_id == user_id)
            .limit(10)
        )
    )
    return result.all()


# imageテーブルからcharacter_image_pathを取得(user_idで10件)
# async def get_ten_character_image(db: AsyncSession, user_id: str):
#     result: Result = await (
#         db.execute(
#             select(production_model.Image.character_image_path)
#             .order_by(desc(production_model.Image.created_at))
#             .filter(production_model.Image.user_id == user_id)
#             .limit(10)
#         )
#     )
#     return result.all()
