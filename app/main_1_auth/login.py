from fastapi import APIRouter, HTTPException, Form
from passlib.context import CryptContext
import importlib

from fastapi import APIRouter, HTTPException, Query

router = APIRouter()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/{user_id}/{path:path}")
async def dynamic_route(user_id: int, path: str, fn: str = Query(...)):
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



from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

@router.post("/{user_id}/{path:path}")
async def dynamic_route(user_id: int, path: str, fn: str = Query(...), method: str = Query(None)):
    # user_id 是用户的主目录
    # path 是子目录
    # fn 是要调用的函数
    # method 是可选的方法参数
    return {"user_id": user_id, "path": path, "function": fn, "method": method}
