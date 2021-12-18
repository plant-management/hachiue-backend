from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import character, home, plant, timeline, user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:19006",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(plant.router)
app.include_router(home.router)
app.include_router(timeline.router)
app.include_router(character.router)
