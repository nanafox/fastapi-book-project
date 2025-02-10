from enum import Enum
from typing import OrderedDict

from pydantic import BaseModel, RootModel


class Genre(str, Enum):
    """Book genres."""

    SCI_FI = "Science Fiction"
    FANTASY = "Fantasy"
    HORROR = "Horror"
    MYSTERY = "Mystery"
    ROMANCE = "Romance"
    THRILLER = "Thriller"


class Book(BaseModel):
    """Book schema.

    Args:
        BaseModel (BaseModel): Pydantic base model.
    """

    id: int
    title: str
    author: str
    publication_year: int
    genre: Genre

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "The Hobbit",
                "author": "J.R.R. Tolkien",
                "publication_year": 1937,
                "genre": "Fantasy",
            }
        }
    }


class BooksResponse(RootModel[OrderedDict[int, Book]]):
    """This model defines the schema for how multiple books will look in a
    response.

    Args:
        RootModel (RootModel): Pydantic root model.
    """

    model_config = {
        "json_schema_extra": {
            "example": {
                "1": {
                    "id": 1,
                    "title": "The Hobbit",
                    "author": "J.R.R. Tolkien",
                    "publication_year": 1937,
                    "genre": "Fantasy",
                },
                "2": {
                    "id": 2,
                    "title": "The Lord of the Rings",
                    "author": "J.R.R. Tolkien",
                    "publication_year": 1954,
                    "genre": "Fantasy",
                },
                "3": {
                    "id": 3,
                    "title": "The Return of the King",
                    "author": "J.R.R. Tolkien",
                    "publication_year": 1955,
                    "genre": "Fantasy",
                },
            }
        }
    }


class BookNotFound(BaseModel):
    """Define the schema for books not found response."""

    detail: str = "Book not found"


class InMemoryDB:
    def __init__(self):
        self.books: OrderedDict[int, Book] = OrderedDict()

    def get_books(self) -> BooksResponse:
        """Gets books from database.

        Returns:
            BooksResponse: Ordered dictionary of books.
        """
        return BooksResponse(root=self.books)

    def add_book(self, book: Book) -> Book:
        """Adds book to database.

        Args:
            book (Book): Book to add.

        Returns:
            Book: Added book.
        """
        self.books.update({book.id: book})
        return book

    def get_book(self, book_id: int) -> Book | None:
        """Gets a specific book from database.

        Args:
            book_id (int): Book ID.

        Returns:
            Book: Book.
        """
        return self.books.get(book_id)

    def update_book(self, book_id: int, data: Book) -> Book | None:
        """Updates a specific book in database.

        Args:
            book_id (int): Book ID.
            data (Book): Book data.

        Returns:
            Book: Updated book.
        """
        self.books.update({book_id: data})
        return self.books.get(book_id)

    def delete_book(self, book_id: int) -> None:
        """Deletes a specific book from database.

        Args:
            book_id (int): Book ID.
        """
        if book_id in self.books:
            del self.books[book_id]
