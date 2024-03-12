import os
import base64
import random
import string

def generate_key(length):
    # 生成随机字节串
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+[]{}|;:,.<>?"
    key = ''.join(random.choices(characters, k=length//8))
    return key.encode()

def base64ToStr(s):
    '''
    将base64字符串转换为字符串
    :param s:
    :return:
    '''
    strDecode = base64.b64decode(bytes(s, encoding='gbk'))
    return str(strDecode, encoding='gbk')

def convert_to_bytes(data):
    if isinstance(data, bytes):  # 如果数据已经是字节流，直接返回
        return data
    elif isinstance(data, str):  # 如果数据是字符串，使用utf-8编码转换为字节流
        return data.encode('utf-8')
    elif isinstance(data, int):  # 如果数据是整数（比特流），使用to_bytes方法转换为字节流
        return (data).to_bytes((data.bit_length() + 7) // 8, 'big' or data == 0)
    elif isinstance(data, str):  # 如果数据是十六进制字符串，使用bytes.fromhex方法转换为字节流
        return bytes.fromhex(data)
    else:
        raise TypeError('Unsupported data type')
    
def convert_slashes(file_path):
    return file_path.replace('\\', '/')



