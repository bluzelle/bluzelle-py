from enum import Enum
from enum import IntEnum

from bluzelle import exceptions


class BzApiErrorCodes(IntEnum):
    """Internal error mappings for the bzapi shim library."""

    success = 0
    uninitialized = 1
    connection_error = 2
    database_error = 3
    timeout_error = 4
    already_exists = 5
    no_space = 6
    no_database = 7


class BzApiErrorStrings(Enum):
    """External error mappings for the bzapi shim library."""

    success = "Success"
    uninitialized = "bzapi uninitialized"
    connection_error = "Connection error"
    database_error = "Database error"
    timeout_error = "Timeout error"
    already_exists = "Database already exists"
    no_space = "No space"
    no_database = "No database"
    unknown = "Unknown error"


error_str_to_exception_map = {
    "bzapi uninitialized": exceptions.UninitializedClientError,
    "Connection error": exceptions.ConnectionError,
    "Database error": exceptions.DatabaseError,
    "Timeout error": exceptions.TimeoutError,
    "Database already exists": exceptions.AlreadyExistsError,
    "No space": exceptions.InsufficientSpaceError,
    "No database": exceptions.DatabaseNotFound,
    "Unknown error": exceptions.DatabaseError,
}
