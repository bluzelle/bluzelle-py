from pprint import pprint
import asyncio
import sys
import json

from bluzelle import bzapi
from bluzelle.lib.udp.udp_support import *
from bluzelle.lib.udp.test_udp import *


class Database:
    def __init__(self, bzapi_db):
        self.bzapi_db = bzapi_db

    def create(self, key, value, expiry=0):
        """Creates a key/value pair in this database.

        Args:
            key (str): Name of the key to create.
            value (str): Value to set the key to.
            expiry (int): Lifetime of the key in seconds (0 = forever). Default
                forever.

        Returns:
            bool: True.

        Raises:
            Exception: When the database encounters an error during the
                operation. Message contains info regarding the failure.

        """
        response = self.bzapi_db.create(key, value, expiry)
        return self._handle_bool_or_raise(response)

    def update(self, *args, **kwargs):
        """Updates the value of a key in this database.

        Args:
            key (str): Name of the key to update.
            value (str): Value to set the key to.

        Returns:
            bool: True.

        Raises:
            Exception: When the database encounters an error during the
                operation. Message contains info regarding the failure.
            Exception: When the shim library responds with insufficient data.
            json.JSONDecodeError: If a malformed response is obtained from the
                shim library.

        """
        response = self.bzapi_db.update(key, value)
        return self._handle_bool_or_raise(response)

    def remove(self, key):
        """Remove a key and its value from this database.

        Args:
            key (str): Name of the key to remove.

        Returns:
            bool: True.

        Raises:
            Exception: When the database encounters an error during the
                operation. Message contains info regarding the failure.

        """
        response = self.bzapi_db.remove(key)
        return self._handle_bool_or_raise(response)

    def has(self, key):
        """Determine if a key exists in this database.

        Args:
            key (str): Name of the key to look for.

        Returns:
            bool: Whether or not the key exists.

        Raises:
            Exception: When the database encounters an error during the
                operation. Message contains info regarding the failure.

        """
        response = self.bzapi_db.has(key)
        return self._handle_bool_or_raise(response)

    def read(self, key):
        """Get the value of a key in this database.

        Args:
            key (str): Name of the key to read.

        Returns:
            str: The value of the key.

        Raises:
            Exception: When the database encounters an error during the
                operation. Message contains info regarding the failure.

        """
        response = self.bzapi_db.read(key)
        results = json.loads(response)
        if "value" in results:
            return results["value"]
        elif "error" in results:
            raise Exception(results["error"])
        else:
            raise Exception("Unknown error")

    def quick_read(self, key):
        """Get the value of a key in the database, skipping consensus checks.

        Args:
            key (str): Name of the key to read.

        Returns:
            str: The value of the key.

        Raises:
            Exception: When the database encounters an error during the
                operation. Message contains info regarding the failure.

        """
        response = self.bzapi_db.quick_read(key)
        results = json.loads(response)
        if "value" in results:
            return results["value"]
        elif "error" in results:
            raise Exception(results["error"])
        else:
            raise Exception("Unknown error")

    def expire(self, key, expiry):
        """Set the expiry time for a key/value pair in this database.

        Args:
            key (str): Name of the key to set expiry for.
            expiry (int): Lifetime of the key in seconds.

        Returns:
            bool: True.

        Raises:
            Exception: When the database encounters an error during the
                operation. Message contains info regarding the failure.

        """
        response = self.bzapi_db.expire(key, expiry)
        return self._handle_bool_or_raise(response)

    def persist(self, key):
        """Set a key/value in the database to be persistent (remove expiry).

        Args:
            key (str): Name of the key to persist.

        Returns:
            bool: True.

        Raises:
            Exception: When the database encounters an error during the
                operation. Message contains info regarding the failure.

        """
        response = self.bzapi_db.persist(key)
        return self._handle_bool_or_raise(response)

    def ttl(self, key):
        """Get the expiry time for a key/value pair in this database.

        Args:
            key (str): Name of the key to get the expiry of.

        Returns:
            int: Time to live for the key, in seconds.

        Raises:
            Exception: When the database encounters an error during the
                operation. Message contains info regarding the failure.

        """
        response = self.bzapi_db.ttl(key)
        results = json.loads(response)
        if "error" in results:
            raise Exception(results["error"])
        elif "ttl" in results:
            return results["ttl"]
        else:
            raise Exception("Unknown error")

    def keys(self):
        """Obtains a list of the keys in this database.

        Returns:
            List[int]: List of keys in the databse.

        Raises:
            Exception: When the database encounters an error during the
                operation. Message contains info regarding the failure.

        """
        response = self.bzapi_db.keys()
        results = json.loads(response)
        if "keys" in results:
            return results["keys"]
        elif "error" in results:
            raise Exception(results["error"])
        else:
            raise Exception("Unknown error")

    def size(self):
        """Obtains information about the utilization of this database.

        Returns:
            dict: Mapping of size values. Keys are:
                bytes - current size, in bytes, of this database.
                keys - number of keys in this database.
                remaining_bytes - space left in the allocation for this database.
                max_size - maximum allowed size for this database.

        Raises:
            Exception: When the database encounters an error during the
                operation. Message contains info regarding the failure.

        """
        response = self.bzapi_db.size()
        results = json.loads(response)
        if "error" in results:
            raise Exception(results["error"])
        else:
            return results

    def swarm_status(self):
        """Gets the current status of the database's swarm.

        Returns:
            str: Information on the current swarm status in which this database
                resides.

        Raises:
            Exception: When the database encounters an error during the
                operation. Message contains info regarding the failure.

        """
        response = self.bzapi_db.swarm_status()
        return response

    @staticmethod
    def _handle_bool_or_raise(json_response_str):
        json_res = json.loads(json_response_str)
        """Handle the common success/failure cases of DB operations.

        Returns:
            bool: True.

        Raises:
            Exception: When the database encounters an error during the
                operation. Message contains info regarding the failure.
        """
        if "result" in json_res:
            return json_res["result"] == 1
        elif "error" in json_res:
            raise Exception(json_res["error"])
        else:
            raise Exception("Unknown error")

    # TODO: Not for public interface yet
    def __writers(self) -> str:
        raise NotImplementedError

    # TODO: Not for public interface yet
    def __add_writer(self, writer: str) -> str:
        raise NotImplementedError

    # TODO: Not for public interface yet
    def __remove_writer(self, writer: str) -> str:
        raise NotImplementedError
