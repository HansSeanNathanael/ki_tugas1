import hashlib
import base64
import string
import random

def generate_random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    
    random_string = ''.join(random.choice(characters) for _ in range(length))
    
    return random_string.encode()

if __name__ == '__main__':
    key128Byte = hashlib.sha256(generate_random_string(32)).digest()
    key128Byte = key128Byte[16:]
    key128B64 = base64.b64encode(key128Byte)
    print(f'\nKey 128 bit')
    print(f'base64.b64decode({key128B64})\n')
    
    key256Byte = hashlib.sha256(generate_random_string(32)).digest()
    key256B64 = base64.b64encode(key256Byte)
    print(f'\nKey 256 bit')
    print(f'base64.b64decode({key256B64})\n')
