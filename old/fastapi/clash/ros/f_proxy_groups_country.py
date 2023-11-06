import re
import os
import sys
import shutil


from ruamel.yaml import YAML

#pip install ruamel.yaml requests

from copy import deepcopy


def copy_file(input_file, output_file):
# 尝试复制 input_file 到 output_file
    try:
        shutil.copyfile(input_file, output_file)
    except Exception as e:
        raise RuntimeError(f"Failed to copy from '{input_file}' to '{output_file}'. Reason: {str(e)}")
    

#提取proxies组的 "name" 字段
def extract_proxies_names(file_path):
    yaml = YAML(typ="safe")
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.load(file)
    names = [proxy['name'] for proxy in data.get('proxies', [])]
    return names



#根据国家代码对 "name" 字段的值进行分类, 按规则返回截取后的name字段的子串（目标是国家名称或代码）
def slice_proxies_name(name, slice_rule):
    if all(isinstance(item, int) for item in slice_rule):
        start, length = slice_rule
        return name[start:start+length]
    if isinstance(slice_rule[0], str) and isinstance(slice_rule[1], int):
        start_str, length = slice_rule
        start = name.find(start_str) + len(start_str) if name.find(start_str) != -1 else 0
        return name[start:start+length]
    if all(isinstance(item, str) for item in slice_rule):
        start_str, end_str = slice_rule
        start_index = name.find(start_str)
        end_index = name.find(end_str, start_index + len(start_str))
        if start_index == -1 or end_index == -1:
            return ""
        return name[start_index + len(start_str):end_index]
    if isinstance(slice_rule[0], int) and isinstance(slice_rule[1], str):
        start, end_str = slice_rule
        end_index = name.find(end_str, start)
        return name[start:] if end_index == -1 else name[start:end_index]
    return name

# 根据国家代码对 "name" 字段的值进行分类,
def classify_proxies_name(names, country_codes, slice_rule=None):
    classified = {country_values[0]: [] for country_values in country_codes.values()}
    # print("slice_rules规则截取后的节点名称:")
    for name in names:
        sliced_name = slice_proxies_name(name, slice_rule) if slice_rule else name
        # print(sliced_name)
        for code, country_values in country_codes.items():
            if code.lower() in sliced_name.lower() or any(country.lower() in sliced_name.lower() for country in country_values):
                classified[country_values[0]].append(name)
                break
        else:
            classified.setdefault('其它', []).append(name)
    return classified






#将分类后的数据写入输出文件
def custom_yaml_format(data):
    """
    Custom formatting function to generate the desired YAML output format in a single line.
    """
    output = []
    for group in data['proxy-groups']:
        formatted_proxies = ", ".join([f"'{proxy}'" for proxy in group['proxies']])
        
        group_items = [
            f"name: {group['name']}",
            f"type: {group['type']}",
            f"url: {group['url']}",
            f"interval: {group['interval']}",
            f"proxies: [{formatted_proxies}]"
        ]
        output_group = "- {" + ", ".join(group_items) + "}"
        output.append(output_group)
    return "proxy-groups:\n" + "\n".join(output) + "\n"




def write_classify_proxies_to_output(output, classified, sort_keywords, proxies_params):
    data = {'proxy-groups': []}
    for country, names in classified.items():
        if names:
            group = deepcopy(proxies_params)  # 使用传入的字典的深拷贝来创建新的代理组
            group['name'] = country
            group['proxies'] = group['proxies'] + names  # 创建新的代理列表并添加代理
            group['proxies'].sort(key=lambda proxy: [re.search(keyword, proxy) is not None for keyword in sort_keywords], reverse=True)
            data['proxy-groups'].append(group)
    formatted_yaml = custom_yaml_format(data)
    output.write(formatted_yaml)




#用于分割节点名称的规则,提取国家代码，例如提取： name: '🇵🇭 菲律宾 IEPL [03] [Air]',  中的 菲律宾
slice_rules = {
    'ZHS1': (".", "/"),
    'ZHS2': (3, 5),
    'ZHS3': ('.', 3),
    'ZHS4': (3, '/'),
    'dler1': (' ', ' '),
    'dler2': (3, ' '),
    # Add more rules as needed...
}

