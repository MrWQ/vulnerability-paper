> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/fladXsIBAZoes3TyvHXt5w)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **45** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/5ria5WVLahGj8W7vu6J2jzTGqRtEaL6ib9CDzENq8PCEZADfU3JXsmibNacJhY7rooNoYIpCsUytNS0k4UcSsnRfw/640?wx_fmt=png)

靶机地址：https://www.vulnhub.com/entry/defcon-toronto-galahad,194/

靶机难度：初级（CTF）

靶机发布日期：2017 年 6 月 1 日

靶机描述：

Defcon Toronto 于 2016 年 9 月主办的在线 CTF 中使用的其中一种 VM，进行了略微修改以适应 boot2root 的挑战。

信息：总共要收集 7 个标记，id 0 是最后一步。

目标：得到 root 权限 & 找到 flag.txt

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/XxZOJAn437TAwOeYFBI2JiamRa34iaqY1IAPG9MaXSIKgPlBicRoyoyHPr0q6YUAhLTYebc4z2qjok0r1riadSujeg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_svg/kiaXicXJs2M4e1LWaSZxYGicECrUwR1s7o8UiblW7CyI0t5KzkBruwlYfgG40XPhDhlBibFriasnSQia9NxU7KZWhPDWZeWJcJr2CH5/640?wx_fmt=svg)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLY4XuVdURNmQPUGrLmh3bDFaTDviayiceQSc2kKhS64xp8NibzU0z7Fic4Q/640?wx_fmt=png)  

我们在 VM 中需要确定攻击目标的 IP 地址，需要使用 nmap 获取目标 IP 地址：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLe3XP39uVpyDXm5iaftFykahFH1VhqZlgPwbztr37sj0aDxZ0yrHziacQ/640?wx_fmt=png)

我们已经找到了此次 CTF 目标计算机 IP 地址：192.168.182.144

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLh5aNnRr4zekEPib2l1FH8Kq8Rw3d0Fo44EC5kRkoyZ9S7lOToMvdibiag/640?wx_fmt=png)

nmap 扫描发现开放了 22、80、50000 端口...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLibtfC8AHaW1oTEKe0ltyecTEMHko1EwTz5eiaA87ib4mhDtibOuT40fkkQ/640?wx_fmt=png)

01 是二进制值... 翻译后：

```
For the cuorius out there the binary translates to:
Welcome
This is were the adventure begins -.-
DC416 Team
btw
no flag here ;(
```

没啥有用的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLiaTXLUa52q8t99as7pVnXxHzVy3scf2kqE6210cAXMITgQ7E44hIl4A/640?wx_fmt=png)

发现前端代码使用 firefox API 在控制台上打印内容... 查看 Console 可以看到这是 ROT-13 加密后的值...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NL8zcV8AqyPe1ibmDsLv0S4icYGEXianBxwj7ibhMZQZ1WIicFl05k2RM1ZsQ/640?wx_fmt=png)

```
flag1{m00nc4ke}n
```

成功查看到 flag1...  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLbdfejBOQO0ianDibF8AHK2lThA1H9CTfAD6wFhgvtTc7NK9Rt6Nnv4VQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLaIcUk99N9auVg0EfUmrK12LA6AGcz2cFRKiaNYHV8bqHPpPvJKNRouw/640?wx_fmt=png)

显示存在 / staff 目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NL7uTV3GyCdV5vKiaSCCjQU6KThaicsq4tKr6arGbpbcp2psU6TS1GCQAw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLIQdvoFLN7XAW0GyYq60lKMXEJVffsuocgVln3T3vLb8wVFMKpDZoSg/640?wx_fmt=png)

dirb、nikto 和 uniscan 发现了三个目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLUYUCE3lW6IKpTibhJIco6ibJESU3Uxbs9MV76xFqwW5Ujbdy09j0B2bQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLJ3iazj5PLSwcXG7VXnqKO7N7zSlOdKFMH9jaYQaC2XHmPNp6Jvk7bVg/640?wx_fmt=png)

在 staff 目录下发现了 s.txt 和 nsa.jpg 文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLEnmLFTN6UJm5ecG8QZ7gWqY4cgUM3Gxnl9UlYJ3nASwMRunicpBG4Xw/640?wx_fmt=png)

应该是 base64 编码... 需要把他解开看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NL8o2YklVqPMib03m8pTEKEI2IVcyQ2jEBVib6IiaIHevlrAtbd349KNZjA/640?wx_fmt=png)

```
or i in $(cat s.txt); do echo -n $i | base64 --decode; done
发现类似密码：edward
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLiaWia9CbdIIBpZBL2vep3NBG20DW9bNbFne8DkI1pt43N5crP3n2aFJg/640?wx_fmt=png)

这边我开始用了各种工具分析，还是没发现 jpg 有啥.. 后来找到了 steghide 隐写工具后，发现了 flag2

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLx5yNYLWicYMIibza1FCLpibzoK0hFCH32XIX7hVEBicsbWwiaIdU6S8QELQ/640?wx_fmt=png)

```
flag2{M00nface}
```

还发现了一个 URL...  ：/cgi-bin/vault.py?arg=message  

继续访问刚给的信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLTRBfGvsleHd1pFQMibss3KL0rm2QqttSsTib5Yr966LCRZW97Mt7nHPA/640?wx_fmt=png)

拒绝访问 nsa.gov？？

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLywN1b1f1fpDtrrPD4gDVEd418cBHqKqo1wRGibLM3KN37XtC7qXOy6g/640?wx_fmt=png)

用 burp suite 渗透分析后，使用上面的脚本进行 intruder 即可找到 flag3...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLzLZFic9gibWBl7BVjQgBia4ZicjRxnWxj3SiaWt3QfNSiaZIBnuDVP5icctAA/640?wx_fmt=png)

```
flag3{p0utin3}
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NL5RDeibKia1vQnJXeX8Bgq3VCS2J6K1g73OzoicMOeHzGBvGiaQEwo3cQ5Q/640?wx_fmt=png)

