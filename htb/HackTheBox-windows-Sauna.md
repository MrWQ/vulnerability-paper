> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/8pIra8Atr5DAFOgXC2ilHQ)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **154** 篇文章，本公众号会每日分享攻防渗透技术给大家。

靶机地址：https://www.hackthebox.eu/home/machines/profile/229

靶机难度：初级（4.3/10）

靶机发布日期：2020 年 4 月 29 日

靶机描述：

Sauna is an easy difficulty Windows machine that features Active Directory enumeration and exploitation. Possible usernames can be derived from employee full names listed on the website. With these usernames, an ASREPRoasting attack can be performed, which results in hash for an account that doesn't require Kerberos pre-authentication. This hash can be subjected to an offline brute force attack, in order to recover the plaintext password for a user that is able to WinRM to the box. Running WinPEAS reveals that another system user has been configured to automatically login and it identifies their password. This second user also has Windows remote management permissions. BloodHound reveals that this user has the DS-Replication-Get-ChangesAll extended right, which allows them to dump password hashes from the Domain Controller in a DCSync attack. Executing this attack returns the hash of the primary domain administrator, which can be used with Impacket's psexec.py in order to gain a shell on the box as NT_AUTHORITY\SYSTEM .

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

  

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/u542j6DNZqibANrqyuqYq3KwXicNtAI4PkbTngiacTDG6oGIUU4zWbT9cCpyZc4VZdBTedLFLr1Xzw3kQE9cxkCqw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Ffv0EPcbq7gH6aqjOkn7TaxjIzicxxZAXyDZGpkmftnmsZr14yStPcqW8LTBdjqHBtJl0mehGp8Sldg3msrgvoQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO0RPwzic5XiaeJFyzy5FXhXc4AFbM2Ok3sA47lusKVicicdqE3iciaPRciaL286Mic4ibHnls01tpqeicb1zlw/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.175...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO0RPwzic5XiaeJFyzy5FXhXctABzxGGuNyicwv5GQfAgbm17ncmg3QohicCPdDdWHrzUNe5ek8AaOOCQ/640?wx_fmt=png)

nmap 扫描输出显示靶机是 egotistical-bank.local 的域控制器，Internet 信息服务（IIS）和 LDAP 在它们各自的默认端口（80 和 389）上，开始枚举看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO0RPwzic5XiaeJFyzy5FXhXc2yYddP2RsiatGNtkC8TKDzLcclo3h8eleIuI4ZZicKQVKw2XLO2hHmdw/640?wx_fmt=png)

访问 80 端口发现这是 Egotistical 银行的一种广告页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO0RPwzic5XiaeJFyzy5FXhXciccWfhno77CA2sW7vzPQPq6Q5icUTBqibobTdTEJiaPK0jvTtKyHibsZbZA/640?wx_fmt=png)

往下翻发现了该页面包含员工团队页面，这里可以枚举很多用户名信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO0RPwzic5XiaeJFyzy5FXhXceQIG5ib1Vh22ZSvmOia1WYPjg0VFCoM6fmOzV635msdaust3XmiaG0yXw/640?wx_fmt=png)

我枚举了这些用户名出来...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO0RPwzic5XiaeJFyzy5FXhXcmRHAnzjwPSQrlkUc9ibKVKlurYfVMHwZe1zp7zQp9iaib6F49wOgoGbSA/640?wx_fmt=png)

这里利用 Impacket 的 GetNPUser 进行 ASREP 的攻击提取到了哈希值....

简单的脚本利用 GetNPUser.py....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO0RPwzic5XiaeJFyzy5FXhXc5dSria5tYISS1sBh6624ia9uaQp9ghqjp9AibWFG9uIpZ73nHbS0PqqBg/640?wx_fmt=png)

利用 john 爆破了哈希值，获得了密码信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO0RPwzic5XiaeJFyzy5FXhXcYqQoJJVdrfzOJMubaBWp4uYZPFwPGibz6MBuicn4CgVr3UL9Xt39Inzg/640?wx_fmt=png)

利用 winrm 直接登录... 获得了 user_flag 信息...

这里很顺利，前面很多端口都是个小坑，直接利用了 enum4linux，ldapsearch，rpcclient 枚举了没任何信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO0RPwzic5XiaeJFyzy5FXhXcqEvPtVXEuCbLzqKEFTcKfeEq7fMy73HpA0yV3zFfuejSjbBClAu7DA/640?wx_fmt=png)

直接上传 winPEAS 进行 win 靶机枚举... 没有的自行 google 下载...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO0RPwzic5XiaeJFyzy5FXhXcA0qjDrFUdL6eZ6ljWFwnEu4DVwZelJlib0x4uIvGrvMgYCHdr1HQqPQ/640?wx_fmt=png)

