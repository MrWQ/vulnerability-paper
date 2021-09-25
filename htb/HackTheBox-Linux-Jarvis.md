> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/ozhnY8L-cHC-29hQqiJkeQ)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **160** 篇文章，本公众号会每日分享攻防渗透技术给大家。

  

靶机地址：https://www.hackthebox.eu/home/machines/profile/194

靶机难度：初级（4.7/10）

靶机发布日期：2019 年 9 月 9 日

靶机描述：

Jarvis is a medium difficulty Linux box running a web server, which has DoS and brute force protection enabled. A page is found to be vulnerable to SQL injection, which requires manual exploitation. This service allows the writing of a shell to the web root for the foothold. The www user is allowed to execute a script as another user, and the script is vulnerable to command injection. On further enumeration, systemctl is found to have the SUID bit set, which is leveraged to gain a root shell.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

  

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMMX7DC2SxNN7aLoJHjm7pLo8AukXTL9tHo1Q0SpktgNLX2ULk4Nzkr6jNrqvCuB9fOLEkYGiao8XA/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.143...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMMX7DC2SxNN7aLoJHjm7pLRpLv5Xfu89ib4s4I9n0OfWKqIqaf3NDVEbLD70JRA8UficfVcz5bAHog/640?wx_fmt=png)

我这里利用 Masscan 快速的扫描出了 21，22，64999 端口，在利用 nmap 详细的扫描了三个端口信息，22 是 ssh，64999 是 http 服务等...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMMX7DC2SxNN7aLoJHjm7pLzp8kOcicI9MPbyB8w9fyjFiae8dEqFj2VrCaXxVcEmVSiclLTGW6YIUDA/640?wx_fmt=png)

访问到端口 80 上的 Apache 服务器，可以看到一个名为 “Stark Hotel” 的页面....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMMX7DC2SxNN7aLoJHjm7pL3Qqib1dP674HmOhtpAog7rr5WEheDwG5nkticWFkLlOokta0aSjEtlcg/640?wx_fmt=png)

可看到该页面有订餐页面，也有订房页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMMX7DC2SxNN7aLoJHjm7pLgF1lNLeJbl7zXDu2Hsz9iapoPjcBkKicZbUqsjIgicApYictvUxWQYyXAA/640?wx_fmt=png)

随意进入一个订房页面，发现 URL，存在 sql 注入...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMMX7DC2SxNN7aLoJHjm7pLsUfhnQWicrNZ5r3oCOFmAUGyQuBxJobXPyqTh50L0rrUiaIE26N4R7aQ/640?wx_fmt=png)

测试发现可利用 sql 注入提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMMX7DC2SxNN7aLoJHjm7pL0tDk2dQSibWbjYiazNOPoEXNHKib9Cy56dbILoFIw957MZ1oKWjicShfzQ/640?wx_fmt=png)

```
http://10.10.10.143/room.php?cod=-1 union select 1,load_file('/etc/passwd'),3,4,5,6,7
```

发现了 2 存在注入点，查看到了 passwd 信息....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMMX7DC2SxNN7aLoJHjm7pL2yD13ibFicBHEUc10KQxaRQh36QWgIu4PqnOxevibuqybo5qPa7UYnFbA/640?wx_fmt=png)

利用 into outfile 创建了文本... 将查看到的信息放入了文本中... 测试看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMMX7DC2SxNN7aLoJHjm7pLsMccNlxDCiaGScAASHHHrojjfFBW9nKUZlkhE8Dx3frAnxTxedYM57w/640?wx_fmt=png)

可看到，成功的，那么简单了，写个 shell 提权即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMMX7DC2SxNN7aLoJHjm7pLicpeTJAUibsA3hW6AdnZIraMxZWw4jkAxlCAIkTDGb4kbnZEh4iak0xSQ/640?wx_fmt=png)

