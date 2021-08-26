> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/qTBiGtC1XQ0flI7R8VKITA)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **127** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/sGWlDp8sFCl67vCmcZr3JtQP0jB8suQiaKaKCVYPOezloiaicS8xMkAriaAQd3dTOPXicBTVStlX66kEffEWJOiczUTA/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/132

靶机难度：初级（3.5/10）

靶机发布日期：2018 年 9 月 8 日

靶机描述：

Poison is a fairly easy machine which focuses mainly on log poisoning and port forwarding/tunneling. The machine is running FreeBSD which presents a few challenges for novice users as many common binaries from other distros are not available.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/o62ddIpxjBd0kv6p3zb6uf1GiaCo9PiaF12hWQQSurxFPuVIDtsNTgUpjjvmib7GxKXNePVMAwJfzuib52MWoORPYg/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/Clq0o4fE5u6X5A1maTmqcvtEibdrsDO41kZPibRCHsX3Koj69GFK2qOyPwdcrgcDkHklrdJzBCiaQPuMVe11oSYHA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsgZldp8DTHcdVWoJmMW626nwhE4kic5HbcSGoYhzNRWN5UMy7zSTpNIG2X4BjHaX2icg7yu7zZ17A/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.84....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsgZldp8DTHcdVWoJmMW62iajCHLJC4XVQSbcNsLXiaOnQ4ddmRvVytDgIxnKxj7M1ajFYnbhZF5dw/640?wx_fmt=png)

Nmap 发现仅开放了 OpenSSH 和 Apache 服务...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsgZldp8DTHcdVWoJmMW62BibWO4YPMMs7qzsPUmazQQNy9UlgiciaB1uMQPOneEK3iccPpN2U4Y3lLQ/640?wx_fmt=png)

访问 apache 服务发现这是测试页面，该站点是测试一些 php 脚本...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsgZldp8DTHcdVWoJmMW62Txz8Ynv41baORhsnJPic08JjnibiaEDw2F3zNTzlAo9BtLHjJsfBNQQhA/640?wx_fmt=png)

查看 listfiles...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsgZldp8DTHcdVWoJmMW62aueSNeV4TeIgsvLiaR85icVoO8cFej2c8rL65NaMLiaRSRnFzPmKfkMQQ/640?wx_fmt=png)

发现了 pwdbackup.txt 文件... 继续查看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsgZldp8DTHcdVWoJmMW627jB6Aa82PPibz8aJSa8aJRaIP3W6B2ia5snEWyVwpf2IO9RRFLiaLQUJg/640?wx_fmt=png)

发现了 base64 值...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsgZldp8DTHcdVWoJmMW626iby2BD1p5YbCRRta5ibtdUKhV4k2qDKia4BFnqGpicqVvVb6NJSicOUBoQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsgZldp8DTHcdVWoJmMW62oib2ahib7UhXk4wtokNVaibyDSM1FlRLJwZZcCLDbu07scKtAibQanUS4g/640?wx_fmt=png)

通过解码发现还是 base64 值，通过解码了很多次后，获得了最终密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsgZldp8DTHcdVWoJmMW62JqnfcooMa28VDwdCBiaLiaW2SOSR5uWNpEOicdv9xElCB8MUXVHwj1rLA/640?wx_fmt=png)

该页面文件还存在 LFI 攻击行为.... 获得了用户名...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsgZldp8DTHcdVWoJmMW62S9jhqyLQibjreibZr9GAyX1VIKaIbgQl4vRxQPIhqzLkwdjlBsaFd0qg/640?wx_fmt=png)

SSH 登录... 获得了 user_flag 信息....

很简单的获得用户名密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsgZldp8DTHcdVWoJmMW622Ctz8WcdSyXaNq1thEPwtTO3YJbHTWEqZcLyUfMsksbmHhoymQSwHg/640?wx_fmt=png)

在 user 目录下，还存在 secret.zip 解压文件... 传到本地解压用的就 base64 的密码，解压后获得文件.. 发现这是 ASCII 编码文件....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsgZldp8DTHcdVWoJmMW62K6JIcZ3H36vRTRY48fo1fPRIU3wV520SZlezRv5X70RLPggqMsNUJw/640?wx_fmt=png)

继续枚举，发现本地开放了 VNC，可以端口转发远程了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsgZldp8DTHcdVWoJmMW62cmSNF6sjeGYx2283HiaEKsdRId7cfTfOVW8m8IryM2ia72uOZcloGL4w/640?wx_fmt=png)

进一步查看，root 执行的... 开始端口转发

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsgZldp8DTHcdVWoJmMW62sXdN5RMPhvE32DKm48HF0bLDPWjKGX3NPfTM4P0I1qqC2uG2YPBDsQ/640?wx_fmt=png)

```
ssh -L 5901:127.0.0.1:5901 charix@10.10.10.84
vncviewer 127.0.0.1::5901 -passwd secret
```

通过本地端口转发，利用 vncviewer -passwd 调用 secret 密匙文件... 成功登录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsgZldp8DTHcdVWoJmMW62c0o9yQ1ibgD5BSgrUicE9c517NgW8eRibgLXuvnz3YHJpp2DSTZPia2yKQ/640?wx_fmt=png)

获得了 root_flag 信息....

![](https://mmbiz.qpic.cn/mmbiz_png/sGWlDp8sFCl67vCmcZr3JtQP0jB8suQiaKaKCVYPOezloiaicS8xMkAriaAQd3dTOPXicBTVStlX66kEffEWJOiczUTA/640?wx_fmt=png)

这台靶机很简单，端口转发遇到太多了...

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台初级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/o62ddIpxjBd0kv6p3zb6uf1GiaCo9PiaF12hWQQSurxFPuVIDtsNTgUpjjvmib7GxKXNePVMAwJfzuib52MWoORPYg/640?wx_fmt=png)

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