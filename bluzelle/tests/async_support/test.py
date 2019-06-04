import unittest
from pprint import pprint
import sys
import json
import os
import os.path
import time
sys.path.extend([os.getcwd()])
sys.path.extend([os.path.abspath(os.path.join(os.getcwd(), os.pardir))])
import asyncio
from socket import *
import uuid
#from bluzelle.lib.udp.udp_support import *
from bluzelle.async_support import bluzelle

class TestLibrary(unittest.TestCase):

    def setUp(self):

        self.priv_key = "-----BEGIN EC PRIVATE KEY-----\n" \
               "MHQCAQEEIBWDWE/MAwtXaFQp6d2Glm2Uj7ROBlDKFn5RwqQsDEbyoAcGBSuBBAAK\n" \
               "oUQDQgAEiykQ5A02u+02FR1nftxT5VuUdqLO6lvNoL5aAIyHvn8NS0wgXxbPfpuq\n" \
               "UPpytiopiS5D+t2cYzXJn19MQmnl/g==\n" \
               "-----END EC PRIVATE KEY-----"

        self.uuid = str(uuid.uuid4())
        self.bluzelle = bluzelle.Bluzelle(self.priv_key)
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None) # throw when clients do asyncio.get_event_loop()


    def tearDown(self):
        try:
            self.loop.stop()
        except:
            pass
        try:
            self.loop.close()
        except:
            pass

        del self.bluzelle # force .terminate to be called in c++


    def test_create_db(self):
        async def go():
            with self.assertRaises(Exception):
                await self.bluzelle.open_db(self.uuid)
            await self.bluzelle.create_db(self.uuid, 0, False)
            self.assertEqual(await self.bluzelle.has_db(self.uuid), True, "database was created successfully")
        self.loop.run_until_complete(go())

    def test_open_db(self):
        async def go():
            await self.bluzelle.create_db(self.uuid, 0, False)
            self.assertNotEqual(await self.bluzelle.open_db(self.uuid), None, "database was opened successfully")
        self.loop.run_until_complete(go())

    def test_has_db(self):
        async def go():
            res0 = await self.bluzelle.has_db(self.uuid)
            self.assertEqual(res0, False, "database does not have to exist")
            res1 = await self.bluzelle.create_db(self.uuid, 0, False)
            self.assertNotEqual(res1, None, "database was created and returned successfully")
            res2 = await self.bluzelle.has_db(self.uuid)
            self.assertEqual(res2, True, "database was read successfully")
        self.loop.run_until_complete(go())

    def test_db_create_read(self):
        async def go():
            db = await self.bluzelle.create_db(self.uuid, 0, False)
            with self.assertRaises(Exception):
                await db.read("a")
            res1 = await db.create("a", "b", 0)
            self.assertEqual(res1, True, "created a db value successfully")
            res2 = await db.read("a")
            self.assertEqual(res2, "b", "wrote and read a db value successfully")
        self.loop.run_until_complete(go())

    def test_db_has_remove(self):
        async def go():
            db = await self.bluzelle.create_db(self.uuid, 0, False)
            res1 = await db.has("a")
            self.assertEqual(res1, False, "first the key does not exist")
            res2 = await db.create("a", "b", 0)
            self.assertEqual(res2, True, "created a db value successfully")
            res3 = await db.has("a")
            self.assertEqual(res3, True, "after we create they key, it should exist")
            with self.assertRaises(Exception):
                await db.remove("zzz")
            res5 = await db.remove("a")
            self.assertEqual(res5, True, "we can remove existing records")
        self.loop.run_until_complete(go())

    def test_db_create_quick_read(self):
        async def go():
            db = await self.bluzelle.create_db(self.uuid, 0, False)
            with self.assertRaises(Exception):
                await db.quick_read("a")
            res1 = await db.create("a", "b", 0)
            self.assertEqual(res1, True, "created a db value successfully")
            res2 = await db.quick_read("a")
            self.assertEqual(res2, "b", "wrote and read a db value successfully")
        self.loop.run_until_complete(go())

    def test_db_create_update(self):
        async def go():
            db = await self.bluzelle.create_db(self.uuid, 0, False)
            res1 = await db.create("a", "b", 0)
            self.assertEqual(res1, True, "created a db value successfully")
            res2 = await db.update("a", "c")
            res3 = await db.read("a")
            self.assertEqual(res3['value'], "c", "updated a db value successfully")


    def test_db_keys(self):
        async def go():
            db = await self.bluzelle.create_db(self.uuid, 0, False)
            res0 = await db.keys()
            self.assertEqual(res0, None, "No keys yet...")
            res1 = await db.create("a", "1", 0)
            self.assertEqual(res1, True, "Record created")
            res2 = await db.keys()
            self.assertEqual(res2, ['a'], "One key should be present")
            res3 = await db.create("b", "2", 0)
            self.assertEqual(res3, True, "Record created")
            res4 = await db.keys()
            self.assertEqual(res4, ['a', 'b'], "two keys should be present")
            res5 = await db.remove("b")
            res6 = await db.keys()
            self.assertEqual(res6, ['a'], "One key should be present")
        self.loop.run_until_complete(go())

    def test_size(self):
        async def go():
            db = await self.bluzelle.create_db(self.uuid, 0, False)
            res1 = await db.size()
            self.assertEqual(res1['keys'], 0, "No keys should be present")
            # todo: check 'res1['remaining_bytes'] once c++ support is provided
            res2 = await db.create("a", "1", 0)
            self.assertEqual(res2, True, "Record created")
            res3 = await db.size()
            self.assertEqual(res3['keys'], 1, "One key should be present")
            # todo: check 'res3['remaining_bytes'] once c++ support is provided
        self.loop.run_until_complete(go())

    def test_ttl(self):
        async def go():
            db = await self.bluzelle.create_db(self.uuid, 0, False)
            res0 = await db.create("a", "1", 0)
            self.assertEqual(res0, True, "Record created")
            with self.assertRaises(Exception):
                await db.ttl("a")

            # todo: tests res1 once c++ support is provided
        self.loop.run_until_complete(go())

    def test_expire(self):
        async def go():
            db = await self.bluzelle.create_db(self.uuid, 0, False)
            res0 = await db.create("a", "1", 0)
            self.assertEqual(res0, True, "Record created")
            #res1 = await db.expire("a", 1)
            # todo: tests res1 once c++ support is provided
        self.loop.run_until_complete(go())

    def test_persist(self):
        async def go():
            db = await self.bluzelle.create_db(self.uuid, 0, False)
            res0 = await db.create("a", "1", 0)
            self.assertEqual(res0, True, "Record created")
            with self.assertRaises(Exception):
                await db.persist("a")
            # todo: tests res1 once c++ support is provided
        self.loop.run_until_complete(go())

    def test_swarm_status(self):
        async def go():
            db = await self.bluzelle.create_db(self.uuid, 0, False)
            status = await db.swarm_status()
            self.assertNotEqual(status, None, "status is not null")
        self.loop.run_until_complete(go())

if __name__ == '__main__':
    unittest.main()