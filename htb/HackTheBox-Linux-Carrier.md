> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/5d_v5ThhbhWl-xvgfPhv2w)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **137** 篇文章，本公众号会每日分享攻防渗透技术给大家。

  

靶机地址：https://www.hackthebox.eu/home/machines/profile/154

靶机难度：高级（5.0/10）

靶机发布日期：2019 年 3 月 13 日

靶机描述：

Carrier is a medium machine with a unique privilege escalation that involves BGP hijacking. The initial access is pretty straight forward but with a little twist to it.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

  

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaP0PRhdCbF5DUibA3BuwNFR8T63k6sApSHgMLroSF4eNdYYlashWIpfNg/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.105..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaPOvWgjdb2xIHDWA5JhQciau1iaKf5DrGSm6r293vjaLeUq3icQ2zMXY2Cg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaPXyIRUNWW1drSd5HicLQdTrTK8Vn0ytQ7w01sialHP6jGx7oBaA6k9f9Q/640?wx_fmt=png)

nmap 发现开放了 ssh 服务，web80 服务，以及一个 SNMP 端口...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaPFCV0y1soudiaSySSoTl8hQTC4uJiaH3kLb6LMGj511sGtvybQXCUlHUA/640?wx_fmt=png)

访问 web 页面，出现了一些错误 Error 45007 和 Error 45009... 任何访问都存在同样的错误...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaPUXOM9fqicbiaTIjM5icWxibvyodDicH3Fzp4SdwOWPwVorNn7LqH94AniaKQ/640?wx_fmt=png)

爆破发现了一些目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaPQibe8TXTRBU6Jl8iaHibv4PZWGPxia6g2VKv6Z1gsAj7GAnZd8hScZ8JIg/640?wx_fmt=png)

许可证过期，退出... 没啥有用的信息

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaPYV0yYPFbKibQKmeMrox2HWgOrKwLEgM7wetQbltL0BveGTuMeEGQFPw/640?wx_fmt=png)

发现 doc 包含了两个文件...diagram_for_tac.png 和 error_codes.pdf

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaPl20nOic1Zf207Egw4nGxl7kHOcFppz5nR6Tert4Ddo1fnh8Bvf9ce6A/640?wx_fmt=png)

diagram_for_tac.png 的图表示三个路由器，AS100~300，这是 BGP 自治系统啊，作为网络出身的... 一看就明白了

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaPYO9ekAfJeLDMQZWW7msPl3DWIibxrrtY44cOdy3e06ibfrs1ZRllWvKw/640?wx_fmt=png)

error_codes.pdf 文档包含两列表，该表提供了各种错误代码的说明，包括错误代码 45007 以及 45009 在 web 登录页面上找到的错误代码...

Error 45007 中的原因是由于许可证无效或已过期，Error 45009 报告尚未设置系统凭据，并且默认 admin 用户的密码是机箱序列号的密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaP8icA8icDjPAMGBnggKKrKgnlXK6tZThqjiciaEYMUyicwgmBanOnubg2JHw/640?wx_fmt=png)

先利用了 MSF 的 snmp_login 模块枚举了 snmp 信息... 枚举到正在 public 内... 无权限查看

直接利用 snmpwalk 工具进行了枚举，发现了密码....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaPoTXrIaSibK1hvIKTHMHlMlxuAyV5gFe6cEhBKichM2Rht2hIAMhiatOjQ/640?wx_fmt=png)

利用密码成功登录进来....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaPQEJXdHqVsdW1EoZ3gicDlLQMwldowQhRUz5KtaR7ckCDPp6wazNTp7Q/640?wx_fmt=png)

这里解释说存在一些网络路由问题，并且网络中存在重要的 FTP 服务器 10.120.15.0/24... 上游 ISP 报告其路由正在泄漏？ISP 可能通过 BGP 错误地发布了路由内容...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaPwotgdTdh8PseGGmU7h2qeAaD3yRAQYMk0kKAOaWiaeNC3uwcic73LiabQ/640?wx_fmt=png)

这里发现了 quagga 目录下存在路由回显的信息提示.... 拦截下看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaP4oicZwgfwRsgLTNKcicYVfIJyInxgTHUoYzPjKRPVXDSPCkVoNUjUbYw/640?wx_fmt=png)

拦截发现了 cXVhZ2dh 值，这是 base64 值，转换后是 quagga...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaPMSoATI3oY2mT6MicmPmksy5SjPsvNNy7JIWAfGKWShbaVOtME3OQTNg/640?wx_fmt=png)

经过测试，只需要吧简单的 shell 通过 quagga 一起转换成 base64 值，输入即可提权....

成功获得了 user_flag 信息...

二、提权

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaP3ejjML0jIPX4sfkZic8VaI6H8xoSJMRHJHwoHJOiaBBlNBeUReiauEuyw/640?wx_fmt=png)

ifconfig 发现我们不在实际的主机 10.10.10.105 上，在另一台主机上....

本机具有三个网络接口（不包括环回接口 lo），eth0: 10.99.64.2/24，eth1: 10.78.10.1/24 和 eth2: 10.78.11.1/24....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaP04uwXsKb9NneUHbCeWhJ8PDAVWw1Lvml84pvy2TvdXddib1E3psLGZg/640?wx_fmt=png)

