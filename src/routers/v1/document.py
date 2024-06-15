from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.routers.dependensies import get_db
from src.schemas.document import DocumentRead, DocumentCreate, DocumentUpdate
from src.db.models import Document
from src.scripts.utils import save_base64_to_file, convert_file_to_base64

router_document = APIRouter(prefix="/documents", tags=["Document"])


@router_document.post("/add-document", status_code=status.HTTP_204_NO_CONTENT)
async def create_document(document: DocumentCreate, db: AsyncSession = Depends(get_db)):
    try:
        if document.filename[-3:] == "pdf":
            document_dict = document.dict()
            document_dict["path_to_file"] = f"documents/{document_dict['filename']}"
            save_base64_to_file(document_dict["data"].split("base64,")[1], document_dict["path_to_file"])
            del document_dict["data"]
            db_document = Document(**document_dict)
            db.add(db_document)
            await db.commit()
            await db.refresh(db_document)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only pdf format is suppoerted")
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )


@router_document.get("/", response_model=list[DocumentRead])
async def read_documents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document))
    documents = result.scalars().all()
    for document in documents:
        try:
            data = convert_file_to_base64(document.path_to_file)
        except:
            data = None
        document.data = data
    return documents


@router_document.get("/{document_id}", response_model=DocumentRead)
async def read_document(document_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document).where(Document.id == document_id))
    document: Document = result.scalar_one_or_none()
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document не найден")
    else:
        try:
            data = convert_file_to_base64(document.path_to_file)
        except:
            data = None
        document.data = data
    return document


@router_document.put("/update-document", response_model=DocumentRead)
async def update_document(document: DocumentUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document).where(Document.id == document.id))
    db_document = result.scalar_one_or_none()
    if not db_document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document не найден")

    for key, value in document.dict().items():
        setattr(db_document, key, value)

    await db.commit()
    await db.refresh(db_document)
    return db_document


@router_document.delete("/delete-document/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(document_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Document).where(Document.id == document_id)
    )
    db_document = result.scalar_one_or_none()
    if not db_document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document не найден")

    await db.delete(db_document)
    await db.commit()
