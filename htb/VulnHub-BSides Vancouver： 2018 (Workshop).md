> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/4HSfzF9EGTasMvL0YGzXkw)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **37** 篇文章，本公众号会每日分享攻防渗透技术给大家。

靶机地址：https://www.vulnhub.com/entry/bsides-vancouver-2018-workshop%2C231/

靶机难度：中级（CTF）

靶机发布日期：2018 年 3 月 21 日

靶机描述：

Boot2root 挑战旨在创建一个安全的环境，您可以在该环境中对（故意）易受攻击的目标执行真实的渗透测试。

该研讨会将为您提供定制的 VM，目标是在其上获得根级别的访问权限。

对于那些想进入渗透测试却又不知道从哪里开始的人来说，这是一个很大的机会。*

如果这听起来令人生畏，请不要担心！在研讨会期间，我们将在渗透测试的每个步骤中讨论各种方法，常见的陷阱和有用的工具。

目标：得到 root 权限 & 找到 flag.txt

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/eYQPCtdp52LibNkiaf6uEFlNLBXkYNLkGrreELUwooJCbCCre3PNVwyB7MD0We5GB7C1iao7ZNneayc3PxQD0iaAmg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/MXiaez6x34s6wqPicKX6MTMsLicycAiarVzaS6YpDetKt5tNvsEibgrDYtBhSPrxZaLerjdvlDm3o3Y5ow9ibVcv8nBA/640?wx_fmt=gif)

一、信息收集

我们在 VM 中需要确定攻击目标的 IP 地址，需要使用 nmap 获取目标 IP 地址：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN8BHmBN5xGmicabECnSAF20Q73orPHD2h0rODpBvRcj1P7LDMic0w8LKEccLKNziaNe0vBDjyia0OJXA/640?wx_fmt=png)

我们已经找到了此次 CTF 目标计算机 IP 地址：

```
192.168.56.134
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN8BHmBN5xGmicabECnSAF20E1iabLRCPk1EP8zcibVUynLgx7jOgpPAiaOh5RJxsbfj851IevaZqeFAg/640?wx_fmt=png)

nmap 扫到了 21、22 和 80 端口在运行...80 端口开放了 / backup_wordpress...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN8BHmBN5xGmicabECnSAF20ZAQUicfwqACG4l7C6y5iciaTwZYJEe1DxlicVich38gEd1g9zpjPynDnAng/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN8BHmBN5xGmicabECnSAF20GsdrMbBsvlnSrBPiaeOSaMlc1MssJJdQnCicVawUnkaAl0MKV6mZMNQg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN8BHmBN5xGmicabECnSAF20JgwhzKtVzMr5R4U0RGiaASHqh2APfNXka7gFcsgQ1YwRD6XNVU65icLw/640?wx_fmt=png)

这边直接访问 FTP，发现了 / public/users.txt.bk 文件，打开发现了：

```
abatchy
john
mai
anne
doomguy
```

这应该是五个用户名...

访问 web...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN8BHmBN5xGmicabECnSAF203xUHZuVaLicpE7vx4B3wWTk5OWoWbvQvn7BibY6HvwX7NKq2GCicdCQLA/640?wx_fmt=png)

说未添加内容，会看到 nmap 发现的目录，访问试试...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN8BHmBN5xGmicabECnSAF20VRlUG6MMt79v3wOialgyG6jZIf9QlwRjo4aTlT9icy1ib3eTO2eutjRNQ/640?wx_fmt=png)

发现了 wordpress site 框架... 查看前端源码，和别的地方都没发现有用的信息... 这边 wpscan 爆破看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN8BHmBN5xGmicabECnSAF20cUQ4ibQKBgLSsgD9lyC125CQ8tIeeeiaEje3KcrIO6QxTtHfvSbJ0Y1w/640?wx_fmt=png)

```
wpscan --url http://192.168.56.134/backup_wordpress/ --enumerate
```

使用过 wpscan 枚举出了 admin 和 john 两个用户是存在的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN8BHmBN5xGmicabECnSAF20hyEicpMtota5c1BQcibDNa2WKPyW0E3Vm1VvXcfqia63pvllrHM12v05g/640?wx_fmt=png)

```
wpscan --url http://192.168.56.134/backup_wordpress --username john --wordlist /root/Desktop/dayubsides/rockyou.txt
```

这边发现了 john 的密码是 enigma

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN8BHmBN5xGmicabECnSAF20cibxphTmROiaNAfPkvibic107vqVzexaY8iaS6AlHXHLCpU5g90gksdWDQA/640?wx_fmt=png)

可以文件上传... 或者利用 wp_admin_shell_upload 漏洞上传都可以获得权限...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN8BHmBN5xGmicabECnSAF202Z6dYB0kAUcP38t8lzYst5ibdNYOjRtsYG2IMxX0WA2IH2zIYibwUDkw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN8BHmBN5xGmicabECnSAF205sFWuS1MhNWhs9hwNC8mn0LicHJWjS2J48MIQ2tVxUiclQd9ZUx6C5eA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN8BHmBN5xGmicabECnSAF20zY0p3VDyCufSGWXVK06DgOjJ04kbjXsSh5gFfoImVnHrMdDFwFicIibQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/MXiaez6x34s6wqPicKX6MTMsLicycAiarVzaS6YpDetKt5tNvsEibgrDYtBhSPrxZaLerjdvlDm3o3Y5ow9ibVcv8nBA/640?wx_fmt=gif)

二、提权

将 shell 上传即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN8BHmBN5xGmicabECnSAF20Lpxw8T31MN2O3iaPQUzbAibFwBWVS6tyTtdODdwT8xuWibWPBUytIZ75Q/640?wx_fmt=png)

访问即可获得 www-data 低权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN8BHmBN5xGmicabECnSAF20z26OusZ4CuBpn2tiazLa3ESrfJfOwEv9Qu8QhYbVXcvfe9SoQS1icgSA/640?wx_fmt=png)

这边发现了 anne 用户可以直接提权？？？

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN8BHmBN5xGmicabECnSAF20YNEpASAnR7L1Rog5qOtj1EsIl9SMm8S7ReDjUOX9UJZhUlItqXSQiag/640?wx_fmt=png)

```
hydra -l anne -P /usr/share/wordlists/rockyou.txt -t 4  192.168.56.134 ssh
通过九头蛇直接破解anne用户密码：princess
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN8BHmBN5xGmicabECnSAF20LmkHdWeuaox97qPKWP3wgpNZ54P4quWia0psvevCNbSkHKB0CsvFQcQ/640?wx_fmt=png)

