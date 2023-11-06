from fastapi import FastAPI, Depends

# 导入路由器
from main_0_conf import root
from main_1_auth import login
# from .main_1_auth.logout import logout
# from .main_1_auth.verify import verify
# from .main_2_crud.create import create
# from .main_2_crud.read import read
# from .main_2_crud.update import update
# from .main_2_crud.delete import delete



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



app.include_router(root.router)
app.include_router(login.router)
# app.include_router(logout.router, dependencies=[Depends(verify)])
# app.include_router(create.router, dependencies=[Depends(verify)])
# app.include_router(read.router, dependencies=[Depends(verify)])
# app.include_router(update.router, dependencies=[Depends(verify)])
# app.include_router(delete.router, dependencies=[Depends(verify)])



from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    # 你的读取逻辑
    ...

@app.post("/files/{file_path:path}")
async def create_file(file_path: str, file_content: str):
    # 你的创建逻辑
    ...

@app.put("/files/{file_path:path}")
async def update_file(file_path: str, new_content: str):
    # 你的更新逻辑
    ...

@app.delete("/files/{file_path:path}")
async def delete_file(file_path: str):
    # 你的删除逻辑
    ...


from fastapi import FastAPI, Query
import os
from fastapi import FastAPI, Query

app = FastAPI()

@app.post("/{user_id}/{path:path}")
# user_id 是用户的主目录
# path 是子目录
# fn 是要调用的python脚本，可能包含“/”
async def dynamic_route(user_id: int, path: str = "", fn: str = Query(...)):

    base_directory = os.path.abspath(user_id)
    target_directory = os.path.abspath(os.path.join(user_id, path))

    if not str(fn).endswith(".py"):
        raise HTTPException(status_code=400, detail="Invalid file type")
    return {"user_home": user_id, "path": path, "function": fn}



from fastapi import FastAPI, Query, HTTPException, Response
import os
import importlib

app = FastAPI()

@app.get("/{user_id}/{path:path}")
# user_id 是用户的主目录
# path 是子目录
# fn 是要调用的python脚本，可能包含“/”
async def dynamic_route(user_id: int, path: str = "", fn: str = Query(...), args: str = Query(None)):
    base_directory = os.path.realpath(str(user_id))
    target_directory = os.path.realpath(os.path.join(base_directory, path))
    # 确保目标目录在基目录下
    if not target_directory.startswith(base_directory):
        raise HTTPException(status_code=400, detail="Invalid path")
    # 获取 target_directory 相对于 base_directory 的路径
    target_directory = target_directory.relative_to("./")

    # 检查文件类型
    if not fn.endswith(".py"):
        raise HTTPException(status_code=400, detail="Invalid file type")

    # 你的其他逻辑...
    module_name = str(fn).replace("/", ".").rstrip(".py")
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
        headers, content = func(argv=args) if args else func()

        # os.chdir(original_directory)
        # print("Current directory:", os.getcwd())
        
        return Response(content=content, headers=headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@app.get("/ls/")
async def list_dir(path: str = Query("", alias='id')):
    base_directory = os.path.abspath("0/")
    target_directory = os.path.abspath(os.path.join("0/", path))

    if action == "get":
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
