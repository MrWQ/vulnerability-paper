> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/AORsj8uUxQVOhGe5g1nflQ)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **72** 篇文章，本公众号会每日分享攻防渗透技术给大家。

  

靶机地址：https://www.hackthebox.eu/home/machines/profile/98

靶机难度：中级（4.7/10）

靶机发布日期：2017 年 10 月 19 日

靶机描述：

Mantis can definitely be one of the more challenging machines for some users. For successful exploitation, a fair bit of knowledge or research of Windows Servers and the domain controller system is required.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/wucQH64lHvpOxUzKZzgrk8rOIbSiaoFokwT3HYichsCpM6ibw80Jw5WmZL4vQs947UAIP2l7bicjV6MJECFp51G6sQ/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_gif/YnfnlicbPtFCfftiaRIe6t8lnrv9ueWwt2uANWPZAx8iaPnlPia0gncwDAsUiahaOibGg7mB0jYgTwdk6uNt4Bib5dHMw/640?wx_fmt=gif)

一、信息收集

  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOhMcLOqmTGpJicGzuDBe4t2G2oxMvK4mKqzlyFel2ibvmciaO4iclbRHLJBqlWVEJqnicdZJbnDGh1SPA/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.52....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOhMcLOqmTGpJicGzuDBe4t2hI33MfPU4QHCf1mKVnJqOetkOIbrg41MFMeqibBVYNOzAichy1ndC4cw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOhMcLOqmTGpJicGzuDBe4t2jFSqTXnDgibRuBhuFKdYatIuHFJK1BnNEkjUveMkbuGMibBia3BJBUw1Q/640?wx_fmt=png)

Nmap 扫描发现开放了很多服务，这里主要关注 1337 端口上的 IIS 服务器和在 1433 端口上的 SQL Server Express 即可.. 扫描还显示了带有主机 mantis.htb.local 以及 htb.local 的域控制器....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOhMcLOqmTGpJicGzuDBe4t2ZnztbFY5urqSc8pMNBfgorjYHibxQVw3MytqzfcfBCicXOVylsNqDFUg/640?wx_fmt=png)

看到了 IIS7 的图像没别的信息，爆破看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOhMcLOqmTGpJicGzuDBe4t2jjicj1BRR828YoiabgibEibbibxJGng6blgjhsorqhyyOpqKlEL6OMrgnpQ/640?wx_fmt=png)

发现了 secure_notes 目录... 访问

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOhMcLOqmTGpJicGzuDBe4t2f0jAP8oY0yLAU8O6nQJY2VzdIlVPTehtxgJXIhmPsFIL7dyic99jicaw/640?wx_fmt=png)

发现两个文件....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOhMcLOqmTGpJicGzuDBe4t2ZmSuEGiaH76E0EEHJu77PCBC2dhnABMXRp5xxFZYOpoCcVXN3cQSWhA/640?wx_fmt=png)

阅读发现，意思是用户名为 admin，然后指向了数据库 orcharddb...

这里只需要知道数据库密码即可登录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOhMcLOqmTGpJicGzuDBe4t2S0IuW5WRjogia90QHRgjic4RlTL8f4iboARyWjNN1Gj5EMicmRnRVa16EA/640?wx_fmt=png)

回头看文件名称，应该是 base64 编码值，解析看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOhMcLOqmTGpJicGzuDBe4t27xbIOzxYFD2jSiala3a1R1m0WnrYOCbZHm2icibmA5YXiagE5Hd1kvlb0w/640?wx_fmt=png)

可以看到解析出十六进制字符串... 将其转换为 ASCII 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOhMcLOqmTGpJicGzuDBe4t2Lc3YkVdlWgwsIPzsnDz1o3DnqWxkbHGuJ2eFPRjvq4r1dYgr3JHrlw/640?wx_fmt=png)

```
echo 6d2424716c5f53405f504073735730726421 | xxd -r -p
m$$ql_S@_P@ssW0rd!
```

解析出了密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOhMcLOqmTGpJicGzuDBe4t22DTDcemcnvxnsMAu0AgiciafJOSjXNVuWImBSCHZJC9SiczhNW5bUL5pQ/640?wx_fmt=png)

这里利用 dbeaver 工具进行链接数据库，本地没用的自行下载即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOhMcLOqmTGpJicGzuDBe4t2GRZz2gsazQOPyU8XqiaTxzx0iaBiaOxJhhQVzmDGaSIVwFzsOwPhGrTlA/640?wx_fmt=png)

在表格 blog_Orchad_Users_UserPartRecord 里找到两个用户名和密码...

这里利用 Impacket 集成中的 goldenPac.py 进行登陆靶机...

Impacket 是用于网络协议的 Python 类的组合。Impacket 专注于提供对数据包的低级编程访问，而对于某些协议（例如 NMB，SMB1-3 和 MS-DCERPC），协议实现本身也是如此。

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOhMcLOqmTGpJicGzuDBe4t2JaiarZibbRHCbh8jiaeL0KnDs3QmRicQH9tPVBh3wdCTmQdjxwZ3qYlmTg/640?wx_fmt=png)

```
git clone https://github.com/CoreSecurity/impacket.git
python3 setup.py install
```

更新完后执行即可..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOhMcLOqmTGpJicGzuDBe4t2zIh6kkr8L2LKdRWw4je25D3xE87bcxW9ebeJ16wm4KXCx7FZYdjxcA/640?wx_fmt=png)

利用 goldenPac.py 登陆即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOhMcLOqmTGpJicGzuDBe4t21YG8TCYr5NPk3bkehuRb99lzsjAIjicw1ExXhTugjiaicwib7vB0iaQf6Hw/640?wx_fmt=png)

```
python3 goldenPac.py htb.local/james:J@m3s_P@ssW0rd\!@mantis.htb.local
```

利用 goldenPac.py 创建与域控制器的 SMB 连接，并使用 PsExec 技术提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOhMcLOqmTGpJicGzuDBe4t2ePjttb7ErrWBFJtltL6AOUlAJicqxP6W8lxaojTYkiaQQqqPdZQfyPUA/640?wx_fmt=png)

成功获得 user 和 root... 信息...

  

还可以利用 MSFconsole 和 MS14-068 漏洞进行提权....

前面登陆数据库还有很多方法，MSF 和别的工具都可以...

由于我们已经成功得到 root 权限查看 user.txt 和 root.txt，因此完成了靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/wucQH64lHvpOxUzKZzgrk8rOIbSiaoFokwT3HYichsCpM6ibw80Jw5WmZL4vQs947UAIP2l7bicjV6MJECFp51G6sQ/640?wx_fmt=gif)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)