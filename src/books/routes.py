from fastapi import APIRouter, status, Depends, HTTPException
from .schemas import Book, BookCreateModel, BookUpdateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import BookService
from uuid import UUID
from src.db.engine import get_session
from typing import List

book_router = APIRouter()
book_service = BookService()


@book_router.get("/", response_model=List[Book])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books


@book_router.get("/{book_id}")
async def get_book(book_id: UUID, session: AsyncSession = Depends(get_session)):
    book = await book_service.get_book(book_id, session)
    if book:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_a_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session)) -> dict:
    new_book = await book_service.create_book(book_data, session)

    return new_book


@book_router.patch("/{book_uid}", response_model=Book)
async def update_book(book_uid: UUID, book_update_data: BookUpdateModel,
                      session: AsyncSession = Depends(get_session)) -> dict:
    updated_book = await book_service.update_book(book_uid, book_update_data, session)

    if updated_book:
        return updated_book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: UUID, session: AsyncSession = Depends(get_session)):
    book_was_deleted = await book_service.delete_book(book_uid, session)

    if not book_was_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    else:
        return
