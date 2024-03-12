from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ed25519, ed448
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64
import os
from utils import convert_to_bytes

def RSA_encrypt(message, len_secret_key):
    len_secret_key = int(len_secret_key)
    if len_secret_key not in [512, 1024, 2048, 4096]:
        raise ValueError("Invalid secret_key length !")
    
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=len_secret_key)
    public_key = private_key.public_key()
    
    messageToEncrypt = convert_to_bytes(message)
    ciphertext = public_key.encrypt(
    messageToEncrypt,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
    
    return base64.b64encode(ciphertext).decode(), public_key, private_key

def RSA_decrypt(ciphertext, private_pem):
    ciphertext = base64.b64decode(ciphertext.encode())
    private_key = private_pem.encode()
    private_key = serialization.load_pem_private_key(private_key, password=None, backend=default_backend())
    print(private_key.key_size)
    print(len(ciphertext))
    
    decrypted_data = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
    
    return decrypted_data.decode()


def generate_RSA_keys(len_secret_key):
    len_secret_key = int(len_secret_key)
    if len_secret_key not in [512, 1024, 2048, 4096]:
        raise ValueError("Invalid secret_key length !")
    
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=len_secret_key)
    public_key = private_key.public_key()
    
    return public_key, private_key

# message = "111"
# Encrypted_message, public_key, private_key = RSA_encrypt(message, 4096)
# print("Encrypted message:", Encrypted_message)
# # print("Public key:", base64.b64encode(public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)).decode())
# # print("Private key:", base64.b64encode(private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())).decode())
# Decrypted_message = RSA_decrypt(Encrypted_message, private_key)
# print("Decrypted message:", Decrypted_message)

# 使用Ed25519算法生成公私钥
def generate_Ed25519_keys():
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    
    return public_key, private_key

def generate_Ed448_keys():
    private_key = ed448.Ed448PrivateKey.generate()
    public_key = private_key.public_key()
    
    return public_key, private_key
    