发现可以下载文件... 下载下来

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLN3EMG5vk8AQH9ia8BDiaTIcNjkj7IxhVVybjibfaPzKe86RW325bsVdCg/640?wx_fmt=png)

在 admin 目录发现 enc.zip 文件，分析下...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLm9wooD4lfZ1ckznIQiclENI1FBhHkIcicOefzEeTFR7XFGr1XoFoOjyw/640?wx_fmt=png)

```
1. git clone https://github.com/wibiti/uncompyle2
 2. cd uncompyle2
 3. python setup.py install
uncompyle2 enc.pyc > enc.py
```

这里可以看到 pyc 文件无法直接阅读... 需要用到 uncompyle2 进行编译 py 后才可以...（没有的需要安装，安装命令在上面...)

这里，我是服了作者的思维... 它的意思是下划线一横代表数量 1，例如 str2 有六横就是数字 6，然后二十六个字母表里，数字第六位就是 F...

按照我这个思路一路填写即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLqtKC1ZdOCCfYrfHCK0rAOnyPs141WCxVdqhLw8v6CLuTPIUFOTfAMQ/640?wx_fmt=png)

```
flag{f0urd1g1tz}
```

 数得我眼睛疼...  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLPDLp0S4UWfwOYrVBaDRSCyLpZ6yecbd2RpJRJOib9CmWBl530pP4w5g/640?wx_fmt=png)

50000？是不是按时 flag5？？

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NL9SOOhuibiaTP0fmksVCx4M8MicsUhhdEoVwzwL34lJicQ1T3h2cH6yuROw/640?wx_fmt=png)

禁止访问???

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLFSTPnKlGtDcGbuPfloIUapfP9Kcoc2A0YrmB1GvzUINF39uR5NBaCQ/640?wx_fmt=png)

SECURITY THROUGH OBSCURITY 34343434 0d 0a UDP

这里的意思是 0x34 是 4... 就是 4444...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NL1zFibhQ3gZxD5ghkXM0oSCS7oKiaOE2jPf9zaVdMsXQ8e2XlL7qibyjKg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLbZAZRibpcgzfNsxO0Hja6b28CxmdFW0WCEFsDGQaocTlZUp5mL31OUA/640?wx_fmt=png)

尝试通过 UDP 敲端口，但没有成功....

```
4444:udp 8331:tcp 7331:tcp 31337:tcp 31338:tcp...
```

这不是最正确的顺序，因为会变...  

可以了解到 knock 敲震方法，如果顺序不对，是不会开门的... 敲对会开 FTP21 端口...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLfaL8eB2H5CKqkywVviatA8GyJA8HYJyT3icXqZiaKWjib0RJHslCnFxJbw/640?wx_fmt=png)

发现 21 端口打开了...

里面有两个文件...bar.pcap 和 foo.pcap... 流量文件...

检查 bar.pcap

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLhOVOj3zf5HL8qHToicp6ZJpv5uaPEKptt4bWibso6FLOF8n0QKVELeSQ/640?wx_fmt=png)

```
flag5{th3fuzz}
```

第二个 foo.pcap 文件中找到了第六个标志的线索...

隔离了包含 JPEG 的数据流后... 获得 jpeg 文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLPR86EiciaJibJo9RtVfYnsYcJYCfMIaMDoArnSqy4pvFk3aerSApUWrog/640?wx_fmt=png)

是个电厂图，左上角还有 uid，看到有个用户名：nitro

看了这个资料我才知道.. 密码是 zeus...

```
[链接](https://en.wikipedia.org/wiki/Nitro_Zeus)
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLOZQ33lZj60qOIibGDQ2geqqMqJUmufYjvXHicYQh6eMhxMfcml3UaYgg/640?wx_fmt=png)

通过 SSH 登陆后发现又要玩游戏?????

游戏要求您赢 3/5 游戏.... 很坑的是每次都是随机的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLmLhThD3thvriawaSicqe2SHRltxxgdGfIUGVlRQfX6IKTGe7kwdicxbZA/640?wx_fmt=png)

别回来问我怎么过的，一个一个一个无限制试... 我这里也花了时间...

```
Flag: flag6{s1xfl4gs}
Hint: Did you know that Galahad is just one of a few round-table knights?
```

需要列出所有圆桌骑士的清单，然后对每个骑士进行了 DNS 查询，才能找到最终的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOEhfvBBMSFNEVwu8j3C9NLoqHduOLKgCZqbzd7lckBZz2VIgBZpTNibSTfhPSKpAdSylRpUf0ceaA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/5ria5WVLahGj8W7vu6J2jzTGqRtEaL6ib9CDzENq8PCEZADfU3JXsmibNacJhY7rooNoYIpCsUytNS0k4UcSsnRfw/640?wx_fmt=png)

先把所有圆桌骑士都统计好... 我这边试了很久都执行不下去...

我这里执行不下去了.... 我放着以后做把... 听说不止 7 个 flag... 好像有 11 个 flag？？？

虽然只拿了六个 flag.... 还是得继续努力加油，脑补把！！！

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定

要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。  

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