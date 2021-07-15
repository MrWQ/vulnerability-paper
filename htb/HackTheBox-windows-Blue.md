> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/1yjHn1MGdEjzGtCKXWZpTA)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **92** 篇文章，本公众号会每日分享攻防渗透技术给大家。

靶机地址：https://www.hackthebox.eu/home/machines/profile/51

靶机难度：初级（4.5/10）

靶机发布日期：2017 年 10 月 5 日

靶机描述：

Blue, while possibly the most simple machine on Hack The Box, demonstrates the severity of the EternalBlue exploit, which has been used in multiple large-scale ransomware and crypto-mining attacks since it was leaked publicly.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/ibqicBWEiaFhaUkEs3YhX1fKvaBcTc3V7YooNTGXoXQEGE8V3BGstZA0g9OpLlWicaefuM0zBUvxG3mPIlLdP7vnYw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/vekKnDibcricu2UWZUgqzbqic9EBkejl6uTaAp9pZqTSiaibKPpbJamzHXyE2iapH87vjcQHV7hz25QFcBibaMpyadLqg/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/sz_mmbiz_png/4yo5kHOX9ibN8ibibPy7W2Hr5gIiaWyWEuIGKPDgfhHf0oA2dpjKy7LLyBHicoTtfRED9OyIK92hpd9GhGqx3iaLln2A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMOXCJWFiaoeLa8bI6QJmiaRc5RMCWQpJias0xiaaOwOXjSsbe6SZric0qPy9wScv0Om9nvl7DV51Q8mnw/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.40....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMOXCJWFiaoeLa8bI6QJmiaRcZvicCe905TZMDBwAaWcZJhCkKegtx5iaCJI7icFTEL4TxSg1MUHPz4U2Q/640?wx_fmt=png)

nmap 发现 SMB、445 是开放着的...

当然靶机的名字是 bule，永恒之蓝.... 那就开始吧...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMOXCJWFiaoeLa8bI6QJmiaRcRGtNk1RnY1V3VFXrCr1KZl08DBTp3TmdMeZgMYw80lDz8VrCPv22JQ/640?wx_fmt=png)

都知道永恒之蓝是 MS17_010，直接 MSF 利用 search 搜索 ms17_010 的 EXP 利用即可...

然后利用 TCP 的 payload... 运行即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMOXCJWFiaoeLa8bI6QJmiaRcy7StYQsBEEHoydoRWEwCCDNE3zXgdqDPr0mGstZnc1XaWVJJqM6qOA/640?wx_fmt=png)

成功通过永恒之蓝漏洞获得了 system 管理员最高权限...

这里失败了几次，是因为 target 没选择...（记得选择版本性质）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMOXCJWFiaoeLa8bI6QJmiaRcu7DcQ5rXmUOiao3WBFCkCQO6PYtF13Ky8TnErhakHQp6Huzhic4auvEw/640?wx_fmt=png)

成功获得了 root 信息....

很简单... 利用 MS17_010 成功提权...

这里不利用 MSF 也行，去 github 下载永恒之蓝的 EXP 直接提权即可...

今天比较累，花了 2 分钟就拿下了靶机.....

由于我们已经成功得到 system 权限查看 root.txt，因此完成这台简单的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/ibqicBWEiaFhaUkEs3YhX1fKvaBcTc3V7YooNTGXoXQEGE8V3BGstZA0g9OpLlWicaefuM0zBUvxG3mPIlLdP7vnYw/640?wx_fmt=png)

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