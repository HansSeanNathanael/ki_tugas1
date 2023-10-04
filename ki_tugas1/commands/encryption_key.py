import hashlib

def get_key(key : str, length : int):
    key128Byte = hashlib.sha256(key).digest()
    return key128Byte[length:]