A Python 3.x client library for Bluzelle.
===================

# Cloning and pulling changes # 

Since we make use of Git submodules, to clone the repository, please run: 

`git clone --recurse-submodules https://github.com/bluzelle/bluzelle-py`

## OSX prerequisites ##

- Homebrew 

`ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)")` 

- The following dependencies 

`brew install python jsoncpp boost protobuf openssl curl cmake pkg-config swig`

## Linux (Ubuntu) prerequisites ##

- Python 3 with pip support and other dependencies

`sudo apt-get install python3-pip libpcre3 libpcre3-dev bison curl cmake protobuf-compiler libboost-all-dev libprotoc-dev libcurl4-openssl-dev pkg-config meson ninja-build`

- jsoncpp v1.8.4 compiled / built from source

```
curl https://codeload.github.com/open-source-parsers/jsoncpp/tar.gz/1.8.4 | tar xvz
cd jsoncp*
BUILD_TYPE=release
LIB_TYPE=shared
meson --buildtype ${BUILD_TYPE} --default-library ${LIB_TYPE} . build-${LIB_TYPE}
ninja -v -C build-${LIB_TYPE}
cd build-${LIB_TYPE}
sudo ninja install
```

- Swig 4.0 compiled / built from sources

```
git clone --branch rel-4.0.0 https://github.com/swig/swig
cd swig
./autogen.sh
./configure
make
sudo make install
```

Installing `jsoncpp` via `apt-get` using the `libjsoncpp-dev` and `libjsoncpp1` dependencies will be supported in the future.

## Install steps ##
During the pip install process, a C++ library would be built. 

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

blz = bluzelle.Bluzelle(priv_key, "127.0.0.1", 50000)

db = blz.create_db(my_uuid)
key = 'a'
try:
      res0 = db.read(key)
except Exception:
    print(f"{key} does not exist")
res1 = db.create("a", "b")
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

blz = bluzelle.Bluzelle(priv_key, "127.0.0.1", 50000)

async def interact():
      db = await blz.create_db(my_uuid)
      key = 'a'
      try:
          res0 = await db.read(key)
      except Exception:
          print(f"{key} does not exist")
      res1 = await db.create("a", "b")
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