from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_
from sqlalchemy.orm import selectinload
from typing import Optional, List

from database import get_db
from models import Building, User, BuildingTag, Photo, Video, SafetyHazard
from schemas import (
    BuildingCreate, BuildingUpdate, BuildingResponse, BuildingListResponse,
    BuildingListWithPagination, BuildingTagResponse
)
from auth import get_current_user
import math

router = APIRouter(prefix="/api/buildings", tags=["建筑档案"])


@router.get("", response_model=BuildingListWithPagination)
async def get_buildings(
    page: int = 1,
    page_size: int = 12,
    keyword: Optional[str] = None,
    building_type: Optional[str] = None,
    danger_level: Optional[int] = None,
    min_year: Optional[int] = None,
    max_year: Optional[int] = None,
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    radius_km: Optional[float] = None,
    sort_by: str = "created_at",
    order: str = "desc",
    db: AsyncSession = Depends(get_db)
):
    query = (
        select(Building)
        .where(Building.status == "approved")
        .options(
            selectinload(Building.tags),
            selectinload(Building.photos)
        )
    )

    if keyword:
        query = query.where(
            or_(
                Building.title.contains(keyword),
                Building.description.contains(keyword),
                Building.address.contains(keyword)
            )
        )
    if building_type:
        query = query.where(Building.building_type == building_type)
    if danger_level is not None:
        query = query.where(Building.danger_level == danger_level)
    if min_year:
        query = query.where(Building.construction_year >= min_year)
    if max_year:
        query = query.where(Building.construction_year <= max_year)

    if lat is not None and lng is not None and radius_km is not None:
        lat_range = radius_km / 111.0
        lng_range = radius_km / (111.0 * math.cos(math.radians(lat)))
        query = query.where(
            and_(
                Building.latitude.between(lat - lat_range, lat + lat_range),
                Building.longitude.between(lng - lng_range, lng + lng_range)
            )
        )

    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    sort_column = getattr(Building, sort_by, Building.created_at)
    if order == "desc":
        sort_column = sort_column.desc()
    query = query.order_by(sort_column)

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    buildings = result.scalars().all()

    return {
        "items": buildings,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/hot", response_model=List[BuildingListResponse])
async def get_hot_buildings(
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    query = (
        select(Building)
        .where(Building.status == "approved")
        .options(
            selectinload(Building.tags),
            selectinload(Building.photos)
        )
        .order_by(Building.explore_count.desc())
        .limit(limit)
    )
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{building_id}", response_model=BuildingResponse)
async def get_building(
    building_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Building)
        .where(Building.id == building_id)
        .options(
            selectinload(Building.tags),
            selectinload(Building.photos),
            selectinload(Building.videos),
            selectinload(Building.hazards),
            selectinload(Building.owner),
            selectinload(Building.comments)
        )
    )
    building = result.scalar_one_or_none()

    if not building:
        raise HTTPException(status_code=404, detail="建筑不存在")

    building.explore_count += 1
    await db.commit()
    await db.refresh(building)

    return building


@router.post("", response_model=BuildingResponse)
async def create_building(
    building_data: BuildingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    building = Building(
        **building_data.model_dump(exclude={"tags"}),
        owner_id=current_user.id,
        status="approved"
    )
    db.add(building)
    await db.flush()

    for tag_name in building_data.tags:
        tag = BuildingTag(building_id=building.id, tag=tag_name)
        db.add(tag)

    await db.commit()
    await db.refresh(building)
    return building


@router.put("/{building_id}", response_model=BuildingResponse)
async def update_building(
    building_id: int,
    building_data: BuildingUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Building).where(Building.id == building_id))
    building = result.scalar_one_or_none()

    if not building:
        raise HTTPException(status_code=404, detail="建筑不存在")

    if building.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限修改")

    update_data = building_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(building, key, value)

    await db.commit()
    await db.refresh(building)
    return building


@router.delete("/{building_id}")
async def delete_building(
    building_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Building).where(Building.id == building_id))
    building = result.scalar_one_or_none()

    if not building:
        raise HTTPException(status_code=404, detail="建筑不存在")

    if building.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限删除")

    await db.delete(building)
    await db.commit()
    return {"message": "删除成功"}


@router.get("/type/list")
async def get_building_types(db: AsyncSession = Depends(get_db)):
    types = ["工厂", "医院", "学校", "住宅", "商业", "军事", "宗教", "交通", "其他"]
    return {"types": types}
