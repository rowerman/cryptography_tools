import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from gmssl import sm4, func
from utils import generate_key, base64ToStr, convert_to_bytes

# 废案
""" def des_encrypt(message):
    key = generate_key(64)
    # 创建一个DES cipher对象
    cipher = Cipher(algorithms.DES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()

    # 对消息进行填充，以确保它的长度是8的倍数
    padder = padding.PKCS7(64).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()

    # 使用DES cipher对象进行加密
    encrypted_message = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(encrypted_message).decode(), key

message = "This is a secret message."
encrypted_message, Sym_Key= des_encrypt(message)
encoded_Sym_Key = base64.b64encode(Sym_Key).decode()
print("Encrypted message:", encrypted_message)
print("Encrypted key:", encoded_Sym_Key)
 """


# AES Encryption
def aes_encrypt(message, len_key, type, key, filepath):
    # type=1:输入密文+自定义密钥 type=2:文件读取密文+自定义密钥 type=3:输入密文+随机密钥 type=4:文件读取密文+随机密钥
    len_key = int(len_key)
    if type == 1:
        # 转换输入信息为byte
        messageToEnc, keyUsed = convert_to_bytes(message), convert_to_bytes(key)
        if len(keyUsed) != len_key:
            return "error_key", "error_key"
    if type == 2:
        # 读取文件内容
        try:
            file = open(filepath,"r")
            message = file.read()
            file.close()
        except:
            return "error_filepath", "error_key"
        # 转换输入信息为byte
        messageToEnc, keyUsed = convert_to_bytes(message), convert_to_bytes(key)
        if len(keyUsed) != len_key:
            return "error_key", "error_key"
    if type == 3:
        keyUsed = generate_key(len_key)
        messageToEnc = convert_to_bytes(message)
        # 指定加密套件的后端，此处使用默
    if type == 4:
        try:
            file = open(filepath,"r")
            message = file.read()
            file.close()
        except:
            return "error_filepath", "error_key"
        keyUsed = generate_key(len_key)
        messageToEnc = convert_to_bytes(message)
    try:
        backend = default_backend()
        # 生成一个长度为16Byte的随机字符串，此时AES密钥长度为128bit
        iv = os.urandom(16)
        # 创建一个Cipher对象，该对象使用AES算法和CFB模式。将密钥转换为字节类型，这里相当于创建了一个加密器
        cipher = Cipher(algorithms.AES(keyUsed), modes.CFB(iv), backend=backend)
        # 调库加密
        encryptor = cipher.encryptor()
        # 这行代码创建了一个PKCS7填充器，填充器的块大小为128。
        # 加密后的数据长度必须为128的倍数，因此使用PKCS7填充器可以确保数据的长度符合要求
        padder = padding.PKCS7(128).padder()
        # 填充数据，保证总长度为128bit的整数倍
        padded_data = padder.update(messageToEnc) + padder.finalize()
        # 进行加密
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(iv + encrypted_data).decode(), keyUsed
    except:
        return "encrypt_error", "error_key"
    

# AES Decryption
def aes_decrypt(ciphertext,key, len_key):
    len_key = int(len_key)
    keyUsed = convert_to_bytes(key)
    print(len(keyUsed))
    if len(keyUsed) != len_key//8:
        return "密钥长度错误，请重新输入"
    
    backend = default_backend()
    ciphertext = base64.b64decode(ciphertext.encode())
    iv = ciphertext[:16]
    cipher = Cipher(algorithms.AES(keyUsed), modes.CFB(iv), backend=backend)
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext[16:]) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    return unpadded_data.decode()

# # Test AES Encryption and Decryption
# message = 'This is a secret message.'
# print("Original Message:", message)
# # 待返回的密文和密钥
# encrypted_data, SymKey = aes_encrypt(message, 256,3,"","")
# print("Encrypted Data:", encrypted_data)
# decrypted_data = aes_decrypt(encrypted_data, SymKey,256)
# print("Decrypted Message:", decrypted_data)
# print("Encoded Symmetric Key:", SymKey)
# print("Encoded Symmetric Key:", SymKey.decode())

