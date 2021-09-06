> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/-EPtKX5Z90hSKIkjxhZ-sg)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **142** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/4gCJbFBBaxgr0WD3mMgto4yFaYwwjQMbuxDDBKibrhNlW5YFLV3K1XvkGj1sP1BiaYtibMLdQVrvth08BVUWP7oGw/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/162

靶机难度：中级（5.0/10）

靶机发布日期：2019 年 4 月 11 日

靶机描述：

RedCross is a medium difficulty box that features XSS, OS commanding, SQL injection, remote exploitation of a vulnerable application, and privilege escalation via PAM/NSS.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/3CSGsOUQKfsq2MZPDdCbRx4QOq5Hu6gwrOCquO8aT36jQ9E11LOX3TlAkU4FMhGlA2GtyiaXia4DpyEf9A6cZHXg/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/CFzCpw2dZa6XK6W3JRCld4jmp0GibCWLXUqvXCSUQzVI4ROVn3Quu5KWKhPcaUMe5MicicTrXO0YGPLY2OyXoiaeEA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHNxYiaYVPyl1lgzLP3vY0eibAgntd25YqfG70w7uS01hmS0aq0mEYmTicg/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.113...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHo9N1YJGXehQJuDE6SqkCicnAf6HnoDCOb9rPkOqn0CLzeozwOTicicNnA/640?wx_fmt=png)

nmap 发现开放了 22、80 和 443 端口....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHGuKNbtU0wTVLHiaibvvI6G8wic7FdTcuVh8uY8Bm9mgfbSBrOMt6k6XEA/640?wx_fmt=png)

访问 80 后跳转到了 443 页面... 但是没有内容，添加域名到 hosts...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHKjgliccia8Eib9hqZYhib6UMmqoSNvAlQWlYuWGHmX6pDrPoYtkNOH52bQ/640?wx_fmt=png)

这里 wfuzz 枚举了域名情况... 发现还存在 admin 域名，将下列三个域名添加进 hosts 即可...

intra.redcross.htb admin.redcross.htb redcross.htb

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHDIsyGt58zYicU5FfmAs64xlDyrCQJ7piaQO0H7R6HEW79EGDaib4jTMQw/640?wx_fmt=png)

这是一个表单登录界面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHQBTRNMN03IT8fwnkAe0iaxZINeJnhMOib4sTOdAa5yfhicOGiarYjmn2Mw/640?wx_fmt=png)

简单的 admin 登录返回的结果...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHuBnyMRGUxORwOGyrAYu9DHzUlZvUvjewYC6g4uFsxWicPvqzxvbzXbw/640?wx_fmt=png)

bp 拦截抓包...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHCAJTm4RNaMSfSFhft33ck6kdpJcjN3Co1tclYeJgiaH3xvtpZM2F0xA/640?wx_fmt=png)

```
wfuzz -c --hh 11 -u "https://intra.redcross.htb/pages/actions.php" -X POST -d "user=FUZZ&pass=FUZZ&action=login" -w top-usernames-shortlist.txt
```

然后利用 wfuzz 枚举用户密码... 发现 guest 可以登录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXH21kGiah3j1QqKMVPpMMCiayNKJTvJgeUm7eqm06yjGysttD1ZDRnbXJg/640?wx_fmt=png)

guest 登录返回的结果...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHdynrfcEN0vZp85BGpVqk5JBNUAKukwsUNtxgtDDqKZs6Fsw0ibZibyZA/640?wx_fmt=png)

返回结果后跳转到了当前页面...userID 信息提示... 应该存在 uid 注入？？试试

试了会发现 sqlmap 能枚举一些基础邮箱信息... 自行测试... 主要这些信息对后面没用...（会解释）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHuRPWRUZRxkHf8RdMeUyFWGuktZxia87Y8p4ocXRjpia2GNyJaVgkSsaQ/640?wx_fmt=png)

继续查看 admin 域名页面，这是一个管理员访问的登录页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHLyMOQyllevUSccf0tTRYqWCp36eJ0w173UPDIqrtr7kmWhFUxRmiaHg/640?wx_fmt=png)

