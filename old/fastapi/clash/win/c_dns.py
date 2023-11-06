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
#来自 zhs.cloud
dns:
  enable: true
  # ipv6: false
  listen: 0.0.0.0:53
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16
  
  # 仅填写 DNS 服务器的 IP 地址，填写的 DNS 服务器将会被用来解析 nameserver 服务的域名
  default-nameserver:
    - 119.29.29.29
    - 223.5.5.5
    
  # 自定义DNS将添加在下方并优先使用 支持Doh/Dot等dns
  # 支持 UDP / TCP / DoT / DoH 协议的 DNS 服务，可以指明具体的连接端口号
  # 所有 DNS 请求将会直接发送到服务器，不经过任何代理
  # Clash 会使用最先获得的解析记录回复 DNS 请求
  nameserver:
    - https://223.5.5.5/dns-query
    - https://1.12.12.12/dns-query
    #- https://doh.pub/dns-query
    #- https://dns.alidns.com/dns-query


  # https://github.com/vernesong/OpenClash/blob/master/luci-app-openclash/root/etc/openclash/custom/openclash_custom_fallback_filter.yaml
  # If IP addresses resolved with servers in `nameservers` are in the specified
  # subnets below, they are considered invalid and results from `fallback`
  # servers are used instead.
  #
  # IP address resolved with servers in `nameserver` is used when
  # `fallback-filter.geoip` is true and when GEOIP of the IP address is `CN`.
  #
  # If `fallback-filter.geoip` is false, results from `nameserver` nameservers
  # are always used if not match `fallback-filter.ipcidr`.
  #
  # This is a countermeasure against DNS pollution attacks.
  fallback-filter:
    geoip: true
    geoip-code: CN
    ipcidr:
      - 0.0.0.0/8
      - 10.0.0.0/8
      - 100.64.0.0/10
      - 127.0.0.0/8
      - 169.254.0.0/16
      - 172.16.0.0/12
      - 192.0.0.0/24
      - 192.0.2.0/24
      - 192.88.99.0/24
      - 192.168.0.0/16
      - 198.18.0.0/15
      - 198.51.100.0/24
      - 203.0.113.0/24
      - 224.0.0.0/4
      - 240.0.0.0/4
      - 255.255.255.255/32
    domain:
      - "+.google.com"
      - "+.facebook.com"
      - "+.youtube.com"
      - "+.githubusercontent.com"
      - "+.googlevideo.com"
      - "+.msftconnecttest.com"
      - "+.msftncsi.com"

      
  # https://github.com/dler-io/Rules/blob/main/Clash/Head_dns.yaml
  fake-ip-filter:
    - "*.lan"
    - "*.localdomain"
    - "*.example"
    - "*.invalid"
    - "*.localhost"
    - "*.test"
    - "*.local"
    - "*.home.arpa"
    - "time.*.com"
    - "time.*.gov"
    - "time.*.edu.cn"
    - "time.*.apple.com"
    - "time1.*.com"
    - "time2.*.com"
    - "time3.*.com"
    - "time4.*.com"
    - "time5.*.com"
    - "time6.*.com"
    - "time7.*.com"
    - "ntp.*.com"
    - "ntp1.*.com"
    - "ntp2.*.com"
    - "ntp3.*.com"
    - "ntp4.*.com"
    - "ntp5.*.com"
    - "ntp6.*.com"
    - "ntp7.*.com"
    - "*.time.edu.cn"
    - "*.ntp.org.cn"
    - "+.pool.ntp.org"
    - "time1.cloud.tencent.com"
    - "music.163.com"
    - "*.music.163.com"
    - "*.126.net"
    - "musicapi.taihe.com"
    - "music.taihe.com"
    - "songsearch.kugou.com"
    - "trackercdn.kugou.com"
    - "*.kuwo.cn"
    - "api-jooxtt.sanook.com"
    - "api.joox.com"
    - "joox.com"
    - "y.qq.com"
    - "*.y.qq.com"
    - "streamoc.music.tc.qq.com"
    - "mobileoc.music.tc.qq.com"
    - "isure.stream.qqmusic.qq.com"
    - "dl.stream.qqmusic.qq.com"
    - "aqqmusic.tc.qq.com"
    - "amobile.music.tc.qq.com"
    - "*.xiami.com"
    - "*.music.migu.cn"
    - "music.migu.cn"
    - "*.msftconnecttest.com"
    - "*.msftncsi.com"
    - "msftconnecttest.com"
    - "msftncsi.com"
    - "localhost.ptlogin2.qq.com"
    - "localhost.sec.qq.com"
    - "+.srv.nintendo.net"
    - "+.stun.playstation.net"
    - "xbox.*.microsoft.com"
    - "xnotify.xboxlive.com"
    - "+.battlenet.com.cn"
    - "+.wotgame.cn"
    - "+.wggames.cn"
    - "+.wowsgame.cn"
    - "+.wargaming.net"
    - "proxy.golang.org"
    - "stun.*.*"
    - "stun.*.*.*"
    - "+.stun.*.*"
    - "+.stun.*.*.*"
    - "+.stun.*.*.*.*"
    - "heartbeat.belkin.com"
    - "*.linksys.com"
    - "*.linksyssmartwifi.com"
    - "*.router.asus.com"
    - "mesu.apple.com"
    - "swscan.apple.com"
    - "swquery.apple.com"
    - "swdownload.apple.com"
    - "swcdn.apple.com"
    - "swdist.apple.com"
    - "lens.l.google.com"
    - "stun.l.google.com"
    - "+.nflxvideo.net"
    - "*.square-enix.com"
    - "*.finalfantasyxiv.com"
    - "*.ffxiv.com"
'''


if __name__ == "__main__":

    input_file = "b.yaml"
    output_file = "c.yaml"
    copy_and_append(input_file, output_file, content_to_append)



