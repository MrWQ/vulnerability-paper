> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/MBqznl86bRqRVVWdrnZTTg)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **26** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/gBSJuVtWXPZE73MPxL1VoDjO3DFaxJA2MQpSSibwsXKVf4VIHh8S9fZXT8pq1ALE3hWEN22AaniaghxGrJqjEsxw/640?wx_fmt=png)

靶机地址：https://www.vulnhub.com/entry/pwnos-20-pre-release,34/

靶机难度：中级（CTF）

靶机发布日期：2011 年 7 月 4 日

靶机描述：pWnOS v2.0 是一个 Virutal 机器映像，它托管一个服务器以进行实践渗透测试。它将测试您利用服务器的能力，并包含多个达到目标（根）的入口点。它是为与 WMWare Workstation 7.0 一起使用而设计的，但也可以与大多数其他虚拟机软件一起使用。

目标：得到 root 权限 & 找到 flag.txt

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/ymNhlIRQRwIDdqQDCiblECK9VN2KquqTzJXM7etEnDcIpDdITqzFuiapav9TDnIiaGgf1e4sP9IO6B5NEtEyg2t5w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/eGDabDaNAhQ72wHWRToOUZR31X9kamiak0wrpr3lxKHpuoTpia329Xu6T0OTYlZic9XeEyQ4twasnibb924VBgIt1g/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9ra9PTgtmEnA4MM0ib3FVcNBEictg5TVicjH2b16DjWQ2VkDguKuXDw14j6ib7GibTS9Cq4rNUNyTjSw/640?wx_fmt=png)

记得这里要按照网站描述的内容修改自己的 IP、掩码和网关... 否则无法开始

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9ra9PTgtmEnA4MM0ib3FVc6KJ4Ajknag1tXyI3Aftd7Zqawqb10FpUzQupJEBpA5Dak5eyoHYprw/640?wx_fmt=png)

我们在 VM 中需要确定攻击目标的 IP 地址，需要使用 nmap 获取目标 IP 地址：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9ra9PTgtmEnA4MM0ib3FVcgghiaRoQqbs6VWhia5WLUWJCIJxssUuVqCMibDjh1MbRGxCAib3owMgYTQ/640?wx_fmt=png)

这其实已经固定了 IP，在描述中有介绍...10.10.10.100

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9ra9PTgtmEnA4MM0ib3FVcOVKSNnpmBlNkiahyWpTDLFQx0833sqmX0A5lvHHLYGXGnCWtSXMFokA/640?wx_fmt=png)

开放了 22 和 80 端口....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9ra9PTgtmEnA4MM0ib3FVcM0LtaOb1iaW8WtQraRor52icqJePnmODcOE6VusydVnUGicLZu9qQ3SbQ/640?wx_fmt=png)

打开网页，在右侧看到三个普通链接，分别是首页 / 注册 / 登录，前车之鉴，直接检查 robots.txt 文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9ra9PTgtmEnA4MM0ib3FVcc85lSNd98tn6zG7m5M7p57nvpuKBWkVwCPDgX3lVNbQ4ibY8oxGUWicA/640?wx_fmt=png)

.....404....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9ra9PTgtmEnA4MM0ib3FVcjafP5H4CaIEbFLNgic2hGC2uVJLHmRPaAddQBBkKT71LuSwmkic66Ozw/640?wx_fmt=png)

nikto 扫出个这地址... 看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9ra9PTgtmEnA4MM0ib3FVcHBakyYUB7JkCnpYJ9MO2FytTyQBOQC8DKib2XxI7YN5Ew8OuVsQHIyA/640?wx_fmt=png)

各种详细信息.... 跳过...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9ra9PTgtmEnA4MM0ib3FVcibIbZrMdIFDIWoWxTDbycs4ZV1ro06058Bqtt6x8dDEZ1R8Kz4ooia4w/640?wx_fmt=png)

扫到了 blog 目录，进去看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9ra9PTgtmEnA4MM0ib3FVcziaflKibrco5wOticvicKcW2LbNXmKTb41D8RibZEQ285clx374IKRmQ4eA/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9ra9PTgtmEnA4MM0ib3FVcF7Oud5iaVtH4icHT8rTuuJV2tM64EVQUKN1GOGZc8QVy12VMXT6KBlRQ/640?wx_fmt=png)

在前段源代码找到了该网站运行在 Simple PHP Blog 和 0.4.0 版上....

简单的 PHP 博客也称为 sphpblog，在 Metasploit 框架中搜索了 sphpblog...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9ra9PTgtmEnA4MM0ib3FVcXM64Hb7IWfpGyKM3SB1ic4cNNicwDjfuxh6l3sZ9NFcOm5MAbTIjTPfQ/640?wx_fmt=png)

