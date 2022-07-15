> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzI2NDQyNzg1OA==&mid=2247484698&idx=1&sn=e28e08ed5a5f7142097afd5891ddde58&chksm=eaad8527ddda0c31bd8f4fefd0027bd05d7e4124eb85c693eb412002cb142935b25a8699e5a6&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtbYTcicAoW9icPXtbEF6vhbuHZZW3aC8ib5Z0VJagnwtPQHeSz5cfagxnA/640?wx_fmt=png)

CobaltStrike 中 DNS Beacon 的使用

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEt3UibmWe8xvzN9soLcT6IXJzaqx83okQ4icbSctrUon5tCzpiaoRUtuL1g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtMF6dDdOoFmnN0sv7KBuSUK1OFRx6ov4h7Se6G4qQWoq73TTJ2xicTQA/640?wx_fmt=png)

目录

1：部署域名解析

2：CS 开启监听 DNS Beacon

3：生成 DNS 木马

4：上线

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtMCib5Py2hjlKWhUArXxwQicPDvuxb88nFUZpibM3KcZEbIJy1yINvXicibg/640?wx_fmt=png)

  

在之前的文章中我介绍了使用 DNS-Shell 和 Dnscat2 利用 DNS 协议来进行命令控制，通过 DNS 协议进行通信，使得流量更加隐秘，躲避 agent/DLP 等安全设备的检测，实现相对隐秘的命令控制。

传送门：使用 DNS 进行命令控制 (DNS-Shell)   、 使用 DNS 进行命令控制 (dnscat2)

本节我将介绍如何使用 CobaltStrike 中的 DNS Beacon 利用 DNS 协议进行命令控制。

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtMCib5Py2hjlKWhUArXxwQicPDvuxb88nFUZpibM3KcZEbIJy1yINvXicibg/640?wx_fmt=png)

  

1：部署域名解析

首先，用一台公网的 Linux 系统的 VPS 作为 C&C 服务器 (注意：VPS 的 53 端口一定要开放)，并准备好一个可以配置的域名 (这里我们假设是 hack.com)。然后，去配置域名的记录。首先创建记录 A，将自己的域名 www.hack.com 解析到 VPS 服务器地址。然后，创建 NS 记录，将 test.hack.com 指向 www.hack.com

*   第一条 A 类解析是在告诉域名系统，www.hack.com 的 IP 地址是 xx.xx.xx.xx 
    
*   第二条 NS 解析是在告诉域名系统，想要知道 test.hack.com 的 IP 地址，就去问 www.hack.com 。
    

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtic4zO2Wlnzgib1pia9u96iazDJVhFJCchCh4yibemECBhWo59YPicRjFG7VA/640?wx_fmt=png)

为什么要设置 NS 类型的记录呢？因为 NS 类型的记录不是用于设置某个域名的 DNS 服务器的，而是用于设置某个子域名的 DNS 服务器的。

**如何验证域名解析设置是否成功？**  
在随便一台电脑上 ping 域名 www.hack.com ，若能 ping 通，且显示的 IP 地址是我们配置的 VPS 的地址，说明第一条 A 类解析设置成功并已生效。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtDadsBegDB6j7BttYa2o9kkZKlOibHNGazFpkzqJzicpUIcgkpvqgBstA/640?wx_fmt=png)

然后在我们的 VPS 上执行以下命令监听 UDP53 端口  

```
tcpdump -n -i eth0 udp dst port 53
```

在任意一台机器上执行  nslookup test.hack.com 命令，如果在我们的 VPS 监听的端口有查询信息，说明第二条记录设置成功

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEt3Dib6AlbgYicuJSM6Sz5AzYYON3wTXsVBj0aFkWbv63JQUSxY5p9yCAg/640?wx_fmt=png)

2：CS 开启监听 DNS Beacon

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEt3SicSzylHiblETwiavlmxVW0ysV8R1KGNpA89POZNUWvQUZc3LNVdMMFA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtrG3mQSyyUMGD3Uic1yeEicmoicdkt2FYTCTHjiaoyuWVgkUFeZVvUktQibQ/640?wx_fmt=png)

3：生成 DNS 木马

注意，这里生成的类型的是 Windows Executable(S)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtstK92WNSjd8rHVsQBOsPovTzJz6H0bvMBJn7PwZkylg6wibQ68cXfYw/640?wx_fmt=png)

这里勾不勾选 x64 取决于目标主机的架构

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtMUuAr52rmjicPIY7iaIC4liaoz44aD3h2JgfwXKmG9x4j4yibz3TDe8LrA/640?wx_fmt=png)

4：上线

只要木马在目标主机执行成功，我们的 CobaltStrike 就能接收到反弹的 shell。但是默认情况下，主机信息是黑色的。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtQ65QF9NAcatpkTxNKlho1yXgbB1pwJOuhMhtRsBUJXMDyjO2jlKFKw/640?wx_fmt=png)

我们需要执行以下命令，让目标主机信息显示出来

```
checkin
mode dns-txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtoIkf0ODaj8yuJyqGAUrfO3JXf3nvicUciaL2KbATEG6H6liaZLtnFnpaQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtaLD0mYI22eJJqxwx6lqRpgJibDOXA9HgxITiatDY5V4IeDm8xSR6YdNA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtMCib5Py2hjlKWhUArXxwQicPDvuxb88nFUZpibM3KcZEbIJy1yINvXicibg/640?wx_fmt=png)

  

责编：vivian

来源：谢公子博客

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtsJuyRVnicFCV2icKzJfAGd7ru8z4dxXLvAsnKuuqHzaG0rrDkicyWOibdw/640?wx_fmt=png)

由于文章篇幅较长，请大家耐心。如果文中有错误的地方，欢迎指出。

有想转载的，可以留言我加白名单。

最后，欢迎加入谢公子的小黑屋（安全交流群）(QQ 群：783820465)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEt3mZ0WohIhKXT7X9ewrSurKzdK64DXn9qxiaspahiafk3K2rfBVibLiaM0w/640?wx_fmt=png)