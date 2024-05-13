from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

secretKey = b'vOVH6sdmpNWjRRIqCc7rdxs01lwHzfr3'

def encrypt(text):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(secretKey), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(text.encode()) + encryptor.finalize()
    return {
        "iv": iv.hex(),
        "content": ciphertext.hex()
    }



def decrypt(hash):
    iv = bytes.fromhex(hash["iv"])
    content = bytes.fromhex(hash["content"])
    cipher = Cipher(algorithms.AES(secretKey), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return (decryptor.update(content) + decryptor.finalize()).decode('utf-8')
