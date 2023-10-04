import io
import sys
import collections
from Crypto.Cipher import AES as AESCIPHER

from ki_tugas1.commands.encryption_key import get_key

class AESBlock:
    def read16(self) -> bytes|False:
        pass
    
class StringBlock(AESBlock):
    def __init__(self, data : str):
        self.data = data.encode()
        self.padding = -1
        
    def read16(self) -> bytes:
        if self.data is None:
            return False
        if self.padding != -1:
            self.data = None
            return self.padding.to_bytes(16, byteorder=sys.byteorder, signed=False)
        
        data = self.data[:16]
        self.data = self.data[16:]
        
        sisa = len(data)
        if sisa == 0:
            self.data = None
            self.padding = 0
            return self.padding.to_bytes(16, byteorder=sys.byteorder, signed=False)
        
        if sisa < 16:
            data += bytes([ord('0')] * (16 - sisa))
            self.padding = 16 - sisa
        
        return data

class StreamBlock(AESBlock):
    def __init__(self, stream : io.BufferedReader):
        self.stream = stream
        self.padding = -1
    
    def read16(self) -> bytes:
        if self.stream is None:
            return False
        if self.padding != -1:
            self.stream = None
            return self.padding.to_bytes(16, byteorder=sys.byteorder, signed=False)
        if not self.stream.peek(1):
            self.stream = None
            self.padding = 0
            return self.padding.to_bytes(16, byteorder=sys.byteorder, signed=False)
        
        data = self.stream.read(16)
        sisa = len(data)
        if sisa < 16:
            self.padding = 16 - sisa
            data += bytes([ord('0')] * (16 - sisa))
        
        return data 
    
class DecryptBlock:
    def read16(self) -> bytes|False:
        pass
    
class StringDecryptBlock(DecryptBlock):
    def __init__(self, data : bytes):
        self.data = data
        
    def read16(self) -> bytes|False:
        data = self.data[:16]
        self.data = self.data[16:]
        return data
    
class StreamDecryptBlock(DecryptBlock):
    def __init__(self, stream : io.BufferedReader):
        self.stream = stream
        
    def read16(self) -> bytes|False:
        return self.stream.read(16)
            

class AES:
    def __init__(self, key : str, type):
        self.encryptor = None
        self.type = type
        self.decrypt_queue = None
        
        
        if type == AESCIPHER.MODE_CBC:
            self.encryptor = AESCIPHER.new(key, AESCIPHER.MODE_CBC, get_key(key))
        elif type == AESCIPHER.MODE_CFB:
            self.encryptor = AESCIPHER.new(key, AESCIPHER.MODE_CFB, get_key(key), 64)
        elif type == AESCIPHER.MODE_OFB:
            self.encryptor = AESCIPHER.new(key, AESCIPHER.MODE_OFB, get_key(key))
        elif type == AESCIPHER.MODE_CTR:
            self.encryptor = AESCIPHER.new(key, AESCIPHER.MODE_OFB)
    
    def encrypt(self, block_data : AESBlock):
        result = b''
        data = block_data.read16()
        while data is not None:
            result += self.encryptor.encrypt(data)
            data = block_data.read16()
        
        return result
    
    def decrypt16(self, block_data : DecryptBlock) -> bytes|None:
        if self.decrypt_queue is None:
            self.decrypt_queue = collections.deque()
            
            for _ in range(2):
                data = block_data.read16()
                data = self.encryptor.decrypt(data)
                self.decrypt_queue.append(data)
        
        if len(self.decrypt_queue) == 0:
            return None
        
        data = self.decrypt_queue.popleft()
        next_data = block_data.read16()
        if next_data is not None:
            next_data = self.encryptor.decrypt(next_data)
            self.decrypt_queue.append(next_data)
        
        if len(self.decrypt_queue.count) == 1:
            padding = self.decrypt_queue.popleft()
            panjang_data = 16 - int.from_bytes(padding, sys.byteorder, False)
            data = data[panjang_data:]
            
        return data
        