#定义节点排序的关键字
sort_keywords = {
    'ZHS1': (r'(AC)', r'IEPL\s+\[\d+\]\s+\[Premium\]', r'IEPL\s+\[\d+\]\s+\[Std\]', r'IEPL\s+\[\d+\]\s+\[Lite\]', r'(DMIT|Aliyun|BBTEC|GIA)', r'(EDGE)',),
    'ZHS2': ('ghi', 'jkl',),
    'dler1': (r'(AC)', r'IEPL\s+\[\d+\]\s+\[Premium\]', r'IEPL\s+\[\d+\]\s+\[Std\]', r'IEPL\s+\[\d+\]\s+\[Lite\]', r'(DMIT|Aliyun|BBTEC|GIA)', r'(EDGE)',),
    'dler2': (r'IEPL\s+\[\d+\]\s+\[Premium\]', r'(AC)', r'IEPL\s+\[\d+\]\s+\[Std\]', r'IEPL\s+\[\d+\]\s+\[Lite\]', r'(DMIT|Aliyun|BBTEC|GIA)', r'(EDGE)',),
    'url_est': (r'([一-龥]+)',),  #表示匹配汉字：[一-龥]
    # Add more rules as needed...
}

#添加fallback类型代理组
proxies_params_fallback = {
    'name': 'Fallback',
    'type': 'fallback',
    'url': 'http://cp.cloudflare.com/generate_204',
    'interval': 7200,
    'proxies': [],
}




