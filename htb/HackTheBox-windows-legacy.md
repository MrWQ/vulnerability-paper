> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/-SaxD7Iqb-X4Wyot_SHb1g)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **55** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/RKmmCHT73fdQQ2nv9rDeddIlJk71QWHcslefZEPQxvuVzXNn9ZlY6dicKOiaJQBXNFYkbHtUsOw0duN5FIUuItSA/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines

靶机难度：容易（2.4/10）

靶机发布日期：2017 年 10 月 10 日

靶机描述：

Prepared By: Alexander Reid (Arrexel)

Machine Author: ch4p

Classification: Official

SYNOPSIS Legacy is a fairly straightforward beginner-level machine which demonstrates the potential security risks of SMB on Windows. Only one publicly available exploit is required to obtain administrator access.

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/xVzbJNmGHSCH5d0fX1bHZYbyKoFLsiapvaq5K6Oo80wFkVAmt04DEn4DSiagPY4oL5QTcTlFhJZsA5mbTUZTJFYQ/640?wx_fmt=png)

  

  

一、信息收集

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPz7JCO1KssgEwW4npruRIsp8PYpibl7f2O9asVvLI6obI7IZiaJMFrFwrjIZicVc0xb1MlYI7TyQe6w/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.4，windows 系统的靶机...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPz7JCO1KssgEwW4npruRIsvNbHb60lr7AhibRuicuXicN6KFVQjiccwYvasu0VOGdBYAqADP3Yibvjraw/640?wx_fmt=png)

开放了 139 和 445 端口...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPz7JCO1KssgEwW4npruRIsyRzrCe8kuGLhrTnJOrACMrSfNYZu4v4C3iaZ8zZPkoXBepPeeFIMlGw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPz7JCO1KssgEwW4npruRIsy6wIXn2eQlyNF1pS1YSKCog1sQPmTPQQPkUP4PHneAAPlKia8OuKkng/640?wx_fmt=png)

往下看可以发现 windows xp sp3 类型的 XP 系统...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPz7JCO1KssgEwW4npruRIsyM6HE0bv6MRPGgIuuaNIhnH7Zg3kibYzgzmSMNeicQpBFDxCXVqfaWPg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPz7JCO1KssgEwW4npruRIsBxrQmutkwwY3vsvgxPPuvrK7vIQ9omoiaaHj0ny75gkGvLoD2joRVRw/640?wx_fmt=png)

谷歌搜索，可以很容易发现利用 MS08-067 即可...

  

  

二、提权

  

  

打开 MSF...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPz7JCO1KssgEwW4npruRIsA5YjbequHmkWnOzrzpzTpLR1BgykBsKdfZIVB97k02LmibibqGeak3rg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPz7JCO1KssgEwW4npruRIsxY61UxYWV8fH4MsHicia2m4dz5PeJfJkNAib0oBclmf4YQXypA1R9ibe7Q/640?wx_fmt=png)

使用 set rhost 命令通过 HTB Legacy 框的 IP 地址设置远程主机...

然后 check 检查是否可执行...

然后执行即可...

可以看到已经进来了... 这边我先不进入 shell

我利用 meterpreter 进行直接查找 user.txt 在哪儿...（meterpreter 具有挺强大的功能，具体的自行查找谷歌）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPz7JCO1KssgEwW4npruRIsMRAQkCib8wBzwnLZwDSp820mJg7yEINTUtb89okQVYNWkibe8WwG3ZdQ/640?wx_fmt=png)

可以看到已经找到了，直接过去查看即可... 这里我就不查看了... 很简单的操作！！我继续看看还有别的方法吗...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPz7JCO1KssgEwW4npruRIsdNYictS8bDdGJaAaJU9HjagdibAuXW3AI6mgfSc8miauWHF3icsCvFiaGIg/640?wx_fmt=png)

这里往下翻，发现还可以利用永恒之蓝，试试...

![](https://mmbiz.qpic.cn/mmbiz_png/RKmmCHT73fdQQ2nv9rDeddIlJk71QWHcslefZEPQxvuVzXNn9ZlY6dicKOiaJQBXNFYkbHtUsOw0duN5FIUuItSA/640?wx_fmt=png)

由于我们已经成功得到 root 权限查看 flag，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/xVzbJNmGHSCH5d0fX1bHZYbyKoFLsiapvaq5K6Oo80wFkVAmt04DEn4DSiagPY4oL5QTcTlFhJZsA5mbTUZTJFYQ/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)