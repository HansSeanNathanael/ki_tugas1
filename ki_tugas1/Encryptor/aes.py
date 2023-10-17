import io
import sys
import collections
from Crypto.Cipher import AES as AESCIPHER, DES as DESCIPHER, ARC4
from Crypto.Util import Counter

from ki_tugas1.commands.encryption_key import get_key
    
    
class EncryptBlock:
    def __init__(self, data : bytes, block_size : int|None):
        self.data = data
        
        if block_size is None:
            self.padding = None
            self.block_size = None
        else:
            self.block_size = block_size
            self.padding = self.block_size - (len(self.data) % self.block_size)
            self.data += bytes([ord('0')] * (self.padding))
            self.data += self.padding.to_bytes(self.block_size, byteorder=sys.byteorder, signed=False)
        
    def read(self) -> bytes:
        return self.data
    
class DecryptBlock:
    def __init__(self, data : bytes, block_size : int|None):
        self.data = data
        self.block_size = block_size
        
    def read(self) -> bytes:
        return self.data
    
    def get_block_size(self) -> int|None:
        return self.block_size
            
class AES:
    def __init__(self, key : bytes, type):
        self.encryptor = None
        self.type = type
        self.decrypt_queue = None
        
        if type == AESCIPHER.MODE_CBC:
            self.encryptor = AESCIPHER.new(key, AESCIPHER.MODE_CBC, get_key(key, 16))
        elif type == AESCIPHER.MODE_CFB:
            self.encryptor = AESCIPHER.new(key, AESCIPHER.MODE_CFB, iv=get_key(key, 16), segment_size=64)
        elif type == AESCIPHER.MODE_OFB:
            self.encryptor = AESCIPHER.new(key, AESCIPHER.MODE_OFB, get_key(key, 16))
        elif type == AESCIPHER.MODE_CTR:
            self.encryptor = AESCIPHER.new(key, AESCIPHER.MODE_CTR, counter=Counter.new(128))
    
    def encrypt(self, block_data : EncryptBlock) -> bytes:
        return self.encryptor.encrypt(block_data.read())
    
    def decrypt(self, block_data : DecryptBlock) -> bytes|None:
        data = self.encryptor.decrypt(block_data.read())
        if block_data.get_block_size() is None:
            return data
        
        block_size = block_data.get_block_size()
        block_store_size = data[-block_size:]
        padding = int.from_bytes(bytes=block_store_size, byteorder=sys.byteorder, signed=False)
        
        return data[:-(block_size+padding)]
    
class DES:
    def __init__(self, key : bytes, type):
        self.encryptor = None
        self.type = type
        self.decrypt_queue = None
        
        if type == DESCIPHER.MODE_CBC:
            self.encryptor = DESCIPHER.new(key, DESCIPHER.MODE_CBC, get_key(key, 8))
        elif type == DESCIPHER.MODE_CFB:
            self.encryptor = DESCIPHER.new(key, DESCIPHER.MODE_CFB, get_key(key, 8))
        elif type == DESCIPHER.MODE_OFB:
            self.encryptor = DESCIPHER.new(key, DESCIPHER.MODE_OFB, get_key(key, 8))
        elif type == DESCIPHER.MODE_CTR:
            self.encryptor = DESCIPHER.new(key, DESCIPHER.MODE_CTR, counter=Counter.new(64))
            
    def encrypt(self, block_data : EncryptBlock) -> bytes:
        return self.encryptor.encrypt(block_data.read())
    
    def decrypt(self, block_data : DecryptBlock) -> bytes|None:
        data = self.encryptor.decrypt(block_data.read())
        if block_data.get_block_size() is None:
            return data
        
        block_size = block_data.get_block_size()
        block_store_size = data[-block_size:]
        padding = int.from_bytes(bytes=block_store_size, byteorder=sys.byteorder, signed=False)
        
        return data[:-(block_size+padding)]
    
class RC4:
    def __init__(self, key : bytes):
        self.encryptor = ARC4.new(key)

    def encrypt(self, data : bytes) -> bytes:
        return self.encryptor.encrypt(data)
    
    def decrypt(self, data : bytes) -> bytes|None:
        return self.encryptor.decrypt(data)