country_codes = {
    "ad": ["安道尔", "安道尔公国"],
    "ae": ["阿拉伯", "阿拉伯联合酋长国"],
    "af": ["阿富汗", "阿富汗伊期兰共和国"],
    "ag": ["安提瓜和巴布达"],
    "ai": ["安圭拉"],
    "al": ["阿尔巴尼亚"],
    "am": ["亚美尼亚"],
    "an": ["安的列斯", "安的列斯群岛", "荷属安的列斯群岛", "安的列斯群岛（荷属）"],
    "ao": ["安哥拉"],
    "aq": ["南极洲"],
    "ar": ["阿根廷"],
    "arpa": ["老式阿帕网"],
    "as": ["美属萨摩亚"],
    "at": ["奥地利"],
    "au": ["澳大利亚"],
    "aw": ["阿鲁巴"],
    "az": ["阿塞拜疆"],
    "ba": ["波斯尼亚", "波斯尼亚-黑塞哥维纳"],
    "bb": ["巴巴多斯"],
    "bd": ["孟加拉国"],
    "be": ["比利时"],
    "bf": ["布基纳法索"],
    "bg": ["保加利亚"],
    "bh": ["巴林"],
    "bi": ["布隆迪"],
    "bj": ["贝宁"],
    "bm": ["百慕大"],
    "bn": ["文莱", "文莱达鲁萨兰国"],
    "bo": ["玻利维亚"],
    "br": ["巴西"],
    "bs": ["巴哈马"],
    "bt": ["不丹"],
    "bv": ["博维特岛"],
    "bw": ["博茨瓦纳"],
    "by": ["白俄罗斯"],
    "bz": ["伯利兹"],
    "ca": ["加拿大"],
    "cc": ["科科斯群岛", "科科斯（基灵）群岛"],
    "cf": ["中非", "中非共和国"],
    "cd": ["刚果金", "刚果（金）", "刚果民主共和国"],
    "cg": ["刚果布", "刚果（布）", "刚果共和国", "刚果"],
    "ch": ["瑞士"],
    "ci": ["象牙海岸"],
    "ck": ["库克群岛"],
    "cl": ["智利"],
    "cm": ["喀麦隆"],
    "cn": ["中国"],
    "co": ["哥伦比亚"],
    "com": ["商业"],
    "cr": ["哥斯达黎加"],
    "cs": ["捷克斯洛伐克", "前捷克斯洛伐克"],
    "cu": ["古巴"],
    "cv": ["佛得角"],
    "cx": ["圣诞岛"],
    "cy": ["塞浦路斯"],
    "cz": ["捷克", "捷克共和国"],
    "de": ["德国"],
    "dj": ["吉布提"],
    "dk": ["丹麦"],
    "dm": ["多米尼加"],
    "do": ["多米尼加共和国"],
    "dz": ["阿尔及利亚"],
    "ec": ["厄瓜多尔"],
    "edu": ["教育"],
    "ee": ["爱沙尼亚"],
    "eg": ["埃及"],
    "eh": ["西撒哈拉"],
    "er": ["厄立特里亚"],
    "es": ["西班牙"],
    "et": ["埃塞俄比亚"],
    "fi": ["芬兰"],
    "fj": ["斐济"],
    "fk": ["福克兰群岛"],
    "fm": ["密克罗尼西亚"],
    "fo": ["法罗群岛"],
    "fr": ["法国"],
    "fx": ["法国（欧洲领土）"],
    "ga": ["加蓬"],
    "gb": ["大不列颠"],
    "gd": ["格林纳达"],
    "ge": ["格鲁吉亚"],
    "gf": ["法属圭亚那"],
    "gh": ["加纳"],
    "gi": ["直布罗陀"],
    "gl": ["格陵兰"],
    "gm": ["冈比亚"],
    "gn": ["几内亚"],
    "gov": ["美国政府"],
    "gp": ["瓜德罗普", "瓜德罗普（法属）"],
    "gq": ["赤道几内亚"],
    "gr": ["希腊"],
    "gs": ["南乔治亚和南桑德韦奇群岛"],
    "gt": ["危地马拉"],
    "gu": ["关岛", "关岛（美属）"],
    "gw": ["几内亚比绍"],
    "gy": ["圭亚那"],
    "hk": ["香港", "中国香港", "中国香港特别行政区"],
    "hm": ["赫德岛和麦克唐纳群岛"],
    "hn": ["洪都拉斯"],
    "hr": ["克罗地亚"],
    "ht": ["海地"],
    "hu": ["匈牙利"],
    "id": ["印度尼西亚"],
    "ie": ["爱尔兰"],
    "il": ["以色列"],
    "in": ["印度"],
    "int": ["国际"],
    "io": ["英属印度洋地区"],
    "iq": ["伊拉克"],
    "ir": ["伊朗"],
    "is": ["冰岛"],
    "it": ["意大利"],
    "jm": ["牙买加"],
    "jo": ["约旦"],
    "jp": ["日本"],
    "ke": ["肯尼亚"],
    "kg": ["吉尔吉斯斯坦", "吉尔吉斯共和国"],
    "kh": ["柬埔寨王国"],
    "ki": ["基里巴斯"],
    "km": ["科摩罗"],
    "kn": ["圣基茨和尼维斯安圭拉"],
    "kp": ["朝鲜", "北韩"],
    "kr": ["韩国", "南韩"],
    "kw": ["科威特"],
    "ky": ["开曼群岛"],
    "kz": ["哈萨克斯坦"],
    "la": ["老挝"],
    "lb": ["黎巴嫩"],
    "lc": ["圣卢西亚"],
    "li": ["列支敦士登"],
    "lk": ["斯里兰卡"],
    "lr": ["利比里亚"],
    "ls": ["莱索托"],
    "lt": ["立陶宛"],
    "lu": ["卢森堡"],
    "lv": ["拉脱维亚"],
    "ly": ["利比亚"],
    "ma": ["摩洛哥"],
    "mc": ["摩纳哥"],
    "md": ["摩尔达维亚"],
    "mg": ["马达加斯加"],
    "mh": ["马绍尔群岛"],
    "mil": ["美国军方"],
    "mk": ["马其顿"],
    "ml": ["马里"],
    "mm": ["缅甸"],
    "mn": ["蒙古"],
    "mo": ["澳门", "中国澳门", "中国澳门特别行政区"],
    "mp": ["马里亚纳", "北马里亚纳群岛"],
    "mq": ["马提尼克", "马提尼克（法属）"],
    "mr": ["毛里塔尼亚"],
    "ms": ["蒙特塞拉特"],
    "mt": ["马耳他"],
    "mu": ["毛里求斯"],
    "mv": ["马尔代夫"],
    "mw": ["马拉维"],
    "mx": ["墨西哥"],
    "my": ["马来西亚"],
    "mz": ["莫桑比克"],
    "na": ["纳米比亚"],
    "nato": ["北约", "北约（1996 年清除了此项 - 参见 hq.nato.int）"],
    "nc": ["新喀里多尼亚", "新喀里多尼亚（法属）"],
    "ne": ["尼日尔"],
    "net": ["网络"],
    "nf": ["诺福克岛"],
    "ng": ["尼日利亚"],
    "ni": ["尼加拉瓜"],
    "nl": ["荷兰"],
    "no": ["挪威"],
    "np": ["尼泊尔"],
    "nr": ["瑙鲁"],
    "nt": ["中立区"],
    "nu": ["纽埃"],
    "nz": ["新西兰"],
    "om": ["阿曼"],
    "org": ["非盈利组织", "非盈利组织（原文）"],
    "pa": ["巴拿马"],
    "pe": ["秘鲁"],
    "pf": ["玻利尼西亚", "玻利尼西亚（法属）"],
    "pg": ["巴布亚新几内亚"],
    "ph": ["菲律宾"],
    "pk": ["巴基斯坦"],
    "pl": ["波兰"],
    "pm": ["圣皮埃尔和密克隆"],
    "pn": ["皮特克恩岛"],
    "pr": ["波多黎各"],
    "pt": ["葡萄牙"],
    "pw": ["帕劳"],
    "py": ["巴拉圭"],
    "qa": ["卡塔尔"],
    "re": ["留尼旺", "留尼旺（法属）"],
    "ro": ["罗马尼亚"],
    "ru": ["俄罗斯", "俄罗斯联邦"],
    "rw": ["卢旺达"],
    "sa": ["沙特", "沙特阿拉伯"],
    "sb": ["所罗门群岛"],
    "sc": ["塞舌尔"],
    "sd": ["苏丹"],
    "se": ["瑞典"],
    "sg": ["新加坡"],
    "sh": ["圣赫勒拿"],
    "si": ["斯洛文尼亚"],
    "sj": ["斯瓦尔巴特和扬马延群岛"],
    "sk": ["斯洛伐克", "斯洛伐克共和国"],
    "sl": ["塞拉利昂"],
    "sm": ["圣马力诺"],
    "sn": ["塞内加尔"],
    "so": ["索马里"],
    "sr": ["苏里南"],
    "st": ["圣多美和普林西比"],
    "su": ["前苏联"],
    "sv": ["萨尔瓦多"],
    "sy": ["叙利亚"],
    "sz": ["斯威士兰"],
    "tc": ["特克斯和凯科斯群岛"],
    "td": ["乍得"],
    "tf": ["法属南部领土"],
    "tg": ["多哥"],
    "th": ["泰国"],
    "tj": ["塔吉克斯坦"],
    "tk": ["托克劳"],
    "tm": ["土库曼斯坦"],
    "tn": ["突尼斯"],
    "to": ["汤加"],
    "tp": ["东帝汶"],
    "tr": ["土耳其"],
    "tt": ["特立尼达和多巴哥"],
    "tv": ["图瓦卢"],
    "tw": ["台湾", "中国台湾"],
    "tz": ["坦桑尼亚"],
    "ua": ["乌克兰"],
    "ug": ["乌干达"],
    "uk": ["英国"],
    "um": ["美国边远小岛"],
    "us": ["美国", "USA"],
    "uy": ["乌拉圭"],
    "uz": ["乌兹别克斯坦"],
    "va": ["圣座", "圣座（梵蒂冈城国）"],
    "vc": ["圣文森特和格林纳丁斯"],
    "ve": ["委内瑞拉"],
    "vg": ["维尔京群岛（英属）"],
    "vi": ["维尔京群岛（美属）"],
    "vn": ["越南"],
    "vu": ["瓦努阿图"],
    "wf": ["瓦利斯和富图纳群岛"],
    "ws": ["萨摩亚"],
    "ye": ["也门"],
    "yt": ["马约特"],
    "yu": ["南斯拉夫"],
    "za": ["南非"],
    "zm": ["赞比亚"],
    "zr": ["扎伊尔"],
    "zw": ["津巴布韦"]
}


if __name__ == "__main__":
    
    input_file = "e.yaml"
    output_file = "f.yaml"

    copy_file(input_file, output_file)
    names = extract_proxies_names(output_file)
    classified = classify_proxies_name(names, country_codes, slice_rule=slice_rules['dler1'])

    with open(output_file, 'a', encoding='utf-8') as file:
        write_classify_proxies_to_output(file, classified, sort_keywords['dler1'], proxies_params_fallback)
