from pprint import pprint
import asyncio
import sys
import json

from ecdsa import SigningKey
from bluzelle import bzapi
from bluzelle.lib.udp.udp_support import *
from bluzelle.db import DB
from bluzelle.log.default import DefaultConsoleLogger

class Bluzelle:

    def __init__(self, priv_key, address="127.0.0.1", port=50000, logger = DefaultConsoleLogger()):
        bzapi.set_logger(logger)
        self.localhost_ip = "127.0.0.1"
        self.ws_address = address
        self.ws_port = port
        self.priv_key = priv_key
        try:
            pem_priv_key = SigningKey.from_pem(priv_key)
            pem_pub_key = pem_priv_key.get_verifying_key().to_pem().decode("utf-8")
            self.pub_key = pem_pub_key.replace("-----BEGIN PUBLIC KEY-----\n","").replace("\n-----END PUBLIC KEY-----\n","")
        except Exception as e:
            logging.error(f'Error parsing private key {priv_key}. Error: {str(e)}')
            raise Exception(f'Error parsing private key {priv_key}')

        full_url = f"ws://{address}:{port}"

        self.init_happened = False
        if (not bzapi.initialize(self.pub_key, self.priv_key, full_url, "")):
            raise Exception('Could not run initialize the Bluzelle object')
        else:
            self.init_happened = True

        self.datagram_endpoint = None
        self.transport = None

    def __del__(self):
        if (self.init_happened):
            bzapi.terminate()

    def load_(self, *args, **kwargs):
        method_handle = getattr(bzapi, kwargs['meth'])
        resp = method_handle(*args[1:])
        return resp

    def create_db(self, *args, **kwargs):
        response = self.load_(self, *args, **kwargs, meth = sys._getframe().f_code.co_name)
        if response:
            return DB(response)
        else:
            raise Exception(bzapi.get_error_str())

    def has_db(self, *args, **kwargs):
        response =  self.load_(self, *args, **kwargs, meth = sys._getframe().f_code.co_name)
        if response != None:
            return response
        else:
            raise Exception(bzapi.get_error_str())

    def open_db(self, *args, **kwargs):
        response = self.load_(self, *args, **kwargs, meth = sys._getframe().f_code.co_name)
        if response:
            return DB(response)
        else:
            raise Exception(bzapi.get_error_str())