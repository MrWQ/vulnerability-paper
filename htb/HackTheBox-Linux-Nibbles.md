> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/yUvDmCgiCVrRYOH9JKbaag)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **122** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/x2A34tB6DJ1OkPcdribDzibshJwyiacGV0dL6xyJSMoUODic9LUULgNOnWiciaLpD2A7HtR7e6GqhqAkw8zXBObGceYA/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/121

靶机难度：初级（2.9/10）

靶机发布日期：2018 年 6 月 30 日

靶机描述：

Nibbles is a fairly simple machine, however with the inclusion of a login blacklist, it is a fair bit more challenging to find valid credentials. Luckily, a username can be enumerated and guessing the correct password does not take long for most.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/Rhl7Fe1Ew2icdiaxAoicRDTOcic6uZqjKNRuQTmL2KnOQaSBwas6DeYNdq479WEFto9n2bssQXlvVic2bGGlQghxWVg/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/Clq0o4fE5u6X5A1maTmqcvtEibdrsDO41kZPibRCHsX3Koj69GFK2qOyPwdcrgcDkHklrdJzBCiaQPuMVe11oSYHA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNXaeb9iapFhQo09qO9dmUGS44Ykm4KGMLzZrPSM6uFn3hBRWdJ9DGO6QHKk3nBnbjVdlGjsyRqllQ/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.75....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNXaeb9iapFhQo09qO9dmUGSvTy73UW71u53fA2S7wcKjRnuZ5TYlnVAFicPTjw6xxncjqGPibxgpYlQ/640?wx_fmt=png)

nmap 发现开放了 ssh 和 apache 服务...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNXaeb9iapFhQo09qO9dmUGSFialGVGFkILoqibHsDk0uL9kXZxm99S3WAkHWPQiaynNfFkILjVS7WI2A/640?wx_fmt=png)

web 访问欢迎.... 查看下前端

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNXaeb9iapFhQo09qO9dmUGSnbMuS61hFKfBMYItZyot0KlcRWGfasdLZPmSn9o2iajdicUiabsW5HicWw/640?wx_fmt=png)

查看前端源码发现存在 / nibbleblog / 目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNXaeb9iapFhQo09qO9dmUGSoHsO9S9DEw4l93ZBsAVwvhEc5DFd69pUtxGOf6RA8W9o3aCP3wamiag/640?wx_fmt=png)

直接对 / nibbleblog / 目录进行爆破... 发现了很多相关页面信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNXaeb9iapFhQo09qO9dmUGSHibJvXVER6VNRcnniclr2pqm8icFGToEpKPx3JN9yTPibGO0oed6FCaIUw/640?wx_fmt=png)

admin.php 登陆页面... 这里直接利用默认密码试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNXaeb9iapFhQo09qO9dmUGSuLiaeVFKcd4cd93R41XT3icdeCN8Yj9elktViaofSVngM9ictNHAAzqCGg/640?wx_fmt=png)

通过默认密码测试，直接靶机名字作为密码进入了....admin/nibbles

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNXaeb9iapFhQo09qO9dmUGSiccloVkK4YGEo4jJbnFlyFauhAzByqOfgvFpOSrlRamrbaLu5HaJstw/640?wx_fmt=png)

/nibbleblog / 前期知道此目录，就 search 本地查找到了 38489.rb 利用 EXP 信息...

我这里直接 MSF 提权... 最近不想找别的方法了，快速过...

发现可利用 EXP...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNXaeb9iapFhQo09qO9dmUGShhqERGjcw6vCbvsYvNibQR5vgh5SqUVicFczOnDvt7D2qYkcXqSibYaDQ/640?wx_fmt=png)

直接填充信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNXaeb9iapFhQo09qO9dmUGSic9BiaGlVOJVl1yhuibVmWZGDPqOjUIUfNHic6jibQukdPjCbx7jMaKehQw/640?wx_fmt=png)

执行后成功获得 nibbler 低权用户外壳.... 并获得了 user_flag 信息....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNXaeb9iapFhQo09qO9dmUGShxcrGTshJyl01Jia56S3NeY3umSHqsyTkAqfzRtFkPpBCpKicdnMqRHA/640?wx_fmt=png)

对于简单靶机，直接 sudo -l 提权... 发现了 / home/nibbler/personal/stuff/monitor.sh 可执行 root 权限获得 shellcode....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNXaeb9iapFhQo09qO9dmUGSY53dO5jVbWATXQZuPIkBicBhnleHxNdRGc5jG8r0f6gTKG7O4iaFhTcw/640?wx_fmt=png)

可是在 nibbler 用户目录下，没有 personal/stuff 目录... 需要自创建...mkdir -p 创建即可...

![](https://mmbiz.qpic.cn/mmbiz_png/x2A34tB6DJ1OkPcdribDzibshJwyiacGV0dL6xyJSMoUODic9LUULgNOnWiciaLpD2A7HtR7e6GqhqAkw8zXBObGceYA/640?wx_fmt=png)

不稳定的 shell... 我还是在本地编辑好 monitor.sh 后，上传...

执行过 10 秒左右获得了 root 权限... 并获得了 root_flag 信息....

简单的漏洞提权... 如果该靶机在 admin.php 设置难度高点的密码... 然后在把密码信息以 hash 或者进制等形式隐藏... 估计会提升一个难度....

哈哈，我已经开始建议作者了吗？

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台初级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/Rhl7Fe1Ew2icdiaxAoicRDTOcic6uZqjKNRuQTmL2KnOQaSBwas6DeYNdq479WEFto9n2bssQXlvVic2bGGlQghxWVg/640?wx_fmt=png)

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