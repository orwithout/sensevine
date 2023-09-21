# uvicorn svd:app --reload --host 0.0.0.0 --port 8002
# http://4.193.54.245:8002/123456/public-test/list

from fastapi import FastAPI, HTTPException, Path, File, UploadFile
from typing import Optional
import os
from pathlib import Path as PythonPath
import shutil
from subprocess import Popen, PIPE
from fastapi.middleware.cors import CORSMiddleware
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

with open("config.json", "r") as f:
    config = json.load(f)

svd_password = config.get("svd-password", "")
svd_password = f"/{svd_password}" if svd_password else ""

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def secure_path(path: str, base_directory: str) -> PythonPath:
    base = PythonPath(base_directory).resolve()
    full_path = (base / path).resolve()
    if base not in full_path.parents:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    return full_path





@app.get("/static/{file_path:path}")
async def read_static(file_path: str):
    complete_path = os.path.join("public-test", file_path)
    if os.path.exists(complete_path) and os.path.isfile(complete_path):
        return FileResponse(complete_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")




@app.get(f"{svd_password}/{{path:path}}/{{action}}")
async def file_operations(action: str, path: str, params: Optional[str] = None):
    base_directory = os.getcwd()
    target_path = secure_path(path, base_directory)
    
    print("svd_password:", svd_password)
    # Read File
    if action == "read":
        if os.path.exists(target_path) and os.path.isfile(target_path):
            with open(target_path, 'r') as f:
                content = f.read()
            return {"content": content}
        else:
            raise HTTPException(status_code=404, detail="File not found")

    # List Directory
    elif action == "list":
        if os.path.exists(target_path) and os.path.isdir(target_path):
            return {"content": os.listdir(target_path)}
        else:
            raise HTTPException(status_code=404, detail="Directory not found")


    # Update File
    elif action == "update":
        if os.path.exists(target_path) and os.path.isfile(target_path):
            with open(target_path, 'a') as f:  # 'a' mode for appending
                f.write("\n" + params)
            return {"status": "File updated"}
        else:
            raise HTTPException(status_code=404, detail="File not found")


    # Create File/Directory
    elif action == "mkdir":
        if not os.path.exists(target_path):
                os.makedirs(target_path)
                return {"status": "Directory created"}



    # Delete File/Directory
    elif action == "delete":
        if os.path.exists(target_path):
            if os.path.isdir(target_path):
                shutil.rmtree(target_path)
            else:
                os.remove(target_path)
            return {"status": "Deleted"}
        else:
            raise HTTPException(status_code=404, detail="File or directory not found")
    
    elif action == "run":
        if os.path.exists(target_path) and os.path.isfile(target_path):
            try:
                cmd_args = ["/usr/bin/python3", target_path] + (params.split() if params else [])
                process = Popen(cmd_args, stdout=PIPE, stderr=PIPE)
                # process = Popen(["python", target_path] + params.split(), stdout=PIPE, stderr=PIPE)
                
                stdout, stderr = process.communicate()
                return {"output": stdout.decode(), "error": stderr.decode()}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        else:
            raise HTTPException(status_code=404, detail="File not found")

    else:
        raise HTTPException(status_code=400, detail="Invalid action")
    

@app.post(f"{svd_password}/{{path:path}}/{{action}}")  # 使用 POST 方法
async def file_operations(action: str, path: str, params: Optional[str] = None, file: UploadFile = File(...)):
    base_directory = os.getcwd()
    target_path = secure_path(path, base_directory)

    if action == "upload":
        try:
            file_contents = await file.read()
            target_file_path = os.path.join(target_path, file.filename)
            
            with open(target_file_path, 'wb') as f:
                f.write(file_contents)
            
            return {"status": "File uploaded"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="Invalid action")
    

