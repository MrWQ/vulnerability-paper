> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/J4hio4XN0NvQWF7ywqG_4g)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **25** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/gBSJuVtWXPZE73MPxL1VoDjO3DFaxJA2MQpSSibwsXKVf4VIHh8S9fZXT8pq1ALE3hWEN22AaniaghxGrJqjEsxw/640?wx_fmt=png)

靶机地址：https://www.vulnhub.com/entry/hacklab-vulnix,48/

靶机难度：初级（CTF）

靶机发布日期：2012 年 9 月 10 日

靶机描述：在这里，我们有一台易受攻击的 Linux 主机，该主机具有配置缺陷，而不是有目的的易受攻击的软件版本（无论如何，在发布之时就如此！）

目标：得到 root 权限 & 找到 flag.txt

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/ymNhlIRQRwIDdqQDCiblECK9VN2KquqTzJXM7etEnDcIpDdITqzFuiapav9TDnIiaGgf1e4sP9IO6B5NEtEyg2t5w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/eGDabDaNAhQ72wHWRToOUZR31X9kamiak0wrpr3lxKHpuoTpia329Xu6T0OTYlZic9XeEyQ4twasnibb924VBgIt1g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/6DdW6admPmWicucEOicwONQBeMWRA7Pq57A9xCTGbIWomiboqObS0bEetoo2qW2hHk2E5GOcuQYUqSlQT5BKsDqRQ/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/M39rvicGKTibrmYlY2VW5XChia77yhteBC7iarNdYSwicq64NZrCHeSZqRpsFRTZkpfgclSWaibqftONNMWLkz6QjyoQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNTUlrYG9pIMRajXAFo2LT4Y7ibX3wE1UmALiaAJPayakxkiaMf1BzsxOEbyJfAfUFFs8qMInf9ShgVQ/640?wx_fmt=png)

我们在 VM 中需要确定攻击目标的 IP 地址，需要使用 nmap 获取目标 IP 地址：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNTUlrYG9pIMRajXAFo2LT4moLJ2UInAticH717265jWHSSKGCdG2ibc9kCkUyaBh7dqjpexQr4Th3A/640?wx_fmt=png)

我们已经找到了此次 CTF 目标计算机 IP 地址：192.168.56.131

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNTUlrYG9pIMRajXAFo2LT4qoaRPLzKL0c5SDOrYxvovHRdt7ksBwDvgjB3QliaqricahJ2U3uIlQWQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNTUlrYG9pIMRajXAFo2LT4pqB2lPENjTbmvHs0K2BX42S2bdicUNkPCoaBYtoBfpicdueaPib9WqQrQ/640?wx_fmt=png)

开了好多端口，应该有很多种方法可以拿到权限.......

昨天就对 25 端口有过研究，今天直接 25 端口下手...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNTUlrYG9pIMRajXAFo2LT41alsOGNKsib6oVdzdib2dvuKGRwia5DPmcpMX3khoJnVDw2gg1biaf0Y2w/640?wx_fmt=png)

这边可以看到 VRFY 未禁用... 验证到存在 Vulnix 用户是存在的... 需要验证更多的用户是否存在

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNTUlrYG9pIMRajXAFo2LT4Hxtw8icldcWp9X4aUKymyvxFsdhibgiaibmhwTxFe6QxgUvmkGThib4nBTQ/640?wx_fmt=png)

找到 sexy 的 smtp-user-enum 脚本，使用 / usr/share/metasploit-framework/data/wordlists/unix_users.txt metasploit 框架中提供的功能...

发现存在很多用户.... 有两个用户比较重要...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNTUlrYG9pIMRajXAFo2LT4bEzicIDr0omMbicxCSAgHeRneeteeicrpqPd0ypAPCCyrCcm5oMLMSOibQ/640?wx_fmt=png)

```
finger user@192.168.182.131
```

看到两个用户都是有效的...

用户 user 具有 devenull 的登录名和名为 Dovecot 的名称....

这边只确认了用户的存在... 密码还需要继续获得...

接下来，我将在端口 2049 上进行 NFS 枚举...（Nmap 扫出来的）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNTUlrYG9pIMRajXAFo2LT4EmmES9FGeTwJicTUxzowRpoljFEJBNv6V8S1EsNNgTziaQHBwwiaLQic3w/640?wx_fmt=png)

需要安装 nfs-common（kali 自带的）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNTUlrYG9pIMRajXAFo2LT48TkHWu615uoiaDfibB178dm3icLEUH0bicn3VUEOhkSeVZL1BY7zuBnIRA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/6DdW6admPmWicucEOicwONQBeMWRA7Pq57A9xCTGbIWomiboqObS0bEetoo2qW2hHk2E5GOcuQYUqSlQT5BKsDqRQ/640?wx_fmt=png)

二、NFS 枚举

![](https://mmbiz.qpic.cn/mmbiz_png/M39rvicGKTibrmYlY2VW5XChia77yhteBC7iarNdYSwicq64NZrCHeSZqRpsFRTZkpfgclSWaibqftONNMWLkz6QjyoQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNTUlrYG9pIMRajXAFo2LT4dwHibkaY2zrfr295byCoAMID5m9PGIHOHuqiblEibECskcpEjJoPvhaJw/640?wx_fmt=png)

看到可以为用户 vulnix 安装文件夹进行共享... 将远程共享文件装在本地 kali 上...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNTUlrYG9pIMRajXAFo2LT4ndzyicvUpgpmbTDTO71BicT3icojHmHicrL1EYYsYoRmiaw8ibFr3KnCndkA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNTUlrYG9pIMRajXAFo2LT4zOZzEIXoC4jic3OnqVSxfEAYqAOWeER9jcc9LYajByficKV66mBSrZjA/640?wx_fmt=png)

