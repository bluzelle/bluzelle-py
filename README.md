<a href="https://bluzelle.com/"><img src='https://raw.githubusercontent.com/bluzelle/api/master/source/images/Bluzelle%20-%20Logo%20-%20Big%20-%20Colour.png' alt="Bluzelle" style="width: 100%"/></a>

# bluzelle-py: Official Bluzelle Cache Client for Python 3.x

## Installation

After addressing dependencies below, installation is as usual for Python
packages.

```sh
pip install bluzelle
```

### Compilation Dependencies

During the pip install process, the [bzapi](https://github.com/bluzelle/bzapi)
shim library is compiled on your machine. Some compilation prerequisties are
found below.

In general the dependencies include `cmake`, `SWIG`, `protobuf`, and `openssl`.

#### Ubuntu Prerequisites

```sh
# Build tools
sudo apt-get install cmake pkg-config swig

# Shim library dependencies
sudo apt-get install protobuf-compiler libprotoc-dev libpcre3 libpcre3-dev
```

#### macOS Prerequisites

1. Install [Homebrew](https://brew.sh/)
2. Install build dependencies:

    `brew install cmake pkg-config swig protobuf openssl`

#### Windows

At this time, Windows is not currently supported. Please
[open an issue](https://github.com/bluzelle/bluzelle-py/issues) or
[submit a pull request](https://github.com/bluzelle/bluzelle-py/pulls) if you
require Windows support.

## Examples

### Synchronous (blocking) Operations

```python
import uuid
import bluzelle

my_uuid = str(uuid.uuid4())

priv_key = """-----BEGIN EC PRIVATE KEY-----
MHQCAQEEIBWDWE/MAwtXaFQp6d2Glm2Uj7ROBlDKFn5RwqQsDEbyoAcGBSuBBAAK
oUQDQgAEiykQ5A02u+02FR1nftxT5VuUdqLO6lvNoL5aAIyHvn8NS0wgXxbPfpuq
UPpytiopiS5D+t2cYzXJn19MQmnl/g==
-----END EC PRIVATE KEY-----"""

blz = bluzelle.Client(priv_key)

blz_cache = blz.create_db(my_uuid)
key = "some_key"
try:
    res0 = blz_cache.read(key)
except bluzelle.exceptions.ItemNotFound:
    print(f"{key} does not exist")

blz_cache.create(key, "some_value")
res = blz_cache.read(key)
print(res)  # "some_value"
```

### Asynchronous Operations

**Note: Not currently available, on roadmap as below.**

Asynchronous variants of most commands are available with the same `Client`
object.

```python
import asyncio
import uuid
import bluzelle

my_uuid = str(uuid.uuid4())

priv_key = """-----BEGIN EC PRIVATE KEY-----
MHQCAQEEIBWDWE/MAwtXaFQp6d2Glm2Uj7ROBlDKFn5RwqQsDEbyoAcGBSuBBAAK
oUQDQgAEiykQ5A02u+02FR1nftxT5VuUdqLO6lvNoL5aAIyHvn8NS0wgXxbPfpuq
UPpytiopiS5D+t2cYzXJn19MQmnl/g==
-----END EC PRIVATE KEY-----"""

blz = bluzelle.Client(priv_key)

async def interact():
    blz_cache = await blz.create_db_async(my_uuid)
    key = "some_key"
    try:
        res0 = await blz_cache.read_async(key)
    except bluzelle.exceptions.ItemNotFound:
        print(f"{key} does not exist")

    await blz_cache.create_async(key, "some_value")
    res = await blz_cache.read_async(key)
    print(res)  # "some_value"

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(interact())
finally:
    loop.close()
```

Please check out the integration tests for other code samples.
