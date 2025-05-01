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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type"
        )

    filename = f"{uuid4()}.{file_extension}"
    file_path = f"{COVER_DIR}/{filename}"

    try:
        with open(file_path, "wb") as f:
            content = await cover_image.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error saving file",
        )

    return file_path


def delete_cover_image(path: str):
    if path and os.path.exists(path):
        os.remove(path)


@router.post("/books", response_model=BookOut, status_code=201)
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
    admin=Depends(get_current_admin),
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
        cover_image=file_path,
    )
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book


@router.get("/books")
async def getallbooks(
    db: AsyncSession = Depends(get_db), admin=Depends(get_current_admin)
):
    data = await db.execute(select(Book))
    result = data.scalars().all()
    return result

@router.get("/books/{bookid}")
async def getaBook(bookid:int, db: AsyncSession = Depends(get_db), admin=Depends(get_current_admin)):
    
    book = await db.execute(select(Book).where(Book.id==bookid))
    
    result = book.scalar_one_or_none()
    
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book with this Id is not found")
    
    return result

@router.delete("/books/{bookid}")
async def deletebook(bookid:int, db: AsyncSession = Depends(get_db), admin=Depends(get_current_admin)):
    
    book = await db.execute(select(Book).where(Book.id==bookid))
    
    result = book.scalar_one_or_none()
    
    if not book :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book with this id not found")
    
    if book.cover_image:
        delete_cover_image(book.cover_image)
        
        
    await db.delete(result)
    await db.commit()
    return {"mesage":"data deleted "}


@router.put("books/{bookid}")
async def updateBook( 
    bookid:int,
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
    admin=Depends(get_current_admin),
    
):
    result = await db.execute(select(Book).where(Book.id==bookid))
    book = result.scalar_one_or_none()
    
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book with this id is not found")
    
    if cover_image :
        if book.cover_image:
            delete_cover_image(book.cover_image)
        book.cover_image = await save_cover_image(cover_image)

    book.title = title
    book.description = description
    book.price = price
    book.stock = stock
    book.pages = pages
    book.author = author
    book.genre = genre
    book.language = language

    await db.commit()
    await db.refresh(book)
    return book
    


