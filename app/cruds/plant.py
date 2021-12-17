from datetime import datetime

import app.models.model as production_model
import app.schemas.plant as plant_schema
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession


# [植物の新規作成]植物情報を登録
async def create_plant(
    db: AsyncSession,
    user_id: str,
    plant_id: str,
    plant_create: plant_schema.PlantCreate,
) -> production_model.Plant:
    plant = production_model.Plant(
        **plant_create.dict(), user_id=user_id, plant_id=plant_id
    )
    db.add(plant)
    await db.commit()
    await db.refresh(plant)


# 画像に関するデータを登録
async def create_image(
    db: AsyncSession,
    user_id: str,
    plant_id: str,
    image_id: str,
    plant_image_path: str,
    character_image_path: str,
    growth: int,
    health: int,
) -> production_model.Image:
    image = production_model.Image(
        user_id=user_id,
        plant_id=plant_id,
        image_id=image_id,
        plant_image_path=plant_image_path,
        character_image_path=character_image_path,
        growth=growth,
        health=health,
    )
    db.add(image)
    await db.commit()
    await db.refresh(image)
    return image


# Dataテーブルに関する情報を登録
async def create_data(
    db: AsyncSession,
    user_id: str,
    plant_id: str,
    image_id: str,
    data_id: str,
    weather_icon: str,
    temp: float,
    humidity: int,
    sunlight: int,
    moisture: int,
    satisfaction: int,
    comment: str,
) -> production_model.Data:
    data = production_model.Data(
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
    db.add(data)
    await db.commit()
    await db.refresh(data)
    return data


# post_code取得
async def get_post_code(db: AsyncSession, user_id: str):
    result: Result = await (
        db.execute(
            select(production_model.User.post_code)
            .filter(production_model.User.user_id == user_id)
            .limit(1)
        )
    )
    data = result.all()
    return data[0]["post_code"]


# 植物新規作成の時刻取得
async def get_plant_create_time(
    db: AsyncSession, user_id: str, plant_id: str
) -> datetime:
    result: Result = await (
        db.execute(
            select(production_model.Plant.created_at)
            .filter(production_model.Plant.user_id == user_id)
            .filter(production_model.Plant.plant_id == plant_id)
            .limit(1)
        )
    )
    time = result.all()
    return time[0]["created_at"]


# 植物名と植物種類を取得
async def get_plant_name_and_type(db: AsyncSession, user_id: str, plant_id: str):
    result: Result = await (
        db.execute(
            select(production_model.Plant.plant_name, production_model.Plant.plant_type)
            .filter(production_model.Plant.user_id == user_id)
            .filter(production_model.Plant.plant_id == plant_id)
        )
    )
    data = result.all()
    return data[0]["plant_name"], data[0]["plant_type"]
