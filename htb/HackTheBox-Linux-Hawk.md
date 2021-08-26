> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/HLtQUuJ3VNw32EF8hieSIQ)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **133** 篇文章，本公众号会每日分享攻防渗透技术给大家。

靶机地址：https://www.hackthebox.eu/home/machines/profile/146

靶机难度：中级（4.2/10）

靶机发布日期：2018 年 11 月 25 日

靶机描述：

Hawk is a medium to hard difficulty machine, which provides excellent practice in pentesting Drupal. The exploitable H2 DBMS installation is also realistic as web-based SQL consoles (RavenDB etc.) are found in many environments. The OpenSSL decryption challenge increases the difficulty of this machine.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/hZ9Y6npXb7RbuQKlbYoTStRYAbKyTqu3fX2nmkd8192YhqJKPLKiac70GiaBNOdic88Ggwcia32qIUKUVwBPlQUIEA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/3CSGsOUQKfsq2MZPDdCbRx4QOq5Hu6gwrOCquO8aT36jQ9E11LOX3TlAkU4FMhGlA2GtyiaXia4DpyEf9A6cZHXg/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/CFzCpw2dZa6XK6W3JRCld4jmp0GibCWLXUqvXCSUQzVI4ROVn3Quu5KWKhPcaUMe5MicicTrXO0YGPLY2OyXoiaeEA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNzHSPBGCdw1e2PcOS8DhXRUzTOicphVxGVaNGcXz1F7mDNPCvyr4cWdduu820BeTEPuhiam1qV716A/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.102..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNzHSPBGCdw1e2PcOS8DhXRvzoBPmAE6nN82L7hkqgtZsZgRjUShib9NF1ianU3l0yXYH3okgUD83IQ/640?wx_fmt=png)

Nmap 发现 FTP 可以匿名访问，开放了 ssh，80 端口的 apache 服务，8082 端口上提供了 H2 数据库控制台...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNzHSPBGCdw1e2PcOS8DhXRiaViczZbkwlMKVyyEQHzr3tLorSyq7qBpibFz2getFicZAIsWpqdXRdBSQ/640?wx_fmt=png)

登陆 FTP 匿名访问，发现了隐藏文件.... 下载

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNzHSPBGCdw1e2PcOS8DhXRL9f7NzoRpmQM9p1vkcBticdpl59O3icfP96qnrOPrIUyaVsVlBcSvVAQ/640?wx_fmt=png)

这是 base64 值...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNzHSPBGCdw1e2PcOS8DhXRW5g9IgQBfdRgQrfFSNUc1icZq1rsKPPb932l310fstKMvI9QzDTJTJA/640?wx_fmt=png)

```
base64 -d drupal.txt > drupal_decoded.txt.enc
openssl aes-256-cbc -d -in drupal_decoded.txt.enc -out drupal1.txt -k friends
openssl enc -d -aes256 -in drupal_decoded.txt.enc -k friends
```

这里我利用 base64 转换后，file 发现是 openssl...

需要利用 bruteforce-salted-openssl 工具进行爆破...

记得该工具默认使用 AES-256-CBC... 成功爆破获得了密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNzHSPBGCdw1e2PcOS8DhXRuMEXVsUBez83WnqEWI81bOOFaYg7Gichkbia1PiahVVrxMqkUaEv12h0w/640?wx_fmt=png)

web 页面... 框架 drupal CMS

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNzHSPBGCdw1e2PcOS8DhXRVyNWk1SDibgjZnBBibtmLIlMOKkfLd0clyryXlEuzbBHuQooZH8ib8jZA/640?wx_fmt=png)

利用获得了密码成功登陆... 这里需要进入 modules 板块中开启 php filter 模块

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNzHSPBGCdw1e2PcOS8DhXR81yfb0O2RVaGdMdkvz4ly5fSnYmibCfCvJ6AX0jkcYDEa4ot5QOsCCQ/640?wx_fmt=png)

开启 php filter 模块，打勾启用...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNzHSPBGCdw1e2PcOS8DhXREQic9d9D8OE9A38u0b2F4ZiartIibypDrUXhE7YlbHCSGh4icrrW65RdPg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNzHSPBGCdw1e2PcOS8DhXRTh6RZaDWpukqCgHL7C3hgPicGVRJKpC357Q7cED9IibEBKOlSJiaMAv7w/640?wx_fmt=png)

直接利用简单的 shell 提权即可... 选择刚启用的 PHP code

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNzHSPBGCdw1e2PcOS8DhXRWibYfQc6nS8lEw65Rfqr5f09XNOdFrEKQv9PjVMxVNTYNjXCJra0xFw/640?wx_fmt=png)

成功获得了反向外壳...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNzHSPBGCdw1e2PcOS8DhXR608o0TLyL5YeDX1wgEBrY7K6ibNBPoHXNP0h1RAunDcLEA4MI17haCw/640?wx_fmt=png)

