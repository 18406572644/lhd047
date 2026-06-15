from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List

from database import get_db
from models import ExplorationRoute, RoutePoint, User, SafetyHazard, Building
from schemas import (
    ExplorationRouteCreate, ExplorationRouteResponse,
    SafetyHazardBase, SafetyHazardResponse
)
from auth import get_current_user

router = APIRouter(tags=["探索路线与安全"])


@router.get("/api/routes", response_model=List[ExplorationRouteResponse])
async def get_routes(
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db)
):
    query = (
        select(ExplorationRoute)
        .where(ExplorationRoute.is_public == True)
        .options(
            selectinload(ExplorationRoute.user),
            selectinload(ExplorationRoute.points)
        )
        .order_by(ExplorationRoute.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/api/routes/{route_id}", response_model=ExplorationRouteResponse)
async def get_route(
    route_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ExplorationRoute)
        .where(ExplorationRoute.id == route_id)
        .options(
            selectinload(ExplorationRoute.user),
            selectinload(ExplorationRoute.points)
        )
    )
    route = result.scalar_one_or_none()
    if not route:
        raise HTTPException(status_code=404, detail="路线不存在")
    return route


@router.post("/api/routes", response_model=ExplorationRouteResponse)
async def create_route(
    route_data: ExplorationRouteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    route = ExplorationRoute(
        user_id=current_user.id,
        **route_data.model_dump(exclude={"points"})
    )
    db.add(route)
    await db.flush()

    for idx, point_data in enumerate(route_data.points):
        point = RoutePoint(
            route_id=route.id,
            order_index=idx,
            **point_data.model_dump(exclude={"order_index"})
        )
        db.add(point)

    await db.commit()

    result = await db.execute(
        select(ExplorationRoute)
        .where(ExplorationRoute.id == route.id)
        .options(
            selectinload(ExplorationRoute.user),
            selectinload(ExplorationRoute.points)
        )
    )
    route = result.scalar_one()
    return route


@router.delete("/api/routes/{route_id}")
async def delete_route(
    route_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(ExplorationRoute).where(ExplorationRoute.id == route_id)
    )
    route = result.scalar_one_or_none()
    if not route:
        raise HTTPException(status_code=404, detail="路线不存在")
    if route.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限删除")

    await db.delete(route)
    await db.commit()
    return {"message": "删除成功"}


@router.get("/api/buildings/{building_id}/hazards", response_model=List[SafetyHazardResponse])
async def get_building_hazards(
    building_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Building).where(Building.id == building_id))
    building = result.scalar_one_or_none()
    if not building:
        raise HTTPException(status_code=404, detail="建筑不存在")

    result = await db.execute(
        select(SafetyHazard).where(SafetyHazard.building_id == building_id)
    )
    return result.scalars().all()


@router.post("/api/buildings/{building_id}/hazards", response_model=SafetyHazardResponse)
async def add_hazard(
    building_id: int,
    hazard_data: SafetyHazardBase,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Building).where(Building.id == building_id))
    building = result.scalar_one_or_none()
    if not building:
        raise HTTPException(status_code=404, detail="建筑不存在")

    hazard = SafetyHazard(
        building_id=building_id,
        **hazard_data.model_dump()
    )
    db.add(hazard)
    await db.commit()
    await db.refresh(hazard)
    return hazard


@router.delete("/api/hazards/{hazard_id}")
async def delete_hazard(
    hazard_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(SafetyHazard).where(SafetyHazard.id == hazard_id))
    hazard = result.scalar_one_or_none()
    if not hazard:
        raise HTTPException(status_code=404, detail="隐患不存在")

    await db.delete(hazard)
    await db.commit()
    return {"message": "删除成功"}
