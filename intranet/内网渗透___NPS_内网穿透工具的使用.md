> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/pB7mVZfDebMBb4rRXqM6FA)

**一、NPS 工具介绍**  

NPS 工具是一款使用 go 语言编写的轻量级、功能强大的内网穿透工具。支持 TCP、UDP 流量转发，支持内网 HTTP、SOCKS5 代理，同时支持 snappy 压缩 (节省带宽和流量)、站点保护、加密传输、多路复用、header 修改等。同时还支持 web 图形化管理。该工具使用简单，相比于 FRP，NPS 是图形化界面，因此配置更加简单。

### **二、NPS 工具原理介绍**

注意: NPS 工具的工作原理和 FRP 工具的工作原理相似，因此我们只需要对其中某一款工具的原理十分熟悉即可，由于之前写过一篇十分详细的 FRP 的工作原理和使用方法，因此，在这不再赘述，大家可以去看这篇文章:

**[内网渗透 | FRP 代理工具详解](http://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247492230&idx=1&sn=8b973bb30ab993bdfad36b7897b093d8&chksm=ec1cb7b9db6b3eaf63ab8758cfeed10fd4a321eda87223c1f90f1de5c0d6c69c6619e937ef78&scene=21#wechat_redirect)**

#### **1.NPS 客户端和服务器端配置**

NPS 工具由 NPS 服务器端和 NPS 客户端组成，我们一般将 NPS 服务器端放在具有公网 IP 的 VPS 上，并且会开启一个端口等待 NPS 的客户端进行连接 (一般会在 NPS 服务器的配置文件中进行说明)，而 NPS 的客户端一般会被放在我们已经拿下的内网主机上，我们会指定 NPS 服务器的客户端需要连接的 NPS 服务器的 IP 和端口，这样，我们就成功的将 NPS 的服务器端和 NPS 的客户端连接了起来。

#### **2. 通过 NPS 进行内网穿透**

按照上面的方法，我们已经配置好了 NPS 服务，现在服务器端和客户端是可以连通的，但是，我们又怎么可以通过 NPS 进行内网穿透呢？其实，NPS 是会在配置文件里面设置图形化界面的登录后台，我们通过登录 NPS 的后台，然后使用配置文件中设置的账号密码进行登录，登录后台之后，首先添加一个客户端，这个客户端会自动生成一个唯一验证密钥，我们需要在配置文件中输入这个唯一验证密钥，这样就可以将 NPS 的客户端和服务端连接起来了，随后我们可以根据我们的需求添加隧道，如 HTTP 隧道、SOCKS 隧道等多条隧道，我们通过隧道设置的端口进行访问，即可访问到内网主机。

### **三、NPS 配置**

#### **1.NPS 下载链接**

```
NPS下载链接:https://github.com/ehang-io/nps/releases/tag/v0.26.9
NPS官方说明文档:https://ehang-io.github.io/nps/#/api
```

#### **2.NPS 服务端配置**

(1): 查看服务器版本

```
arch
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK3GSpicpBUmucr9huicEs4us9mPX4WpDplpGcA65r90XRsT7vicNN3hynuQ/640?wx_fmt=png)  

(2): 下载对应版本的 NPS 服务器

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK3FX5h36icY2OZgl5vnJYib0DoUWhTCUJVuzOMcwztCdNDO2kNlwDdxv4Q/640?wx_fmt=png)

(3): 上传到服务器端进行解压

```
tar -xvzf linux_amd64_server.tar.gz
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK3VWdyclEwQXQAOqdUl0vvsUO5fpgTDr3Gh9S9Pib1vKVr3TticUhCVBqg/640?wx_fmt=png)  

(4): 安装 NPS

```
./nps install   #linux
nps.exe install #windows
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK3adKKK7BdHZeiaZKQXGE7MCMP9GHhZKsIAzZkdu0EdG7Pz9wTd1Igrtw/640?wx_fmt=png)  

(5): 查看配置文件

```
cd conf/
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK3IZf8eHNa9FcIOJBGOsicICdde77o83zhoiaRBDIT0qtNjNZS1X809icsg/640?wx_fmt=png)  

配置文件中的内容如下

