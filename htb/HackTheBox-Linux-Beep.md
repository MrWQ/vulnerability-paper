> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/83XAA6yJu75gGvjdoMjEDQ)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **94** 篇文章，本公众号会每日分享攻防渗透技术给大家。

靶机地址：https://www.hackthebox.eu/home/machines/profile/4

靶机难度：初级（4.6/10）

靶机发布日期：2017 年 10 月 16 日

靶机描述：

Beep has a very large list of running services, which can make it a bit challenging to find the correct entry method. This machine can be overwhelming for some as there are many potential attack vectors. Luckily, there are several methods available for gaining access.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/Rs43JcQMG15gQCkPJecqeZhHEYZSpnU4CtpugwowtibgcCJWF5xRByEzISmkYebj0iarlAL5XGEL0kb5kfq6r94A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljDgCvEnq3Qj3cUJqh96vvWRyEFQsPE3gH4A1PViaUSWqMn2rgfibGAeQmg/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.7....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljDV7t3PZgDttoZuLEVJoQqAialZ09x4ZHtBg0GfPE0iaQdKgL5c2zzia54A/640?wx_fmt=png)

Nmap 发现运行了很多端口，80 和 443 端口主要分析对象...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljD253BtsfBzImQ6xvsl4Gn54z063RwPoHcWzaKgBAbFLCxXZfhRrrkzQ/640?wx_fmt=png)

可以看到 https 服务是 elastix 软件系统，该软件系统是否存在漏洞... 查看下

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljD0WBtphTEZJcW9d9aFU57wU93UI8lm9cVu6fhiakY4Jy2ic4vvWfehAmA/640?wx_fmt=png)

可利用的漏洞有挺多，这里直接测试 37637.lp 即可......

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljDvvv3sD3WdkoF3I7u8URzfKkIuWyxrdqZVicb6OR7VtwHm9RbmicCbalw/640?wx_fmt=png)

理解：攻击者可以使用本地文件包含 LFI 来欺骗 Web 应用程序以在 Web 服务器上公开或运行文件，LFI 攻击可能导致信息泄露，远程执行代码甚至跨站点脚本 XSS...

这里存在 LFI 漏洞攻击...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljD5sFh9ZSNZXbYsWsUGteZq9viaO2v6SJfQ89lEF133B8dvtKicOV54F1w/640?wx_fmt=png)

通过直接利用 LFI 攻击...（就是简单的利用 URL 输入即可）

获得了有用的信息... 看起来很乱

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljDFJCHH9SWQa5cusFDuBC4ygKiaoQxibK9Bgz7rHSG75UGicUlPSTqamG0Q/640?wx_fmt=png)

通过查看前端源码会列举清晰... 可以看到了用户名和密码信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljDacIj5f6wI0aHEuibIiaPSqia8JvibVeHluH71mibwI64olHaxicThj7HlEpw/640?wx_fmt=png)

```
https://www.jianshu.com/p/4d8cd3e2a7d2
```

前面 nmap 发现开放了 ssh 端口，直接利用 ssh 登录 root 即可...

但是这里出错了...

Terminal 找不到支持的密钥交换方法，因为新版 Openssh 中认为 SHA1 这种 hash 散列算法过于薄弱，已经不再支持，所以我们需要手动去 enable 对于 SHA1 的支持... 推荐链接在上面... 修改即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljDQ6ro1DAAXxu1lXYcXiathSc1LvricgNice2zlu2Sf6LIDpa1YDf8SmpWA/640?wx_fmt=png)

通过 ssh 成功登录，获得了 root 权限... 成功获取了 user 和 root 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/Zo04aoPGhhftaGG0yuEeaxw97HRiaFa8WJW7libBkFeicrPny8KnvKmeezoNnqicGdpWHkOm3eGAIXwGohqRuZ6S6Q/640?wx_fmt=png)

这里还有很多可以利用的漏洞，我就不演示了...

例如：靶机系统应用版本 vTiger CRM 5.1.0 存在 vtiger 漏洞利用、或者 10000 端口存在 webmin 漏洞利用，mysql 看到 roundcube 显示的版本是 0.3.1.... 或者登录后利用文件上传获得 shell 等等...

千奇百怪的利用方式，只要抓住漏洞原理即可...

加油，学习~~~

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台简单的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/py7L4cx8wYvBYkElUsqDz94g2u3uiaKibfK2IkLjMkEBKezINP2n0PyX4GwcXC1vl0K8KWnITP6HhjIuhyUBIXbA/640?wx_fmt=png)

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