import io
import sys
import collections
from Crypto.Cipher import AES as AESCIPHER, DES as DESCIPHER, ARC4

from ki_tugas1.commands.encryption_key import get_key

class EncryptBlock:
    def read(self) -> bytes|None:
        pass
    
class StringBlock(EncryptBlock):
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
        
    def read(self) -> bytes|None:
        if self.block_size is None:
            return self.data
        
        if self.data is None or len(self.data) == 0:
            return None
        data = self.data[:self.block_size]
        self.data = self.data[self.block_size:]
        
        return data

# class StreamBlock(EncryptBlock):
#     def __init__(self, stream : io.BufferedReader, block_size : int|None):
#         self.stream = stream
#         self.padding = -1
#         self.block_size = block_size
    
#     def read(self) -> bytes|None:
#         if self.block_size is None:
#             return self.stream.read()
        
#         if self.stream is None:
#             return None
#         if self.padding != -1:
#             self.stream = None
#             return self.padding.to_bytes(self.block_size, byteorder=sys.byteorder, signed=False)
#         if not self.stream.peek(1):
#             self.stream = None
#             self.padding = 0
#             return self.padding.to_bytes(self.block_size, byteorder=sys.byteorder, signed=False)
        
#         data = self.stream.read(self.block_size)
#         sisa = len(data)
#         if sisa < self.block_size:
#             self.padding = self.block_size - sisa
#             data += bytes([ord('0')] * (self.block_size - sisa))
        
#         return data 
    
class DecryptBlock:
    def read(self) -> bytes|None:
        pass
    
class StringDecryptBlock(DecryptBlock):
    def __init__(self, data : bytes, block_size : int|None):
        self.data = data
        self.block_size = block_size
        
    def read(self) -> bytes|None:
        if self.block_size is None:
            return self.data
        
        data = self.data[:self.block_size]
        self.data = self.data[self.block_size:]
        if data is None or len(data) == 0:
            return None
        return data
    
class StreamDecryptBlock(DecryptBlock):
    def __init__(self, stream : io.BufferedReader, block_size : int|None):
        self.stream = stream
        self.block_size = block_size
        
    def read(self) -> bytes|None:
        if self.block_size is None:
            return self.stream.read()
        
        return self.stream.read(self.block_size)
            

class AES:
    def __init__(self, key : bytes, type):
        self.encryptor = None
        self.type = type
        self.decrypt_queue = None
        
        if type == AESCIPHER.MODE_CBC:
            self.encryptor = AESCIPHER.new(key, AESCIPHER.MODE_CBC, get_key(key, 16))
        elif type == AESCIPHER.MODE_CFB:
            self.encryptor = AESCIPHER.new(key, AESCIPHER.MODE_CFB, get_key(key, 16), 64)
        elif type == AESCIPHER.MODE_OFB:
            self.encryptor = AESCIPHER.new(key, AESCIPHER.MODE_OFB, get_key(key, 16))
        elif type == AESCIPHER.MODE_CTR:
            self.encryptor = AESCIPHER.new(key, AESCIPHER.MODE_CTR)
    
    def encrypt(self, block_data : EncryptBlock) -> bytes:
        result = bytes()
        data = block_data.read()
        while data is not None:
            result += self.encryptor.encrypt(data)
            data = block_data.read()
        
        return result
    
    def decrypt(self, block_data : DecryptBlock) -> bytes|None:
        if self.decrypt_queue is None:
            self.decrypt_queue = collections.deque()
            
            for _ in range(2):
                data = block_data.read()
                data = self.encryptor.decrypt(data)
                self.decrypt_queue.append(data)
        
        if len(self.decrypt_queue) == 0:
            return None
        
        data = self.decrypt_queue.popleft()
        next_data = block_data.read()
        if next_data is not None:
            next_data = self.encryptor.decrypt(next_data)
            self.decrypt_queue.append(next_data)
        else:
            padding = self.decrypt_queue.popleft()
            panjang_data = 16 - int.from_bytes(bytes=padding, byteorder=sys.byteorder, signed=False)
            data = data[:panjang_data]
            
        return data
    
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
            self.encryptor = DESCIPHER.new(key, DESCIPHER.MODE_CTR)
            
    def encrypt(self, block_data : EncryptBlock) -> bytes:
        result = bytes()
        data = block_data.read()
        while data is not None:
            result += self.encryptor.encrypt(data)
            data = block_data.read()
        
        return result
    
    def decrypt(self, block_data : DecryptBlock) -> bytes|None:
        if self.decrypt_queue is None:
            self.decrypt_queue = collections.deque()
            
            for _ in range(2):
                data = block_data.read()
                data = self.encryptor.decrypt(data)
                self.decrypt_queue.append(data)
        
        if len(self.decrypt_queue) == 0:
            return None
        
        data = self.decrypt_queue.popleft()
        next_data = block_data.read()
        if next_data is not None:
            next_data = self.encryptor.decrypt(next_data)
            self.decrypt_queue.append(next_data)
        else:
            padding = self.decrypt_queue.popleft()
            panjang_data = 8 - int.from_bytes(bytes=padding, byteorder=sys.byteorder, signed=False)
            data = data[:panjang_data]
            
        return data
    
class RC4:
    def __init__(self, key : bytes):
        self.encryptor = ARC4.new(key)

    def encrypt(self, data : bytes) -> bytes:
        return self.encryptor.encrypt(data)
    
    def decrypt(self, data : bytes) -> bytes|None:
        return self.encryptor.decrypt(data)