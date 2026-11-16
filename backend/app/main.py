# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from app.database.connection import engine, Base
# from app.models.user import User
# from app.routers.auth import router as auth_router

# Base.metadata.create_all(bind=engine)

# app = FastAPI(title="Vocal-X API")

# # Allow React frontend to communicate with FastAPI
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(auth_router)


# @app.get("/")
# def home():
#     return {"message": "Vocal-X Backend is running!"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.speech import router as speech_router
from app.routers.speech import router as speech_router

from app.database.connection import engine, Base
from app.models.user import User
from app.routers.auth import router as auth_router
from app.routers.voice import router as voice_router
from app.routers.translation import router as translation_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vocal-X API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(voice_router)
app.include_router(translation_router)
app.include_router(speech_router)
app.include_router(speech_router)


@app.get("/")
def home():
    return {"message": "Vocal-X Backend is running!"}