import os
import subprocess


def gen_conf(headers_file='a.headers.txt', body_file='h.yaml', argv='win'):


    # 获取当前脚本的绝对路径
    current_script_path = os.path.abspath(__file__)

    # 获取当前脚本的目录
    current_script_dir = os.path.dirname(current_script_path)
    print("current_script_dir:", current_script_dir)


    print("Current directory:", os.getcwd())
    original_directory = os.getcwd()

    os.chdir(os.path.join(current_script_dir, argv))
    print("Current directory:", os.getcwd())

    try:
        # 使用 subprocess 执行脚本, 生成h.yaml
        subprocess.run(['/usr/bin/python3', 'a_download.py'], check=True)
        subprocess.run(['/usr/bin/python3', 'b_init.py'], check=True)
        subprocess.run(['/usr/bin/python3', 'c_dns.py'], check=True)
        subprocess.run(['/usr/bin/python3', 'd_proxies.py'], check=True)
        subprocess.run(['/usr/bin/python3', 'e_rule_providers.py'], check=True)
        subprocess.run(['/usr/bin/python3', 'f_proxy_groups_country.py'], check=True)
        subprocess.run(['/usr/bin/python3', 'g_proxy_groups_def.py'], check=True)
        subprocess.run(['/usr/bin/python3', 'h_rules.py'], check=True)


    except subprocess.CalledProcessError:
        raise Exception("Error occurred while executing one of the scripts.")


    headers = {}
    with open(headers_file, 'r') as file:
        for line in file.readlines():
            key, value = line.strip().split(': ', 1)
            headers[key] = value

    # 读取body_file文件的内容
    with open(body_file, 'r', encoding='utf-8') as file:
        content = file.read()


    os.chdir(original_directory)
    print("Current directory:", os.getcwd())
    return headers, content



# 下面的代码块只在脚本单独执行时运行
if __name__ == "__main__":
    headers_file = "a.headers.txt"
    body_file = "h.yaml"
    gen_conf(headers_file, body_file, 'win')