可以看出其实共享已经实现，估计设置了 root_squash 标志，只是不允许我们去访问... 只允许 vulnix 用户去访问....

目前只允许 vulnix 用户登陆，并且得具有与目标上相同的 id 和 gid...

（可以看出前面有 root 和 user 两个 root 权限的用户，可以创建用户去修改代码去针对用户提权，这边我没涉及很深，后期我慢慢脑补...）

我直接用九头蛇爆破了 user 用户密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNTUlrYG9pIMRajXAFo2LT4MB1X6RqEYUdbictqQYSODPMNWpdKbr6YXu9NI9yc8V9McCFXPgKJUbQ/640?wx_fmt=png)

```
命令：hydra -l user -P rockyou.txt 192.168.182.131 ssh -t 4
账号：user
密码：letmein
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNTUlrYG9pIMRajXAFo2LT4JwPbBCvZAaM5QEQII1Kk3xyAZuNxicQROiciaDJLQUI95Se6KCpsjLMfg/640?wx_fmt=png)

没安装 GCC，所以本地漏洞利用无法利用 C 语言编写...

无法访问共享的目录，看到 id 和 gid 后，可以创建了临时的用户和他们具有相同的 i 和 gid 值去访问共享目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNTUlrYG9pIMRajXAFo2LT4N9eNzlAt44ErxWFH5HcGBwYBO6L2YdZG2Ic7lIlwJChmYeT9cXibNhg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNTUlrYG9pIMRajXAFo2LT4hDrr2DsOoJBcGiaYp1sLBriamMnvR53vH806vvLHiaycGK2YkEKuq5ZqA/640?wx_fmt=png)

创建好临时用户 mnt 后，这边用 ssh 生成密匙直接登录... 开始

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNTUlrYG9pIMRajXAFo2LT4K5abn5nURY68Axx2Eia54tiaTicabIiaichnWzhOrfqr9gb6ffCypTLntPQ/640?wx_fmt=png)

这边用 ssh 生成密匙后，回到临时用户 mnt 下将密匙导入进去...（生成一直默认回车即可）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNTUlrYG9pIMRajXAFo2LT4l9AFK42L6kfEj31rE78AhsAfjpIicNErD5gd7boUuPWHXbY82BnJjzw/640?wx_fmt=png)

然后直接登录即可，会自动匹配 ssh 密匙...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNTUlrYG9pIMRajXAFo2LT4fCvWNFlb3Fv0nSwsic0hwCZc0Mq9icyppbDER7U5QlIeVLmsJsxMjfuA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/6DdW6admPmWicucEOicwONQBeMWRA7Pq57A9xCTGbIWomiboqObS0bEetoo2qW2hHk2E5GOcuQYUqSlQT5BKsDqRQ/640?wx_fmt=png)

三、提权

![](https://mmbiz.qpic.cn/mmbiz_png/M39rvicGKTibrmYlY2VW5XChia77yhteBC7iarNdYSwicq64NZrCHeSZqRpsFRTZkpfgclSWaibqftONNMWLkz6QjyoQ/640?wx_fmt=png)

我已经在目标的系统上了，我可以继续枚举来尝试提升特权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNTUlrYG9pIMRajXAFo2LT4ibAJ2RdibLf5ias1VVYS8vNBLZTD2698A4TORVv8Gas1mcia9LUXdIf3Rg/640?wx_fmt=png)

可以看到 sudo 提权，可以以 root 用户身份执行 sudoedit /etc/exports，编辑 / etc/exports 该文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNTUlrYG9pIMRajXAFo2LT4uAPCBWxq4QyU9kMxC6NFM47zqalQeFUiatPsImhMwfZQlpcHq3yxXVQ/640?wx_fmt=png)

通过用 no_root_squash 替换 root_squash 来实现....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNTUlrYG9pIMRajXAFo2LT49aUVqlpM46teGF2hlLoeVWbG8HUw9szYzIh0w6WkNKB04Xy0FkmjAA/640?wx_fmt=png)

修改完后，我们需要把挂载点挂掉...

然后这边比较坑... 因为我搭建是用 VM 搭建的，没有 root 用户权限无法对它进行 shutdown -r 命令... 这边得重启下 VM 下的 vulnix 靶机...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNTUlrYG9pIMRajXAFo2LT410icxqibN8qFD0rB5JLodcoALoFx996emHfyMiaI48z5rv4mFjbmLTNag/640?wx_fmt=png)

因前面挂开了 nfs 目录，这边重新挂载下创建的 mnt 共享...（有点卡）

本地计算机的 / bin/bash 复制到 / tmp/nfs，利用目录下的 bash 来提权... 赋予 4777 权限...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNTUlrYG9pIMRajXAFo2LT49k3zLBIkG4Juz36icQicSIBVnryK2tFaLwv4HPnFJKoflQsF84yLvKuQ/640?wx_fmt=png)

进入 vulnix 用户去执行./bash -p 报错了，无法打开... 重新在此目录下在复制一次

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNTUlrYG9pIMRajXAFo2LT498XNK9ypEvQYxqDEmeSWzU1vbPlwSdJCyuNKdsLZdQx3kz8pab7ibEg/640?wx_fmt=png)

成功提权！！！

![](https://mmbiz.qpic.cn/mmbiz_png/gBSJuVtWXPZE73MPxL1VoDjO3DFaxJA2MQpSSibwsXKVf4VIHh8S9fZXT8pq1ALE3hWEN22AaniaghxGrJqjEsxw/640?wx_fmt=png)

这是有逻辑性向渗透的一台靶机，非常有趣... 一定要动手操作几遍，熟能生巧，加油！！

由于我们已经成功得到 root 权限 & 找到 flag.txt，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

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