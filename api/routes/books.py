from typing import OrderedDict

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from api.db.schemas import Book, Genre, InMemoryDB

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


@router.get(
    "/", response_model=OrderedDict[int, Book], status_code=status.HTTP_200_OK
)
async def get_books() -> OrderedDict[int, Book]:
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


async def update_book(book_id: int, book: Book) -> Book:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=db.update_book(book_id, book).model_dump(),
    )


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int) -> None:
    db.delete_book(book_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
