from fastapi import HTTPException, status


class BookNotFoundError(HTTPException):
    """Raises an HTTPException for error 404 when a book is not found."""

    def __init__(self):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = "Book not found"
