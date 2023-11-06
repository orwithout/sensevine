import os
import shutil
from io import StringIO


def copy_and_append(input_file, output_file, content_to_append):
    # 检查 input_file 是否存在
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"'{input_file}' does not exist.")
    
    # 创建 output_file 所在的目录
    os.makedirs(os.path.dirname(output_file), exist_ok=True) if os.path.dirname(output_file) else None
    
    # 尝试复制 input_file 到 output_file
    try:
        shutil.copyfile(input_file, output_file)
    except Exception as e:
        raise RuntimeError(f"Failed to copy from '{input_file}' to '{output_file}'. Reason: {str(e)}")
    
    # 在 output_file 末尾追加内容
    with open(output_file, 'a', encoding="utf-8") as f:
        f.write(content_to_append)





import yaml

def modify_yaml_content(content_to_append):
    data = yaml.safe_load(content_to_append)
    
    output_lines = ["rule-providers:"]
    if 'rule-providers' in data:
        for key, value in data['rule-providers'].items():
            single_line_value = yaml.dump({key: value}, default_flow_style=True, width=float("inf")).replace("\n", "").strip()
            single_line_value = single_line_value[1:-1]  # Remove the enclosing {}
            output_lines.append("  " + single_line_value)

    return "\n".join(output_lines)



def modified_copy_and_append(input_file, output_file, content_to_append):
    # Modify the content_to_append to ensure each item is written in one line.
    modified_content = modify_yaml_content(content_to_append)
    
    # 检查 input_file 是否存在
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"'{input_file}' does not exist.")
    
    # 创建 output_file 所在的目录
    os.makedirs(os.path.dirname(output_file), exist_ok=True) if os.path.dirname(output_file) else None
    
    # 尝试复制 input_file 到 output_file
    try:
        shutil.copyfile(input_file, output_file)
    except Exception as e:
        raise RuntimeError(f"Failed to copy from '{input_file}' to '{output_file}'. Reason: {str(e)}")
    
    # 在 output_file 末尾追加内容
    with open(output_file, 'a', encoding="utf-8") as f:
        f.write(modified_content)
        f.write("\n\n")



content_to_append = '''



rule-providers:
  # https://github.com/dler-io/Rules/tree/main/Clash/Provider/Media
  Speedtest:
    type: http
    behavior: classical
    url: 'https://api.sensevine.com/1234567/clash/rule_providers/Speedtest.yaml/raw'
    path: ./Rules/Speedtest
    interval: 86400
  OpenAI:
    type: http
    behavior: classical
    url: 'https://api.sensevine.com/1234567/clash/rule_providers/OpenAI.yaml/raw'
    path: ./Rules/OpenAI
    interval: 86400

  
  # https://github.com/Loyalsoldier/clash-rules
  apple:
    type: http
    behavior: domain
    url: "https://api.sensevine.com/1234567/clash/rule_providers/apple.txt/raw"
    path: ./ruleset/apple.yaml
    interval: 86400
  applications:
    type: http
    behavior: classical
    url: "https://api.sensevine.com/1234567/clash/rule_providers/applications.txt/raw"
    path: ./ruleset/applications.yaml
    interval: 86400
  cncidr:
    type: http
    behavior: ipcidr
    url: "https://api.sensevine.com/1234567/clash/rule_providers/cncidr.txt/raw"
    path: ./ruleset/cncidr.yaml
    interval: 86400
  direct:
    type: http
    behavior: domain
    url: "https://api.sensevine.com/1234567/clash/rule_providers/direct.txt/raw"
    path: ./ruleset/direct.yaml
    interval: 86400
  gfw:
    type: http
    behavior: domain
    url: "https://api.sensevine.com/1234567/clash/rule_providers/gfw.txt/raw"
    path: ./ruleset/gfw.yaml
    interval: 86400
  google:
    type: http
    behavior: domain
    url: "https://api.sensevine.com/1234567/clash/rule_providers/google.txt/raw"
    path: ./ruleset/google.yaml
    interval: 86400
  icloud:
    type: http
    behavior: domain
    url: "https://api.sensevine.com/1234567/clash/rule_providers/icloud.txt/raw"
    path: ./ruleset/icloud.yaml
    interval: 86400
  lancidr:
    type: http
    behavior: ipcidr
    url: "https://api.sensevine.com/1234567/clash/rule_providers/lancidr.txt/raw"
    path: ./ruleset/lancidr.yaml
    interval: 86400
  private:
    type: http
    behavior: domain
    url: "https://api.sensevine.com/1234567/clash/rule_providers/private.txt/raw"
    path: ./ruleset/private.yaml
    interval: 86400
  proxy:
    type: http
    behavior: domain
    url: "https://api.sensevine.com/1234567/clash/rule_providers/proxy.txt/raw"
    path: ./ruleset/proxy.yaml
    interval: 86400
  reject:
    type: http
    behavior: domain
    url: "https://api.sensevine.com/1234567/clash/rule_providers/reject.txt/raw"
    path: ./ruleset/reject.yaml
    interval: 86400
  telegramcidr:
    type: http
    behavior: ipcidr
    url: "https://api.sensevine.com/1234567/clash/rule_providers/telegramcidr.txt/raw"
    path: ./ruleset/telegramcidr.yaml
    interval: 86400
  tld-not-cn:
    type: http
    behavior: domain
    url: "https://api.sensevine.com/1234567/clash/rule_providers/tld-not-cn.txt/raw"
    path: ./ruleset/tld-not-cn.yaml
    interval: 86400

        
'''





if __name__ == "__main__":

    input_file = "d.yaml"
    output_file = "e.yaml"
    modified_copy_and_append(input_file, output_file, content_to_append)

