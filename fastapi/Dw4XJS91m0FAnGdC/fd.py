import secrets
import base64

# Generate 24 random bytes
random_bytes = secrets.token_bytes(12)
print("Random Bytes:", random_bytes)

hex_representation = random_bytes.hex()
print("Random Bytes in Hex:", hex_representation)

# Encode the bytes to a URL-safe base64 string
token = base64.urlsafe_b64encode(random_bytes).decode('utf-8').rstrip('=')
print("Token:", token)


