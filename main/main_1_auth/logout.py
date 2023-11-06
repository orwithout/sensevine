import os
from fastapi import HTTPException


def logout(user_id: int, verify_token=True, token_in_header: str = "", token_in_url: str = ""):
    if not token_in_header:
        token_in_header = token_in_url
    if not token_in_header:
        raise HTTPException(status_code=401, detail="No token provided.")

    try:
        auth_dir = os.path.join(str(user_id), ".auth")
        os.makedirs(auth_dir, exist_ok=True)  # 确保目录存在，如果不存在则创建
        blacklist_path = os.path.join(auth_dir, "token_blacklist.txt")

        with open(blacklist_path, "a") as blacklist_file:
            blacklist_file.write(token_in_header + "\n")

        return {"message": "Logged out successfully."}
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"Error writing to blacklist file: {e}")