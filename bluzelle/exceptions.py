class Error(Exception):
    """Base class from which all Bluzelle Client exceptions are derived."""


class UninitializedClientError(Error):
    """Raised when operations are attempted before the client is initialized."""


class TimeoutError(Error):
    """Raised when any operation fails due to a timeout."""


class NetworkError(Error):
    """Base error class for issues when interacting with the Bluzelle Network."""


class ConnectionError(NetworkError):
    """Raised when connectivity issues occur for the Bluzelle Network."""


class DatabaseNotFound(NetworkError):
    """Raised when the requested database does not exist on the network."""


class AlreadyExistsError(NetworkError):
    """Raised when requesting to create a database that already exists."""


class DatabaseError(Error):
    """Base error class for Bluzelle Client errors involving operations on DBs."""


class InsufficientSpaceError(DatabaseError):
    """Raised when a creation or modification exceeds reserved space."""


class ItemNotFound(DatabaseError):
    """Raised when a key was not found in the database."""
