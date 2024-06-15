import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.routers.dependensies import get_db
from src.schemas.photo import PhotoRead, PhotoCreate, PhotoUpdate
from src.db.models import Photo
from src.scripts.utils import save_base64_to_file, convert_file_to_base64

router_photo = APIRouter(prefix="/photos", tags=["Photo"])


@router_photo.post("/add-photo", status_code=status.HTTP_204_NO_CONTENT)
async def create_photo(photo: PhotoCreate, db: AsyncSession = Depends(get_db)):
    try:
        photo_dict = photo.dict()
        photo_dict["filename"] = f"{uuid.uuid4()}.png"
        photo_dict["path_to_photo"] = f"photos/{photo_dict['filename']}"
        save_base64_to_file(photo_dict["data"].split("base64,")[1], photo_dict["path_to_photo"])
        del photo_dict["data"]
        db_photo = Photo(**photo_dict)
        db.add(db_photo)
        await db.commit()
        await db.refresh(db_photo)
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )


@router_photo.get("/", response_model=list[PhotoRead])
async def read_photos(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Photo))
    photos = result.scalars().all()
    for photo in photos:
        try:
            data = convert_file_to_base64(photo.path_to_photo)
        except:
            data = None
        photo.data = data
    return photos


@router_photo.get("/{photo_id}", response_model=PhotoRead)
async def read_photo(photo_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Photo).where(Photo.id == photo_id))
    photo: Photo = result.scalar_one_or_none()
    if not photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo не найден")
    else:
        try:
            data = convert_file_to_base64(photo.path_to_photo)
        except:
            data = None
        photo.data = data
    return photo


@router_photo.put("/update-photo", response_model=PhotoRead)
async def update_photo(photo: PhotoUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Photo).where(Photo.id == photo.id))
    db_photo = result.scalar_one_or_none()
    if not db_photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo не найден")

    for key, value in photo.dict().items():
        setattr(db_photo, key, value)

    await db.commit()
    await db.refresh(db_photo)
    return db_photo


@router_photo.delete("/delete-photo/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_photo(photo_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Photo).where(Photo.id == photo_id)
    )
    db_photo = result.scalar_one_or_none()
    if not db_photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo не найден")

    await db.delete(db_photo)
    await db.commit()
