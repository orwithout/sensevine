# senseVine 项目说明

查看： [设计文档](https://github.com/orwithout/sensevine/tree/main/doc)




## 一、演示
**DEMO** v0.0.1: http://sensevine.com


## 二、开发环境设定（针对 Windows 用户）

### 步骤 1：克隆项目

打开电脑系统的命令提示符（Cmd）并运行以下命令以克隆项目：

```bash
# 需要先安装git: https://git-scm.com/book/zh/v2/%E8%B5%B7%E6%AD%A5-%E5%AE%89%E8%A3%85-Git
git clone https://www.github.com/orwithout/sensevine.git
```

### 步骤 2：安装后端依赖并运行后端

1. 访问 [Python 官方下载页面](https://www.python.org/downloads/windows/)
2. 选择适合您的 Windows 版本的 Python 3 安装程序
3. 下载并运行安装程序，记得在安装过程中选择“Add Python 3.x to PATH”
   
4. 导航到克隆下来的 `sensevine/fastapi` 目录：
    ```bash
    cd sensevine/fastapi
    ```
5. 安装依赖：
    ```bash
    pip install -r requirements.txt
    ```
6. 运行后端：
    ```bash
    uvicorn svd:app --reload --host 0.0.0.0 --port 8002
    ```
7. 问题，如果出现问题，可能需要给fastapi/svd.py 添加可执行权限：
    ```bash
    chmod +x svd.py
    ```
### 步骤 3：安装前端依赖并运行前端
1. 访问 [Node.js 官方下载页面](https://nodejs.org/zh-cn)
2. 选择适合您的 Windows 版本
3. 下载并运行安装程序
   
4. 导航到克隆下来的 `sensevine/svelte` 目录：
    ```bash
    cd sensevine/svelte
    ```
5. 安装依赖：
    ```bash
    npm install
    ```
6. 运行前端：
    ```bash
    npm run dev
    ```

---

## 三、开发环境设定（针对 Linux 用户）

### 步骤 1：克隆项目

打开终端并运行以下命令以克隆项目：

```bash
# 需要先安装git: https://git-scm.com/book/zh/v2/%E8%B5%B7%E6%AD%A5-%E5%AE%89%E8%A3%85-Git
git clone https://www.github.com/orwithout/sensevine.git
```

### 步骤 2：安装后端依赖并运行后端主程序svd.py

1. 打开终端
2. 运行以下命令以使用包管理器安装 Python 3：
    ```bash
    #ubuntu
    sudo apt-get update
    sudo apt-get install python3
    ```
    ```bash
    # centos
    sudo yum update
    sudo yum install python3
    ```

3. 导航到克隆下来的 `sensevine/fastapi` 目录：
    ```bash
    cd sensevine/fastapi
    ```
4. 安装依赖：
    ```bash
    pip install -r requirements.txt
    ```
5. 运行后端：
    ```bash
    uvicorn svd:app --reload --host 0.0.0.0 --port 8002
    ```
- **[fastapi入门参考](https://fastapi.tiangolo.com/zh/#:~:text=%E8%B4%9F%E8%B4%A3%E6%95%B0%E6%8D%AE%E9%83%A8%E5%88%86%E3%80%82-,%E5%AE%89%E8%A3%85,-%C2%B6)**

### 步骤 3：安装前端依赖并运行前端
1. 打开终端
2. 运行以下命令以安装nvm：
   ```bash
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
   # 或：
   wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
   ```
3. 安装完成后，重启终端或命令提示符
4. 运行以下命令以安装 Node.js：
    ```bash
    source ~/.bashrc  #刷新环境
    nvm install node
    ```

5. 导航到克隆下来的 `sensevine/svelte` 目录：
    ```bash
    cd sensevine/svelte
    ```
6. 安装依赖：
    ```bash
    npm install
    ```
7. 运行前端：
    ```bash
    npm run dev
    ```
- **前端可以静态部署**
如果是生产环境，可以在sensevine/svelte 中执行：
    ```bash
    npm run build
    ```

  然后将sensevine/svelte/public 目录做静态部署

- **如何初始化一个新的svelte项目？**
    ```bash
    npx degit sveltejs/template your-project-name
    #如果使用typescript模板：npx degit sveltejs/template#typescript 
    cd your-project-name
    npm install  #安装依赖
    npm run dev  #运行服务，会实时编译，方便开发调试
    #如果要构建生成版本，以静态部署：npm run build
    #编译后将your-project-name/src/public进行静态部署即可，具体可查看或修改rollup.config.js
    ```

    初始化新项目后，可以通过修改your-project-name/src/main.js 和your-project-name/src/App.svelte文件来开始创建你自己的页面。  
src/main.js：这是应用程序的入口点。通常，你只需在这里初始化并挂载主Svelte组件。但你也可以在这里进行一些全局设置，如路由、状态管理等。  
src/App.svelte：这通常是主要的Svelte组件，它会被挂载到public/index.html中的某个元素上。  

---

### 关于 `node_modules` 和 `package-lock.json`

通常，在将前端代码上传到 GitHub 时，建议您删除 `sensevine/svelte` 目录下的 `node_modules` 和 `package-lock.json`。这样做是因为 `node_modules` 包含了大量的依赖文件，而 `package-lock.json` 是自动生成的。这两者都不需要在版本控制系统中跟踪。

对于Linux系统，您可以使用以下命令进行删除：

```bash
# 删除 node_modules 目录
rm -rf sensevine/svelte/node_modules

# 删除 package-lock.json 文件
rm sensevine/svelte/package-lock.json
```

然后，您可以将项目推送到 GitHub。


### 框架文档
1. 后端 [FastAPI 官方文档](https://fastapi.tiangolo.com/zh/)
2. 前端 [Svelte 官方文档](https://svelte.dev/examples/file-inputs)






# Nginx 配置指南
请自行替配置文件中使用的域名
## 安装 Nginx

### Ubuntu

```bash
sudo apt update
sudo apt install nginx
```

## 启动和停止 Nginx

启动 Nginx：

```bash
sudo systemctl start nginx
```

停止 Nginx：

```bash
sudo systemctl stop nginx
```


## 配置虚拟主机

在 `/etc/nginx/sites-available/` 目录下创建一个新的配置文件，例如 `sensevine.com`：

```bash
sudo nano /etc/nginx/sites-available/sensevine.com
```

然后将以下内容粘贴到该文件中：

```nginx
server {
    listen 80;
    server_name sensevine.com www.sensevine.com;

    root /var/www/svelte;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}

server {
    listen 80;
    server_name api.sensevine.com;

    location / {
        proxy_pass http://localhost:8002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

保存并退出编辑器。

接下来，创建一个软链接到 `/etc/nginx/sites-enabled/` 目录：

```bash
sudo ln -s /etc/nginx/sites-available/sensevine.com /etc/nginx/sites-enabled/
```

测试 Nginx 配置以确保没有语法错误：

```bash
sudo nginx -t
```

如果测试成功，重新加载 Nginx 以应用新的配置：

```bash
sudo systemctl reload nginx
```

现在，您应该可以通过访问 `http://sensevine.com` 和 `http://api.sensevine.com` 来看到相应的内容。




# Systemd 启动使用说明

- 后端svd.py 的systemd 启动模板 ：

    ```
    [Unit]
    Description=senseVine-backend
    After=network.target

    [Service]
    Type=simple
    User=mian
    Group=mian
    WorkingDirectory=/home/mian/senseVine/fastapi
    ExecStart=/home/mian/.local/bin/uvicorn svd:app --port 8002
    ExecReload=/bin/kill -HUP ${MAINPID}
    RestartSec=1
    Restart=always


    [Install]
    WantedBy=multi-user.target
    ```


1. **编辑其中 `WorkingDirectory、User、Group、ExecStart`字段**: 确保都设置为您的工作目录或用户。
2. **保存为 `/etc/systemd/system/svd.service`**

## 基础命令

- **启动服务**
    ```bash
    sudo systemctl start svd.service
    ```
    使用此命令启动名为 `svd.service` 的 systemd 服务。

- **设置开机自启**
    ```bash
    sudo systemctl enable svd.service
    ```
    使用此命令将 `svd.service` 设置为开机自启动。

- **查看服务状态**
    ```bash
    sudo systemctl status svd.service
    ```
    使用此命令可以查看 `svd.service` 的运行状态信息。

## 复合命令

- **一键操作**
    ```bash
    sudo cp svd.service /etc/systemd/system/ && sudo systemctl daemon-reload && sudo systemctl start svd.service ;sudo systemctl status svd.service
    ```
    这是一个复合命令，用于一次性执行多个操作：复制服务文件、重新加载 systemd、启动服务，并查看其状态。

## 其他命令

- **重新加载 systemd**
    ```bash
    sudo systemctl daemon-reload
    ```
    当你修改了 systemd 的服务定义文件后，使用此命令使改动生效。

- **查看最近的 50 条日志**
    ```bash
    journalctl -u svd.service -n 50
    ```
    使用此命令可以查看 `svd.service` 的最近 50 条日志。

- **查看最近 10 分钟的日志**
    ```bash
    journalctl -u svd.service --since "10 minutes ago"
    ```
    使用此命令查看过去 10 分钟内 `svd.service` 的日志。

- **实时查看 Nginx 错误日志**
    ```bash
    sudo tail -f /var/log/nginx/error.log
    ```
    使用此命令可以实时查看 Nginx 的错误日志。
