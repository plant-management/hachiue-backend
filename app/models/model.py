from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp

from app.db import Base

# ユーザー情報登録
class User(Base):
    __tablename__ = "user"
    user_id = Column(String(128),primary_key=True)
    user_name = Column(String(128))
    post_code = Column(String(8))
    wifi_ssid = Column(String(128))
    wifi_pass = Column(String(128))
    birthday = Column(Date)

    plant = relationship("Plant",back_populates="user")
    image = relationship("Image",back_populates="user")
    data = relationship("Data",back_populates="user")


# 植物情報を登録
class Plant(Base):
    __tablename__ = "plant"
    user_id = Column(String(128),ForeignKey("user.user_id"))
    plant_id = Column(String(128),primary_key=True)
    plant_name = Column(String(128),)
    plant_type = Column(String(128))
    plant_label_color = Column(String(128))
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())

    user = relationship("User",back_populates="plant")
    image = relationship("Image",back_populates="plant")
    data = relationship("Data",back_populates="plant")


# 画像情報を登録
class Image(Base):
    __tablename__ = "image"
    user_id = Column(String(128),ForeignKey("user.user_id"))
    plant_id = Column(String(128),ForeignKey("plant.plant_id"))
    image_id = Column(String(128), primary_key=True) 
    plant_image_path = Column(String(128))
    character_image_path = Column(String(128),nullable=True)
    growth = Column(Integer)
    health = Column(Integer)
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())

    plant = relationship("Plant",back_populates="image")
    user = relationship("User",back_populates="image")


# 環境等のデータを登録
class Data(Base):
    __tablename__ = "data"
    user_id = Column(String(128),ForeignKey("user.user_id"))
    plant_id = Column(String(128),ForeignKey("plant.plant_id"))
    data_id = Column(String(128), primary_key=True) 
    weather_icon = Column(String(128))
    temp = Column(Float)
    humidity = Column(Integer)
    sunlight = Column(Float,nullable=True) 
    moisture = Column(Integer,nullable=True)
    satisfaction = Column(Integer)
    comment = Column(String(128),server_default="よろしくね!!")
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())

    plant = relationship("Plant",back_populates="data")
    user = relationship("User",back_populates="data")