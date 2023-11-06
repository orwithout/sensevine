import jwt
from datetime import datetime, timedelta
from .login_env import init_settings  # 导入 settings 对象


def login_gen_token(user_id: int, data: dict):
    to_encode = data.copy()
    settings = init_settings(user_id)
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt
