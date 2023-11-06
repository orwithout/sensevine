import re
from copy import deepcopy
import shutil
import yaml
#pip install ruamel.yaml



def copy_file(input_file, output_file):
# 尝试复制 input_file 到 output_file
    try:
        shutil.copyfile(input_file, output_file)
    except Exception as e:
        raise RuntimeError(f"Failed to copy from '{input_file}' to '{output_file}'. Reason: {str(e)}")



#proxy-groups组的 "name" 字段
def extract_proxies_names(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    names = [proxy['name'] for proxy in data.get('proxy-groups', [])]
    return names




# 在 proxy-groups: 后面追加内容
def insert_after_proxy_groups(file_path, content_to_insert):
    # 读取文件的所有内容
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # 找到'proxy-groups:'行的位置
    for i, line in enumerate(lines):
        if line.strip() == "proxy-groups:":
            # 插入内容到该行的后面
            lines.insert(i + 1, content_to_insert + "\n")
            break
    
    # 将修改后的内容重新写入文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)




def append_proxies_to_file(file_path, classified, sort_keywords, proxies_params, proxies_name='Auto_Url_Test'):
    # Since 'classified' is a list of proxy names, we'll use it directly as 'countries'
    countries = classified
    group = deepcopy(proxies_params)  # Use a deep copy of the passed dictionary to create a new proxy group
    group['name'] = proxies_name
    group['proxies'].extend(countries)  # Add proxy list to proxy group
    group['proxies'].sort(key=lambda proxy: [re.search(keyword, proxy) is not None for keyword in sort_keywords[proxies_name]], reverse=True)
    
    # Convert the group to a YAML string with specific settings
    group_yaml = yaml.dump(group, default_flow_style=True, allow_unicode=True, width=float("inf")).strip()
    

    
    # Append the generated YAML string to the file
    insert_after_proxy_groups(file_path, "- " + group_yaml)






#定义节点排序的关键字
sort_keywords = {
    'Auto_Url_Test': (r'([一-龥]+)',),  #表示匹配汉字：[一-龥]
    'common': (r'(REJECT)',r'(DIRECT)',r'(Auto_Url_Test)',r'([a-zA-Z])',r'(香港)',r'(新加坡)',r'(美国)',r'(韩国)',r'(台湾)',r'(日本)',),
    'PROXY': (r'(Auto_Url_Test)',r'(新加坡)',r'(香港)',r'(韩国)',r'(台湾)',r'(日本)',r'(美国)',r'([一-龥]+)',),
    'PROXY1': (r'(美国)',r'(新加坡)',r'(台湾)',r'(韩国)',r'(日本)',r'([一-龥]+)',),
    'PROXY2': (r'(美国)',r'(新加坡)',r'(台湾)',r'(韩国)',r'(日本)',r'([一-龥]+)',),
    'ChatGPT': (r'(韩国)',r'(美国)',r'(新加坡)',),
    'AdBlock': (r'(REJECT)',),
    'dev': (r'(DIRECT)',r'(Auto_Url_Test)',),
    'IPtest': (r'([a-zA-Z]+)',),
    # Add more rules as needed...
}




#添加url-test类型代理组
proxies_params_auto_url_test = {
    'name': 'Auto_Url_Test',
    'type': 'url-test',
    'url': 'http://cp.cloudflare.com/generate_204',
    'interval': 3600,
    'proxies': [],

}

#添加select类型代理组
proxies_params_select = {
    'name': 'Proxy',
    'type': 'select',
    'proxies': ["Auto_Url_Test", "DIRECT", "REJECT",],   #请自行注意 Auto_Url_Test 代理是否添加且名字匹配
}

#添加select类型代理组-选择应用
proxies_params_select_app = {
    'name': 'app',
    'type': 'select',
    'proxies': ["PROXY", "PROXY1", "PROXY2", "Auto_Url_Test", "DIRECT", "REJECT"],   #请自行注意 PROXY PROXY1 PROXY2…… 代理是否添加且名字匹配
}

#添加select类型代理组-选择应用
proxies_params_select_iptest = {
    'name': 'app',
    'type': 'select',
    'proxies': ["ChatGPT", "PROXY", "PROXY1", "PROXY2", "Auto_Url_Test", "DIRECT", "REJECT"],   #请自行注意 PROXY PROXY1 PROXY2…… 代理是否添加且名字匹配
}

#添加select类型代理组-选择应用
proxies_params_select_ad = {
    'name': 'AdBlock',
    'type': 'select',
    'proxies': ["REJECT", "DIRECT", "Auto_Url_Test", "PROXY1", "PROXY2"],   #请自行注意 PROXY PROXY1 PROXY2…… 代理是否添加且名字匹配
}






if __name__ == "__main__":
    input_file = "f.yaml"
    output_file = "g.yaml"

    copy_file(input_file, output_file)
    names = extract_proxies_names(output_file)
    print (names)
    append_proxies_to_file(output_file, names, sort_keywords, proxies_params_select_app,'dev')
    append_proxies_to_file(output_file, names, sort_keywords, proxies_params_auto_url_test,'Auto_Url_Test')
    append_proxies_to_file(output_file, names, sort_keywords, proxies_params_select_ad,'AdBlock')
    append_proxies_to_file(output_file, names, sort_keywords, proxies_params_select_iptest,'IPtest')
    append_proxies_to_file(output_file, names, sort_keywords, proxies_params_select_app,'ChatGPT')
    append_proxies_to_file(output_file, names, sort_keywords, proxies_params_select,'PROXY2')
    append_proxies_to_file(output_file, names, sort_keywords, proxies_params_select,'PROXY1')
    append_proxies_to_file(output_file, names, sort_keywords, proxies_params_select,'PROXY')



