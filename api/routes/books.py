from typing import OrderedDict

from fastapi import APIRouter, status

from api.db.schemas import Book, BookNotFound, BooksResponse, Genre, InMemoryDB
from exceptions import BookNotFoundError

router = APIRouter()

db = InMemoryDB()
db.books = OrderedDict(
    {
        1: Book(
            id=1,
            title="The Hobbit",
            author="J.R.R. Tolkien",
            publication_year=1937,
            genre=Genre.SCI_FI,
        ),
        2: Book(
            id=2,
            title="The Lord of the Rings",
            author="J.R.R. Tolkien",
            publication_year=1954,
            genre=Genre.FANTASY,
        ),
        3: Book(
            id=3,
            title="The Return of the King",
            author="J.R.R. Tolkien",
            publication_year=1955,
            genre=Genre.FANTASY,
        ),
    }
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Book,
    operation_id="create_book",
)
async def create_book(book: Book) -> Book:
    return db.add_book(book)


@router.get(
    "/",
    response_model=BooksResponse,
    status_code=status.HTTP_200_OK,
    summary="List books",
    operation_id="list_books",
)
async def get_books() -> BooksResponse:
    """This endpoint returns all the books."""
    return db.get_books()


@router.get(
    "/{book_id}",
    summary="Fetch a book",
    responses={
        200: {"description": "Successful Response", "model": Book},
        404: {"description": "Book not found", "model": BookNotFound},
    },
    operation_id="get_book",
)
async def get_book(book_id: int) -> Book:
    """This endpoint retrieves a single book by ID.

    The book is returned successfully when found, otherwise an error 404
    is sent to the user to alert them of books unavailability.
    """
    if book := db.get_book(book_id):
        return book

    raise BookNotFoundError


@router.put(
    "/{book_id}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Successful Response", "model": Book},
        404: {"description": "Book not found", "model": BookNotFound},
    },
    operation_id="update_book",
)
async def update_book(book_id: int, book: Book) -> Book:
    """Update a book by ID."""
    if _ := db.get_book(book_id):
        db.update_book(book_id, book)
        return book

    raise BookNotFoundError


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Successful Response", "model": None},
        404: {"description": "Book not found", "model": BookNotFound},
    },
    operation_id="delete_book",
)
async def delete_book(book_id: int) -> None:
    """Delete a book by ID."""
    if _ := db.get_book(book_id):
        db.delete_book(book_id)
        return None

    raise BookNotFoundError