系统的主机名是 r1.... 并查看了 arp 表...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaPMQcZrX29qUUF4l2kUftadl4W8erTSN6ejxXYGHRdmyYCGH9iarFtibQQ/640?wx_fmt=png)

通过前面提示，在 etc 目录下发现了 quagga 目录... 并一个一个查看里面的文件...

查看 bgpd.conf 后...

这是通过 vtysh 工具进行的配置更改保存的，vtysh 是思科操作系统的命令... 显示了 r1 上 bgp 的配置信息...

bgp 100 是当前所在的自治系统 AS 100 中，可以参考前面获得的图...

10.101.8.0/21 和 10.101.16.0/21 是 BGP 的邻居路由环境... 分别表示 AS 200 和 AS 300...

在这里就可以发现，缺少了 10.120.15.0 的路由信息... 应该是走在 AS200 和 AS300 系统内...r1 没有路由拿不到流量信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaPic9ec8DlG5NL4Eibh7yts1zpgTWRzq24BaN6pJwR4Zao9WQHkSoNyywQ/640?wx_fmt=png)

从以上可以看到，目标 IP 地址为 10.120.15.0-254 的流量应发送 10.78.11.2 与 eth2 接口相连的目的地...

这里涉及到 BGP 的原理：

BGP 协议的一部分，如果两个不同的 AS 编号（即 BGP 邻居）通告了两条重叠的路由，并且没有 AS 前缀，则更具体的路由将被接收到接收者的路由表中...

这里就存在 BGP 劫持攻击行为，可以将 FTP 存在的子网段路由转发到 R1 中，我们目前在的 R1 就能查看到 FTP 的流量包行为等情况...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaPOnniaUmvN0u3YM8f9vNuWwnjBakAzFicl6gpYTR9NxhOG2cXllXazlYw/640?wx_fmt=png)

进一步查看了 10.120.15.0 段内的自治系统情况...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaPuibApH9bl3WeDNgyQ545l8xLiaxRMfYlIVvdXqZB1ZqS1BWSibicRkJBnA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaPcGWF5qfrkGtd02DK0iaPPv0j0cm7QAeCBclKmIb9dBUWUMDUTpd565Q/640?wx_fmt=png)

会 CCIE 和 HCIE 的都非常了解有很多方法查看 AS 环境... 这里也体现了...

为了就是能让看到这篇文章的人更深入了解下 BGP 环境....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaPIo4odBtJPCwPW5GT9xhZt8ibo2hJQKA4DKYj6PwO3XQMaBPhArCxnibw/640?wx_fmt=png)

利用 cisco 中 vtysh 特性，添加 10.120.15.0 路由到 r1 中...（不理解的硬记，这是网络基础知识）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaPwqTwvYwjUF56MASnNnzibPoHSCpe6FhZ9cxhJmcbtE8MAxaKJ4vveSw/640?wx_fmt=png)

回看成功添加...

这里可以继续利用 tcpdump -A 等命令对子网段中 FTP 流量经过进行抓包保存在自命名的文件中...

我这里没这么操作... 利用 tcpdump 的好处是可以直接查看到流量包中的 FTP 准确的 IP，以及流量包中的各种包头信息...

因为我的外壳很不稳定，就没这么操作....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaP6Rlcz2SkTFiaibJUE66ibUbcQ1vLA9LOia40GlY9dnLwTxJlY1SsHL0JSg/640?wx_fmt=png)

```
for i in $(seq 254 $END); do nc -w 1 -vz 10.120.15.$i 21; done
```

如果不抓包分析流量，就得通过类似 ping 等方法枚举出 FTP 的真实准确 IP 地址....

获得了 10.120.15.10 为 FTP 的 IP 地址....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaPCia26cMNAlQ5RzX4djgjdrykqz2DZoTA6IQTJSz4eFcOJZItEdVujTw/640?wx_fmt=png)

直接加该 IP 入组内，意思和 ip route add 一样，就是加条静态路由... 这样路由会将发往 10.120.15.10 的流量到本地经过...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaPGX35pPMpPJv3bF8ZTVPCicfzP68NeoaDrxpibnRqkY6W6cax0QPpMxDQ/640?wx_fmt=png)

该环境安装了 nc，只需要 nc 监听 FTP 的 21 端口即可...

等待了几秒钟，获得了流量中显示的明文 root 密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNo9t3O9yPElvVWK2eoJviaPnPUZuW4K0t2nBXvFklvyNJxakQOrZriaibmfjwfJyJQkjlraTZEjly4g/640?wx_fmt=png)

有了密码后，直接 ssh 成功登陆 root 权限... 获得了 root_flag 信息...

  

这里获得 root 后，继续枚举了... 发现前期外壳不稳定，在前期的 R1 权限下，可以查看到 root/.ssh 目录下存在 rsa 的 key 信息... 可以替换 key 登陆，获得稳定些的外壳....

打了将近 100 台 HTB 靶机了... 这是第一次遇到网络协议中 BGP 高级路由协议的渗透环境... 我是 HCIE 出身，非常兴趣和意外的遇到了此靶机，也是很开心的完成了... 感谢作者...

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台高级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

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