from fastapi import APIRouter, Query
import os

router = APIRouter()

@router.get("/")
async def root(path: str = Query("", alias='id')):
    base_directory = os.path.abspath("0/")
    target_directory = os.path.abspath(os.path.join("0/", path))

    # Ensure the target directory is within the base directory
    if not target_directory.startswith(base_directory):
        return {"error": "Invalid path"}

    # List the items in the target directory
    try:
        items = os.listdir(target_directory)
        return {"items": items}
    except Exception as e:
        return {"error": str(e)}








