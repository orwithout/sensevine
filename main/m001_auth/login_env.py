from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from jose.constants import ALGORITHMS
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import base64, os

class Settings(BaseSettings):
    secret_key: str
    algorithm: str = ALGORITHMS.HS256
    access_token_expire_minutes: int = 4320

    class Config:
        env_file_encoding = 'utf-8'
        # We remove the env_file attribute from here 

def create_secret_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    return base64.b64encode(private_pem).decode()

def create_default_env_file(env_file):
    with open(env_file, "w") as f:
        f.write(f"SECRET_KEY={create_secret_key()}\n")
        f.write("ALGORITHM=HS256\n")
        f.write("ACCESS_TOKEN_EXPIRE_MINUTES=4320\n")  # token 有效期为3天

def init_settings(user_id: int):
    env_file = os.path.join(str(user_id), ".auth", "login.env")
    if not Path(env_file).exists():
        print(f"Creating a new .env file at {env_file}")
        create_default_env_file(env_file)
    
    # Load the environment variables from the specified .env file
    load_dotenv(dotenv_path=env_file)
    
    # Now you can instantiate the Settings class
    return Settings()