枚举到了 svc_loanmgr 用户信息....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO0RPwzic5XiaeJFyzy5FXhXcs7n9SQxp6qf1xXfFezSsa0h72t2GvnBDQLepwtKUDhFIhzKiarajYhQ/640?wx_fmt=png)

利用 winrm 登录了 svc 用户，查看发现该用户密码是永久有效的....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO0RPwzic5XiaeJFyzy5FXhXc5AYhyv0sk3fvjGdXzHFL7250E6rjpzQb2BnnXtx5osUB4USd02iaTSQ/640?wx_fmt=png)

由于 nmap 发现了域，而且存在多个用户情况下，我直接利用 bloodhound 进行了域枚举查看...

首先根据图先 `sudo apt install bloodhound` 下载，然后运行 `bloodhound`，`sudo neo4j console` 在运行启动 web 版，主要用于修改密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO0RPwzic5XiaeJFyzy5FXhXcI9W9ILpW0PbsSvT5dr1TZVVE9keqLRKiaghPojiaBL5fUJqswIsP3rMQ/640?wx_fmt=png)

登录 web 版本提示用新密码后修改即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO0RPwzic5XiaeJFyzy5FXhXcibJVK2ibWcWqlH6KlpYn6ZtseWaTicT7ibfKQlfck4tHM5vuIK5c6zOMzA/640?wx_fmt=png)

回到程序刷新下，登录修改好的密码即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO0RPwzic5XiaeJFyzy5FXhXc9FzW1Qib54GWwb1OnDUh53Ln4FibOtA0wUohJyNUZpm5PyZf0lTFOWlQ/640?wx_fmt=png)

```
wget https://github.com/BloodHoundAD/BloodHound/raw/master/Ingestors/SharpHound.exe
```

下载 SharpHound.exe 集成域所有信息... 包含策略啊什么的，也有弱项参考... 上传执行即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO0RPwzic5XiaeJFyzy5FXhXcXdQZj1ria3zSXOahTqd20BfERC3rhPO8N1d5VzzxJWCJ00ueWOGx1bw/640?wx_fmt=png)

将生成的域信息包丢入 bloodhound 即可...

然后把 svc 用户列出...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO0RPwzic5XiaeJFyzy5FXhXcBYzvqseDTHUibPiaibO9fiaX5WXfsNO20HuFtQQAolmzOvR5BIrL8ajIcA/640?wx_fmt=png)

把目前知道的 fsmith 用户也列出...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO0RPwzic5XiaeJFyzy5FXhXckDcibMYygsibfeGFwMWhvYibXfbNjP498KA2ee5KhYj3bR3lIPuqXSZKg/640?wx_fmt=png)

选择 Find Principals with DCSync Rights，查看到最短路径，查看 help 发现了此边缘不授予执行攻击的能力，但结合 DS-Replication-Get-Changes-All，委托人可能会执行 DCSync 攻击...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO0RPwzic5XiaeJFyzy5FXhXc4z3GSVs2jsKxHqewkfdiaRMsqA39999UPOVKicRwGR7rI6CZWjjT5OWQ/640?wx_fmt=png)

继续查看 Abuse Info 发现在 BloodHound 中同时具有 GetChanges 和 GetChangesAll 特权，可以使用 mimikatz 进行 dcsync 攻击以获取任意主体的密码哈希，或者还可以执行更复杂的 ExtraSids 攻击来跳跃域信任，还推荐了 hamj0y 博客自行查询等方案... 非常好...

这里我没有在 win 上进行渗透靶机，所以 mimikatz 我就不进行操作了... 知道此方法即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO0RPwzic5XiaeJFyzy5FXhXcLdPmYdTeYNZVV7stuibMmz7RN9wfxeVm88t0ibgKULV2g84Ox6vGUurw/640?wx_fmt=png)

```
/usr/bin/impacket-secretsdump svc_loanmgr@10.10.10.175
```

针对 DCSync 的攻击，还可以利用 Impacket 的 secretsdump.py 执行此攻击，该脚本将使用复制特权显示所有域用户的 NTLM 哈希值...

执行命令后，发现了转储主域管理员的密码哈希，非常好...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KO0RPwzic5XiaeJFyzy5FXhXcy6n6SOWHDyxqn7yyIwdBN2EgX2FfpDuQ97Fl7b4SINJ2XibRQibtxvrA/640?wx_fmt=png)

利用发现的密码 hash，直接 winrm 登录进入 administrator 用户中... 并获得了 root_flag 信息....

该靶机很简单，把 win 渗透的一些端口使用的脚本和工具，熟悉工具的原理，输出产生的信息学会分析，即可简单拿下该靶机！！加油~~

坚持！！

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台初级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

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