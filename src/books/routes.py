from fastapi import APIRouter, HTTPException, Header, status
from typing import Optional, List
from src.books.schemas import Book, BookUpdate
from src.books.book_data import books

books_router = APIRouter()

@books_router.get("/headers")
async def get_headers(user_agent: str = Header(None), host: str = Header(None), origin: str = Header(None)) -> dict:
    return {"User-Agent": user_agent, "Host": host}

@books_router.get("/search") # test query parameters with this endpoint e.g. /search?limit=10&category=fiction
async def search_books(limit : int, category : str = "all") -> dict :
    return {"limit": limit, "category": category}

@books_router.get("/",response_model=List[Book])
async def get_books():
    return books

@books_router.get("/{book_id}", response_model=Book)
async def get_book(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@books_router.post("/", response_model=Book, status_code = status.HTTP_201_CREATED)
async def create_book(book_data: Book) -> Book:
    new_book = book_data.model_dump()  # Converting the Pydantic model to a dictionary
    books.append(new_book)
    return new_book

@books_router.patch("/{book_id}", response_model=Book)
async def update_book(book_id: int, book_update_data: BookUpdate) -> dict:
    for index, book in enumerate(books):  # track index directly
        if book["id"] == book_id:
            updated_book = book.copy()
            update_data = book_update_data.model_dump(exclude_unset=True)
            updated_book.update(update_data)
            books[index] = updated_book  # use index directly, no .index() call
            return updated_book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@books_router.delete("/{book_id}")
async def delete_book(book_id: int) -> dict:
    for book in books: 
        if book["id"] == book_id:
            books.remove(book)
            return {"detail": "Book deleted"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

