> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/i7iuqR3lRFuKS7ZQ5I08iA)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **114** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/9qXnTkZPuxe8H1QicBcbrQQVKOeKw2PsaPtbkhed7icVWmmGk0o3VgYFqKdtNwPFicT2aW803Yp7DqjdiaoFRYVX3A/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/64

靶机难度：初级（4.3/10）

靶机发布日期：2017 年 10 月 3 日

靶机描述：

Mirai demonstrates one of the fastest-growing attack vectors in modern times; improperly configured IoT devices. This attack vector is constantly on the rise as more and more IoT devices are being created and deployed around the globe, and is actively being exploited by a wide variety of botnets. Internal IoT devices are also being used for long-term persistence by malicious actors.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/gUVKXuw5icTuicMe1TSd3CYPJzxFcxUnzpBLmOY2lYosbSmH5Ro01bJbqOVUwZ97d098kTPyiaWWicblornticcLu9w/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/xm4F2hYetPjEQESs45UQXRGBy3wswtHDWMZz77ibhszjBEbNjYqjTeF5Oiabq6YwXD7bWyT7xPAPcTPnasSXbSkA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/ZkKbicS7g7ZHYZnHJIaEIGnCFUcfEpoZzbNbicBMkmZsoicIR4wRS4gabRwDEkG2qXlDxM2mJPI62cpq1pM3Alm5w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM28fbZ0nwxxta8buPuaT8GwQckqAaqk5icKR9EAMibs67JuO1Xyh7pXV3MyUm162JuqVOWlLAGyq5A/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.48....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM28fbZ0nwxxta8buPuaT8G3OPkWpABZJZZ47p1GIZnxPMxPya9s5hbljc3sHprxUAttlIc6hajGA/640?wx_fmt=png)

nmap 发现开放了 ssh、dnsmasq、http....

访问 web 空白页... 直接爆破...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM28fbZ0nwxxta8buPuaT8GFHF8VNVsFxd3c7o0Iv3ZGzTHibV8BA20UkcJeqUJSaCIADh2gicMVpMw/640?wx_fmt=png)

爆破发现两个目录....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM28fbZ0nwxxta8buPuaT8GdzyjjEeoM7kic9icTdAnxSriauQebXfxgPIFmnH38hia8L3lwdKV0z4cpA/640?wx_fmt=png)

访问 admin 目录，这是一个 Pi-hole 框架的页面....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM28fbZ0nwxxta8buPuaT8GDamvGSe6Ym8ezMXiaC0WORBnIln7kzZFLjYR6YWSsKv1NzLOFFejbag/640?wx_fmt=png)

google 引擎搜索该框架默认密码.... 获得了

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM28fbZ0nwxxta8buPuaT8GjHtWKXuWyyGt8NPaRSs8CZibGN7rfbdtc18ZlpOJBokMPJvWZWiaXrwQ/640?wx_fmt=png)

```
medusa -h 10.10.10.48 -u pi -p raspberry -M ssh
```

或者利用 medusa（美杜莎和九头蛇 hydra 差不多）进行强行爆破....

获得了账号密码....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM28fbZ0nwxxta8buPuaT8GoBCNsvun66IoNoyT4icvcefvNWT5h56TWL9w7Ixbo0FfJsKOjiaXicevA/640?wx_fmt=png)

成功登陆，并获得 user_flag 信息....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM28fbZ0nwxxta8buPuaT8GvLvDICmFjQliaCXtvSzKRJQbU9CeNLY1SVIYNK7Vou4RjkZ60Hr9XYg/640?wx_fmt=png)

sudo 发现 ALL... 可以执行任何命令提权... 直接提到 root 权限...

读取 root_flag 发现该内容存在了 USB Stick 内...

检查了靶机上的内存利用和挂载... 发现了 / media/usbstick 和 / dev/sdb 两个文件都是 USB 挂载的内容...root_flag 应该隐藏在其中...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM28fbZ0nwxxta8buPuaT8GRNfdwcbogXWQ1cVEJG2MWsWLSkoNVH0PteT2REUhTRIxcKPibSEpxMw/640?wx_fmt=png)

mount 看到了他们的权限... 查看 usbstick 提示了不小心删除了内容... 需要恢复删除掉的内容...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM28fbZ0nwxxta8buPuaT8GIzvhwRmSDtsiclyAv3GxMviaL8q5KyRm6fGia6OqWCBjl8ia1a3LqrNXNA/640?wx_fmt=png)这里利用了 string 检查了 sdb 丢失的信息... 运行后直接显示了 root_flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/9qXnTkZPuxe8H1QicBcbrQQVKOeKw2PsaPtbkhed7icVWmmGk0o3VgYFqKdtNwPFicT2aW803Yp7DqjdiaoFRYVX3A/640?wx_fmt=png)

简单的靶机....

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