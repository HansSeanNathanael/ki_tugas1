import hashlib

def get_key(key : bytes, length : int) -> bytes:
    key128Byte = hashlib.sha256(key).digest()
    return key128Byte[:length]