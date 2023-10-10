import os
import shutil

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


content_to_append = '''

rules:
  #https://github.com/Dreamacro/clash/wiki/Configuration#:~:text=tls%0A%20%20%0A%20%20%23%20%E2%80%A6%E2%80%A6-,Rules,-Available%20keywords%3A
  # - IP-CIDR,127.0.0.0/8,DIRECT
  #- SRC-IP-CIDR,192.168.1.201/32,DIRECT
  #- RULE-SET,Special,DIRECT
  #- GEOIP,CN,Domestic

  #vPeer
  - IP-CIDR,67.230.178.193/32,DIRECT
  - IP-CIDR,4.193.135.33/32,DIRECT
  - IP-CIDR,4.193.54.245/32,DIRECT

  #远程ToDesk远程软件
  - PROCESS-NAME,ToDesk.exe,DIRECT
  #远程桌面
  - PROCESS-NAME,mstsc.exe,DIRECT
  #蓝叠
  - PROCESS-NAME,BstkSVC.exe,PROXY
  - PROCESS-NAME,HD-Player.exe,PROXY
  #浏览器
  - PROCESS-NAME,chrome0.exe,DIRECT
  - PROCESS-NAME,chrome1.exe,PROXY1
  - PROCESS-NAME,chrome2.exe,PROXY2
  - PROCESS-NAME,chrome3.exe,PROXY3
  - PROCESS-NAME,msedge1.exe,PROXY1
  - PROCESS-NAME,msedge2.exe,PROXY2
  - PROCESS-NAME,firefox1.exe,PROXY1
  - PROCESS-NAME,firefox2.exe,PROXY2
  #绿色版火狐
  - PROCESS-NAME,phyrox-portable1.exe,PROXY1
  - PROCESS-NAME,phyrox-portable2.exe,PROXY2
  #海外聊天软件
  - PROCESS-NAME,Discord.exe,PROXY
  - PROCESS-NAME,Telegram.exe,PROXY
  #OneDrive
  - PROCESS-NAME,OneDrive.exe,PROXY
  #windows命令行终端
  - PROCESS-NAME,WindowsTerminal.exe,dev
  - PROCESS-NAME,OpenConsole.exe,dev
  - PROCESS-NAME,powershell.exe,dev
  # - PROCESS-NAME,cmd.exe,dev
  # - PROCESS-NAME,conhost.exe,dev
  - PROCESS-NAME,Code.exe,dev
  - PROCESS-NAME,git.exe,dev
  - PROCESS-NAME,git-remote-https.exe,dev
  # 自定义规则组
  - RULE-SET,OpenAI,ChatGPT
  - RULE-SET,Speedtest,IPtest
  - DOMAIN,ipinfo.io,IPtest

  
  # ChatGPT
  - DOMAIN-SUFFIX,openai.com,PROXY
  - DOMAIN-SUFFIX,cloudflare.com,PROXY
  - DOMAIN-SUFFIX,sentry.com,PROXY

  # bing
  - DOMAIN-SUFFIX,bing.com,PROXY
  - DOMAIN-SUFFIX,www.bing.com,PROXY
  - DOMAIN-SUFFIX,cn.bing.com,PROXY
  - DOMAIN-SUFFIX,global.bing.com,PROXY


  #https://github.com/Loyalsoldier/clash-rules
  #白名单模式
  - RULE-SET,applications,DIRECT
  - DOMAIN,clash.razord.top,DIRECT
  - DOMAIN,yacd.haishan.me,DIRECT
  - RULE-SET,private,DIRECT
  - RULE-SET,reject,REJECT
  - RULE-SET,icloud,DIRECT
  - RULE-SET,apple,DIRECT
  - RULE-SET,google,DIRECT
  - RULE-SET,proxy,PROXY
  - RULE-SET,direct,DIRECT
  - RULE-SET,lancidr,DIRECT
  - RULE-SET,cncidr,DIRECT
  - RULE-SET,telegramcidr,PROXY
  - GEOIP,LAN,DIRECT
  - GEOIP,CN,DIRECT
  - MATCH,PROXY

'''






if __name__ == "__main__":

    input_file = "g.yaml"
    output_file = "h.yaml"
    copy_and_append(input_file, output_file, content_to_append)



