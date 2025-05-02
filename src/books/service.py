import uuid
from datetime import datetime
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, BookUpdateModel
from sqlmodel import desc, select
from .models import Book

class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)

        return result.all()

    async def get_book(self, book_uid: UUID , session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement) # type: ignore
        return result.first()
        # return book if book is not None else None

    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        # book_data_dict = book_data.model_dump()
        # new_book = Book(**book_data_dict)
        published_date = datetime.strptime(book_data.published_date, "%Y-%m-%d").date()
        new_book = Book(
            uid=uuid.uuid4(),
            title=book_data.title,
            author=book_data.author,
            publisher=book_data.publisher,
            published_date=published_date,
            language=book_data.language,
            created_at=datetime.now(),
            update_at=datetime.now()
        )
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book

    async def update_book(self, book_uid: UUID, update_data: BookUpdateModel, session: AsyncSession):
        book_to_update = await self.get_book(book_uid, session)

        if book_to_update is not None:
            update_data_dict = update_data.model_dump(exclude_unset=True)

            for k, v in update_data_dict.items():
                setattr(book_to_update, k, v)

            await session.commit()
            await session.refresh(book_to_update)

            return book_to_update

        return None

    async def delete_book(self, book_uid: UUID, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)

        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()
            return True
        else:
            return False