> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/6r__h1dMG0gX2TcQEZdvhQ)

> 本文作者：**Spark**（Ms08067 内网安全小组成员）

Spark 微信（欢迎骚扰交流）：

![](https://mmbiz.qpic.cn/mmbiz_jpg/XWPpvP3nWa9ZzfluJuFOwazw8MppYN1xzs5KHPYp6lazzH2MyicaiaJibLUoTTgj9dPyF6iaSf4PguTTiboumy7RNiaQ/640?wx_fmt=jpeg)

**1. 概述**

Haproxy 是一个使用 c 语言开发的高性能负载均衡代理软件，提供 tcp 和 http 的应用程序代理，免费、快速且可靠。

类似 frp，使用一个配置文件 + 一个 server 就可以运行。

优点：

*   大型业务领域应用广泛
    
*   支持四层代理（传输层）以及七层代理（应用层）
    
*   支持 acl（访问控制列表），可灵活配置路由
    
*   windows 使用 cygwin 编译后可运行（可跨平台）
    

访问控制列表（Access Control Lists，ACL）是应用在路由器接口的指令列表，这些指令列表用来告诉路由器哪些数据包可以接受，哪些数据包需要拒绝。

**2. 配置**

官方配置手册：

https://cbonte.github.io/haproxy-dconv/2.2/configuration.html

配置文件由全局配置和代理配置组成：

全局配置（global）：

*   定义 haproxy 进程管理安全及性能相关的参数
    

代理设定（proxies）：

*   defaults
    

*   为其他配置段提供默认参数，默认配置参数可由下一个 "defaults" 重新设定
    

*   **frontend**
    

*   定义一系列监听的套接字，这些套接字可接受客户端请求并与之建立连接
    

*   **backend**
    

*   定义 "后端" 服务器，前端代理服务器将会把哭护短的请求调度至这些服务器
    

*   listen
    

*   定义监听的套接字和后端的服务器，类似于将 frontend 和 backend 段放在一起
    

示例：

```
global
defaults
  log global
  mode tcp
  option dontlognull
  timeout connect 5000
  timeout client 50000
  timeout server 50000

frontend main
  mode tcp
  bind *:8888
  option forwardfor except 127.0.0.1
  option forwardfor header X‐Real‐IP

# 配置acl规则
  acl is‐proxy‐now urlp_reg(proxy) ^(http|https|socks5)$
# 分发到对应的backend
  use_backend socks5 if is‐proxy‐now
  use_backend http
backend socks5
  mode tcp
  timeout server 1h
  server ss 127.0.0.1:50000
backend http
  mode tcp
  server http 127.0.0.1:80
```

重点关注 frontend 和 backend。

Frontend 中需要编写 acl 规则，配置转发。比如，当 http 流量来的时候，转发给 web 服务；当 rdp 流量来的时候，转发给 rdp 服务。

Backend 中需要编写具体的操作，就是转达到哪个目标的哪个端口。

**3. 思路**

**(1) 思路一（通用）**

编写 acl 规则，在四层（传输层）进行负载，根据协议类型进行分发，例如：遇到 http 流量发送给 http 服务，遇到 rdp 发送给 rdp 服务等。

**(2) 思路二**

编写 acl 规则，在七层（应用层）进行负载，判断应用类型进行分发，例如，遇到 http 分发到 http 服务，否则发送到 xxx 服务。

**4. 步骤**

以思路一为例：  

1.  通过 wireshark 捕获 tpkt（应用层数据传输协议）信息
    
2.  编写 acl 规则路由进行流量分发
    
3.  添加后端 server
    
4.  原始接口接管
    
5.  完成
    

**4.1 捕获 tpkt**

关于 tpkt 可百度或查看参考链接

三次握手后，开始应用层数据传输。

使用 wireshark 抓包：

ssh 协议：

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaicgBaDV3h3MwicqrsX57MGibaOVYTBfRsZswGckHu9HWuVHR0HSMcfSicHTrYpbtKLpnk4eO19lxfotw/640?wx_fmt=png)

前三个包为三次握手，第四个包的起始三位，便是我们需要的 tpkt，例如 ssh 为 535348。

rdp 协议：030000

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaicgBaDV3h3MwicqrsX57MGibaxWF3hsrhrh12w4IZ00tOYqoSiacyGPQj79T89M7JFAnnDND6fIYtuGA/640?wx_fmt=png)

速查：