这里的场景是利用 cookie 中的 ssid 值替换获得管理员权限... 场景以前做过两三次类似的了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXH7geVSR1pTXbJ21DR8k9IO6QWibFX2cQ6ia6g4td2WrRCrG54PibdPP8tQ/640?wx_fmt=png)

利用 cookie editor 插件或者 F12 查看 storage 即可... 查看到了 cookie_value 值...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHHuOeAAq0Zsx8GTq9lo43dPJA9AQlu7VcQA0icfkDkg18OOAySlMWkjg/640?wx_fmt=png)

将值覆盖替换下... 保存刷新页面，可看到获得了 admin 权限页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHKVg0ADWGBD9CHvb4XjqfF0mIibwUDNwEaHIDBDkcmUrwj7VNlHgvcng/640?wx_fmt=png)

第一个这是创建添加 ssh 用户的界面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHpRzxaV8buMd1uET7tkgqySww0dp5e8wP6GmEgJjVIeUf7FzpS9xiccw/640?wx_fmt=png)

简单创建了个 ssh 用户名 dayu....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHPGXbEG2UbnOoocSkEnMt3O2asibUibuh7eZZQmOTW1decegNIOye84bw/640?wx_fmt=png)

利用 ssh 登录进来后，权限很低，查看到了 iptctl.c 文件信息，该文件包含防火墙管理应用程序在管理页面上调用的程序代码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHFhpvb5dFeEwox0vibnNNbMCq4qNGgHHYWwFibv0R83Hzo1F8xsgEJFDw/640?wx_fmt=png)

并看到了只有两个用户...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHic41gtcHSnpOeEBmBepHclhqXn4Pvd9jib5FSWAGy4Dy4RaoLgeGPnlg/640?wx_fmt=png)

在 Network Access 中，可以添加 IP 和删除 IP 到防火墙规则白名单中...

从防火墙 ACL 中添加 / 删除 IP 时，PHP 代码都会调用 system（）来运行程序并更改防火墙规则...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHDNKD1jF5jCic6micwbibXiaETxWF9F2dql64KibDvibTlWDIs7o0vDiabo1Tg/640?wx_fmt=png)

添加了一个白名单本地...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXH3fjqk7ZtduKd7HJENS8JVChQON2WENrxGWdBTK7zOOAa2icXqLzw96w/640?wx_fmt=png)

如果在 id 参数中添加分号，则可以注入命令并获得代码执行...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXH5uLGPNJVtaeBOfVRwzgKwYc9DnIz3HxNic8OWxlmFaRdWB3h57ibyB9g/640?wx_fmt=png)

注入查看到了本目录下文件信息... 这里直接 shell 提权即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHFuUDAib0wFUk8ibQXzhmcloeHcTLqf0QlibNqkRibZBJjL3z67Ribic4Z1Cg/640?wx_fmt=png)

利用简单的 pentestmonkey_shell 提权成功... 但不能读取 user_flag 信息..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXH0icUKePWia5ElP4qcpvCpZOPBezWzQcZgz2tXa35z1ZjXmMicZd1sOQvg/640?wx_fmt=png)

SMTP 服务器 Haraka 存在漏洞....

可以看到运行着 haraka，在本地或者 google 都可以查到可利用 41162.py 进行提权...

MSF 也提供了 EXP 利用，我都试过了...

两个方法都无法提权... 坑... 浪费了一些时间...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHUTgtHWr8FCKibjGg9X5FrWKdx7Hv10cz92xfO1vKaaI8pIbhcFxzxIg/640?wx_fmt=png)我把 kali 本地 tun0 的 IP 加入了防火墙 ACL 白名单中... 去检查下过滤后扫描是否能多下可用信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHsgSBdOabZyMBB4utB11GV6nZlNEB0pCSZac0ZZ6w24w10ybicSjSgxg/640?wx_fmt=png)

可以看到本地放行后，多了 1025 和 5432 端口开放着...

