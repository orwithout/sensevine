import sys
import secrets
import base64

# 从命令行参数获取长度，默认为12
length = int(sys.argv[1]) if len(sys.argv) > 1 else 12

random_bytes = secrets.token_bytes(length)
# print("Random Bytes:", random_bytes)

# hex_representation = random_bytes.hex()
# print("Random Bytes in Hex:", hex_representation)

token = base64.urlsafe_b64encode(random_bytes).decode('utf-8').rstrip('=')
print("Token:", token)