<table><tbody><tr><td width="104" valign="top">协议</td><td width="100" valign="top">TPKT</td></tr><tr><td width="104" valign="top">SSH</td><td width="100" valign="top">535348</td></tr><tr><td width="104" valign="top">RDP</td><td width="100" valign="top">030000</td></tr><tr><td width="104" valign="top">HTTP(GET)</td><td width="100" valign="top">474554</td></tr><tr><td width="104" valign="top">HTTP(POS)</td><td width="100" valign="top">504f53</td></tr><tr><td width="104" valign="top">HTTP(PUT)</td><td width="100" valign="top">505554</td></tr><tr><td width="104" valign="top">HTTP(DEL)</td><td width="100" valign="top">44454c</td></tr><tr><td width="104" valign="top">HTTP(OPT)</td><td width="100" valign="top">4f5054</td></tr><tr><td width="104" valign="top">HTTP(HEA)</td><td width="100" valign="top">484541</td></tr><tr><td width="104" valign="top">HTTP(CON)</td><td width="100" valign="top">434f4e</td></tr><tr><td colspan="1" rowspan="1" width="104" valign="top">HTTP(TRA)</td><td colspan="1" rowspan="1" width="100" valign="top">545241</td></tr><tr><td colspan="1" rowspan="1" width="104" valign="top">HTTPS</td><td colspan="1" rowspan="1" width="100" valign="top">160301</td></tr></tbody></table>

**4.2 编写 acl 规则**

```
global
defaults
  timeout connect 5000
  timeout client 50000
  timeout server 50000
frontend main
  mode tcp
  bind *:8888
# 重点：编写acl规则进行转发
  tcp‐request inspect‐delay 3s
  acl is_http req.payload(0,3) ‐m bin 474554 504f53 505554 44454c 4f5054 484541 434f4e 545241
  acl is_ssh req.payload(0,3) ‐m bin 535348
  acl is_rdp req.payload(0,3) ‐m bin 030000
# 设置四层允许通过
  tcp‐request content accept if is_http
  tcp‐request content accept if is_ssh
  tcp‐request content accept if is_rdp
  tcp‐request content accept
# 分发到对应的backend
  use_backend http if is_http
  use_backend ssh if is_ssh
  use_backend rdp if is_rdp
  use_backend socks5
backend socks5
  mode tcp
  timeout server 1h
  server ss 127.0.0.1:50000
backend http
  mode tcp
  server http 127.0.0.1:80
backend ssh
  mode tcp
  server ssh 127.0.0.1:22
backend rdp
  mode tcp
  server rdp 192.168.213.129:3389
```

该配置文件的功能是监听 8888 端口，将 http 流量（速查表中 http 协议的 8 种 tpkt）转发到本地的 80 上，将 ssh 流量转发到本地的 22 端口上，将 rdp 流量转发到另一主机的 3389 上。

**5. 实验**

*   Target1：Ubuntu 16.04 x64
    
*   IP：192.168.213.128
    
*   开启 22 端口、80 端口
    

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaicgBaDV3h3MwicqrsX57MGiba0pOLCr2WkVAttpoNA2aKOKr33QMoMHL4FicMiajVU9nDoJCHVmYzp8PQ/640?wx_fmt=png)

*   Target2：Win7 x64
    
*   IP：192.168.213.129
    
*   开启 3389 端口
    

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaicgBaDV3h3MwicqrsX57MGibaIwsUZe2w2pPK9OXZUf9SXlUIP09kJGCbx0YcRWStgAStl47zMe4nxQ/640?wx_fmt=png)

启动 haproxy，-f 指定配置文件，开启 8888 端口表示启动成功。-d：调试模式，可不加。

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaicgBaDV3h3MwicqrsX57MGiba2Dm4U3j0nBWVgt84pfkr0vdsuvZP8Yj0saBRszic9oK4BTMJIFLokaQ/640?wx_fmt=png)

HTTP 协议：访问靶机的 8888 端口，流量被 haproxy 分发至本机的 80。

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaicgBaDV3h3MwicqrsX57MGibavh8YSpicGxE3KRdkECec5dRjw0Jv8UqGHZuDxdnVeuxqUlVlcYGmPtg/640?wx_fmt=png)

RDP 协议：访问靶机的 8888 端口，流量被 haproxy 分发至 192.168.213.129 的 3389。

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaicgBaDV3h3MwicqrsX57MGibaxwBxMhplhqbdbLZ6gKoW4RSHv6dt28Q58txSwkmwviaHxqib7cJvYy6g/640?wx_fmt=png)