这里又是一个坑...

可以到 www 权限外壳下，通过 telnet 登录 1025 端口... 按理说，可以利用 EXP 放到 WWW 外壳的 / dev/shm 中，直接提权能获得反向外壳... 思路失败了... 估计是技术还不够... 跳过...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXH2YmLTpa0hDuno1yuDxKD1RAZ1QEVSQlibJocgLKgQbRxwIPuqB2eb8A/640?wx_fmt=png)

在 admin 目录下发现了 actions.php 文件，查看后发现了用户名和密码信息... 开头是：pg_connect，全体搜索下看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXH4koMKMp3fm1UqQ57yqDBzHXbmSWIysKukkw31TOhSDC8fibZJic7GyeA/640?wx_fmt=png)

发现了一些用户名信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHUONic4vq9A5nKxOTJ0z3Dib0r8XCF653VEVd7vEXnPvGtajyq7ySfonQ/640?wx_fmt=png)

有了一些凭证后，用户 unixusrmgr 可以登录到数据库中...

通过 \ d 发现了可查看的目录情况...

查看 passwd_table 后，发现这是前面添加 SSH 创建 ID 的信息表...

我又进行了添加两个 ssh 信息测试...

发现目前 gid 添加后默认是 1001，root 的 gid 是 0，可以进行修改.. 然后就能直接获得 root 权限... 试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHICEklIIHpTCslJzMFJjU94Rj0mREOnaQfmPgicbIWOicejwuJx5gOcQQ/640?wx_fmt=png)

```
update passwd_table set gid=0 where gid=1001;
update passwd_table set homedir='/home' where homedir='/var/jail/home';
```

成功修改...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXH5JZoJBrPR91CicnyZMXiciblNaSg2TsdlbN6Enql5GKo4ZuDomoq5U4TA/640?wx_fmt=png)

检查后可以看到将 gid 全部修改为和 root 一样...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHykBoQRu5gHNb76omd0lDTQXYmdmbNHaVeWAdrCiaXic2sTdFpnW87ycQ/640?wx_fmt=png)

通过 ssh 登录发现获得了 root 权限...

还是无法读取 user_flag 信息... 继续检查下

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHrjesSS6dnIPUInwDA95AUDREiaC3zEmJaYjsE64OskFTlicQYqK76OoQ/640?wx_fmt=png)

sudo 发现无权限 sudo???，root 都无权限 sudo... 检查了 sudoers 配置信息，发现 sudo 可以提权到 ALL...

如果拥有 gid 该组的 sudo，将能够运行 sudo 提权获得 flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHVfJbsvIL8FsG83dNOfia50cS8aGUQDbVIoZtpibUQ2J9Lxb5US5bKOkA/640?wx_fmt=png)

检查发现 sudo 的 gid 是 27....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHyXI7xtWuf2rtwhqo3ZkEgwq0XGEq2gCbENic0JQfxAicrHc6tQmf8DXg/640?wx_fmt=png)

回到数据库在修改下 gid... 为 27

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXH5Xibyn1cCXTwQhYXL9fy8ZK84cLCFLJMEbeaeEFBOG2Kve0x9HO2ib7g/640?wx_fmt=png)

已修改成功...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNAZq5ZtwuDnfSb8ByTRvXHgDf4vjhGAhAgCzOEozXD2ibsfgU78dVkfo0xMOzDewViaGDDAs60IXyw/640?wx_fmt=png)

ssh 登录后，获得了 sudo 权限...sudo su 获得了最终的 root 权限用户外壳...

并同时获得了 user 和 root_flag 信息... 这里是有点坑，估计是我对于 haraka 漏洞理解不深，没有提权成功，所以导致 user 得 root 权限获得，哈哈....

加油吧....

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台中级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/mOcxDEIvrQXjKq4u8WBtxHcSvTMPpTEKv2hGbMbxR5ic3iapf3RFeETmwkrHdGnMqZdZ8cFHBpyOsEgvx1QnJRpw/640?wx_fmt=png)

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