from fastapi import HTTPException
from jose import ExpiredSignatureError, JWTError, jwt
from .login_env import init_settings  # 导入 settings 对象
from .login_gen_token import login_gen_token

def refresh_token(user_id: int, verify_token=True, token_in_header: str = "", token_in_url: str = ""):
        
    if not token_in_header:
        token_in_header = token_in_url
        
    settings = init_settings(str(user_id))
    payload = jwt.decode(token_in_header, settings.secret_key, algorithms=[settings.algorithm])
    account: str = payload.get("sub")
    login_method: str = payload.get("mod")
    access_token = login_gen_token(user_id=user_id, data={"sub": account,"mod":login_method})
    return {"access_token": access_token, "token_type": "bearer"}





# fetch('http://your-api-url.com/0/some-protected-route', {
#   method: 'GET',
#   headers: {
#     'token_in_header': 'token'
#   }
# })
# .then(response => response.json())
# .then(data => console.log(data));