SSH 协议：访问靶机的 8888 端口，流量被 haproxy 分发至本机的 22。

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaicgBaDV3h3MwicqrsX57MGibag9jboBsAcXibkUnBTh1Vv2iaIDzia9zLGPiaGSO9o3norSDlakUwFdic6KQ/640?wx_fmt=png)

haproxy 日志：

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaicgBaDV3h3MwicqrsX57MGibaa7tpyaNb5JOXbekwlh1PMchBgqMiaGaOSVymIXTyXadzv2ZJRvPSTqw/640?wx_fmt=png)

**6. 端口重定向**

为了不影响正常的 80 端口的访问，将过来的 80 端口流量转发到 8888 端口上。这样用户正常访问 80 端口时，流量会先转发到 8888 端口上，再由 haproxy 转发回 80 端口。

*   Linux：iptables（不需要重启服务）
    

```
iptables ‐t nat ‐A PREROUTING ‐i eth0 ‐p tcp ‐‐dport 80 ‐j REDIRECT ‐‐to‐port 8888
```

访问 80 可以正常访问：

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaicgBaDV3h3MwicqrsX57MGibaEoozqCgk6kIrmVKibDiafwelOQyQuvwQ14IvQfd13pRtkvp7EBjs9tuA/640?wx_fmt=png)

Haproxy 日志有记录，说明流量由 80 先到 8888，再回到 80。

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaicgBaDV3h3MwicqrsX57MGibaNSqkUnGEfoQNYdFnNoBAkH4uw5gEMz6yLlNjQzYhe3niapyuX4y8tZQ/640?wx_fmt=png)

*   Windows：netsh（需要重启 web 服务）
    

```
netsh interface portproxy add v4tov4 listenport=80 connectport=8888 connectaddress=127.0.0.1
```

**注意：如果在 windows 下启用端口重定向，需要在端口启动前添加 netsh 端口转发规则。**

**7. 参考链接**

*   https://www.cnblogs.com/readygood/p/9776403.html
    
*   https://blog.csdn.net/qq_28710983/article/details/82194404
    
*   https://wenku.baidu.com/view/9f509844e2bd960591c67723.html?fr=search-1-wk_seaincome
    

[一文打尽 Linux/Windows 端口复用实战](http://mp.weixin.qq.com/s?__biz=MzU1NjgzOTAyMg==&mid=2247489510&idx=1&sn=3ecd8cd6d115a44791c4c5f8684e2aa2&chksm=fc3faee7cb4827f15caae59fbb588cc18d163676e0f0c3f12715a7ad564cb213d758e20c9588&scene=21#wechat_redirect)
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**扫描二维码，****加入内网小组，一起畅游内网！**

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9l9FNcvFsJZ3BvAGHhTVOzKWkTtDU8iaQePhu5BbEibDolILr4Qrh9qa4f0xibBc0b9814Uiaq604kUQ/640?wx_fmt=png)

**扫描下方****二维码学习更多安全知识！**

![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9Y7Ac6gb6JZVymJwS3gu8cniaUZzJeYAibE3v2VnNlhyC6fSTgtW94Pz51p0TSUl3AtZw0L1bDaAKw/640?wx_fmt=png) ![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWa9Y7Ac6gb6JZVymJwS3gu8cT2rJYbRzsO9Q3J9rSltBVzts0O7USfFR8iaFOBwKdibX3hZiadoLRJIibA/640?wx_fmt=png)

 ![](https://mmbiz.qpic.cn/mmbiz_jpg/XWPpvP3nWaicjovru6mibAFRpVqK7ApHAwiaEGVqXtvB1YQahibp6eTIiaiap2SZPer1QXsKbNUNbnRbiaR4djJibmXAfQ/640?wx_fmt=jpeg) ![](https://mmbiz.qpic.cn/mmbiz_png/XWPpvP3nWaicJ39cBtzvcja8GibNMw6y6Amq7es7u8A8UcVds7Mpib8Tzu753K7IZ1WdZ66fDianO2evbG0lEAlJkg/640?wx_fmt=png)

**目前 30000 + 人已关注加入我们**

![](https://mmbiz.qpic.cn/mmbiz_gif/XWPpvP3nWa9FwrfJTzPRIyROZ2xwWyk6xuUY59uvYPCLokCc6iarKrkOWlEibeRI9DpFmlyNqA2OEuQhyaeYXzrw/640?wx_fmt=gif)