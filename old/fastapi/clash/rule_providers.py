import os
import subprocess
def update_or_clone_repo(directory_name="rule_providers"):
    repo_url = "https://github.com/Loyalsoldier/clash-rules.git"
    branch = "release"
    
    # Check if directory exists
    if not os.path.exists(directory_name):
        # Clone the repo if directory doesn't exist
        subprocess.run(["git", "clone", repo_url, directory_name, "--branch", branch, "--single-branch"])
    else:     
        subprocess.run(["git", "reset", "--hard", "HEAD"], cwd=directory_name)
        subprocess.run(["git", "pull"], cwd=directory_name)


import requests
def download_file(url: str, save_path: str):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    with open(save_path, 'wb') as f:
        f.write(response.content)





def rule_providers():
    directory_name = "rule_providers"
    # 获取当前脚本的绝对路径
    current_script_path = os.path.abspath(__file__)

    # 获取当前脚本的目录
    current_script_dir = os.path.dirname(current_script_path)
    print("current_script_dir:", current_script_dir)
    original_directory = os.getcwd()

    os.chdir(current_script_dir)
    print("Current directory:", os.getcwd())


    update_or_clone_repo(directory_name)

    os.chdir(directory_name)
    print("Current directory:", os.getcwd())

    # 下载文件
    download_file("https://raw.githubusercontent.com/dler-io/Rules/main/Clash/Provider/OpenAI.yaml", "OpenAI.yaml")
    download_file("https://raw.githubusercontent.com/dler-io/Rules/main/Clash/Provider/Speedtest.yaml", "Speedtest.yaml")







# 下面的代码块只在脚本单独执行时运行
if __name__ == "__main__":
    rule_providers()
