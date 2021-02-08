> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/gFGL8FRTa-00yxMdvZW2dA)

遗憾的是：从来没有被坚定选择过，就像是，他只是刚好需要，你只是刚好在。。。

----  网易云热评

一、windows 常见用户及用户组

1、System

本地机器上拥有最高权限的用户

2、Administrator

基本上是本地机器上拥有最高权限的用户

3、Guest

只拥有相对极少权限的用户，在默认情况下是被禁用的

4、Administrators

最高权限用户组

5、Backup Operators

没有 Administrators 权限高，但也差不多

6、Guests

与 user 组权限相同

7、Distributed Com Users

域及域控制器相关用户组

8、Network Configuration Operators

专门管理网络配置的情况

9、Performance Log Users

专门远程安排性能计数器的日志工作

10、Performance Monitor Users

专门远程监控计算机的运行情况

11、Power Users

低于 Administrators，高于 Guests 组

12、Print Operators

低于 Administrators 组权限

13、Users

用户账户组，低权限的用户组

14、IIS_WPG

如果安装了 IIS，用来运行和控制 web 应用程序的账户

![](https://mmbiz.qpic.cn/mmbiz_png/8H1dCzib3UibvR8vUSG7AovrYfCdIAiaHV9hzXAnSQ3PANsACmMFiciauWibRtuniaKQ5eDL5yx0ZiaghWvOFv1Tuufyuw/640?wx_fmt=png)

二、windows 目录权限

1、右击文件或文件夹，修改其读写权限

![](https://mmbiz.qpic.cn/mmbiz_png/8H1dCzib3UibvR8vUSG7AovrYfCdIAiaHV92aRfdeW4vUWtptnKnZJkF9nPd5q9xicbZtdWekYGeWKDC7oibt6ibeWWA/640?wx_fmt=png)

2、点击添加，计入相应的用户组

![](https://mmbiz.qpic.cn/mmbiz_png/8H1dCzib3UibvR8vUSG7AovrYfCdIAiaHV9RNxvicgcc3a2zZfVLia2GZF97GuIhbEPMywddBV9ayCLe4EHRxY7dI6g/640?wx_fmt=png)

三、windows2003 默认权限

1、默认只安装静态 http 服务器

2、匿名账号不再具有 web 服务器根目录的写权限

3、IIS6.0 中默认禁用了对父目录的访问

4、坚持最小原则，不要给文件多余的权限，需要执行的不要给写权限，需要写权限的不要给执行权限等等

四、不同环境下的木马运行区别

1、在系统上运行木马是系统权限运行, 在 Webshell 下运行木马是以当前内置中间件（IIS，apache，tomcat）权限运行。

2、IIS 下是以 IIS IUSER 安全帐户运行的, 第三软件一般是管理员权限运行的。

五、服务器常见端口

1、445 端口

 SMB，windows 协议族，445 端口是一个毁誉参半的端口，有了它我们可以在局域网中轻松访问各种共享文件夹或共享打印机，但也正是因为有了它，黑客们才有了可乘之机，他们能通过该端口偷偷共享你的硬盘，甚至会在悄无声息中将你的硬盘格式化掉，永恒之蓝漏洞就是利用该端口。

2、137/138/139 端口

137、138 为 UDP 端口，主要用于内网传输文件，而 NetBIOS、smb 服务的获取主要是通过 139 端口。

3、135 端口

135 端口主要用于使用 RPC（RemoteProcedureCall，远程过程调用）协议并提供 DCOM（分布式组件对象模型）服务，通过 RPC 可以保证在一台计算机上运行的程序可以顺利地执行远程计算机上的代码；使用 DCOM 可以通过网络直接进行通信，能够跨包括 HTTP 协议在内的多种网络传输。

4、53 端口

53 端口是 DNS 服务的通信端口，所以一般来说，这个端口不到万不得已时不会关闭的。

5、389 端口

服务器上的 389 端口用于 LDAP，使用 TCP 和 UDP 协议。当客户端访问服务器的 LDAP 服务时，首先使用 TCP 协议连接服务器的 389 端口，如果失败则转用 UDP。在域过程中一般在域控上出现该端口。

6、88 端口

Kerberos 协议是一种 bai 基于密钥分发模型的网络身份验证方法。该 du 协议使在网络上进行通信的实 zhi 体能够证明彼此的身份，同时该协议可以阻止窃听或重放攻击。Kerberos 密钥分发中心 (KDC) 在该端口上侦听票证请求。Kerberos 协议的 88 端口也可以是 TCP/UDP。

7、5985 端口

该端口是 WinRm 服务，允许远程用户使用工具对 windows 服务器进行管理并获取数据。

禁止非法，后果自负

欢迎关注公众号：web 安全工具库

![](https://mmbiz.qpic.cn/mmbiz_jpg/8H1dCzib3UibvR8vUSG7AovrYfCdIAiaHV90VH3goAzXCsht7exXWD6n7vCsHWWTiaNITMtI0nXgicfT3Yjb5lSjqZA/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/8H1dCzib3UibvR8vUSG7AovrYfCdIAiaHV9E2Pxt8nsVtVeMsdgSicR137bvmg4tttTEcsKKicGULpk0XWKZY2kHo8Q/640?wx_fmt=jpeg)