```
appname = nps
#Boot mode(dev|pro)
runmode = dev

#HTTP(S) proxy port, no startup if empty
http_proxy_ip=0.0.0.0
http_proxy_port=80     #域名代理http代理监听端口
https_proxy_port=443   #域名代理https代理监听端口(一般会修改这两个端口，避免端口冲突)
https_just_proxy=true
#default https certificate setting
https_default_cert_file=conf/server.pem
https_default_key_file=conf/server.key

##bridge
bridge_type=tcp      #客户端与服务端连接方式kcp或tcp
bridge_port=8024     #服务端客户端通信端口，也就是说客户端通过访问服务端的这个端口可以进行连接
bridge_ip=0.0.0.0

# Public password, which clients can use to connect to the server
# After the connection, the server will be able to open relevant ports and parse related domain names according to its own configuration file.
public_vkey=123      #客户端以配置文件模式启动时的密钥，设置为空表示关闭客户端配置文件连接模式

#Traffic data persistence interval(minute)
#Ignorance means no persistence
#flow_store_interval=1   #服务端流量数据持久化间隔，单位分钟，忽略表示不持久化

# log level LevelEmergency->0  LevelAlert->1 LevelCritical->2 LevelError->3 LevelWarning->4 LevelNotice->5 LevelInformational->6 LevelDebug->7
log_level=7         #日志输出级别
#log_path=nps.log

#Whether to restrict IP access, true or false or ignore
#ip_limit=true      #是否限制ip访问，true或false或忽略

#p2p
#p2p_ip=127.0.0.1    #服务端IP，使用p2p模式必填
#p2p_port=6000       #p2p模式开启的udp端口

#web
web_host=a.o.com
web_username=admin   #web界面管理账号
web_password=123     #web界面管理密码
web_port = 8080      #web管理端口，通过访问该端口可以访问NPS后台
web_ip=0.0.0.0
web_base_url=        #web管理主路径,用于将web管理置于代理子路径后面
web_open_ssl=false
web_cert_file=conf/server.pem
web_key_file=conf/server.key
# if web under proxy use sub path. like http://host/nps need this.
#web_base_url=/nps

#Web API unauthenticated IP address(the len of auth_crypt_key must be 16)
#Remove comments if needed
#auth_key=test       #web api密钥
auth_crypt_key =1234567812345678    #获取服务端authKey时的aes加密密钥，16位

#allow_ports=9001-9009,10001,11000-12000

#Web management multi-user login
allow_user_login=false
allow_user_register=false
allow_user_change_username=false


#extension
allow_flow_limit=false
allow_rate_limit=false
allow_tunnel_num_limit=false
allow_local_proxy=false
allow_connection_num_limit=false
allow_multi_ip=false
system_info_display=false

#cache
http_cache=false
http_cache_length=100

#get origin ip
http_add_origin_header=false

#pprof debug options
#pprof_ip=0.0.0.0       #debug pprof 服务端IP
#pprof_port=9999        #debug pprof 端口

#client disconnect timeout
disconnect_timeout=60   #客户端连接超时，单位 5s，默认值 60，即 300s = 5mins
```

**注意: 在上面的配置文件中，我们主要是要注意以下方面:**  

①: 一般会修改域名代理的端口，避免端口冲突

②:NPS 的 web 页面默认端口是 8080，默认用户名密码是 admin/123

③:NPS 的服务端和客户端进行连接的默认端口是 8024，这个端口可以进行修改，修改之后，在连接时注意使用修改后的端口

④:NPS 服务端开启的端口 (也就是我们需要访问的 VPS 的端口) 不在配置文件中，需要我们 web 界面中进行配置

#### **3.NPS 客户端配置**

(1): 下载对应版本的 NPS 客户端

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK3FNCibIK1Z4nLa70vcgVB86BYecQiamk9cY7JQ1kQIDanD3yUA5Y0akPA/640?wx_fmt=png)

(2): 客户端连接方式

①: 使用 vkey 进行连接

```
Windows：npc.exe -server=ip:port -vkey=服务端生成的key
Linux：./npc -server=ip:port -vkey=服务端生成的key
```

②使用配置文件进行连接  

```
windows:   npc.exe -config=npc配置文件路径
linux:     ./npc -config=npc配置文件路径
```

(3): 客户端配置文件  

**友情提示: 这里将配置文件写出来主要是为了让大家了解配置文件的内容，如果觉得配置文件太过繁琐，大多数情况下只需要关注** **server_addr****_、_****conn_type****、和 vkey 这三个参数即可。**