直接利用试试吧... 直接暴力提权试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9ra9PTgtmEnA4MM0ib3FVctEeXMu94P91pghOpTPn0FtBgwVVfzJWIf8hPc60l8pmTay4PEcUSiaw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9ra9PTgtmEnA4MM0ib3FVcbTlXnta0iboTXgwSibYNncgGyWCyyDIbmhKA2rxMib0657S5J0Y23TXYQ/640?wx_fmt=png)

设置完后执行... 此漏洞未能直接拿 shell，但是创建了登录的凭证...（登录凭证都是随机的)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9ra9PTgtmEnA4MM0ib3FVcdHCVKibcjbry3VWGZUKXBSfYZzcpWzCg4c6WR8zqShu5VzdOa1xZjbA/640?wx_fmt=png)

登录成功....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9ra9PTgtmEnA4MM0ib3FVcjfyxHaEPUzomUNvdfzgHwoa0gzkia2O9icfkOt1nE1CmrCwQH4bYTgzQ/640?wx_fmt=png)

扫完每个大的模块... 这个直接可以上传... 简单的试了 txt 文件，可以上传....

制作个木马上传提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9ra9PTgtmEnA4MM0ib3FVcO37EXw4cM6jGIjebsYaXyUM9mQBGXI7MwO0G7iamx8MyKh9rtPIrgyw/640?wx_fmt=png)

上传成功...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9ra9PTgtmEnA4MM0ib3FVcQC5iaCHbD7DBvzZdoSBNxPicMQicJwhMguFLn6soRTvAfGLm5MEHlGFew/640?wx_fmt=png)

可以在前面爆破中对 blog 目录爆破结果，有 images 目录，这就是上传后的地址...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9ra9PTgtmEnA4MM0ib3FVc3nGLMM1TVJmsdu1uplgAaWaacs8BM5zQBIjaSVGaUlPwNZJp0g5xlg/640?wx_fmt=png)

可以看到我刚上传的 php-reverse-shell.php 木马文件（此文件在 / usr/share/webshells/php 中）

这里发现没改 PHP 数据，重新改下...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9ra9PTgtmEnA4MM0ib3FVciamZYC4RSQTCRibVPrSvjDME9ichiahevWyQM9fAO1T2HQj7ho6DTkibxDQ/640?wx_fmt=png)

成功提低权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9ra9PTgtmEnA4MM0ib3FVcGzZras0vDkkDgeic08wRicCWc2ZjhFibJNub3aZKicKBNoeaZHE9JbewfQ/640?wx_fmt=png)

这里经历了很多时间... 遍历了各种目录... 在 var 目录下的 mysqli_connect.php 文件中找到了 root 账号密码...root@ISIntS

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO9ra9PTgtmEnA4MM0ib3FVcHibFQ3UZMsGHptic8xBcicsJeldpMialg7Hz1DeaTricJ6RamibcEUu7CIxQ/640?wx_fmt=png)

成功提权... 没有 flag... 只要获得 root 权限即可成功...

![](https://mmbiz.qpic.cn/mmbiz_png/gBSJuVtWXPZE73MPxL1VoDjO3DFaxJA2MQpSSibwsXKVf4VIHh8S9fZXT8pq1ALE3hWEN22AaniaghxGrJqjEsxw/640?wx_fmt=png)

这边在低权用户查看内核版本后，谷歌搜索 Linux Kernel 2.6.38  perf exploit 利用 25444.c，直接 gcc 编译后提权也可获得 root 权限...

前期还可以用 Burp Suite 渗透工具进行 SQL 语句攻击，通过 Repeater 对 email 注入... 一步一步找到 shell.php 进行提权...

方法非常多，只要细心，漏洞就在身边... 加油！！

由于我们已经成功得到 root 权限，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/ymNhlIRQRwIDdqQDCiblECK9VN2KquqTzJXM7etEnDcIpDdITqzFuiapav9TDnIiaGgf1e4sP9IO6B5NEtEyg2t5w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/eGDabDaNAhQ72wHWRToOUZR31X9kamiak0wrpr3lxKHpuoTpia329Xu6T0OTYlZic9XeEyQ4twasnibb924VBgIt1g/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_jpg/O7dWXt4o5KO9ra9PTgtmEnA4MM0ib3FVcXC5Sow2w1Ogn5kn5LEJ2od1u2z9HYT6ibUbsLseiazBGP1M6xNTmdx8A/640?wx_fmt=jpeg)