import unittest
from pprint import pprint
import sys
import json
import os
import os.path
import time
import asyncio
from socket import *
import bluzelle
import uuid
from bluzelle import bzapi

class TestLibrary(unittest.TestCase):

    def setUp(self):

        self.priv_key = "-----BEGIN EC PRIVATE KEY-----\n" \
               "MHQCAQEEIBWDWE/MAwtXaFQp6d2Glm2Uj7ROBlDKFn5RwqQsDEbyoAcGBSuBBAAK\n" \
               "oUQDQgAEiykQ5A02u+02FR1nftxT5VuUdqLO6lvNoL5aAIyHvn8NS0wgXxbPfpuq\n" \
               "UPpytiopiS5D+t2cYzXJn19MQmnl/g==\n" \
               "-----END EC PRIVATE KEY-----"

        self.uuid = str(uuid.uuid4())
        self.bluzelle = bluzelle.Bluzelle(self.priv_key)


    def tearDown(self):
        del self.bluzelle # force .terminate to be called in c++
    #
    # def test_create_db(self):
    #     self.bluzelle.create_db(self.uuid)
    #     self.assertEqual(self.bluzelle.has_db(self.uuid), True, "database was created successfully")
    #
    # def test_open_db(self):
    #     self.assertRaises(Exception, self.bluzelle.open_db,self.uuid)
    #     self.bluzelle.create_db(self.uuid)
    #     self.assertNotEqual(self.bluzelle.open_db(self.uuid), None, "database was opened successfully")
    #
    # def test_has_db(self):
    #     res0 = self.bluzelle.has_db(self.uuid)
    #     self.assertEqual(res0, False, "database does not have to exist")
    #     res1 = self.bluzelle.create_db(self.uuid)
    #     self.assertNotEqual(res1, None, "database was created and returned successfully")
    #     res2 = self.bluzelle.has_db(self.uuid)
    #     self.assertEqual(res2, True, "database was read successfully")

    # def test_db_create_read(self):
    #     db = self.bluzelle.create_db(self.uuid)
    #     self.assertRaises(Exception, db.read, "non_existing")
    #     res1 = db.create("a", "b")
    #     self.assertEqual(res1, True, "created a db value successfully")
    #     res2 = db.read("a")
    #     self.assertEqual(res2, "b", "wrote and read a db value successfully")


    def test_db_has_remove(self):
        db = self.bluzelle.create_db(self.uuid)
        res1 = db.has("a")
        self.assertEqual(res1, False, "first the key does not exist")
        #res2 = db.create("a", "b")
        # self.assertEqual(res2, True, "created a db value successfully")
        # res3 = db.has("a")
        # self.assertEqual(res3, True, "after we create they key, it should exist")
        # self.assertRaises(Exception, db.remove, "zzz")
        # res5 = db.remove("a")
        # self.assertEqual(res5, True, "we can remove existing records")
    #
    #
    # def test_db_create_quick_read(self):
    #     db = self.bluzelle.create_db(self.uuid)
    #     self.assertRaises(Exception, db.quick_read,"non_existing")
    #     res1 = db.create("a", "b")
    #     self.assertEqual(res1, True, "created a db value successfully")
    #     res2 = db.quick_read("a")
    #     self.assertEqual(res2, "b", "wrote and read a db value successfully")
    #
    #
    # def test_db_create_update(self):
    #     db = self.bluzelle.create_db(self.uuid)
    #     res1 = db.create("a", "b")
    #     self.assertEqual(res1, True, "created a db value successfully")
    #     res2 = db.update("a", "c")
    #     res3 = db.read("a")
    #     self.assertEqual(res3, "c", "updated a db value successfully")
    #
    #
    # def test_db_keys(self):
    #     db = self.bluzelle.create_db(self.uuid)
    #     res0 = db.keys()
    #     self.assertEqual(res0, None, "No keys yet...")
    #     res1 = db.create("a", "1")
    #     self.assertEqual(res1, True, "Record created")
    #     res2 = db.keys()
    #     self.assertEqual(res2, ['a'], "One key should be present")
    #     res3 = db.create("b", "2")
    #     self.assertEqual(res3, True, "Record created")
    #     res4 = db.keys()
    #     self.assertEqual(res4, ['a', 'b'], "two keys should be present")
    #     res5 = db.remove("b")
    #     res6 = db.keys()
    #     self.assertEqual(res6, ['a'], "One key should be present")
    #
    #
    # def test_size(self):
    #     db = self.bluzelle.create_db(self.uuid)
    #     res1 = db.size()
    #     self.assertEqual(res1['keys'], 0, "No keys should be present")
    #     # todo: check 'res1['remaining_bytes'] once c++ support is provided
    #     res2 = db.create("a", "1")
    #     self.assertEqual(res2, True, "Record created")
    #     res3 = db.size()
    #     self.assertEqual(res3['keys'], 1, "One key should be present")
    #     # todo: check 'res3['remaining_bytes'] once c++ support is provided
    #
    #
    # def test_ttl(self):
    #     db = self.bluzelle.create_db(self.uuid)
    #     res0 = db.create("a", "1")
    #     self.assertEqual(res0, True, "Record created")
    #     self.assertRaises(Exception, db.ttl, "a")
    #     pass
    #     # todo: tests res1 once c++ support is provided
    #
    #
    # def test_expire(self):
    #     db = self.bluzelle.create_db(self.uuid)
    #     res0 = db.create("a", "1")
    #     self.assertEqual(res0, True, "Record created")
    #     res1 = db.expire("a", 1)
    #     #res2 = db.ttl("a")
    #     pass
    #     # todo: tests res1 once c++ support is provided
    #
    #
    # def test_persist(self):
    #     db = self.bluzelle.create_db(self.uuid)
    #     res0 = db.create("a", "1")
    #     self.assertEqual(res0, True, "Record created")
    #     self.assertRaises(Exception, db.persist, "a")
    #     pass
    #     # todo: tests res1 once c++ support is provided
    #
    #
    # def test_swarm_status(self):
    #     db = self.bluzelle.create_db(self.uuid)
    #     status = db.swarm_status()
    #     self.assertNotEqual(status, None, "status is not null")


if __name__ == '__main__':
    unittest.main()