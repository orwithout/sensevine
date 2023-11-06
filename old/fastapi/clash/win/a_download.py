import requests
import os
import sys
import time
#pip install ruamel.yaml requests


# 下载文件    (如果文件存在，且大小不为0，且最后修改时间距离现在的秒数小于给定的参数，则跳过下载
def download_file(url, output_file, output_file2, download_name, skip_if_modified_within_seconds=0):
    # Check if the file exists, is not empty, and was modified within the specified time range
    if (os.path.exists(output_file) and os.path.getsize(output_file) > 0 and
        (time.time() - os.path.getmtime(output_file)) <= skip_if_modified_within_seconds):
        return

    response = requests.get(url)
    

    response.raise_for_status()  # Raise an exception for HTTP errors

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True) if os.path.dirname(output_file) else None

    # Write the content to the output file
    with open(output_file, 'wb') as file:
        file.write(response.content)

    # 获取原始的HTTP头
    headers = dict(response.headers)

    # 修改headers 中下载文件名
    if "Content-Disposition" in headers:
        disposition = headers["Content-Disposition"].replace("Dler Cloud - Love.yaml", download_name)
        headers["Content-Disposition"] = disposition

    # 删除Content-Length头，让FastAPI自动为你设置
    if "Content-Length" in headers:
        del headers["Content-Length"]

    with open(output_file2, 'w') as file:
        for key, value in headers.items():
            file.write(f"{key}: {value}\n")

# Testing the function with one of the earlier URLs
# download_file("https://raw.githubusercontent.com/dler-io/Rules/main/Clash/Provider/OpenAI.yaml", "OpenAI.yaml")
# Since we can't access external URLs in this environment, we've commented out the test. But you can run it on your machine.



if __name__ == "__main__":
    
    source_url = "https://dler.cloud/subscribe/Qfefefeffffffffffg?clash=smart&type=love"


    # https://github.com/Loyalsoldier/clash-rules  #优选 无fake-ip-filter
    # https://raw.githubusercontent.com/G4free/clash-ruleset/main/ruleset/ChatGPT.yaml  #补充 chatGPT


    # https://github.com/dler-io/Rules #商业 有fake-ip-filter  视频分流超详细
    # https://github.com/vernesong/OpenClash/blob/master/luci-app-openclash/root/etc/openclash/custom/openclash_custom_fake_filter.list  #openclash 官方  有fake-ip-filter

    # https://github.com/GeQ1an/Rules/blob/master/Clash/Clash.yaml  #基于 dler-io
    # https://github.com/blackmatrix7/ios_rule_script  #综合 ？

    output_file = "a.yaml"
    output_file2 = "a.headers.txt"
    download_name = "hahaha.yaml"
    seconds = int(sys.argv[1]) if len(sys.argv) > 1 else 3600

    download_file(source_url, output_file, output_file2, download_name, seconds)