def Camellia_encrypt(message, len_key, type, key, filepath):

    # type=1:输入密文+自定义密钥 type=2:文件读取密文+自定义密钥 type=3:输入密文+随机密钥 type=4:文件读取密文+随机密钥
    len_key = int(len_key)
    if type == 1:
        # 转换输入信息为byte
        messageToEnc, keyUsed = convert_to_bytes(message), convert_to_bytes(key)
        if len(keyUsed) != len_key:
            return "error_key", "error_key"
    if type == 2:
        # 读取文件内容
        try:
            file = open(filepath,"r")
            message = file.read()
            file.close()
        except:
            return "error_filepath", "error_key"
        # 转换输入信息为byte
        messageToEnc, keyUsed = convert_to_bytes(message), convert_to_bytes(key)
        if len(keyUsed) != len_key:
            return "error_key", "error_key"
    if type == 3:
        keyUsed = generate_key(len_key)
        messageToEnc = convert_to_bytes(message)
        # 指定加密套件的后端，此处使用默
    if type == 4:
        try:
            file = open(filepath,"r")
            message = file.read()
            file.close()
        except:
            return "error_filepath", "error_key"
        keyUsed = generate_key(len_key)
        messageToEnc = convert_to_bytes(message)
    try:
        backend = default_backend()
        # 生成一个长度为16Byte的随机字符串，此时AES密钥长度为128bit
        iv = os.urandom(16)
        # 创建一个Cipher对象，该对象使用AES算法和CFB模式。将密钥转换为字节类型，这里相当于创建了一个加密器
        cipher = Cipher(algorithms.Camellia(keyUsed), modes.CFB(iv), backend=backend)
        # 调库加密
        encryptor = cipher.encryptor()
        # 这行代码创建了一个PKCS7填充器，填充器的块大小为128。
        # 加密后的数据长度必须为128的倍数，因此使用PKCS7填充器可以确保数据的长度符合要求
        padder = padding.PKCS7(128).padder()
        # 填充数据，保证总长度为128bit的整数倍
        padded_data = padder.update(messageToEnc) + padder.finalize()
        # 进行加密
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(iv + encrypted_data).decode(), keyUsed
    except:
        return "encrypt_error", "error_key"

def Camellia_decrypt(ciphertext,key, len_key):
    len_key = int(len_key)
    keyUsed = convert_to_bytes(key)
    print(len(keyUsed))
    if len(keyUsed) != len_key // 8:
        return "密钥长度错误，请重新输入"
    
    backend = default_backend()
    ciphertext = base64.b64decode(ciphertext.encode())
    iv = ciphertext[:16]
    cipher = Cipher(algorithms.Camellia(keyUsed), modes.CFB(iv), backend=backend)
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext[16:]) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    return unpadded_data.decode()

""" # Test AES Encryption and Decryption
message = 'This is a secret message.'
print("Original Message:", message)
# 待返回的密文和密钥
encrypted_data, SymKey = Camellia_encrypt(message, 256)
print("Cali_Encrypted Data:", encrypted_data)
decrypted_data = Camellia_decrypt(encrypted_data, SymKey)
print("Cali_Decrypted Message:", decrypted_data)
print("Encoded Symmetric Key:", SymKey) """

def ChaCha20Poly1305_encrypt(message,type, key, filepath):
    if type == 1:
        # 转换输入信息为byte
        messageToEnc, keyUsed = convert_to_bytes(message), convert_to_bytes(key)
        if len(keyUsed) != 256:
            return "error_key", "error_key"
    if type == 2:
        # 读取文件内容
        try:
            file = open(filepath,"r")
            message = file.read()
            file.close()
        except:
            return "error_filepath", "error_key"
        # 转换输入信息为byte
        messageToEnc, keyUsed = convert_to_bytes(message), convert_to_bytes(key)
        if len(keyUsed) != 256:
            return "error_key", "error_key"
    if type == 3:
        keyUsed = generate_key(256)
        messageToEnc = convert_to_bytes(message)
        # 指定加密套件的后端，此处使用默
    if type == 4:
        try:
            file = open(filepath,"r")
            message = file.read()
            file.close()
        except:
            return "error_filepath", "error_key"
        keyUsed = generate_key(256)
        messageToEnc = convert_to_bytes(message)
    
    
    chacha = ChaCha20Poly1305(keyUsed)
    # 96位新鲜数
    nonce = generate_key(96)
    ciphertext = chacha.encrypt(nonce, messageToEnc,None)
    
    return base64.b64encode(nonce + ciphertext).decode(), keyUsed, nonce

