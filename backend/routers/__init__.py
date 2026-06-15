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
