import os


# 创建目标文件
def create_file_with_initial_content(output_file, initial_content):
    os.makedirs(os.path.dirname(output_file), exist_ok=True) if os.path.dirname(output_file) else None
    with open(output_file, 'w', encoding="utf-8") as f:
        f.write(initial_content)





initial_content = '''---
mode: Rule
log-level: silent
allow-lan: true
bind-address: "*"
port: 3456
socks-port: 3457
mixed-port: 3458
redir-port: 3459
external-controller: '0.0.0.0:3450'
external-ui: ui
secret: ''


cfw-latency-url: http://cp.cloudflare.com/generate_204
cfw-latency-timeout: 3000
cfw-latency-type: 1
cfw-conn-break-strategy: true


clash-for-android:
  ui-subtitle-pattern: '[一-龥]{2,4}'
experimental:
  ignore-resolve-fail: true
tun:
   enable: true
   stack: system
auto-redir:
    enable: true
    auto-route: true
url-rewrite:
- ^https?:\/\/(www.)?(g|google)\.cn https://www.google.com 302
- ^https?:\/\/(ditu|maps).google\.cn https://maps.google.com 302

'''






if __name__ == "__main__":

    output_yml = "b.yaml"
    create_file_with_initial_content(output_yml, initial_content)
    