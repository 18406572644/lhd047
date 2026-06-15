from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from database import engine, Base
from routers.auth import router as auth_router
from routers.buildings import router as buildings_router
from routers.media import router as media_router
from routers.comments import router as comments_router
from routers.statistics import router as stats_router
from routers.routes import router as routes_router
from routers.timeline import router as timeline_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="城市废墟探索 API",
    description="废弃建筑记录与地图全栈系统后端接口",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads/photos", exist_ok=True)
os.makedirs("uploads/videos", exist_ok=True)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth_router)
app.include_router(buildings_router)
app.include_router(media_router)
app.include_router(comments_router)
app.include_router(stats_router)
app.include_router(routes_router)
app.include_router(timeline_router)


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "城市废墟探索 API 运行正常"}
