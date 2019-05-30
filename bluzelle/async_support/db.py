from pprint import pprint
import asyncio
import sys
import json
from bluzelle import bzapi
from bluzelle.lib.udp.udp_support import *
from bluzelle.lib.udp.test_udp import *

class DB:

    def __init__(self, response):
        self.localhost_ip = "127.0.0.1"
        self.async_udp_port = get_next_free()
        self.response = response
        self.cpp_db = response.get_db()
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

    async def load_(self, *args, **kwargs):
        self.async_udp_port = self.async_udp_port
        if not self.datagram_endpoint:
            res = await open_local_endpoint(self.localhost_ip, self.async_udp_port)
            self.datagram_endpoint = res[2]
            self.transport = res[1]
        method_handle = getattr(self.cpp_db, kwargs['meth'])
        resp = method_handle(*args[1:])
        resp.set_signal_id(self.async_udp_port)
        data, address = await self.datagram_endpoint._endpoint.receive()
        return resp

    async def create(self, *args, **kwargs):
        response = await self.load_(self, *args, **kwargs, meth = sys._getframe().f_code.co_name)
        results = json.loads(response.get_result())
        if 'result' in results:
            return results['result'] == 1
        elif 'error' in results:
            raise Exception(results['error'])
        else:
            raise Exception("Unknown error")

    async def update(self, *args, **kwargs):
        response = await self.load_(self, *args, **kwargs, meth = sys._getframe().f_code.co_name)
        results = json.loads(response.get_result())
        if 'result' in results:
            return results['result'] == 1
        elif 'error' in results:
            raise Exception(results['error'])
        else:
            raise Exception("Unknown error")

    async def remove(self, *args, **kwargs):
        response = await self.load_(self, *args, **kwargs, meth = sys._getframe().f_code.co_name)
        results = json.loads(response.get_result())
        if 'result' in results:
            return results['result'] == 1
        elif 'error' in results:
            raise Exception(results['error'])
        else:
            raise Exception("Unknown error")

    async def has(self, *args, **kwargs):
        response = await self.load_(self, *args, **kwargs, meth = sys._getframe().f_code.co_name)
        results = json.loads(response.get_result())
        if 'result' in results:
            return results['result'] == 1
        elif 'error' in results:
            raise Exception(results['error'])
        else:
            raise Exception("Unknown error")

    async def read(self, *args, **kwargs):
        response = await self.load_(self, *args, **kwargs, meth = sys._getframe().f_code.co_name)
        results = json.loads(response.get_result())
        if 'value' in results:
            return results['value']
        elif 'error' in results:
            raise Exception(results['error'])
        else:
            raise Exception("Unknown error")

    async def quick_read(self, *args, **kwargs):
        response = await self.load_(self, *args, **kwargs, meth = sys._getframe().f_code.co_name)
        results = json.loads(response.get_result())
        if 'value' in results:
            return results['value']
        elif 'error' in results:
            raise Exception(results['error'])
        else:
            raise Exception("Unknown error")

    async def expire(self, *args, **kwargs):
        response = await self.load_(self, *args, **kwargs, meth = sys._getframe().f_code.co_name)
        results = json.loads(response.get_result())
        if 'result' in results:
            return results['result'] == 1
        elif 'error' in results:
            raise Exception(results['error'])
        else:
            raise Exception("Unknown error")

    async def persist(self, *args, **kwargs):
        response = await self.load_(self, *args, **kwargs, meth = sys._getframe().f_code.co_name)
        results = json.loads(response.get_result())
        if 'result' in results:
            return results['result'] == 1
        elif 'error' in results:
            raise Exception(results['error'])
        else:
            raise Exception("Unknown error")

    async def ttl(self, *args, **kwargs):
        response = await self.load_(self, *args, **kwargs, meth = sys._getframe().f_code.co_name)
        results = json.loads(response.get_result())
        if 'error' in results:
            raise Exception(results['error'])
        elif 'ttl' in results:
            return results['ttl']
        else:
            raise Exception("Unknown error")

    async def keys(self):
        response = await self.load_(self, meth = sys._getframe().f_code.co_name)
        results = json.loads(response.get_result())
        if 'keys' in results:
            return results['keys']
        elif 'error' in results:
            raise Exception(results['error'])
        else:
            raise Exception("Unknown error")

    async def size(self):
        response = await self.load_(self, meth = sys._getframe().f_code.co_name)
        results = json.loads(response.get_result())
        if 'error' in results:
            raise Exception(results['error'])
        else:
            return results


    async def swarm_status(self):
        response = self.cpp_db.swarm_status()
        return response