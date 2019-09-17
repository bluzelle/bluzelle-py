import uuid
import pytest
import bluzelle


@pytest.fixture
def blz_db():
    blz = bluzelle.Client(PRIVATE_KEY)
    db = blz.create_db(str(uuid.uuid4()))
    return db


def test_embedded_null_is_propogated(blz_db):
    """Verify that null bytes are communicated appropriately.

    Values can be any binary data, so the presence of 0x00 bytes should not
    interrupt any encoding.

    Keys as well can theoretically be any binary data, such as a binary hash.

    Thus, both keys and values should support null bytes.
    """
    binary_data = b"abc\x00xyz"
    blz_db.create("testkey", binary_data)
    assert blz_db.read("testkey") == binary_data
    assert blz_db.quick_read("testkey") == binary_data
