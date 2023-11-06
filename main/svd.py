









from fastapi import FastAPI, Query
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/ls/")
async def list_dir(path: str = Query("", alias='id')):
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








