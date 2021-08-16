> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/AqJM6kRlIptnx4ZoZJRtkA)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **124** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/c6lNmDMELgVefhqyswkhNcG53sbopmNFb6w6BGUZCXq83PjE80maj43XT7BjARoN3xKWuFdAc2IBPs0urI5ktA/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/129

靶机难度：中级（3.5/10）

靶机发布日期：2018 年 9 月 24 日

靶机描述：

Stratosphere focuses on the use of an Apache Struts code execution vulnerability which was leveraged in a large-scale breach, resulting in the disclosure of millions of peoples’ credit information.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

  

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/Clq0o4fE5u6X5A1maTmqcvtEibdrsDO41kZPibRCHsX3Koj69GFK2qOyPwdcrgcDkHklrdJzBCiaQPuMVe11oSYHA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOqGDxCsymX1cZ9ID7ApD2BQ8A41Jwx5pEbuNxfbhx9vUC2nVGaoSXE8jGRVNXicZIFE7RS6PVkkBQ/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.64....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOqGDxCsymX1cZ9ID7ApD2BibTuvuRImlGgeHGnngZ1JCP0ibnf3icoJ9PV3S7Rmr5Gsd7tqYIozVg6A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOqGDxCsymX1cZ9ID7ApD2BYHULMhgD34RWEkIYv2pthryic1iacRribSCVF3KsI527KlVqWXHMF1JeQ/640?wx_fmt=png)

Nmap 发现运行着 OpenSSH 和 Apache Tomcat...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOqGDxCsymX1cZ9ID7ApD2BWV3GYRNGvdRibW9I6XP300pAQaN3KA4db5D3unbicGldLnR3H2luuQpQ/640?wx_fmt=png)

主页面没啥信息... 直接爆破...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOqGDxCsymX1cZ9ID7ApD2BZmrib8xqGibwKU7lL32spcBQA8HMHjkFlKd99WqicRF6p2edhsy6WBMPw/640?wx_fmt=png)

发现了 Monitoring 目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOqGDxCsymX1cZ9ID7ApD2BqcNwG2ITbuiaNljSmOWgztxTauY4WJiaoEUHhiaenM5ug5aLTrRzKicibpg/640?wx_fmt=png)

访问后跳转到了 example/Welcome.action 下...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOqGDxCsymX1cZ9ID7ApD2BIbT6g71AjSc9l2NOIibl7aYWuG6xN5UCQCcGDkpXAIXGuUTu1iayZ3GQ/640?wx_fmt=png)

google 搜索 Welcome.action 存在 EXP 漏洞可利用....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOqGDxCsymX1cZ9ID7ApD2BNH7ibaLeZ2xhoHBLPxC6NSaZ782WKhhe2Lxe7ibRtYpObqUuK6ZhDC2w/640?wx_fmt=png)

```
https://github.com/mazen160/struts-pwn
```

下载试试... 不懂的看文章解释，最近快速过，就不解释了...cve-2017-5638

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOqGDxCsymX1cZ9ID7ApD2BA2FRhbjtqiaACyPiaibibEXGXMMKricV9nHBcCuQSkTA2iaR49fsnaM3VINQ/640?wx_fmt=png)

直接按照提示，利用后成功获得 ID...

然后直接利用获得了 mysql 底层密码信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOqGDxCsymX1cZ9ID7ApD2B6s1zuJ2JtR7hE2G25ebw9dbfWjBdxMsaBialGyEIEopNibqctbMGFhRQ/640?wx_fmt=png)

通过密码成功登录了 richard 用户... 并获得了 root_flag 信息....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOqGDxCsymX1cZ9ID7ApD2BJD1IcsgZ675LTWhVibEtpKMVJEm2DuaOibaciaKd1qPboQibY245q13yicw/640?wx_fmt=png)

sudo-l 发现了可直接提权的路径....

查看了 test.py 信息后，发现该脚本是通过 python 调用的，import hashlib 提示了 python 库中存在 hashlib??

还发现很多哈希值，破解后，尝试都没办法登录 root....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOqGDxCsymX1cZ9ID7ApD2BSibcffpHYyaCS1fMgiaV2SOkP8WJX98MM7zicZ4Qd3r9icjnB78ngePib5w/640?wx_fmt=png)

检查发现存在 python2 和 python3.5 两个库....

尝试执行提权也失败....

方法 1：

![](https://mmbiz.qpic.cn/mmbiz_png/xm4F2hYetPjEQESs45UQXRGBy3wswtHDWMZz77ibhszjBEbNjYqjTeF5Oiabq6YwXD7bWyT7xPAPcTPnasSXbSkA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/ZkKbicS7g7ZHYZnHJIaEIGnCFUcfEpoZzbNbicBMkmZsoicIR4wRS4gabRwDEkG2qXlDxM2mJPI62cpq1pM3Alm5w/640?wx_fmt=png)

直接利用 python2 库执行代码提权

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOqGDxCsymX1cZ9ID7ApD2B9VK4t6KaD55LHc1JZzjEXXTFYa0SUesqyIxlvC1H5cVJiaJfxOcUZEw/640?wx_fmt=png)

成功获得 root_flag 信息....

方法 2：

![](https://mmbiz.qpic.cn/mmbiz_png/xm4F2hYetPjEQESs45UQXRGBy3wswtHDWMZz77ibhszjBEbNjYqjTeF5Oiabq6YwXD7bWyT7xPAPcTPnasSXbSkA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/ZkKbicS7g7ZHYZnHJIaEIGnCFUcfEpoZzbNbicBMkmZsoicIR4wRS4gabRwDEkG2qXlDxM2mJPI62cpq1pM3Alm5w/640?wx_fmt=png)

利用 python3 库中 hashlib 提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOqGDxCsymX1cZ9ID7ApD2Bgwj9Icfic45aXC8kU8UchhMt3BDnuCgaOdSBh3bgc4Bx6us1VfkMosw/640?wx_fmt=png)

查看到 hashlib 存在 python3 库中...python2 没...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOqGDxCsymX1cZ9ID7ApD2B38xRqdlLLxAmdd3UA5Tk0VIoHpE0fpicVCj8k6htDW6op5Jvxp0yYzQ/640?wx_fmt=png)

然后直接在用户目录下创建一个 hashlib.py 执行即可...

![](https://mmbiz.qpic.cn/mmbiz_png/TaLibElTFqBjNpYLEVorsaLMeHScCZR2CQcXF4QQuCmtUwOYTolRMZkXEOKJKKHnrJNjWo2g0h75l4aweJQQwAQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/4wW5pibnKd0rib9mFlhgF2CWl6ibhJn9yNL1gIWU97JjNekJGTgEZ9wjNgOhiaqibaxPYfJnUKVHnMM9JHthC6kj1Ew/640?wx_fmt=png)

这里直接修改 python3_hashlib.py 的话，无法修改... 可自行查看 test.py...

直接 sudo 成功提权获得 root_flag.....

主要方法简单，漏洞单一... 拥有 EXP...

说明漏洞的严重性在安全中很重要，有一个漏洞，就能搜到一个 EXP...

加油

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