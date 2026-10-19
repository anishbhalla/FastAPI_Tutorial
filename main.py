from fastapi import FastAPI, HTTPException, Header, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


# Book schema using Pydantic
class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

# Book update schema using Pydantic
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    page_count: Optional[int] = None
    language: Optional[str] = None

#Performing dummy CRUD on a list of items.
books = [
    {
        "id": 1,
        "title": "Think Python",
        "author": "Allen B. Do  wney",
        "publisher": "O'Reilly Media",
        "published_date": "2015-12-01",
        "page_count": 292,
        "language": "English",
    },
    {
        "id": 2,
        "title": "Django 4 By Example",
        "author": "Antonio Melé",
        "publisher": "Packt Publishing Ltd",
        "published_date": "2022-08-29",
        "page_count": 764,
        "language": "English",
    },
    {
        "id": 3,
        "title": "Fluent Python",
        "author": "Luciano Ramalho",
        "publisher": "O'Reilly Media",
        "published_date": "2022-04-01",
        "page_count": 1012,
        "language": "English",
    },
    {
        "id": 4,
        "title": "Python Crash Course",
        "author": "Eric Matthes",
        "publisher": "No Starch Press",
        "published_date": "2023-01-10",
        "page_count": 552,
        "language": "English",
    },
    {
        "id": 5,
        "title": "Automate the Boring Stuff with Python",
        "author": "Al Sweigart",
        "publisher": "No Starch Press",
        "published_date": "2019-11-12",
        "page_count": 592,
        "language": "English",
    },
    {
        "id": 6,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "publisher": "Prentice Hall",
        "published_date": "2008-08-01",
        "page_count": 464,
        "language": "English",
    },
    {
        "id": 7,
        "title": "The Pragmatic Programmer",
        "author": "David Thomas, Andrew Hunt",
        "publisher": "Addison-Wesley Professional",
        "published_date": "2019-09-13",
        "page_count": 352,
        "language": "English",
    },
    {
        "id": 8,
        "title": "Designing Data-Intensive Applications",
        "author": "Martin Kleppmann",
        "publisher": "O'Reilly Media",
        "published_date": "2017-03-16",
        "page_count": 616,
        "language": "English",
    },
    {
        "id": 9,
        "title": "Eloquent JavaScript",
        "author": "Marijn Haverbeke",
        "publisher": "No Starch Press",
        "published_date": "2018-12-04",
        "page_count": 472,
        "language": "English",
    },
    {
        "id": 10,
        "title": "Learning React",
        "author": "Alex Banks, Eve Porcello",
        "publisher": "O'Reilly Media",
        "published_date": "2020-06-12",
        "page_count": 310,
        "language": "English",
    },
    {
        "id": 11,
        "title": "Building Data Science Applications with FastAPI",
        "author": "François Voron",
        "publisher": "Packt Publishing Ltd",
        "published_date": "2021-10-08",
        "page_count": 426,
        "language": "English",
    },
    {
        "id": 12,
        "title": "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow",
        "author": "Aurélien Géron",
        "publisher": "O'Reilly Media",
        "published_date": "2022-10-04",
        "page_count": 864,
        "language": "English",
    },
    {
        "id": 13,
        "title": "Introduction to Algorithms",
        "author": "Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein",
        "publisher": "MIT Press",
        "published_date": "2022-04-05",
        "page_count": 1312,
        "language": "English",
    },
    {
        "id": 14,
        "title": "Cracking the Coding Interview",
        "author": "Gayle Laakmann McDowell",
        "publisher": "CareerCup",
        "published_date": "2015-07-01",
        "page_count": 687,
        "language": "English",
    },
    {
        "id": 15,
        "title": "Python Tricks",
        "author": "Dan Bader",
        "publisher": "Dan Bader",
        "published_date": "2017-10-25",
        "page_count": 302,
        "language": "English",
    },
]

@app.get("/books",response_model=list[Book])
async def get_books():
    return books

@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.post("/books", response_model=Book, status_code = status.HTTP_201_CREATED)
async def create_book(book_data: Book) -> Book:
    new_book = book_data.model_dump()  # Converting the Pydantic model to a dictionary
    new_book["id"] = len(books) + 1
    books.append(new_book)
    return new_book

@app.patch("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, book_update_data: BookUpdate) -> dict:
    for book in books:
        if book["id"] == book_id:
            updated_book = book.copy()
            update_data = book_update_data.model_dump(exclude_unset=True)
            updated_book.update(update_data)
            books[books.index(book)] = updated_book
            return updated_book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.delete("/books/{book_id}")
async def delete_book(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {"detail": "Book deleted"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.get("/headers")
async def get_headers(user_agent: str = Header(None), host: str = Header(None), origin: str = Header(None)) -> dict:
    return {"User-Agent": user_agent, "Host": host}

@app.get("/books/search") # test query parameters with this endpoint e.g. /books/search?limit=10&category=fiction
async def search_books(limit : int, category : str = "all") -> dict :
    return {"limit": limit, "category": category}