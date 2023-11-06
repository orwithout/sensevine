import os
from ..main_1_auth.token_verify import token_verify

@token_verify(user_id=0)
def read(full_path=""):
    # List the items in the target directory
    try:
        items = os.listdir(full_path)
        return {"items": items}
    except Exception as e:
        return {"error": str(e)}

