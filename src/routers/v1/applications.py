import json

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette import status

from src.db.models import Application, User
from src.routers.dependensies import get_db
from src.schemas.application import ApplicationRead, ApplicationCreate, ApplicationUpdate, ApplicationReadWithOutJoin


router_application = APIRouter(prefix="/applications", tags=["Application"])


@router_application.post("/add-application", response_model=ApplicationReadWithOutJoin)
async def create_application(application: ApplicationCreate, db: AsyncSession = Depends(get_db)):
    new_application = Application(**application.dict())
    db.add(new_application)
    await db.commit()
    await db.refresh(new_application)
    return new_application


@router_application.get("/{application_id}", response_model=ApplicationRead)
async def get_application(application_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Application).
        where(Application.id == application_id).
        options(joinedload(Application.creator).options(joinedload(User.role))).
        options(joinedload(Application.administrator).options(joinedload(User.role)))
    )
    application = result.scalars().first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router_application.get("/", response_model=list[ApplicationRead])
async def get_applications(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Application).
        options(joinedload(Application.creator).options(joinedload(User.role))).
        options(joinedload(Application.administrator).options(joinedload(User.role)))
    )
    applications = result.scalars().all()
    return applications


@router_application.put("/update-application", response_model=ApplicationReadWithOutJoin)
async def update_application(application: ApplicationUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Application).where(Application.id == application.id))
    existing_application = result.scalars().first()
    if not existing_application:
        raise HTTPException(status_code=404, detail="Application not found")

    for key, value in application.dict().items():
        setattr(existing_application, key, value)

    await db.commit()
    await db.refresh(existing_application)
    return existing_application


@router_application.delete("/delete-application/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(application_id: int, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Application).where(Application.id == application_id))
    application = result.scalars().first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    await session.delete(application)
    await session.commit()
