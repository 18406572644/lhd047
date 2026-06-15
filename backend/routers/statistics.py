from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, extract
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime, timedelta
import io
import csv

from database import get_db
from models import Building, User, Photo, Comment, BuildingTag
from schemas import StatisticsResponse, BuildingListResponse, TimeSeriesPoint, GeoPoint

router = APIRouter(prefix="/api/statistics", tags=["统计"])


def get_date_range(days: Optional[int]):
    if days is None:
        return None, None
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


@router.get("", response_model=StatisticsResponse)
async def get_statistics(
    days: Optional[int] = Query(None, description="时间范围天数：7/30/None(全部)"),
    db: AsyncSession = Depends(get_db)
):
    start_date, end_date = get_date_range(days)

    date_filter_building = None
    date_filter_user = None
    date_filter_comment = None
    date_filter_photo = None

    if start_date and end_date:
        date_filter_building = and_(Building.created_at >= start_date, Building.created_at <= end_date)
        date_filter_user = and_(User.created_at >= start_date, User.created_at <= end_date)
        date_filter_comment = and_(Comment.created_at >= start_date, Comment.created_at <= end_date)
        date_filter_photo = and_(Photo.created_at >= start_date, Photo.created_at <= end_date)

    building_query = select(func.count(Building.id))
    user_query = select(func.count(User.id))
    comment_query = select(func.count(Comment.id))
    photo_query = select(func.count(Photo.id))

    if date_filter_building is not None:
        building_query = building_query.where(date_filter_building)
    if date_filter_user is not None:
        user_query = user_query.where(date_filter_user)
    if date_filter_comment is not None:
        comment_query = comment_query.where(date_filter_comment)
    if date_filter_photo is not None:
        photo_query = photo_query.where(date_filter_photo)

    total_buildings = await db.scalar(building_query)
    total_users = await db.scalar(user_query)
    total_comments = await db.scalar(comment_query)
    total_photos = await db.scalar(photo_query)

    type_query = select(Building.building_type, func.count(Building.id)).group_by(Building.building_type)
    if date_filter_building is not None:
        type_query = type_query.where(date_filter_building)
    type_result = await db.execute(type_query)
    buildings_by_type = {row[0]: row[1] for row in type_result.all()}

    danger_query = select(Building.danger_level, func.count(Building.id)).group_by(Building.danger_level)
    if date_filter_building is not None:
        danger_query = danger_query.where(date_filter_building)
    danger_result = await db.execute(danger_query)
    buildings_by_danger_level = {str(row[0]): row[1] for row in danger_result.all()}

    year_query = select(Building.construction_year, func.count(Building.id))\
        .where(Building.construction_year.isnot(None))\
        .group_by(Building.construction_year)\
        .order_by(Building.construction_year)
    if date_filter_building is not None:
        year_query = year_query.where(date_filter_building)
    year_result = await db.execute(year_query)
    buildings_by_year = {str(row[0]): row[1] for row in year_result.all()}

    geo_query = select(
        func.round(Building.latitude, 2).label("lat"),
        func.round(Building.longitude, 2).label("lng"),
        func.count(Building.id).label("count")
    ).group_by("lat", "lng")
    if date_filter_building is not None:
        geo_query = geo_query.where(date_filter_building)
    geo_result = await db.execute(geo_query)
    geo_distribution = [
        {"latitude": row[0], "longitude": row[1], "count": row[2]}
        for row in geo_result.all()
    ]

    top_query = select(Building)\
        .where(Building.status == "approved")\
        .options(selectinload(Building.tags), selectinload(Building.photos))\
        .order_by(Building.explore_count.desc())\
        .limit(10)
    if date_filter_building is not None:
        top_query = top_query.where(date_filter_building)
    top_result = await db.execute(top_query)
    top_explored = top_result.scalars().all()

    return {
        "total_buildings": total_buildings,
        "total_users": total_users,
        "total_comments": total_comments,
        "total_photos": total_photos,
        "buildings_by_type": buildings_by_type,
        "buildings_by_danger_level": buildings_by_danger_level,
        "buildings_by_year": buildings_by_year,
        "geo_distribution": geo_distribution,
        "top_explored": top_explored
    }


@router.get("/timeseries")
async def get_timeseries(
    days: Optional[int] = Query(None, description="时间范围天数：7/30/None(全部)"),
    db: AsyncSession = Depends(get_db)
):
    start_date, end_date = get_date_range(days)

    if start_date and end_date:
        start_dt = start_date
        end_dt = end_date
    else:
        min_building_date = await db.scalar(select(func.min(Building.created_at)))
        min_user_date = await db.scalar(select(func.min(User.created_at)))
        min_date = min(
            d for d in [min_building_date, min_user_date, datetime.utcnow() - timedelta(days=365)]
            if d is not None
        )
        start_dt = min_date
        end_dt = datetime.utcnow()

    building_query = select(
        extract('year', Building.created_at).label('year'),
        extract('month', Building.created_at).label('month'),
        func.count(Building.id).label('count')
    ).group_by('year', 'month').order_by('year', 'month')

    user_query = select(
        extract('year', User.created_at).label('year'),
        extract('month', User.created_at).label('month'),
        func.count(User.id).label('count')
    ).group_by('year', 'month').order_by('year', 'month')

    if start_date and end_date:
        building_query = building_query.where(
            and_(Building.created_at >= start_date, Building.created_at <= end_date)
        )
        user_query = user_query.where(
            and_(User.created_at >= start_date, User.created_at <= end_date)
        )

    building_result = await db.execute(building_query)
    user_result = await db.execute(user_query)

    def to_points(rows):
        points = []
        for row in rows:
            year, month, count = int(row[0]), int(row[1]), row[2]
            label = f"{year}-{month:02d}"
            points.append({"date": label, "count": count})
        return points

    return {
        "buildings": to_points(building_result.all()),
        "users": to_points(user_result.all())
    }


@router.get("/export/csv")
async def export_csv(
    days: Optional[int] = Query(None, description="时间范围天数：7/30/None(全部)"),
    db: AsyncSession = Depends(get_db)
):
    start_date, end_date = get_date_range(days)

    query = select(Building).options(
        selectinload(Building.tags),
        selectinload(Building.photos),
        selectinload(Building.owner)
    ).order_by(Building.created_at.desc())

    if start_date and end_date:
        query = query.where(
            and_(Building.created_at >= start_date, Building.created_at <= end_date)
        )

    result = await db.execute(query)
    buildings = result.scalars().all()

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow([
        'ID', '标题', '类型', '建造年份', '废弃年份', '地址',
        '纬度', '经度', '危险等级', '探索次数', '状态',
        '创建时间', '标签', '描述'
    ])

    for b in buildings:
        tags = ', '.join([t.tag for t in b.tags]) if b.tags else ''
        writer.writerow([
            b.id, b.title, b.building_type,
            b.construction_year if b.construction_year else '',
            b.abandonment_year if b.abandonment_year else '',
            b.address, b.latitude, b.longitude,
            b.danger_level, b.explore_count, b.status,
            b.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            tags, (b.description or '')[:200]
        ])

    buffer.seek(0)
    date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"buildings_export_{date_str}.csv"

    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv; charset=utf-8-sig",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
