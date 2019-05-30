from pprint import pprint
import asyncio
import sys
import json

from bluzelle import bzapi
from bluzelle.lib.udp.udp_support import *
from bluzelle.lib.udp.test_udp import *

class DB:

    def __init__(self, cpp_db):
        self.localhost_ip = "127.0.0.1"
        self.cpp_db = cpp_db

    def load_(self, *args, **kwargs):
        method_handle = getattr(self.cpp_db, kwargs['meth'])
        resp = method_handle(*args[1:])
        return resp

    def create(self, *args, **kwargs):
        results = json.loads(self.load_(self, *args, **kwargs, meth = sys._getframe().f_code.co_name))
        if 'result' in results:
            return results['result'] == 1
        elif 'error' in results:
            raise Exception(results['error'])
        else:
            raise Exception("Unknown error")

    def update(self, *args, **kwargs):
        response = self.load_(self, *args, **kwargs, meth = sys._getframe().f_code.co_name)
        results = json.loads(response)
        if 'result' in results:
            return results['result'] == 1
        elif 'error' in results:
            raise Exception(results['error'])
        else:
            raise Exception("Unknown error")

    def remove(self, *args, **kwargs):
        response = self.load_(self, *args, **kwargs, meth = sys._getframe().f_code.co_name)
        results = json.loads(response)
        if 'result' in results:
            return results['result'] == 1
        elif 'error' in results:
            raise Exception(results['error'])
        else:
            raise Exception("Unknown error")

    def has(self, *args, **kwargs):
        response = self.load_(self, *args, **kwargs, meth = sys._getframe().f_code.co_name)
        results = json.loads(response)
        if 'result' in results:
            return results['result'] == 1
        elif 'error' in results:
            raise Exception(results['error'])
        else:
            raise Exception("Unknown error")

    def read(self, *args, **kwargs):
        response = self.load_(self, *args, **kwargs, meth=sys._getframe().f_code.co_name)
        results = json.loads(response)
        if 'value' in results:
            return results['value']
        elif 'error' in results:
            raise Exception(results['error'])
        else:
            raise Exception("Unknown error")

    def quick_read(self, *args, **kwargs):
        response = self.load_(self, *args, **kwargs, meth = sys._getframe().f_code.co_name)
        results = json.loads(response)
        if 'value' in results:
            return results['value']
        elif 'error' in results:
            raise Exception(results['error'])
        else:
            raise Exception("Unknown error")

    def expire(self, *args, **kwargs):
        response = self.load_(self, *args, **kwargs, meth = sys._getframe().f_code.co_name)
        results = json.loads(response)
        if 'result' in results:
            return results['result'] == 1
        elif 'error' in results:
            raise Exception(results['error'])
        else:
            raise Exception("Unknown error")

    def persist(self, *args, **kwargs):
        response = self.load_(self, *args, **kwargs, meth = sys._getframe().f_code.co_name)
        results = json.loads(response)
        if 'result' in results:
            return results['result'] == 1
        elif 'error' in results:
            raise Exception(results['error'])
        else:
            raise Exception("Unknown error")

    def ttl(self, *args, **kwargs):
        response = self.load_(self, *args, **kwargs, meth = sys._getframe().f_code.co_name)
        results = json.loads(response)
        if 'error' in results:
            raise Exception(results['error'])
        elif 'ttl' in results:
            return results['ttl']
        else:
            raise Exception("Unknown error")

    def keys(self):
        response = self.load_(self, meth = sys._getframe().f_code.co_name)
        results = json.loads(response)
        if 'keys' in results:
            return results['keys']
        elif 'error' in results:
            raise Exception(results['error'])
        else:
            raise Exception("Unknown error")

    def size(self):
        response = self.load_(self, meth = sys._getframe().f_code.co_name)
        results = json.loads(response)
        if 'error' in results:
            raise Exception(results['error'])
        else:
            return results


    def swarm_status(self):
        response = self.cpp_db.swarm_status()
        return response