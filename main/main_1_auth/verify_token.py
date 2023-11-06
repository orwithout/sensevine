from fastapi import HTTPException
from jose import ExpiredSignatureError, JWTError, jwt
import os
from .login_env import init_settings  # 导入 settings 对象

def verify_token(user_id: int, verify_token=False, token_in_header: str = "", token_in_url: str = ""):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not token_in_header:
        token_in_header = token_in_url
    if not token_in_header:
        raise credentials_exception

    settings = init_settings(str(user_id))
    
    try:
        payload = jwt.decode(token_in_header, settings.secret_key, algorithms=[settings.algorithm])
        account: str = payload.get("sub")
        login_method: str = payload.get("mod")
        if account is None:
            raise credentials_exception
        
        # 检查黑名单
        blacklist_path = os.path.join(str(user_id), ".auth", "token_blacklist.txt")
        if os.path.exists(blacklist_path):
            with open(blacklist_path, "r") as blacklist_file:
                if token_in_header in blacklist_file.read():
                    raise credentials_exception
    except ExpiredSignatureError:
        raise credentials_exception
    except JWTError:
        raise credentials_exception

    # 从文件加载用户数据
    passwd_file = os.path.join(str(user_id), ".auth", f"{login_method}.{account}.txt")
    if not os.path.exists(passwd_file):
        raise credentials_exception



# fetch('http://your-api-url.com/0/some-protected-route', {
#   method: 'GET',
#   headers: {
#     'token_in_header': 'token'
#   }
# })
# .then(response => response.json())
# .then(data => console.log(data));