```
http://10.10.10.143/room.php?cod=-1 union select 1,'<?php system($_REQUEST["dayu"]);?>',3,4,5,6,7 into outfile '/var/www/html/dayu.php'
```

简单写入 cmd 命令...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMMX7DC2SxNN7aLoJHjm7pLTL8iaibCIrzlurw71gUSapOygwmI9blrBh1iauicXsrtFgLgZgZ0cibke5w/640?wx_fmt=png)

然后利用 cmd 直接写入 shell，获得了反向外壳 www 权限.... 但是无法读取 user_flag 信息....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMMX7DC2SxNN7aLoJHjm7pLTj2MmaMU8ttTp3gDNObsRoVDC8iaNiaBSza9t9aeMjeZq2OhM7I4Wgag/640?wx_fmt=png)

sudo 发现了 all 存在 simpler.py 脚本... 查看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMMX7DC2SxNN7aLoJHjm7pLqiciaXCqGKVc999Ud6ZChYP5zSZHTic7jGibCrzcZQ3IDAia16YHcA5pTtw/640?wx_fmt=png)

查看脚本，看到它使用 - p 参数获取 IP 地址，然后使用 os.system（）函数执行 ping....

脚本还阻止了一些字符（＆;-`| |）以防止注入...

但不会阻止字符 “$”，“（）字符，这可以通过 bash 命令替换即“ $（cmd）” 注入命令提权....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMMX7DC2SxNN7aLoJHjm7pLv94w9T273Kbt9mRDJkn9rDN3OiamFJq8euUB9PG2FV7DAFW7G8lPWsQ/640?wx_fmt=png)

可以看到该命令被用户名 pepper 代替，并且 ping 尝试将其解析为主机名说明命令执行成功...

那么可以使用它来执行 bash 反向 shell，并获得一个 shell 作为 Pepper....

由于某些特殊字符被阻止，我将命令写入脚本并通过注入执行它....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMMX7DC2SxNN7aLoJHjm7pLoxJM01ricBo4c8vGNFTx92vj72V7EicnH9hUD7K8fk54u33ia9JPCjt7g/640?wx_fmt=png)

简单的 shell 写入即可...

然后执行 shell 获得了反向外壳 pepper 用户权限... 获得了 user_flag 信息...

由于这个外壳不稳定... 我进行了 ssh

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMMX7DC2SxNN7aLoJHjm7pLxibTK4AB8icIBvaSjFdOdCY9Nkx5SE1OT7LZX9gastg02tdoNfHtjfkw/640?wx_fmt=png)

创建. ssh，并本地生成 ssh-key.... 然后写入到 pepper 中...（简单操作）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMMX7DC2SxNN7aLoJHjm7pL4ItTOyLqSVqfgTOBVLIqIBbIdTwibnrDgh4Us3vuxOuS7ibeJhABfgSw/640?wx_fmt=png)

ssh 登录后，枚举了 SUID，发现存在 systemctl....

systemctl 命令用于管理运行 systemd 的系统上的服务....google 看看怎么利用...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMMX7DC2SxNN7aLoJHjm7pLnD0qFTqy0ZEiay2h9mJJmPgevBQtwT4GrWb1gLdczT6Cy96bdl6gRSw/640?wx_fmt=png)

google 发现了挺多提权的办法...

只需要创建一个服务，该服务在启动时执行我们选择的文件，然后使用它 systemctl 来启用和启动它.. 这样就能执行了

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMMX7DC2SxNN7aLoJHjm7pL3ukBf3kVhSkaVYI2QG2H0zHrTu2HSg0DBwFAt8oM0yud7icJVhtv6rQ/640?wx_fmt=png)

  

我创建了一个简单的 bash-shell，然后创建 service 服务，并利用 systemctl 进行启动，启动后执行. sh 的 shell，并获得了 root 权限的反向外壳...

获得了 root_flag 信息...

简单的 sql 注入 --systemctl(SUID）提权....

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