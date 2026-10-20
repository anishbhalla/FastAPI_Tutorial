from fastapi import FastAPI
from src.books.routes import books_router

version = "v1"

app = FastAPI(
    title="Book API",
    description="A simple API for managing books",
    version=version,
)

app.include_router(books_router, prefix="/api/{version}/books", tags=["Books"])