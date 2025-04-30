from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import uuid4
import os

from app.db.db import get_db
from app.model.v1.bookmodel import Book
from app.schema.v1.bookschema import BookOut
from app.utilities.auth import get_current_admin

router = APIRouter(prefix="/api/v1/books", tags=["Books"])

COVER_DIR = "static/covers"


async def save_cover_image(cover_image: UploadFile) -> str:
    os.makedirs(COVER_DIR, exist_ok=True)
    allowed_extensions = ["jpg", "jpeg", "png"]
    file_extension = cover_image.filename.split(".")[-1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type")

    filename = f"{uuid4()}.{file_extension}"
    file_path = f"{COVER_DIR}/{filename}"

    try:
        with open(file_path, "wb") as f:
            content = await cover_image.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error saving file")

    return file_path

def delete_cover_image(path: str):
    if path and os.path.exists(path):
        os.remove(path)
        

@router.post("/", response_model=BookOut, status_code=201)
async def create_book(
    title: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    stock: int = Form(...),
    pages: int = Form(...),
    author: str = Form(...),
    genre: str = Form(...),
    language: str = Form(...),
    cover_image: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):
    file_path = await save_cover_image(cover_image) if cover_image else None

    new_book = Book(
        title=title,
        description=description,
        price=price,
        stock=stock,
        pages=pages,
        author=author,
        genre=genre,
        language=language,
        cover_image=file_path
    )
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book