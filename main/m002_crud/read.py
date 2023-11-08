import os

def read(verify_token=False, full_path=""):  
    try:
        items = os.listdir(full_path)
        return {"items": items}
    except Exception as e:
        return {"error": str(e)}
