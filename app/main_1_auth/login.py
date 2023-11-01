
from .login_gen_token import create_access_token
from fastapi import HTTPException
import json
# from passlib.context import CryptContext
import os

def login(user_id: int, user_input: str = "", args: str = ""):
    # 如果 user_input 为空，尝试从 args 中获取
    if not user_input:
        user_input = args

    print(user_input)
    # 解析用户名和密码
    if ":" not in user_input:
        raise HTTPException(status_code=400, detail="Invalid input format")
    username, password = user_input.split(":", 1)
    print(username)
    print(password)
    print(user_id)

    # 从 JSON 文件加载用户数据
    #os.chdir(os.path.join(current_script_dir, argv))
    print("Current directory:", os.getcwd())
    try:
        with open(f"{user_id}/.passwd.json", "r") as f:
            user_data = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")

    # 验证用户名和密码
    if username + ':' + password != user_data["username"] + ':' + user_data["password"]:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # if not pwd_context.verify(password, user_data["password"]):
    #     raise HTTPException(status_code=400, detail="Invalid username or password")

    # 创建令牌
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}



