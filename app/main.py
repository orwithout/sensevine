from fastapi import FastAPI, Query, HTTPException, Response
import os
import importlib
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
        # 动态导入模块
        module = importlib.import_module(module_name)

        # 从模块中获取函数并执行它
        func = getattr(module, path.split("/")[-1].rstrip(".py"))


        result = func(args=args) if args else func()

        
        headers, content = func(args=args) if args else func()

        
        return Response(content=content, headers=headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # except HTTPException as e:
    #     # 直接抛出 HTTPException 异常
    #     raise e
    # except Exception as e:
    #     # 在生产环境中，你可能不想公开底层错误的详细信息
    #     print(e)  # 仅用于调试
    #     raise HTTPException(status_code=500, detail="Internal Server Error")




from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import os
import importlib
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

@app.get("/{user_id}/{path:path}")
async def dynamic_route(user_id: int, path: str = "", fn: str = Query(...), args: str = Query(None)):
    # 省略安全和路径处理的代码...

    try:
        module = importlib.import_module("your_module")
        func = getattr(module, "your_function")
        result = func(args=args) if args else func()

        if isinstance(result, dict):
            return JSONResponse(content=result)
        else:
            # 如果结果不是字典，你可以选择如何处理
            return result
    except HTTPException as e:
        # 直接抛出 HTTPException 异常
        raise e
    except Exception as e:
        # 在生产环境中，你可能不想公开底层错误的详细信息
        print(e)  # 仅用于调试
        raise HTTPException(status_code=500, detail="Internal Server Error")
