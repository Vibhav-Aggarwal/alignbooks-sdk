"""Custom exceptions for AlignBooks SDK."""


class AlignBooksError(Exception):
    """Base exception for AlignBooks SDK."""

    def __init__(self, message: str, return_code: int | None = None):
        self.message = message
        self.return_code = return_code
        super().__init__(message)


class AuthenticationError(AlignBooksError):
    """Raised when authentication fails."""
    pass


class SessionExpiredError(AlignBooksError):
    """Raised when the server session has expired."""
    pass


class APIError(AlignBooksError):
    """Raised when the API returns a non-zero ReturnCode."""

    def __init__(self, message: str, return_code: int, endpoint: str = ""):
        self.endpoint = endpoint
        super().__init__(f"[{endpoint}] RC {return_code}: {message}", return_code)


class NotFoundError(AlignBooksError):
    """Raised when a requested resource is not found."""
    pass


class ValidationError(AlignBooksError):
    """Raised for client-side validation errors."""
    pass
