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
import importlib
from fastapi import FastAPI, HTTPException, Response



# 获取当前脚本的绝对路径
current_script_path = os.path.abspath(__file__)

# 获取当前脚本的目录
current_script_dir = os.path.dirname(current_script_path)

# 切换当前工作目录到current_script_dir
os.chdir(current_script_dir)



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
    # 获取target_path相对于base_directory的路径
    relative_path = target_path.relative_to(base_directory)

    # print("svd_password:", svd_password)
    # Read File
    if action == "read":
        if os.path.exists(target_path) and os.path.isfile(target_path):
            with open(target_path, 'r') as f:
                content = f.read()
            return {"content": content}
        else:
            raise HTTPException(status_code=404, detail="File not found")



    elif action == "raw":
        if os.path.exists(target_path) and os.path.isfile(target_path):
            return FileResponse(target_path)
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

    elif action == "get":
        # 确保路径是一个Python文件
        if not str(target_path).endswith(".py"):
            raise HTTPException(status_code=400, detail="Invalid file type")
        module_name = str(relative_path).replace("/", ".").rstrip(".py")
        try:

            # print("Current directory:", os.getcwd())
            # original_directory = os.getcwd()

            # os.chdir(os.path.dirname(target_path))
            # print("Current directory:", os.getcwd())

            # 动态导入模块
            module = importlib.import_module(module_name)

            # 从模块中获取函数并执行它
            func = getattr(module, path.split("/")[-1].rstrip(".py"))
            # headers, content = func(argv=params)  # 传递params参数
            headers, content = func(argv=params) if params else func()

            # os.chdir(original_directory)
            # print("Current directory:", os.getcwd())
            
            return Response(content=content, headers=headers)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

    # elif action == "get":
    #     # 确保路径是一个Python文件
    #     if not str(target_path).endswith(".py"):
    #         raise HTTPException(status_code=400, detail="Invalid file type")
        
    #     # 假设所有模块都在'api'包内
    #     relative_module_path = "." + str(target_path).replace("/", ".").rstrip(".py")
    #     print(relative_module_path)
    #     try:
    #         # 动态导入模块
    #         module = importlib.import_module(relative_module_path, package="api")

    #         # 从模块中获取函数并执行它
    #         func = getattr(module, path.split("/")[-1].rstrip(".py"))
    #         headers, content = func(params)  # 传递params参数

    #         return Response(content=content, headers=headers)
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=str(e))
    # else:
    #     raise HTTPException(status_code=400, detail="Invalid action")







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
    

