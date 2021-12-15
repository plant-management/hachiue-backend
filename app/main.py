from fastapi import FastAPI

from app.routers import plant, user  # , home, timeline, character

app = FastAPI()
app.include_router(user.router)
app.include_router(plant.router)
# app.include_router(home.router)
# app.include_router(timeline.router)
# app.include_router(character.router)
