from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.routers.dependensies import get_db
from src.schemas.feedback import FeedBackRead, FeedBackCreate, FeedBackUpdate
from src.db.models import Feedback

router_feedback = APIRouter(prefix="/feedbacks", tags=["FeedBack"])


@router_feedback.post("/add-feedback", response_model=FeedBackRead)
async def create_feedback(feedback: FeedBackCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_feedback = Feedback(**feedback.dict())
        db.add(db_feedback)
        await db.commit()
        await db.refresh(db_feedback)
        return db_feedback
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка в параметрах при создании отзыва"
        )


@router_feedback.get("/", response_model=list[FeedBackRead])
async def read_feedbacks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Feedback))
    feedbacks = result.scalars().all()
    return feedbacks


@router_feedback.get("/{feedback_id}", response_model=FeedBackRead)
async def read_feedback_by_id(feedback_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Feedback).where(Feedback.id == feedback_id))
    feedback = result.scalar_one_or_none()
    if not feedback:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="отзыв не найден")
    return feedback


@router_feedback.get("/by-territory/{territory_id}", response_model=list[FeedBackRead])
async def read_feedbacks_by_territory(territory_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Feedback).
        where(Feedback.territory_id == territory_id)
    )
    feedbacks = result.scalars().all()
    if not feedbacks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Отзывы не найдены")
    return feedbacks


@router_feedback.get("/by-track/{track_id}", response_model=list[FeedBackRead])
async def read_feedbacks_by_track(track_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Feedback).
        where(Feedback.track_id == track_id)
    )
    feedbacks = result.scalars().all()
    if not feedbacks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Отзывы не найдены")
    return feedbacks


@router_feedback.put("/update-feedback", response_model=FeedBackRead)
async def update_feedback(feedback: FeedBackUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Feedback).where(Feedback.id == feedback.id))
    db_feedback = result.scalar_one_or_none()
    if not db_feedback:
        raise HTTPException(status_code=404, detail="Отзыв не найдена")

    for key, value in feedback.dict().items():
        setattr(db_feedback, key, value)

    await db.commit()
    await db.refresh(db_feedback)
    return db_feedback


@router_feedback.delete("/delete-feedback/{feedback_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_feedback(feedback_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Feedback).where(Feedback.id == feedback_id)
    )
    db_feedback = result.scalar_one_or_none()
    if not db_feedback:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Отзыв не найден")
    await db.delete(db_feedback)
    await db.commit()
