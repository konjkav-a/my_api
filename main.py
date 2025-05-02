from fastapi import FastAPI
from src.db.engine import init_db
from contextlib import asynccontextmanager
from src.books.routes import book_router

@asynccontextmanager
async def life_span(app: FastAPI):
    print("🚀 Server is starting...")
    await init_db()
    yield
    print(" Server has been stopped.")

version = "v1"

app = FastAPI(lifespan=life_span,title="BOOK",description="MY API",version= version)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])

