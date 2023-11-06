import os

def read(verify_token=True, full_path=""):  
    # List the items in the target directory
    print("readxxx")
    try:
        items = os.listdir(full_path)
        return {"items": items}
    except Exception as e:
        return {"error": str(e)}
