from cryptography.hazmat.primitives import hashes, cmac, hmac, poly1305, serialization
from cryptography.hazmat.primitives.asymmetric import ed448
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os
from utils import generate_key

def Ed448_Sig(message):
    private_key = ed448.Ed448PrivateKey.generate()
    public_key = private_key.public_key()
    messageToEncrypt = message.encode()
    signature = private_key.sign(messageToEncrypt)
    
    return base64.b64encode(signature).decode(), public_key, private_key

def Ed448_Verify(message, signature, public_pem):
    try:
        signature = base64.b64decode(signature.encode())

        messageToEnc = message.encode()
        public_pem = public_pem.encode()
        
        public_key = serialization.load_pem_public_key(public_pem, default_backend())

        # Verify the signature
        public_key.verify(signature, messageToEnc)
        # If the verification is successful, return True
        return True
    except:
        # If the verification fails, return False
        return False



# 消息认证码
def CMAC_en(message, len_key):
    len_key = int(len_key)
    if len_key not in [128, 192, 256]:
        raise ValueError("Invalid key size. Key size must be 128, 192, or 256.")
    key = generate_key(len_key)
    messageToEncrypt = message.encode()
    
    c = cmac.CMAC(algorithms.AES(key))
    c.update(messageToEncrypt)
    # 生成认证码
    tag = c.finalize()
    
    return base64.b64encode(tag).decode(), key

def CMAC_de(message, key, tag):
    key = key.encode()
    c = cmac.CMAC(algorithms.AES(key))
    c.update(message.encode())
    
    try:
        c.verify(base64.b64decode(tag.encode()))
        return True
    except:
        return False
    
""" message = "Hello, world! I 'm Ed448."
MacGenerated, key = CMAC_en(message, 256)
print("MAC:",MacGenerated)
print("Key:",key)
result = CMAC_de(message, key, MacGenerated)
print(result) """

def HMAC_en(message):
    key = generate_key(256)
    h = hmac.HMAC(key, hashes.SHA256())
    h.update(message.encode())
    tag = h.finalize()
    
    return base64.b64encode(tag).decode(), key

def HMAC_de(message, key, tag):
    key = key.encode()
    h = hmac.HMAC(key, hashes.SHA256())
    h.update(message.encode())
    
    try:
        h.verify(base64.b64decode(tag.encode()))
        return True
    except:
        return False
    
""" message = "Hello, world! I 'm Ed448."
MacGenerated, key = HMAC_en(message)
print("MAC:",MacGenerated)
print("Key:",key)
result = HMAC_de(message, key, MacGenerated)
print(result) """

def poly1305_en(message):
    key = generate_key(256)
    p = poly1305.Poly1305(key)
    p.update(message.encode())
    tag = p.finalize()
    
    return base64.b64encode(tag).decode(), key

def poly1305_de(message, key, tag):
    key = key.encode()
    p = poly1305.Poly1305(key)
    p.update(message.encode())
    try:
        p.verify(base64.b64decode(tag.encode()))
        return True
    except:
        return False
    
""" message = "Hello, world! I 'm Ed448."
MacGenerated, key = poly1305_en(message)
print("MAC:",MacGenerated)
print("Key:",key)
result = poly1305_de(message, key, MacGenerated)
print(result) """

def SHA_family(message, type_sha):
    sha_types = {
        "SHA-224": hashes.SHA224,
        "SHA-256": hashes.SHA256,
        "SHA-384": hashes.SHA384,
        "SHA-512": hashes.SHA512,
        "SHA3_224": hashes.SHA3_224,
        "SHA3_256": hashes.SHA3_256,
        "SHA3_384": hashes.SHA3_384,
        "SHA3_512": hashes.SHA3_512,
    }

    if type_sha in sha_types:
        digest = hashes.Hash(sha_types[type_sha](), backend=default_backend())
        digest.update(message.encode())
        return base64.b64encode(digest.finalize()).decode()
    else:
        raise ValueError(f"Invalid SHA type: {type_sha}")
    
def Shake_family(message, len_output, type_shake):
    len_output = int(len_output)
    if len_output < 128 or len_output > 8192:
        raise ValueError("The length of output must be between 128 and 8192 bits.")
    message = message.encode()
    if type_shake == "SHAKE128":
        digest = hashes.Hash(hashes.SHAKE128(len_output), backend=default_backend())
    elif type_shake == "SHAKE256":
        digest = hashes.Hash(hashes.SHAKE256(len_output), backend=default_backend())
    else :
        raise ValueError("Invalid SHAKE type.")
    digest.update(message)
    return base64.b64encode(digest.finalize()).decode()
    