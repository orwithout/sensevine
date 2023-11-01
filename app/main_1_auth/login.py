from fastapi import APIRouter, HTTPException, Form
from passlib.context import CryptContext
import importlib

from fastapi import APIRouter, HTTPException, Query



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def read(user_id=0, user_input="", args="",):
    # 导入用户数据
    try:
        user_module = importlib.import_module(f"{user_id}.id")
        user_data = getattr(user_module, "user_data")
    except ImportError:
        raise HTTPException(status_code=400, detail="User not found")

    # 验证用户名
    if user_data["username"] != username:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # 验证密码
    if not pwd_context.verify(password, user_data["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    return {"message": "Login successful!"}