```
[common]
server_addr=127.0.0.1:8024
conn_type=tcp
vkey=123
auto_reconnection=true
max_conn=1000
flow_limit=1000
rate_limit=1000
basic_username=11
basic_password=3
web_username=user
web_password=1234
crypt=true
compress=true
#pprof_addr=0.0.0.0:9999
disconnect_timeout=60

[health_check_test1]
health_check_timeout=1
health_check_max_failed=3
health_check_interval=1
health_http_url=/
health_check_type=http
health_check_target=127.0.0.1:8083,127.0.0.1:8082

[health_check_test2]
health_check_timeout=1
health_check_max_failed=3
health_check_interval=1
health_check_type=tcp
health_check_target=127.0.0.1:8083,127.0.0.1:8082

[web]
host=c.o.com
target_addr=127.0.0.1:8083,127.0.0.1:8082

[tcp]
mode=tcp
target_addr=127.0.0.1:8080
server_port=10000

[socks5]
mode=socks5
server_port=19009
multi_account=multi_account.conf

[file]
mode=file
server_port=19008
local_path=/Users/liuhe/Downloads
strip_pre=/web/

[http]
mode=httpProxy
server_port=19004

[udp]
mode=udp
server_port=12253
target_addr=114.114.114.114:53

[ssh_secret]
mode=secret
password=ssh2
target_addr=123.206.77.88:22

[ssh_p2p]
mode=p2p
password=ssh3

[secret_ssh]
local_port=2001
password=ssh2

[p2p_ssh]
local_port=2002
password=ssh3
target_addr=123.206.77.88:22
```

注意: NPS 的客户端启动有两种启动方式，一种是不需要配置文件，直接输入相关命令即可启动，另一种是使用配置文件启动 NPS 客户端。如果需要使用配置文件来启动 NPS 客户端，那么需要配置如下内容 (其余内容可以忽略)。  

```
server_addr   #服务端ip/域名:port
conn_type       #与服务端通信模式(tcp或kcp)
vkey           #服务端配置文件中的密钥
```

首先 server_addr _是需要填写 NPS 服务端的 IP 和端口，_conn_type 选择合适的类型 (一般选择 TCP)，vkey 的值设置为服务端配置文件的密钥。这样服务端和客户端就可以进行连接了。  

### **四、NPS 使用实例**

#### **1.NPS 服务端配置**

**首先先按照上面的内容在 VPS 上下载并安装 NPS 的服务端。**

(1): 修改 NPS 服务端配置

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK3AlgcWA5lmo4TZgr8S9ibwI1RRG6Tia25UwZic58ian5nKngiaHoXqOFU6BQ/640?wx_fmt=png)

(2): 重载配置文件

```
./nps reload
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK3yjaHIxwwenenDrOYnicY7mGTnrGMSbRicMmuUIPGe5JSpJ7vkz9ze4Zw/640?wx_fmt=png)  

这块加载失败了，目前还不清楚原因。

(3): 启动 NPS 服务端

```
./nps start
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK3SkofiaiaYzbUUicbsa5jLUrlUhVASIeotpfxatIcFoscOVslnFSSiboa5A/640?wx_fmt=png)  

```
./nps stop     #停止nps服务
./nps restart  #重启nps服务
```

(4): 访问 NPS 服务端  

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK3X7t7NeNIogoScHAiar2I2q5xsY7AB96V9LwdWdo4orZAJBVFzAXkPicg/640?wx_fmt=png)

(5): 使用账号密码登录成功

如下为 nps 控制台。

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK3vGT0e6OM0ocCH7pdj8tIMHlTDspHmqrlvbM3X2DAJicODpWQOmEoicOQ/640?wx_fmt=png)

(6): 新增一个客户端

这块新建的客户端主要是要使用生成的唯一验证密钥，通过这个唯一验证密钥才能将 NPS 的服务端和客户端连接起来，因此至少需要添加一个客户端。

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK33tZ9cQ91MZ31zFHkRx9HuZW6g12Etx5usq0px6PictZ0YyBnCWkFPwg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK3vyzHh57gBG5bjuibWast9LzX4UW2YOOfYm2icxHiczs4fTerE0LAHZ50g/640?wx_fmt=png)

(7): 添加 SOCKS 代理

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK3libibw0ibyj81YwKualiaSZWXot4jgw94QibmlQgDBia1hZO4GdM0kkaRR9A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK3XZVicTkwQ0jTOCYdrlpIibQKaKJd4V3TyszKbGdiaUdfJ0BdHMtXmA9zA/640?wx_fmt=png)

#### **2. 客户端配置**

**第一种方法: 无配置文件**

(1): 将 NPS 对应版本的文件上传到内网主机中

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK3YwbU9HHqJh8sIjLfwuYPSv99NzG6N6slZqKydPpIjntzswxib0kMJMA/640?wx_fmt=png)

(2): 执行如下命令