查看果然可以使用 sudo 提权... 这边成功获得 root 权限和 flag...（这是提权经验多的一看就能直接拿到权限了）

另外介绍数据库提权，这么多篇过来，都应该知道 wordpress 存在 wp-config.php 文件，里面有 mysql 账号密码... 这边看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN8BHmBN5xGmicabECnSAF20SKlBAushQ5x4LNAMibhJTtJwmxHGO4V3Y0Hsd9tUIDibwpXjEQibn6LtA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN8BHmBN5xGmicabECnSAF20Jic9yVfYyMY6qlLlD95Hl4Su7hrPyTI3PX590mpsGSwRwXC51Ytk6ibg/640?wx_fmt=png)

thiscannotbeit 密码... 登陆试试...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN8BHmBN5xGmicabECnSAF202sjce9G2dRiaM3zInLnzc68gnBxicGHQve5BolrZib00O7I5icqzRaOZpw/640?wx_fmt=png)

拒绝登陆....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN8BHmBN5xGmicabECnSAF20e7P7HUO5H6hlO9ewIyicVrkDO2qLUU0rWB1YAKqWUdtjJdPkvCBa4jA/640?wx_fmt=png)

拒绝...

在找找另外一条路....(加油）

mysql 这条路行不通... 尴尬....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN8BHmBN5xGmicabECnSAF20av0G1ThbLXYWJFNQJk6FTIwgRm9ZqO9guQvDP7ybNUaFY6Px7Pqvrw/640?wx_fmt=png)

```
lsb_release -a
```

这边查询到可以版本漏洞... 可以使用脏牛提权... 试试

我发现这里无法上传文件...

![](https://mmbiz.qpic.cn/mmbiz_gif/MXiaez6x34s6wqPicKX6MTMsLicycAiarVzaS6YpDetKt5tNvsEibgrDYtBhSPrxZaLerjdvlDm3o3Y5ow9ibVcv8nBA/640?wx_fmt=gif)

第二种提权

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN8BHmBN5xGmicabECnSAF20gWICGP9zOQZgaibugrIwr7YaAOMBA2bdhicHKKUN3BrdAnxDKfIicOVfA/640?wx_fmt=png)

这边用 MSF 内核提权... 耻辱提权，但也是一种方法...

利用 exploit/unix/webapp/wp_admin_shell_upload 上传外壳 shell 提权...

命令：

```
1. set rhost 192.168.56.134
 2. set targeturi /backup_wordpress
 3. set username john
 4. set password enigma
```

可以看到 session 1 已经渗透进去了... 这边和前面方法一样... 可以获得 root 和 flag....

这边就不演示下去了，我相信还有最少几种不同的方法能渗透拿到 root 和 flag...（这边如果哪位兄弟发现了，记得告知我）

由于我们已经成功得到 root 权限和 flag，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/eYQPCtdp52LibNkiaf6uEFlNLBXkYNLkGrreELUwooJCbCCre3PNVwyB7MD0We5GB7C1iao7ZNneayc3PxQD0iaAmg/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)