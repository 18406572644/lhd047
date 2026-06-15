from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List

from database import get_db
from models import Comment, Building, User
from schemas import CommentCreate, CommentResponse
from auth import get_current_user

router = APIRouter(prefix="/api/comments", tags=["评论"])


@router.get("/building/{building_id}", response_model=List[CommentResponse])
async def get_building_comments(
    building_id: int,
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Building).where(Building.id == building_id))
    building = result.scalar_one_or_none()
    if not building:
        raise HTTPException(status_code=404, detail="建筑不存在")

    query = (
        select(Comment)
        .where(Comment.building_id == building_id, Comment.parent_id.is_(None))
        .options(
            selectinload(Comment.user),
            selectinload(Comment.replies)
        )
        .order_by(Comment.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(query)
    comments = result.scalars().all()
    return comments


@router.post("/building/{building_id}", response_model=CommentResponse)
async def create_comment(
    building_id: int,
    comment_data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Building).where(Building.id == building_id))
    building = result.scalar_one_or_none()
    if not building:
        raise HTTPException(status_code=404, detail="建筑不存在")

    if comment_data.parent_id:
        parent_result = await db.execute(
            select(Comment).where(Comment.id == comment_data.parent_id)
        )
        parent = parent_result.scalar_one_or_none()
        if not parent:
            raise HTTPException(status_code=404, detail="父评论不存在")

    comment = Comment(
        building_id=building_id,
        user_id=current_user.id,
        content=comment_data.content,
        rating=comment_data.rating,
        parent_id=comment_data.parent_id
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


@router.post("/{comment_id}/like")
async def like_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()

    if not comment:
        raise HTTPException(status_code=404, detail="评论不存在")

    comment.likes += 1
    await db.commit()
    return {"likes": comment.likes}


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()

    if not comment:
        raise HTTPException(status_code=404, detail="评论不存在")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限删除")

    await db.delete(comment)
    await db.commit()
    return {"message": "删除成功"}
