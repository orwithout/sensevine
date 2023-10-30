import os

def read(user_id=0, full_path="", args=""):
    # List the items in the target directory
    try:
        items = os.listdir(full_path)
        return {"items": items}
    except Exception as e:
        return {"error": str(e)}

