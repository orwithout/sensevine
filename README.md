# Sensevine 项目设置说明文档

此文档将指导您如何在 Windows 和 Linux 系统上设置并运行 Sensevine 项目。




## 一、针对 Windows 用户

### 步骤 1：克隆项目

打开命令提示符（Cmd）并运行以下命令以克隆项目：

```bash
git clone https://www.github.com/orwithout/sensevine.git
```

### 步骤 2：安装后端依赖并运行后端

1. 访问 [Python 官方下载页面](https://www.python.org/downloads/windows/)
2. 选择适合您的 Windows 版本的 Python 3 安装程序
3. 下载并运行安装程序，记得在安装过程中选择“Add Python 3.x to PATH”
   
4. 导航到 `sensevine/fastapi` 目录：
    ```bash
    cd sensevine/fastapi
    ```
5. 安装依赖：
    ```bash
    pip install -r requirements.txt
    ```
6. 运行后端：
    ```bash
    uvicorn main:app --reload
    ```

### 步骤 3：安装前端依赖并运行前端
1. 访问 [Node.js 官方下载页面](https://nodejs.org/zh-cn)
2. 选择适合您的 Windows 版本
3. 下载并运行安装程序
   
4. 导航到 `sensevine/svelte` 目录：
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

## 二、针对 Linux 用户

### 步骤 1：克隆项目

打开终端并运行以下命令以克隆项目：

```bash
git clone https://www.github.com/orwithout/sensevine.git
```

### 步骤 2：安装后端依赖并运行后端

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

3. 导航到 `sensevine/fastapi` 目录：
    ```bash
    cd sensevine/fastapi
    ```
4. 安装依赖：
    ```bash
    pip install -r requirements.txt
    ```
5. 运行后端：
    ```bash
    uvicorn main:app --reload
    ```

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
    nvm install node
    ```

5. 导航到 `sensevine/svelte` 目录：
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
