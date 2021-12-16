import app.models.model as production_model
import app.schemas.user as user_schema
from sqlalchemy.ext.asyncio import AsyncSession

# from sqlalchemy import select
# from sqlalchemy.engine import Result


# 新規のユーザー登録
async def create_user(
    db: AsyncSession, user_id: str, user_create: user_schema.UserCreate
) -> production_model.User:
    user = production_model.User(**user_create.dict(), user_id=user_id)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


# [検証用]ユーザー情報の取得
# async def get_users(db: AsyncSession) -> production_model.User:
#     result: Result =await (
#         db.execute(
#             select(
#                 production_model.User.user_id,
#                 production_model.User.user_name,
#                 production_model.User.birthday,
#                 production_model.User.post_code,
#                 production_model.User.wifi_ssid,
#                 production_model.User.wifi_pass
#             )
#         )
#     )
#     return result.all()
