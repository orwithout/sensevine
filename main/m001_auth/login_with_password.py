
from fastapi import HTTPException
import os
import re
from .login_gen_token import login_gen_token


# fetch('http://your-api-url.com/0/some-protected-route', {
#   method: 'GET',
#   headers: {
#     'args_in_header': 'account:password_hash'
#   }
# })
# .then(response => response.json())
# .then(data => console.log(data));





def login_with_password(user_id: int, verify_token=False, args_in_header: str="", args_in_url: str=""):
    # 如果 args_in_header 为空，尝试从 args_in_url 中获取
    if not args_in_header:
        args_in_header = args_in_url

    # 解析用户名和密码
    if ":" not in args_in_header:
        raise HTTPException(status_code=400, detail="Invalid input format")
    account, password_hash = args_in_header.split(":", 1)

    if not re.match(r'^[a-zA-Z0-9_.+-]{1,127}@[a-zA-Z0-9-.]{1,126}$', account) or not re.match(r'^.{1,256}$', password_hash):
        raise HTTPException(status_code=400, detail="Invalid account or password format")
    
    passwd_file = os.path.join(str(user_id), ".auth", f"password_hash.{account}.txt")
    print(passwd_file)
    # 从文件加载用户数据
    try:
        with open(passwd_file, "r") as f:
            user_data = f.read().strip()
    except IOError:
        raise HTTPException(status_code=500, detail="Internal server error")

    # 验证用户名和密码
    print("password_hash:", password_hash)
    print("user_data:", user_data)
    if password_hash != user_data:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # 创建令牌
    access_token = login_gen_token(user_id=user_id, data={"sub": account,"mod":"password_hash"})
    return {"access_token": access_token, "token_type": "bearer"}