def ChaCha20Poly1305_decrypt(ciphertext,key,nonce):
    keyUsed = convert_to_bytes(key)
    print(len(keyUsed))
    if len(keyUsed) != 32:
        return "error_key"
    ciphertext = convert_to_bytes(ciphertext)
    chacha = ChaCha20Poly1305(keyUsed)
    ciphertext = base64.b64decode(ciphertext)[12:]
    decrypted_data = chacha.decrypt(nonce.encode(), ciphertext, None)
    return decrypted_data.decode()

""" message = 'This is a secret message.'
print("Original Message:", message)
encrypted_data, SymKey, nonce = ChaCha20Poly1305_encrypt(message, 256)
print("Chacha_Encrypted Data:", encrypted_data)
decrypted_data = ChaCha20Poly1305_decrypt(encrypted_data, SymKey,nonce)
print("Chacha_Decrypted Message:", decrypted_data)
print("Encoded Symmetric Key:", SymKey) """

def SM4_encrypt(message,type, key, filepath):
    # type=1:输入密文+自定义密钥 type=2:文件读取密文+自定义密钥 type=3:输入密文+随机密钥 type=4:文件读取密文+随机密钥
    if type == 1:
        # 转换输入信息为byte
        messageToEnc, keyUsed = convert_to_bytes(message), convert_to_bytes(key)
        if len(keyUsed) != 16:
            return "error_key", "error_key"
    if type == 2:
        # 读取文件内容
        try:
            file = open(filepath,"r")
            message = file.read()
            file.close()
        except:
            return "error_filepath", "error_key"
        # 转换输入信息为byte
        messageToEnc, keyUsed = convert_to_bytes(message), convert_to_bytes(key)
        if len(keyUsed) != 16:
            return "error_key", "error_key"
    if type == 3:
        keyUsed = generate_key(128)
        messageToEnc = convert_to_bytes(message)
        # 指定加密套件的后端，此处使用默
    if type == 4:
        try:
            file = open(filepath,"r")
            message = file.read()
            file.close()
        except:
            return "error_filepath", "error_key"
        keyUsed = generate_key(128)
        messageToEnc = convert_to_bytes(message)
    
    sm4Alg = sm4.CryptSM4()  # 实例化sm4
    sm4Alg.set_key(keyUsed, sm4.SM4_ENCRYPT)
    
    enRes = sm4Alg.crypt_ecb(messageToEnc)  # 开始加密,bytes类型，ecb模式
    return base64.b64encode(enRes).decode(), keyUsed

def SM4_decrypt(ciphertext,key):
    keyUsed = convert_to_bytes(key)
    ciphertext = convert_to_bytes(ciphertext)
    if len(keyUsed) != 16:
        return "error_key"
    
    sm4Alg = sm4.CryptSM4()  # 实例化sm4
    sm4Alg.set_key(keyUsed, sm4.SM4_DECRYPT)  # 设置密钥
    deRes = sm4Alg.crypt_ecb(base64.b64decode(ciphertext))
    return deRes.decode()

""" message = 'This is a secret message.'
print("Original Message:", message)
encrypted_data, SymKey = SM4_encrypt(message)
print("SM4_Encrypted Data:", encrypted_data)
decrypted_data = SM4_decrypt(encrypted_data, SymKey)
print("SM4_Decrypted Message:", decrypted_data)
print("Encoded Symmetric Key:", SymKey) """

