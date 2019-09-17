from pprint import pprint
import asyncio
import sys
import json
import logging
import base64

from ecdsa import SigningKey
from bluzelle import bzapi
from bluzelle.lib.udp.udp_support import *
from bluzelle.db import DB
from bluzelle.log.default import DefaultLogger


class Client:
    def __init__(
        self,
        priv_key,
        swarm_id="0",
        address="127.0.0.1",
        port=50000,
        logger=DefaultLogger(),
    ):
        """Represents and initializes a primary connection to Bluzelle swarms.

        This instance can be used to create, connect to, and check for databses
        using synchronous operations. Please see
        :py:class:`bluzelle.async_support.bluzelle.Bluzelle` for a client using
        asynchronous operations.

        Args:
            priv_key (str): A private key in PEM format.
            swarm_id (str): Optional. Unknown.
            address (str): Optional. IP address of a swarm node to connect to.
            port (int): Optional. Port of a swarm node to connect to.
            logger (bzapi.logger): A Bluzelle logging object. See `bluzelle.log`
                for more info.

        Raises:
            Exception: When there is an issue parsing the private key.
            Exception: When there is an issue initializing the Bluzelle
                connection.

        """

        bzapi.set_logger(logger)
        self.localhost_ip = "127.0.0.1"
        self.ws_address = address
        self.ws_port = port
        self.priv_key = priv_key.replace(
            "-----BEGIN EC PRIVATE KEY-----\n", ""
        ).replace("\n-----END EC PRIVATE KEY-----\n", "")

        try:
            tmp_priv_key = SigningKey.from_der(base64.b64decode(self.priv_key))
            self.pub_key = base64.b64encode(
                tmp_priv_key.get_verifying_key().to_der()
            ).decode("utf-8")
        except Exception as e:
            logging.error(f"Error parsing private key {priv_key}. Error: {str(e)}")
            raise Exception(f"Error parsing private key {priv_key}")

        full_url = f"ws://{address}:{port}"

        self.init_happened = False
        if not bzapi.initialize(self.pub_key, self.priv_key, full_url, swarm_id):
            raise Exception("Could not run initialize the Bluzelle object")
        else:
            self.init_happened = True

        self.datagram_endpoint = None
        self.transport = None

    def __del__(self):
        if self.init_happened:
            bzapi.terminate()

    def create_db(self, uuid: str, max_size: int = 0, random_evict: bool = False):
        """Create a new database on the Bluzelle network with the given UUID.

        Args:
            uuid: Identity of the database to create.
            max_size: Optional. The maximum size of the database (0 for
                infinite). Default is infinite.
            random_evict: Whether or not to use the random eviction policy when
                the database is full.

        Returns:
            A database client, for interacting with the database.

        Raises:
            bluzelle.exceptions.AlreadyExists: When the database already exists
                and thus cannot be created.
            bluzelle.exceptions.InsufficientSpaceError: When there isn't enough
                room to accommodate the requested ``max_size``.
            bluzelle.exceptions.NetworkError: When creating the database fails.
                Message contains info regarding the failure.

        """

        response = bzapi.create_db(uuid, max_size, random_evict)
        if response:
            return DB(response)
        else:
            raise Exception(bzapi.get_error_str())

    def has_db(self, uuid: str) -> bool:
        """Determine if the given database exists within the Bluzelle network.

        Args:
            uuid: Identity of the database to check.

        Returns:
            True if databse exists, otherwise False.

        Raises:
            bluzelle.exceptions.NetworkError: When checking the database fails.
                Message contains info regarding the failure.

        """
        response = bzapi.has_db(uuid)
        if response != None:
            return response
        else:
            # TODO: Is it possible to hit this case?
            raise Exception(bzapi.get_error_str())

    def open_db(self, uuid: str):
        """Open an existing database from Bluzelle network with the given UUID.

        Args:
            uuid: Identity of the database to connect to.

        Returns:
            A database client for synchronous operations.

        Raises:
            bluzelle.exceptions.DatabaseNotFound: If the database does not exist.
            bluzelle.exceptions.NetworkError: If an error occurs while
                connecting to the database. Message contains info regarding the
                failure.

        """
        response = bzapi.open_db(uuid)
        if response:
            return DB(response)
        else:
            raise Exception(bzapi.get_error_str())
