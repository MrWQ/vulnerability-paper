> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/8-KsqPrvKwxo0btqLKKW0A)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **85** 篇文章，本公众号会每日分享攻防渗透技术给大家。

靶机地址：https://www.hackthebox.eu/home/machines/profile/180

靶机难度：中级（4.4/10）

靶机发布日期：2019 年 11 月 20 日

靶机描述：

Heist is an easy difficulty Windows box with an “Issues” portal accessible on the web server, from which it is possible to gain Cisco password hashes. These hashes are cracked, and subsequently RID bruteforce and password spraying are used to gain a foothold on the box. The user is found to be running Firefox. The firefox.exe process can be dumped and searched for the administrator’s password.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/eLJRzA69wl7hIRHbBfpwg183icXPqYhOnfYicXOtt4iclEsBT585JmXFvq05Ieibib0szIulE9r8BG58HzUePwUpxhw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/7uQztnLo2WrIicprPLicbDPNdwFfmnlntwYXSXQClxAibN46YnoSHbePjQ6gibXdEbuh0pTTiaiczgMN9dgkLx7mD5Ug/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSJggfx8Mz3a0rxJg6RSLeGe4dtslFPg7JtpHDOnNmHibWic5ibVo5Q2xjNEM2nq1rsFETJXAgx7TkA/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.149....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSJggfx8Mz3a0rxJg6RSLeHX6Kxic7JXab3l3ZH4VUIqp1TBH5LAeSlj6KxmRJibc0urlRLkvbHmSw/640?wx_fmt=png)

nmap 可以看到 IIS 在端口 80 上运行着，135 端口上运行 MSR PC，445 上运行 SMB... 还开放了端口 5985（与 WinRM 相关联），这可能允许远程会话...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSJggfx8Mz3a0rxJg6RSLeiaM6WCvwpcibaE77oxib50riajnibwe8BX7sQgxM7Xo5YHIUaw9iblIJK7ww/640?wx_fmt=png)

在进入 “guest 问题页面”（进入该问题页面）后：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSJggfx8Mz3a0rxJg6RSLeyOo0KgcOnevrSSia74W08DZNI8b2Mj2CVPc0XpJIhiaLXCpIt2vJrq0w/640?wx_fmt=png)

一个叫的用户 hazard 发布了一个问题，该问题是他的 Cisco 路由器存在问题，并且他在配置文件中附加了该问题。

配置文件具有一些密码哈希和用户名：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSJggfx8Mz3a0rxJg6RSLexQuEhIfExdEMDoiaJZCCjztz30OCoaK1n9LMXGXZtmRiaVfeVLic2Lv1A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSJggfx8Mz3a0rxJg6RSLeRxSKjFyaXh8tG8rKXsLF39r6nHThpZgBfZrFFx0qPwmJJmGnrkIicyA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSJggfx8Mz3a0rxJg6RSLeaiaJrNfiaHCeVwZK4icSEUIiaHQxJYiatjCsYlGYJr4Rotjda8spBjf5upg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSJggfx8Mz3a0rxJg6RSLeHY4nFsEFAsHCGiclPKSFnic3oH1h5IwCwASicnW9nuGnDTlx1IM3MicT9A/640?wx_fmt=png)

获得了密码：

```
$uperP@ssword、stealth1agent和Q4)sJu\Y8qz*A3?d
```

三个用户存在... 但是不知道是哪个用户是和 Q4)sJu\Y8qz*A3?d 密码匹配的....

这里利用 impacket 的 lookupsid.py 枚举用户列表即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSJggfx8Mz3a0rxJg6RSLep9TGkN4bNM8wcEH7yyo4QD7DZYib0uGbH9JPVVuYvjr3GuHkBXt4ZFQ/640?wx_fmt=png)

枚举出了所有存在的用户...

