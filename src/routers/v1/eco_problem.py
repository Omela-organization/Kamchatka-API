from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, Load
from starlette import status

from src.db.models import EcoProblem, Territory, Track, Photo, Document, User
from src.routers.dependensies import get_db
from src.schemas.eco_problem import EcoProblemCreate, EcoProblemUpdate, EcoProblemRead, EcoProblemReadWithOutJoin


router_eco_problem = APIRouter(prefix="/eco_problems", tags=["EcoProblem"])


@router_eco_problem.post("/add-eco-problem", response_model=EcoProblemReadWithOutJoin)
async def create_eco_problem(eco_problem: EcoProblemCreate, db: AsyncSession = Depends(get_db)):
    new_eco_problem = EcoProblem(**eco_problem.dict())
    db.add(new_eco_problem)
    await db.commit()
    await db.refresh(new_eco_problem)
    return new_eco_problem


@router_eco_problem.get("/{eco_problem_id}", response_model=EcoProblemRead)
async def get_eco_problem(eco_problem_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(EcoProblem).
        where(EcoProblem.id == eco_problem_id).
        options(joinedload(EcoProblem.creator).options(joinedload(User.role))).
        options(joinedload(EcoProblem.administrator).options(joinedload(User.role))).
        options(joinedload(EcoProblem.status)).
        options(joinedload(EcoProblem.type_incident)).
        options(joinedload(EcoProblem.territory).options(Load(Territory).load_only(Territory.id, Territory.name, Territory.description))).
        options(joinedload(EcoProblem.track).options(Load(Track).load_only(Track.id, Track.name, Track.type_track, Track.time_passing_track, Track.territory_id, Track.basic_recreational_capacity, Track.length))).
        options(joinedload(EcoProblem.photos).options(Load(Photo).load_only(Photo.id, Photo.eco_id))).
        options(joinedload(EcoProblem.documents).options(Load(Document).load_only(Document.id, Document.eco_id)))
    )
    eco_problem = result.scalars().first()
    if not eco_problem:
        raise HTTPException(status_code=404, detail="Eco problem not found")
    return eco_problem


@router_eco_problem.get("/", response_model=list[EcoProblemRead])
async def get_eco_problems(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(EcoProblem).
        options(joinedload(EcoProblem.creator).options(joinedload(User.role))).
        options(joinedload(EcoProblem.administrator).options(joinedload(User.role))).
        options(joinedload(EcoProblem.status)).
        options(joinedload(EcoProblem.type_incident)).
        options(joinedload(EcoProblem.territory).options(
            Load(Territory).load_only(Territory.id, Territory.name, Territory.description))).
        options(joinedload(EcoProblem.track).options(
            Load(Track).load_only(Track.id, Track.name, Track.type_track, Track.time_passing_track, Track.territory_id,
                                  Track.basic_recreational_capacity, Track.length))).
        options(joinedload(EcoProblem.photos).options(Load(Photo).load_only(Photo.id, Photo.eco_id))).
        options(joinedload(EcoProblem.documents).options(Load(Document).load_only(Document.id, Document.eco_id)))
    )
    eco_problems = result.unique().scalars().all()
    return eco_problems


@router_eco_problem.put("/update-eco-problem", response_model=EcoProblemReadWithOutJoin)
async def update_eco_problem(eco_problem: EcoProblemUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EcoProblem).where(EcoProblem.id == eco_problem.id))
    existing_eco_problem = result.scalars().first()
    if not existing_eco_problem:
        raise HTTPException(status_code=404, detail="Eco problem not found")

    for key, value in eco_problem.dict().items():
        setattr(existing_eco_problem, key, value)

    await db.commit()
    await db.refresh(existing_eco_problem)
    return existing_eco_problem


@router_eco_problem.delete("/delete-eco-problem/{eco_problem_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_eco_problem(eco_problem_id: int, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(EcoProblem).where(EcoProblem.id == eco_problem_id))
    eco_problem = result.scalars().first()
    if not eco_problem:
        raise HTTPException(status_code=404, detail="Eco problem not found")

    await session.delete(eco_problem)
    await session.commit()
