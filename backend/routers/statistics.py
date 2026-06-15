from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import List

from database import get_db
from models import Building, User, Photo, Comment, BuildingTag
from schemas import StatisticsResponse, BuildingListResponse

router = APIRouter(prefix="/api/statistics", tags=["统计"])


@router.get("", response_model=StatisticsResponse)
async def get_statistics(db: AsyncSession = Depends(get_db)):
    total_buildings = await db.scalar(select(func.count(Building.id)))
    total_users = await db.scalar(select(func.count(User.id)))
    total_comments = await db.scalar(select(func.count(Comment.id)))
    total_photos = await db.scalar(select(func.count(Photo.id)))

    type_result = await db.execute(
        select(Building.building_type, func.count(Building.id))
        .group_by(Building.building_type)
    )
    buildings_by_type = {row[0]: row[1] for row in type_result.all()}

    danger_result = await db.execute(
        select(Building.danger_level, func.count(Building.id))
        .group_by(Building.danger_level)
    )
    buildings_by_danger_level = {str(row[0]): row[1] for row in danger_result.all()}

    top_result = await db.execute(
        select(Building)
        .where(Building.status == "approved")
        .options(
            selectinload(Building.tags),
            selectinload(Building.photos)
        )
        .order_by(Building.explore_count.desc())
        .limit(10)
    )
    top_explored = top_result.scalars().all()

    return {
        "total_buildings": total_buildings,
        "total_users": total_users,
        "total_comments": total_comments,
        "total_photos": total_photos,
        "buildings_by_type": buildings_by_type,
        "buildings_by_danger_level": buildings_by_danger_level,
        "top_explored": top_explored
    }
