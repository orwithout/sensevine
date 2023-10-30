from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseSettings
from jose.constants import ALGORITHMS
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

class Settings(BaseSettings):
    secret_key: str
    algorithm: str = ALGORITHMS.HS256
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

def create_secret_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    return private_pem.decode()

def create_default_env_file():
    with open(".env", "w") as f:
        f.write(f"SECRET_KEY={create_secret_key()}\n")
        f.write("ALGORITHM=HS256\n")
        f.write("ACCESS_TOKEN_EXPIRE_MINUTES=30\n")

# 检查当前目录是否存在.env文件
env_path = Path(".env")
if not env_path.exists():
    create_default_env_file()

# 加载环境变量
load_dotenv()

# 初始化设置
settings = Settings()

# 使用settings对象获取配置
print(settings.secret_key)
print(settings.algorithm)
