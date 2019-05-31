from pprint import pprint
import asyncio
import sys
import json

from ecdsa import SigningKey
import logging
from bluzelle import bzapi
from bluzelle.lib.udp.udp_support import *
from bluzelle.lib.udp.test_udp import *
from bluzelle.async_support.db import DB
from bluzelle.log.default import DefaultConsoleLogger

class Bluzelle:

    def __init__(self, priv_key, address="127.0.0.1", port=50000, logger = DefaultConsoleLogger()):
        bzapi.set_logger(logger)
        self.localhost_ip = "127.0.0.1"
        self.async_udp_port = get_next_free()
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
        if (self.datagram_endpoint):
            try:
                self.datagram_endpoint._endpoint.close()
            except:
                pass
        if (self.transport):
            try:
                self.transport.abort()
            except:
                pass

            try:
                self.transport.close()
            except:
                pass

            try:
                self.transport._sock.close()
            except:
                pass

        if (self.init_happened):
            bzapi.terminate()

    async def load_(self, *args, **kwargs):
        if not self.datagram_endpoint:
            res = await open_local_endpoint(self.localhost_ip, self.async_udp_port)
            self.datagram_endpoint = res[2]
            self.transport = res[1]
        method_handle = getattr(bzapi, 'async_'+kwargs['meth'])
        resp = method_handle(*args[1:])
        resp.set_signal_id(self.async_udp_port)
        data, address = await self.datagram_endpoint._endpoint.receive()
        return resp


    async def create_db(self, *args, **kwargs):
        response = await self.load_(self, *args, **kwargs, meth = sys._getframe().f_code.co_name)
        results = json.loads(response.get_result())
        if 'error' in results:
            raise Exception(results['error'])
        else:
            return DB(response)


    async def has_db(self, *args, **kwargs):
        response = await self.load_(self, *args, **kwargs, meth = sys._getframe().f_code.co_name)
        results = json.loads(response.get_result())
        if 'error' in results:
            raise Exception(results['error'])
        else:
            return results['result'] == 1


    async def open_db(self, *args, **kwargs):
        response = await self.load_(self, *args, **kwargs, meth = sys._getframe().f_code.co_name)
        results = json.loads(response.get_result())
        if 'error' in results:
            raise Exception(results['error'])
        else:
            return DB(response)