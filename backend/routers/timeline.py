from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from database import get_db
from models import TimelineEvent, Building, User
from schemas import TimelineEventCreate, TimelineEventUpdate, TimelineEventResponse
from auth import get_current_user

router = APIRouter(prefix="/api/timeline", tags=["时间轴"])


@router.get("/building/{building_id}", response_model=List[TimelineEventResponse])
async def get_timeline_events(
    building_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(TimelineEvent)
        .where(TimelineEvent.building_id == building_id)
        .where(TimelineEvent.status == "approved")
        .order_by(TimelineEvent.year)
    )
    return result.scalars().all()


@router.post("/building/{building_id}", response_model=TimelineEventResponse)
async def create_timeline_event(
    building_id: int,
    event_data: TimelineEventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Building).where(Building.id == building_id))
    building = result.scalar_one_or_none()
    if not building:
        raise HTTPException(status_code=404, detail="建筑不存在")

    event = TimelineEvent(
        building_id=building_id,
        year=event_data.year,
        title=event_data.title,
        description=event_data.description,
        image_url=event_data.image_url,
        source=event_data.source,
        status="approved",
        submitted_by=current_user.id
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event


@router.put("/{event_id}", response_model=TimelineEventResponse)
async def update_timeline_event(
    event_id: int,
    event_data: TimelineEventUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(TimelineEvent).where(TimelineEvent.id == event_id))
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="事件不存在")

    if event.submitted_by != current_user.id:
        raise HTTPException(status_code=403, detail="无权限修改")

    update_data = event_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(event, key, value)

    await db.commit()
    await db.refresh(event)
    return event


@router.delete("/{event_id}")
async def delete_timeline_event(
    event_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(TimelineEvent).where(TimelineEvent.id == event_id))
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="事件不存在")

    if event.submitted_by != current_user.id:
        raise HTTPException(status_code=403, detail="无权限删除")

    await db.delete(event)
    await db.commit()
    return {"message": "删除成功"}
