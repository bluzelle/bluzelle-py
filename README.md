A Python 3.x client library for Bluzelle.
===================

# Cloning and pulling changes # 

Since we make use of Git submodules, to clone the repository, please run: 

`git clone --recurse-submodules https://github.com/bluzelle/bluzelle-py`

## OSX prerequisites ##

- Homebrew 

`ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)")` 

- The following dependencies 

`brew install python jsoncpp protobuf openssl curl cmake pkg-config swig https://raw.githubusercontent.com/Homebrew/homebrew-core/44767c8ffdaf47b95b6d0af5b6917c454467dc56/Formula/boost.rb`

Note, that we are using the yet unreleased Boost 1.7 Homebrew dependency.  

## Linux (Ubuntu) prerequisites ## 

- Python 3 with pip support and other dependencies

`sudo apt-get install python3-pip libpcre3 libpcre3-dev curl cmake protobuf-compiler libprotoc-dev libcurl4-openssl-dev pkg-config swig libjsoncpp-dev libjsoncpp1`

- Latest Boost 1.70. Support for using `libboost-all-dev` will be provided soon.

## Install steps ##
During the pip install process, the [bzapi](https://github.com/bluzelle/bzapi/tree/devel/library) library would be built with cmake. 

`python3 -m pip install --index-url https://test.pypi.org/simple/ bluzelle --upgrade --force-reinstall --no-cache-dir`

## Example code (blocking) ##

The following tests assume that we have a local swarm running on `127.0.0.1:50000`.
You can alternatively test on our public testnet `testnet.bluzelle.com:51010`.

```
import uuid
from bluzelle import bluzelle

my_uuid = str(uuid.uuid4())

priv_key = "-----BEGIN EC PRIVATE KEY-----\n" \
      "MHQCAQEEIBWDWE/MAwtXaFQp6d2Glm2Uj7ROBlDKFn5RwqQsDEbyoAcGBSuBBAAK\n" \
      "oUQDQgAEiykQ5A02u+02FR1nftxT5VuUdqLO6lvNoL5aAIyHvn8NS0wgXxbPfpuq\n" \
      "UPpytiopiS5D+t2cYzXJn19MQmnl/g==\n" \
      "-----END EC PRIVATE KEY-----"

blz = bluzelle.Bluzelle(priv_key, swarm_id = "", address = "127.0.0.1", port = 50000)

db = blz.create_db(my_uuid, 0, False)
key = 'a'
try:
      res0 = db.read(key)
except Exception:
    print(f"{key} does not exist")
res1 = db.create("a", "b", 0)
print(res1) # True
res2 = db.read("a")
print(res2) # "b"


```

## Example code (async) ##
```
import asyncio
import uuid
from bluzelle.async_support import bluzelle

my_uuid = str(uuid.uuid4())

priv_key = "-----BEGIN EC PRIVATE KEY-----\n" \
      "MHQCAQEEIBWDWE/MAwtXaFQp6d2Glm2Uj7ROBlDKFn5RwqQsDEbyoAcGBSuBBAAK\n" \
      "oUQDQgAEiykQ5A02u+02FR1nftxT5VuUdqLO6lvNoL5aAIyHvn8NS0wgXxbPfpuq\n" \
      "UPpytiopiS5D+t2cYzXJn19MQmnl/g==\n" \
      "-----END EC PRIVATE KEY-----"

blz = bluzelle.Bluzelle(priv_key, swarm_id = "", address = "127.0.0.1", port = 50000)

async def interact():
      db = await blz.create_db(my_uuid, 0, False)
      key = 'a'
      try:
          res0 = await db.read(key)
      except Exception:
          print(f"{key} does not exist")
      res1 = await db.create("a", "b", 0)
      print(res1)  # True
      res2 = await db.read("a")
      print(res2)  # "b"



try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(interact())
finally:
    loop.close()
```

Please check out the integration tests for other code samples. 