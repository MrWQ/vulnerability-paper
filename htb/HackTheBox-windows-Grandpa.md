> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/r8x-9vt6B0zNGDUQCZTong)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **60** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/2ichQqW6XvPlgohk6kjVu8GYOQ2Oco557j1bibkVCOsbLrO28pO7Lws1oVXcvS90GtYFe9Va2cepbqXjuziaDrnibg/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/9

靶机难度：中级（4.7/10）

靶机发布日期：2017 年 10 月 4 日

靶机描述：

Grandpa is one of the simpler machines on Hack The Box, however it covers the widely-exploited CVE-2017-7269. This vulnerability is trivial to exploit and granted immediate access to thousands of IIS servers around the globe when it became public knowledge.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/70aCp38I3nX6dfnC3RPrQfDeuwyvRCkVZ5NrvqgrPsUd76ALjnYzdoWubzsdbaGpIBU9LdWWaN6eK2jaDkibicFA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/b96CibCt70iaaicHUKVLMp2vK1qtPdpGSbdv2jBibBxItFggOpRe3hL5TOp65RnqnPwwqOUjiaJ345H9Ps0n4VMOm7Q/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOhuIibf5Qx9UEibOk15jYXeUuwOzdpCYqR6svibX4l74rm8vsfZlP6zyDTwo8zuAYf9CUVdsOEsr8zg/640?wx_fmt=png)  

可以看到靶机的 IP 是 10.10.10.14，windows 系统的靶机..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOhuIibf5Qx9UEibOk15jYXeUynGoWYSp1cBwugsD6nwAqqDss1sQNwfibcQ3DJKOncozADMVENjtl0w/640?wx_fmt=png)

nmap 扫描发现的内容很熟悉，和 Granny 一样....

Microsoft IIS version 6.0/、webdav、Windows Server 2003 ....

还有官方文档介绍的可以利用 CVE-2017-7269 漏洞...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOhuIibf5Qx9UEibOk15jYXeUQzUVkj8P1YjP6ibBdWpIqJicABbRbtcKKLBU3UuYOPJ84PPARo2jVmUg/640?wx_fmt=png)

访问 80 也是和 Granny 一样 web 服务器处于建设开发状态...

![](https://mmbiz.qpic.cn/mmbiz_png/b96CibCt70iaaicHUKVLMp2vK1qtPdpGSbdv2jBibBxItFggOpRe3hL5TOp65RnqnPwwqOUjiaJ345H9Ps0n4VMOm7Q/640?wx_fmt=png)

二、提权

这里直接利用 Metasploit...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOhuIibf5Qx9UEibOk15jYXeUxkLthQ90Ch5tH5qsp9qyABcdlZibicpRFXrbJySGvdUXmtjO0e9FibymA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOhuIibf5Qx9UEibOk15jYXeU6XpPmTbLLEHmxwUfC4wJ68Q1v1PmSicRXic0zhAmiaRibUSvwZkRIb8LuQ/640?wx_fmt=png)

直接利用 CVE-2017-7269 漏洞提权... 成功...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOhuIibf5Qx9UEibOk15jYXeUFf6ytyomYynbuDibABnrIHDia4NPuBicibohtUgGpqtX2qbqoCQvTicj4EA/640?wx_fmt=png)

漏扫发现还是有 7 个可以利用成功的漏洞...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOhuIibf5Qx9UEibOk15jYXeUMkMTLj18K7He7uLR5sokXtWEVlWMZ9SHCkiaIBibwclNbxyWmn8ZluYg/640?wx_fmt=png)

已经利用 EXE 成功，但是还是 network service...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOhuIibf5Qx9UEibOk15jYXeUVThoeaiaVm8McfIaMubyI9ic6iatzJzo2EzSMoIibvfCHGLm60UdkAAbRw/640?wx_fmt=png)

这里随便利用了 7 个漏洞中的一个... 成功获得 system...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOhuIibf5Qx9UEibOk15jYXeU1JmowvCY0HWQkTd5PbAJBdBS6XmRMyGouDv2DocPKByM3DUax6y8gw/640?wx_fmt=png)

可以看到，直接获得了 root 和 user 的 txt 文本信息...

利用 Metasploit 提权几分钟就完事了....

![](https://mmbiz.qpic.cn/mmbiz_png/2ichQqW6XvPlgohk6kjVu8GYOQ2Oco557j1bibkVCOsbLrO28pO7Lws1oVXcvS90GtYFe9Va2cepbqXjuziaDrnibg/640?wx_fmt=png)

这台靶机水友们综合评价是 4.7 分，如果用 webdav 进行渗透提权的话，肯定值 4.7 分... 可是我反正来了，这台我直接几分钟搞定了，反而另外一台 Granny 靶机 3.0 分我用了 webdav 进行渗透提权...

另外一种方法不利用 MSF 的，直接参考 Granny... 我都写得很详细，现在深夜凌晨了... 休息了... 明天看全明星赛！！加油...

由于我们已经成功得到 root 权限查看 user.txt 和 root.txt，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/70aCp38I3nX6dfnC3RPrQfDeuwyvRCkVZ5NrvqgrPsUd76ALjnYzdoWubzsdbaGpIBU9LdWWaN6eK2jaDkibicFA/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

**2021.6.9~2021.6.16 号开启收徒模式，实战教学，有想法的私聊！**  

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)