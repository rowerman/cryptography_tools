import os
import base64

def generate_key(length):
    if length not in [64, 128, 192, 256]:
        raise ValueError("Invalid key length !")
    # 生成随机字节串
    key_bytes = os.urandom(length // 8)

    return key_bytes

def base64ToStr(s):
    '''
    将base64字符串转换为字符串
    :param s:
    :return:
    '''
    strDecode = base64.b64decode(bytes(s, encoding='gbk'))
    return str(strDecode, encoding='gbk')
