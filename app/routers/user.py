import uuid

import app.cruds.user as user_cruds
import app.schemas.user as user_schame
from app.db import get_db
from fastapi import APIRouter, Depends  # ,HTTPException,status
from sqlalchemy.ext.asyncio.session import AsyncSession

# from typing import List


router = APIRouter()


# 初回のユーザー新規登録
@router.post("/create_user", response_model=user_schame.UserCreateResponse)
async def create_user(
    user_create: user_schame.UserCreate, db: AsyncSession = Depends(get_db)
):
    user_id = str(uuid.uuid4())
    return await user_cruds.create_user(db, user_id=user_id, user_create=user_create)


# #検証用:ユーザー情報の取得
# @router.get("/test_user",response_model=List[user_schame.User])
# async def test_get_user(db: AsyncSession = Depends(get_db)):
#     return await user_crud.get_users(db)
