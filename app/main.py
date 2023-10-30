from fastapi import FastAPI, Query, HTTPException, Header, File, UploadFile
import os
import importlib
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, PlainTextResponse, Response

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



import aiofiles
from tempfile import NamedTemporaryFile
async def handle_upload(file: UploadFile, user_id: int):
    tmp_dir = os.path.join(str(user_id), 'tmp')
    os.makedirs(tmp_dir, exist_ok=True)
    
    with NamedTemporaryFile(delete=False, dir=tmp_dir) as temp_file:
        async with aiofiles.open(temp_file.name, 'wb') as out_file:
            while content := await file.read(1024):
                await out_file.write(content)
        
        return temp_file.name


import inspect
import logging
logger = logging.getLogger(__name__)
from pathlib import Path

@app.api_route("/{user_id}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
# user_id 是用户的主目录
# path 是子目录
# fn 是要调用的python脚本，可能包含“/”
async def dynamic_route(user_id: int = 0, path: str = "", file: UploadFile = File(None), fn: str = Query("main_2_crud/read.py"), args: str = Query(None), accept: str = Header(None)):
    base_dir = Path(str(user_id)).resolve()
    full_path = (base_dir / path).resolve()

    # 确保目标路径在基目录下
    if not full_path.is_relative_to(base_dir):
        raise HTTPException(status_code=400, detail="Invalid path")

    # 获取 target_dir 相对于 base_dir 的路径
    sub_path = full_path.relative_to(base_dir)

    if not fn.endswith(".py"):
        raise HTTPException(status_code=400, detail="Invalid file type")

    # 如果有上传文件，保存到 temp_file_path
    if file:
        try:
            temp_file_path = await handle_upload(file, base_dir)
            # 现在你可以使用 temp_file_path 来处理上传的文件了
            # 例如：result = some_function(file_path=temp_file_path)
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"File upload error: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error file")
    else:
        temp_file_path = None

    # 获取模块名、函数名（约定：文件中必须定义与文件名同名的函数）
    module_name = str(fn).replace("/", ".").rstrip(".py")
    function_name = os.path.basename(fn).rstrip(".py")
    print(fn)
    print(module_name)
    print(function_name)
    try:
        module = importlib.import_module(module_name)
        if hasattr(module, function_name):
            # 获取目标函数
            func = getattr(module, function_name)
            # 获取 func 函数的参数信息
            parameters = inspect.signature(func).parameters
            
            # 准备要传递给函数的参数
            func_args = {'user_id': user_id, 'full_path': full_path, 'sub_path': sub_path, 'file_contents': temp_file_path, 'args': args}
            
            # 过滤掉不在函数参数列表中的参数
            filtered_args = {k: v for k, v in func_args.items() if k in parameters}

            if accept == "application/json":
                result = func(**filtered_args)
                return JSONResponse(content=result)
            elif accept == "text/plain":
                headers, content = func(**filtered_args)
                return Response(content=content, headers=headers)
            else:
                # If Accept header is not provided, default to JSON
                result = func(**filtered_args)
                return JSONResponse(content=result)
    except Exception as e:
        # traceback.print_exc()
        logger.error(f"Internal server error: {str(e)}", extra={"user_id": user_id, "path": sub_path, "function": fn})
        raise HTTPException(status_code=500, detail="Internal Server Error")

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            logger.info(f"Temporary file {temp_file_path} has been deleted.")


