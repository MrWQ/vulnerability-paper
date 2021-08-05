> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/x3GK7o_jxoWsqKJ0bm7lVA)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **109** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/AhUATAqa6tibYa4zTrlvc4l1rFIH7HV8c7ibcicw1jgibbwVW2zia9JeVCleEKLjkT0RO7sJS34DVSzMJ9sGsIAn5Fg/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/48

靶机难度：初级（4.5/10）

靶机发布日期：2017 年 10 月 5 日

靶机描述：

Blocky is fairly simple overall, and was based on a real-world machine. It demonstrates the risks of bad password practices as well as exposing internal files on a public facing system. On top of this, it exposes a massive potential attack vector: Minecraft. Tens of thousands of servers exist that are publicly accessible, with the vast majority being set up and configured by young and inexperienced system administrators.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/oQI1m5hhwD5Gicl7xUf6kh3ISTH6iacM05s8G12QVAykGzh7S5Po8EgeS5XJvZbiacbS8AuRQJ1VaRic18jlToOhVQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/0fb0Y1M6icJJia7t9xsBuUuxZQgOLeWHYicicRpfEiahMz3mlpK0icx8qLpfMLDojhD7IwSE2IalXVBBFs9E1Z88Ka3Q/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/PRVgXdHra5CzBfuOaOX4dpiaoOia6WZfdos1RiaJEZJG7nrnxTkXBoianpRmkQTmqkmW3zkbaQqjAu6WwBYAmyGibiaQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMLuticE5cpNXc6y1duWStWLXfmUAWQGlYRG8R95eiaoFNpPcAFyNMh9SugYDCsbWlcKAUmCaG83SVw/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.37....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMLuticE5cpNXc6y1duWStWLFKWicnRP64bOcAtLRiaFpUuXc6r9ibGepSHDwVibaWyZ221GDQPWq4ib11g/640?wx_fmt=png)

nmap 发现开放了 22 和 80 端口....wordpress 4.8....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMLuticE5cpNXc6y1duWStWLIPCdcvaOMxzW2x7weo2icRcaicZcQ9icDjtPfk9Zd97aeSwuViakftexAg/640?wx_fmt=png)

浏览主页未发现有用信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMLuticE5cpNXc6y1duWStWL1OhHUmSDxCWvOAjMQDI8jolNMefeMHrkR6m6aetnOuucH3iaNIHFesQ/640?wx_fmt=png)通过爆破目录... 发现了 wp-admin 和 plugins 有用的目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMLuticE5cpNXc6y1duWStWLs3fDgJxMf7aUBMN7TrBjkuXnO0jhicMq21l9esERESA1icjiaPm9zOibsA/640?wx_fmt=png)

这是个博客登录页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMLuticE5cpNXc6y1duWStWL4jXibO1Jx3FS6nuTZeGflGVtpKyXly3FjdUk3AaNZyv7NbvJdCHRh0A/640?wx_fmt=png)

访问 plu... 目录发现两个文件... 下载查看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMLuticE5cpNXc6y1duWStWLicpbtVacibExBWCslC9hjUpdfySEWiclzBPCjqYhcvD5460KgsQkjFZMg/640?wx_fmt=png)

发现这是 java 文件... 需要利用 jad 查看....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMLuticE5cpNXc6y1duWStWLVhcgLnu2PcwnR5zkWwXSRt8VfD8uOazQJHFr24fX0agobjItnzniaFA/640?wx_fmt=png)

安装 jad....（2020 版本 kali 没自带）...

然后转存 jad 文件.....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMLuticE5cpNXc6y1duWStWLiadP3GSzkVnQnibQf8fRQmgrhshURCus4ePiaP1z8DGkZx4D5C3TKrgGg/640?wx_fmt=png)

通过查看，发现了里面内容存在 password 信息....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMLuticE5cpNXc6y1duWStWLaNdbZPdAZiaZo3byNwcsL6sVBQXyb40M18k2maehMxsB0jNIb1sNbPA/640?wx_fmt=png)

通过获得密码登录 wp-admin，账号密码错误.... 利用 wpscan 枚举看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMLuticE5cpNXc6y1duWStWLecKUEteQYREAXLniceUCiaMf9uic64MWHmfUnClFEKibdpPaAxzULSZ38g/640?wx_fmt=png)

利用 wpscan 枚举发现 notch 用户名.... 但是继续利用密码登录 wordpress 博客还是无法访问....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMLuticE5cpNXc6y1duWStWL6piaOYc2oLGA3Spnib7jLTb4JgbJgxe1ctZ95fEFlCCkB05zysE8x3Tg/640?wx_fmt=png)

通过 ssh 成功登录了 notch 用户... 并查看到了 user 的 flag 信息....

sudo 查看到 ALL/ALL.... 直接提权即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMLuticE5cpNXc6y1duWStWLRvVr6uLYQ55wemhfUlK36CQZfszQEp2x8OtkjbKbmQCroohKgQHEJA/640?wx_fmt=png)

直接提权 root 获得 flag 信息....

![](https://mmbiz.qpic.cn/mmbiz_png/AhUATAqa6tibYa4zTrlvc4l1rFIH7HV8c7ibcicw1jgibbwVW2zia9JeVCleEKLjkT0RO7sJS34DVSzMJ9sGsIAn5Fg/640?wx_fmt=png)

简单的一台靶机....

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台初级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/oQI1m5hhwD5Gicl7xUf6kh3ISTH6iacM05s8G12QVAykGzh7S5Po8EgeS5XJvZbiacbS8AuRQJ1VaRic18jlToOhVQ/640?wx_fmt=png)

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