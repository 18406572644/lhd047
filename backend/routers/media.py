from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
import os
import uuid
from pathlib import Path

from database import get_db
from models import Building, Photo, Video, User
from schemas import PhotoResponse, VideoResponse
from auth import get_current_user

router = APIRouter(prefix="/api/media", tags=["媒体文件"])

UPLOAD_DIR = Path("uploads")
PHOTO_DIR = UPLOAD_DIR / "photos"
VIDEO_DIR = UPLOAD_DIR / "videos"

PHOTO_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
ALLOWED_VIDEO_TYPES = {"video/mp4", "video/webm", "video/quicktime"}

MAX_PHOTO_SIZE = 10 * 1024 * 1024  # 10MB
MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100MB


@router.post("/photos", response_model=PhotoResponse)
async def upload_photo(
    building_id: int = Form(...),
    caption: str = Form(""),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Building).where(Building.id == building_id))
    building = result.scalar_one_or_none()
    if not building:
        raise HTTPException(status_code=404, detail="建筑不存在")

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="不支持的图片格式")

    file_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename or "photo.jpg")[1]
    filename = f"{file_id}{ext}"
    file_path = PHOTO_DIR / filename

    content = await file.read()
    if len(content) > MAX_PHOTO_SIZE:
        raise HTTPException(status_code=400, detail="图片大小不能超过10MB")

    with open(file_path, "wb") as f:
        f.write(content)

    photo = Photo(
        building_id=building_id,
        url=f"/uploads/photos/{filename}",
        caption=caption,
        uploaded_by=current_user.id
    )
    db.add(photo)
    await db.commit()
    await db.refresh(photo)

    return photo


@router.delete("/photos/{photo_id}")
async def delete_photo(
    photo_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Photo).where(Photo.id == photo_id))
    photo = result.scalar_one_or_none()

    if not photo:
        raise HTTPException(status_code=404, detail="照片不存在")

    if photo.uploaded_by != current_user.id:
        raise HTTPException(status_code=403, detail="无权限删除")

    file_path = photo.url.lstrip("/")
    if os.path.exists(file_path):
        os.remove(file_path)

    await db.delete(photo)
    await db.commit()
    return {"message": "删除成功"}


@router.post("/videos", response_model=VideoResponse)
async def upload_video(
    building_id: int = Form(...),
    title: str = Form(""),
    description: str = Form(""),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Building).where(Building.id == building_id))
    building = result.scalar_one_or_none()
    if not building:
        raise HTTPException(status_code=404, detail="建筑不存在")

    if file.content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(status_code=400, detail="不支持的视频格式")

    file_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename or "video.mp4")[1]
    filename = f"{file_id}{ext}"
    file_path = VIDEO_DIR / filename

    content = await file.read()
    if len(content) > MAX_VIDEO_SIZE:
        raise HTTPException(status_code=400, detail="视频大小不能超过100MB")

    with open(file_path, "wb") as f:
        f.write(content)

    video = Video(
        building_id=building_id,
        url=f"/uploads/videos/{filename}",
        title=title,
        description=description,
        uploaded_by=current_user.id
    )
    db.add(video)
    await db.commit()
    await db.refresh(video)

    return video


@router.delete("/videos/{video_id}")
async def delete_video(
    video_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Video).where(Video.id == video_id))
    video = result.scalar_one_or_none()

    if not video:
        raise HTTPException(status_code=404, detail="视频不存在")

    if video.uploaded_by != current_user.id:
        raise HTTPException(status_code=403, detail="无权限删除")

    file_path = video.url.lstrip("/")
    if os.path.exists(file_path):
        os.remove(file_path)

    await db.delete(video)
    await db.commit()
    return {"message": "删除成功"}