```
Windows：npc.exe -server=ip:port -vkey=服务端生成的key
Linux：./npc -server=ip:port -vkey=服务端生成的key
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK3bia9hURBD25sC9FI5JzkCo62bnicgTFicqrpwpprrX0fHyciaXa12KA4wA/640?wx_fmt=png)  

客户端连接成功。

(3): 使用浏览器设置代理访问内网主机

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK3xSoGJialAAJ2fAyfg6l0fon0LKes6hsxMLHcyIzt7LIaiaaUy2flCJBg/640?wx_fmt=png)

成功访问到内网主机的通达 OA，但是在笔者测试的过程中发现似乎 NPS 的速度和稳定性不如 FRP。

**第二种方法: 有配置文件**

此模式使用 nps 的公钥或者客户端私钥验证，各种配置在客户端完成，同时服务端 web 也可以进行管理

(1): 将 NPS 对应版本的文件上传到内网主机中

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK3YwbU9HHqJh8sIjLfwuYPSv99NzG6N6slZqKydPpIjntzswxib0kMJMA/640?wx_fmt=png)

(2): 修改配置文件

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK3txmXn0RjpHu0v7PGVEPKelphE3hhoHBEfyIG30ebRggFdNuh6KTGmw/640?wx_fmt=png)

(3): 执行如下命令

```
windows:   npc.exe -config=npc配置文件路径
linux:     ./npc -config=npc配置文件路径
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK3gxiaE307dJGvCibk4fBAbPqlvgzEuKORRibCHbVVcVm4ymPBAcSa5ffZw/640?wx_fmt=png)  

(4): 浏览器通过代理成功访问目标主机

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK3beibEMwZkTudCZ574QYtib9cg1gQ4DIom68JWibBZ6JBuJmPc7IQUUh4Q/640?wx_fmt=png)

### **五、NPS 其他场景使用**

#### 1. 使用 NPS 代理 SSH 服务

(1): 在内网主机上进行下载解压

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK3MppZWPNibFtiaa6weobmmcU8URDdaJW5xHmBMTSXabh6ibECfAYmVhkoA/640?wx_fmt=png)

(2): 在服务端创建一条 TCP 隧道

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK3DU0lLIkFgVna8bytMcdS9ica2g69KqBHiaX3bfPtlEdWhpDvffpfM3ww/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK31dWlax2LqTVgxeLcoh8PT39ftBTA8cC8WVicaIpKKKJE4HOdYMnmqoA/640?wx_fmt=png)

(3): 启动客户端连接服务端

```
./npc -server=ip:port -vkey=服务端生成的key
```

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK3D1iaY0dvgYFldgKf0FDpFibbE1MPB3aEyVGQJ0HBvHIcULVtboDQSFYQ/640?wx_fmt=png)  

(4): 使用另一台 VPS 访问该 VPS 的 222 端口连接内网主机

![](https://mmbiz.qpic.cn/mmbiz_png/Uq8QfeuvouibFr7ialuQUjEJkUpd5XoCK3tHTQmSMica6Neprznibic6JIdtYLdvVoBYgEcRqicaAOAXYXbYib8BxibcbA/640?wx_fmt=png)

成功访问到内网主机。

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)**推荐阅读：****[内网渗透 | 常用的内网穿透工具使用](http://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247492155&idx=1&sn=3e0a217a784eb250cad2f2f41a488f68&chksm=ec1cb704db6b3e12f9840f33deccebc488f0369cd5e0cd46286c89fbac39f41b52e2436af845&scene=21#wechat_redirect)**[**内网渗透 | FRP 代理工具详解**](http://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247492230&idx=1&sn=8b973bb30ab993bdfad36b7897b093d8&chksm=ec1cb7b9db6b3eaf63ab8758cfeed10fd4a321eda87223c1f90f1de5c0d6c69c6619e937ef78&scene=21#wechat_redirect)  

[![](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou80h6Jor7Py4sKIwfiaowozsMP0Yjn9RcoJAmPMKa5hQVczeXoDxIic2QaZYKKrLDlJFT5v6EpREmjg/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=MzI5MDU1NDk2MA==&mid=2247492102&idx=1&sn=aa09a4f38ae21b73a1d3a938d97aae20&chksm=ec1cb739db6b3e2f7d7edc43d338e9f2dc4563edc768a34fb4214618f5107ecfc89f9d7b802c&scene=21#wechat_redirect)

**点赞 在看 转发**

原创投稿作者：想走安全的小白

![](https://mmbiz.qpic.cn/mmbiz_gif/Uq8QfeuvouibQiaEkicNSzLStibHWxDSDpKeBqxDe6QMdr7M5ld84NFX0Q5HoNEedaMZeibI6cKE55jiaLMf9APuY0pA/640?wx_fmt=gif)