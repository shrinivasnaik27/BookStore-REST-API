
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional

# Initialize FastAPI
app = FastAPI(
    title="BookStore REST API",
    description="Book management system with Pydantic validation",
    version="1.0.0"
)


# Pydantic model
class Book(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    author: str = Field(min_length=2, max_length=100)
    price: float = Field(gt=0)
    category: str
    published_year: int = Field(gt=0)


# Temporary storage
books = {}
next_book_id = 1


# HOME: Welcome message
@app.get("/")
async def home():
    return {
        "message": "Welcome to BookStore REST API"
    }


# GET: Display all books with filters
@app.get("/books")
async def get_books(
    category: Optional[str] = None,
    author: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    result = list(books.values())

    if category:
        result = [
            book for book in result
            if book["category"].lower() == category.lower()
        ]

    if author:
        result = [
            book for book in result
            if author.lower() in book["author"].lower()
        ]

    if min_price is not None:
        result = [
            book for book in result
            if book["price"] >= min_price
        ]

    if max_price is not None:
        result = [
            book for book in result
            if book["price"] <= max_price
        ]

    return result


# GET: Display a particular book
@app.get("/books/{book_id}")
async def get_book(book_id: int):

    if book_id not in books:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return books[book_id]


# POST: Add a new book
@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    global next_book_id

    new_book = book.model_dump()
    new_book["id"] = next_book_id

    books[next_book_id] = new_book
    next_book_id += 1

    return new_book


# PUT: Update book details
@app.put("/books/{book_id}")
async def update_book(book_id: int, updated_book: Book):

    if book_id not in books:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    book_data = updated_book.model_dump()
    book_data["id"] = book_id

    books[book_id] = book_data

    return {
        "message": "Book updated successfully",
        "book": books[book_id]
    }


# DELETE: Delete a book
@app.delete("/books/{book_id}")
async def delete_book(book_id: int):

    if book_id not in books:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    deleted_book = books.pop(book_id)

    return {
        "message": "Book deleted successfully",
        "book": deleted_book
    }