枚举了一段时间，在目录底层发现了 ssh 登陆的密码.... 这里枚举需要数据库知识，不然也是大海捞针

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNzHSPBGCdw1e2PcOS8DhXRJibGIS7rvZB9EoHSuTjzMkIclhJicibLjSL67STVJOlECRHKXk9fWawGg/640?wx_fmt=png)

利用密码登陆 ssh，获得了 user_flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNzHSPBGCdw1e2PcOS8DhXRFwFxWE9Au1G4sAoicRsaSRkb7ico9VwzV1ribIAzrEFibMDEaUJ148JSuQ/640?wx_fmt=png)

和 nmap 枚举信息一致，开放了 8082，这是前面 nmap 就发现的 H2...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNzHSPBGCdw1e2PcOS8DhXRIYv96JfwUPZUoJDiasQyZ0CclW2oiaCnw3UQM6PicB06Q7kgUwacGY9tg/640?wx_fmt=png)

测试访问，发现远程连接已禁用了，需要 ssh 流量做个隧道，在本地链接即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNzHSPBGCdw1e2PcOS8DhXRMia0Lok5yFzfwUOQicRBibhPYVJ0CiaEkW2icr2NGuSibTkAhsLD9ePRYXhQ/640?wx_fmt=png)

```
ssh -L 8080:127.0.0.1:8082 daniel@10.10.10.102
```

成功转发...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNzHSPBGCdw1e2PcOS8DhXRSQLUFSSYk7awFThNlhgX79tgmszb82FqUT5BEvbpyF6QzCxznEnSAQ/640?wx_fmt=png)

直接在本地访问... 成功进入

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNzHSPBGCdw1e2PcOS8DhXRc54hnsIuIcOUowC6z3c4znzZAL0xfcRPNNiadH4GkIFffa80EyLss9w/640?wx_fmt=png)

将 test 改为 root 即可进入 root 数据库中...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNzHSPBGCdw1e2PcOS8DhXRdopvXG09hSbbtUzbxuqJSKug9I8iawBVrSYoiaTOTwx4rY0pcovGv1Qg/640?wx_fmt=png)

直接可以访问控制台了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNzHSPBGCdw1e2PcOS8DhXRaXnuOj8eNnvtR5mPpgtRHvotrWEDXnxh82aibbj6VSmu9UZXhlEjwxA/640?wx_fmt=png)

这里搜索下 google Abusing H2 Database ALIAS 很多例子都会教如何在 H2 上获得 shell...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNzHSPBGCdw1e2PcOS8DhXRd7ovnRVHveGlyz1xyHRAibBsUt9Vh0XCPzlvnsIeHLUey2YSFicyxbicw/640?wx_fmt=png)

```
CREATE ALIAS SHELLEXEC AS $$ String shellexec(String cmd) throws java.io.IOException { java.util.Scanner s = new java.util.Scanner(Runtime.getRuntime().exec(cmd).getInputStream()).useDelimiter("\\A"); return s.hasNext() ? s.next() : "";  }$$;
```

意思就是创建了一个执行 Java 代码函数...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNzHSPBGCdw1e2PcOS8DhXRWiaNkLslBlNRgJukKKbic3GC6ichj9HIiaqtHPA2Gvqgyj8yjngF5w57eA/640?wx_fmt=png)

然后通过调用创建的函数来执行系统命令，成功查看了 ID...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNzHSPBGCdw1e2PcOS8DhXR5VvibS1JMOsibcUlMhS1NlqTBsD3CQPQY14cSZEKVgRxs8TUHO0wibukA/640?wx_fmt=png)

那就继续利用调用的函数，直接上传 shell，提权即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNzHSPBGCdw1e2PcOS8DhXRvXZ3N7gnFknENfvQNZ9XzltAJWfAI0woCt4a0eaqeAr5Gqrf8WN9eg/640?wx_fmt=png)

成功上传...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNzHSPBGCdw1e2PcOS8DhXRPTL14Y37VC60CFeJ7N7d5kHFvc80kmibINByicQ14K3ZmUSbkWu5jXicw/640?wx_fmt=png)

赋权

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNzHSPBGCdw1e2PcOS8DhXRK0cEzLvfMc4ibj9CgpYpMSc1Xc0P4j9KhJianjJ4pOyKIWQVVO7u7pLQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/sGWlDp8sFCl67vCmcZr3JtQP0jB8suQiaKaKCVYPOezloiaicS8xMkAriaAQd3dTOPXicBTVStlX66kEffEWJOiczUTA/640?wx_fmt=png)

成功获得了 root 权限外壳，并获得了 root_flag 信息....

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台中级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/o62ddIpxjBd0kv6p3zb6uf1GiaCo9PiaF12hWQQSurxFPuVIDtsNTgUpjjvmib7GxKXNePVMAwJfzuib52MWoORPYg/640?wx_fmt=png)

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