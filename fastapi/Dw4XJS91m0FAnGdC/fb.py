# 定义四个函数
import base64

# 1. 将汉字转化为unicode输出
def chinese_to_unicode(chinese_str):
    return ''.join(['\\u{:04x}'.format(ord(c)) for c in chinese_str])

# 2. 将unicode编码的前面的\u去掉
def strip_unicode_prefix(unicode_str):
    return unicode_str.replace("\\u", "")

# 3. 将unicode编码为base64
def unicode_hex_to_base64(unicode_hex: str) -> str:
    unicode_bytes = bytes.fromhex(unicode_hex)
    return base64.b64encode(unicode_bytes).decode('utf-8')

# 4. 将任意字符串编码为base64
def str_to_base64(input_str):
    return base64.b64encode(input_str.encode('utf-8')).decode('utf-8')

# 测试函数
chinese_str = "时日无多"
unicode_str = chinese_to_unicode(chinese_str)
print("1. Unicode:", unicode_str)

stripped_unicode = strip_unicode_prefix(unicode_str)
print("2. Stripped Unicode:", stripped_unicode)

base64_encoded_unicode = unicode_hex_to_base64(stripped_unicode)
print("3. Base64 Encoded Unicode:", base64_encoded_unicode)

base64_encoded_str = str_to_base64("c2hpcmlidWR1bw")
print("4. Base64 Encoded String:", base64_encoded_str)
