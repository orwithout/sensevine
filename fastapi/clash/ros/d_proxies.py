
import os
from ruamel.yaml import YAML
import shutil


def copy_file(input_file, output_file):
# 尝试复制 input_file 到 output_file
    try:
        shutil.copyfile(input_file, output_file)
    except Exception as e:
        raise RuntimeError(f"Failed to copy from '{input_file}' to '{output_file}'. Reason: {str(e)}")


#读嵌套主键
def extract_key(input_file, input_file2, output_file, key):
    copy_file(input_file2, output_file)
    os.makedirs(os.path.dirname(output_file), exist_ok=True) if os.path.dirname(output_file) else None  # 创建必要的目录
    with open(input_file, 'r', encoding="utf-8") as input_f, open(output_file, 'a', encoding="utf-8") as output_f:
        key_indent = None
        for line in input_f:
            stripped = line.lstrip()
            if stripped.startswith(f"{key}:"):
                key_indent = len(line) - len(line.lstrip(' '))
            elif key_indent is not None and not stripped.startswith("-") and (len(line) - len(line.lstrip(' '))) <= key_indent:
                break  # Stop processing once we have finished with the first occurrence of the key
            if key_indent is not None:
                output_f.write(line)


def extract_key2(input_file, input_file2, output_file, key):
    shutil.copyfile(input_file2, output_file)  # 使用 shutil.copyfile 替代了未定义的 copy_file
    os.makedirs(os.path.dirname(output_file), exist_ok=True) if os.path.dirname(output_file) else None  # 创建必要的目录
    
    yaml = YAML(typ='rt')  # 使用 'rt' 类型以保留格式信息
    yaml.width = 14096  # 设置一个足够大的行宽，以确保内容不会被折叠
    with open(input_file, 'r', encoding="utf-8") as input_f:
        data = yaml.load(input_f)
        key_data = data.get(key)
        if key_data is not None:
            with open(output_file, 'a', encoding="utf-8") as output_f:
                yaml.dump({key: key_data}, output_f)


#不少换行版：
def extract_key2(input_file, input_file2, output_file, key):
    shutil.copyfile(input_file2, output_file)  # 使用 shutil.copyfile 替代了未定义的 copy_file
    os.makedirs(os.path.dirname(output_file), exist_ok=True) if os.path.dirname(output_file) else None  # 创建必要的目录
    
    yaml = YAML(typ='rt')  # 使用 'rt' 类型以保留格式信息
    yaml.width = 4096  # 设置一个足够大的行宽，以确保内容不会被折叠
    yaml.indent(mapping=4, sequence=6, offset=4)  # 调整缩进设置以避免折叠
    with open(input_file, 'r', encoding="utf-8") as input_f:
        data = yaml.load(input_f)
        key_data = data.get(key)
        if key_data is not None:
            with open(output_file, 'a', encoding="utf-8") as output_f:
                yaml.dump({key: key_data}, output_f)





if __name__ == "__main__":
    
    input_file = "a.yaml"
    input_file2 = "c.yaml"
    output_file = "d.yaml"

    extract_key2(input_file, input_file2, output_file, 'proxies')