![](https://mmbiz.qpic.cn/mmbiz_png/7uQztnLo2WrIicprPLicbDPNdwFfmnlntwYXSXQClxAibN46YnoSHbePjQ6gibXdEbuh0pTTiaiczgMN9dgkLx7mD5Ug/640?wx_fmt=png)

user 获取

![](https://mmbiz.qpic.cn/mmbiz_png/s2yGkkgtNibcwvktzPbHWTJqI6KLXpQrkmNuAH9iavySSYSic8s9zkfEFku4821YZFgYHprDiawG811yPZwQ5Z47Fg/640?wx_fmt=png)

方法 1：

![](https://mmbiz.qpic.cn/mmbiz_png/WGK8zlB9bXibFvCwGvJBl3TkichTmQfF8BIZwoqyam3gUmdLKgKa9tFqia2K7Yh4CahtN5Uw8JwibNfbLczgk1aicBw/640?wx_fmt=png)

```
https://github.com/WinRb/WinRM
```

利用 winRM 的 Example 进行修改登录即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSJggfx8Mz3a0rxJg6RSLeiaW3qh7CYokeaLgZoQC69HxpEPxAKvdj9K8sHxczzD3jq00IUYbpcrw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSJggfx8Mz3a0rxJg6RSLeDSPAGInpjyIptcGK15ibWvwTTXZG1oR2GsgBmiaUIQdYa4y1LbCSEbcQ/640?wx_fmt=png)

这里可以一个一个试用户，对应的密码... 使用最前面的两个用户密码无法登录...

成功获得了 user...

![](https://mmbiz.qpic.cn/mmbiz_png/s2yGkkgtNibcwvktzPbHWTJqI6KLXpQrkmNuAH9iavySSYSic8s9zkfEFku4821YZFgYHprDiawG811yPZwQ5Z47Fg/640?wx_fmt=png)

方法 2：

![](https://mmbiz.qpic.cn/mmbiz_png/WGK8zlB9bXibFvCwGvJBl3TkichTmQfF8BIZwoqyam3gUmdLKgKa9tFqia2K7Yh4CahtN5Uw8JwibNfbLczgk1aicBw/640?wx_fmt=png)

```
https://github.com/Hackplayers/evil-winrm
```

利用 evil-winrm 同理登录即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSJggfx8Mz3a0rxJg6RSLeH0r2PNhON4dcuCyjJLSdDWq3pcZnqPoGOibmtcyFfhJITf8cNomHlHw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/7uQztnLo2WrIicprPLicbDPNdwFfmnlntwYXSXQClxAibN46YnoSHbePjQ6gibXdEbuh0pTTiaiczgMN9dgkLx7mD5Ug/640?wx_fmt=png)

root 获取

利用靶机上安装的 Firefox 进行提权...

靶机上安装了 Firefox，Firefox 进程存在 password 日志登录记录... 查询到就能通过 user 方法一致查看到 root...GO

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSJggfx8Mz3a0rxJg6RSLeNek0qr0vm5e2JzE1xHhv2rFxbBWDCm2nxTSUZwtmVLIgtjvLeh8Exg/640?wx_fmt=png)

存在 Firefox...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSJggfx8Mz3a0rxJg6RSLeVMVOgmhVxxFOguEm8fk7l5BRtrBXPOhfvdGBat6vvF5pgwOqV9cFIA/640?wx_fmt=png)

查看到了 Firefox 进程 ID... 利用

```
[procdump.exe](https://live.sysinternals.com/)
```

SysInternal 的 procdump 工具可以转储它们的过程中产生的数据信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSJggfx8Mz3a0rxJg6RSLeOfGNUgNmZOXotvV0B7bGd8oWEO25EaOPB9T8zVic1SPtr8NqWJz4XKA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSJggfx8Mz3a0rxJg6RSLeAibdZInp3QA6vU7T7oiaTyc9LuulpbmIia1A5CxFXyCRV0fXIuUYq5abA/640?wx_fmt=png)

成功转储了 Firefox 进程的信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSJggfx8Mz3a0rxJg6RSLeLVql0ibv0dWKBGTMy1Dh8gFa4xJtRK67pJg7mXjJEQTRzib82yj6IxSA/640?wx_fmt=png)

查询 htb 或者 password 等关键字即可查询到密码信息...

这里也可以利用：

```
[strings.exe](https://docs.microsoft.com/en-us/sysinternals/downloads/strings)
```

将 dmp 转储为 txt 文本，利用 find 查询 password 也可查看...  

成功获得密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSJggfx8Mz3a0rxJg6RSLeKkLs0xeT8K3IIg1wXQKgEiazgEtNQKnZcMICoEicRElhYG7um2fAmmdw/640?wx_fmt=png)

同理 user 信息获取方法一致，套用即可...

成功获得了 root 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/90uI9kWZONf3Vtrusjqsd1GiaM6KOIZBsXy5uveXdick8Xu5bT5SkWAjm8rXMUf4iaaQe0Xvz8kLg8kWGZzTpydxw/640?wx_fmt=png)

这台靶机过程就是无限制的尝试各个用户登录的操作，思路抓住，尝试下去就能发现正确的....

GO~~

由于我们已经成功得到 root 权限查看 user.txt 和 root.txt，因此完成这台简单的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/afYQgZLdADhibgtcdjetYfZl0AH0kzia4I1R0k63EdpbicQYdsicJJ3fwVpib8mHNCtJb5ibB9GoBDyzE1FeImL3UuBQ/640?wx_fmt=png)

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