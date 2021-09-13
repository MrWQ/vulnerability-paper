> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/NqQ6FnieDGaYYv7Af9xlXA)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **150** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_gif/vlvamJrTPeG5nET2PXlWHKQ3vLE8qBnoicLE2Rob1c9IwHp17PmKusuaFIP9exOic3G6SRppL4GWWhjhyJnXQg5A/640?wx_fmt=gif)

靶机地址：https://www.hackthebox.eu/home/machines/profile/173

靶机难度：初级（4.7/10）

靶机发布日期：2019 年 5 月 13 日

靶机描述：

FriendZone is an easy difficulty Linux box which needs fair amount enumeration. By doing a zone transfer vhosts are discovered. There are open shares on samba which provides credentials for an admin panel. From there, an LFI is found which is leveraged to get RCE. A cron is found running which uses a writable module, making it vulnerable to hijacking.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/C4gxftskfhPHbgia3ShTwT8zUkJK7U8wCNeRmXOiac3SZ7W7uxhJgtdPP455e48IGjk8jcgkTcg9outvozseH3Wg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/XrTibiasJJtTGCeNnvsRZqfmYBstz1lHuPA72aRQYQiaOKfQicLkWLWJ5ePZY21XO6W37XzXKoeyPYz4ZJXqEXNZFw/640?wx_fmt=gif)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsK4hzZgEkssHX8kqmIYz7O59vv3qGWWGuMTias9TW2a2pCnU7PXMWaFrUbFfcuUgztPlyGP5Agyg/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.123...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsK4hzZgEkssHX8kqmIYz75M8MqktcquwT8BCyXD82TgiazMHicrNCd9UCKJia8mROWC9do64K0aCicw/640?wx_fmt=png)

可看到开放了一些端口，ftp 不允许匿名登陆，443 端口和 445 端口也开放着，要利用 smb 了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsK4hzZgEkssHX8kqmIYz7mqpnCNOfvR9QjN6NqugRZG1h8r0dDYAQ9CaUjzCh5lzibekpEPtpRvw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsK4hzZgEkssHX8kqmIYz7Ljaib8wkda0syaVS1lTs9R3UD2oibIKiaLHicdLo4UYzXrv3vSIh8YKCNQ/640?wx_fmt=png)

访问页面发现了域名信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsK4hzZgEkssHX8kqmIYz7Dj7bQ1ic6P9I7z6ZtHHKZ5xXVbPf1j8P6gELvUZDgicQSVapOGKUBr8g/640?wx_fmt=png)

枚举域名信息，获得了另外三个 DNS 域名... 都添加到 hosts 中即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsK4hzZgEkssHX8kqmIYz7jUmy7HITQRA1sh2EibfursIgoBPVed22iaM1u9CX9FDeolBdYWOQTqkQ/640?wx_fmt=png)

enum4linux 枚举发现了 smb 中存在得用户和目录情况...

只有 general 和 devolopment 可正常进入...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsK4hzZgEkssHX8kqmIYz7WML9If2TEKTzQOMKHC2zAu3gj6zTgR2geicicsII2E7peYs8ibYGL3hicQ/640?wx_fmt=png)

首先查看了 general 发现了 creds.txt 文件... 获得了用户名密码...

查看 developmengt 是空目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsK4hzZgEkssHX8kqmIYz76HuBadkhNDMrb1Lmt5wUU6MbRVsjLLQUZVJhtLWKaeyxsLnV0EO3HA/640?wx_fmt=png)

访问枚举到的域名，这是表单登陆页面，利用前面 smb 获得的密码登陆即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsK4hzZgEkssHX8kqmIYz7Zj4PV4W6d4oe1byHKibXa0pNgmTWLtwHY0950xGOlyLWbYjwsGsia7RQ/640?wx_fmt=png)

登录后，要求去 dashboard.php 页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsK4hzZgEkssHX8kqmIYz7icJOVeCVDzvLyiaibNCVF8ibPgN1dtscO2Wvel5DCkyCQzIvQYNuSRUjrw/640?wx_fmt=png)

仪表板页面似乎是处理图像的某些应用程序，但是除了将图像名称作为参数和页面名称之外，还提示了 image_id=a.jpg&pagename=...

很熟悉，应该是 url 的后缀，可能存在 LFI 利用...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsK4hzZgEkssHX8kqmIYz7iaQ3MDsyxqxgGicZlre3TibbfZWiaXyRFQWmQDYhaibgGf1GFe3NwndOK6g/640?wx_fmt=png)

我尝试在后面 image_id=a.jpg&pagename = 添加访问，页面报错了... 脚本还在测试中，可存在 php 文件等信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsK4hzZgEkssHX8kqmIYz742O5bMiatLovt50gAVdNo3sNibBs2GVeVNOIzZ6iaIkQgiaWK8thycttqQ/640?wx_fmt=png)

配合 nmap 扫描，这里怀疑 image_id=a.jpg&pagename = 和 smb 的 development 有关联...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsK4hzZgEkssHX8kqmIYz77zic9K1eDbeaZ6vecvtYCOndkXHUUJzvh7OBM8se9vkN2bEib0AuFjHA/640?wx_fmt=png)

```
https://administrator1.friendzone.red/dashboard.php?image_id=a.jpg&pagename=../../../../../../../../etc/Development/php-reverse-shell
```

经过测试，存在 PHP 路径截断利用...

通过上传简单 shell 到 smb_development 中，然后在页面通过 LFI 利用...

获得了反向外壳...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsK4hzZgEkssHX8kqmIYz7pibqAicZibQc94kTVKUkaMFwcmjOOAX2bET40OYIDUiaqU4icZtDckp4jWw/640?wx_fmt=png)

获得了 www 低权外壳，读取到了 user_flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsK4hzZgEkssHX8kqmIYz7bpJicpAXLKE5t9jDazT8Bd9g12iaNmSSka9vyIhNSricDN3KKnEuic5Vlw/640?wx_fmt=png)

上传 pspy32 挂着枚举时，发现 reporter.py 文件每两分钟执行一次...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsK4hzZgEkssHX8kqmIYz7GgmVwX85U3EFwVDleXXusnvjm3a508KzibicTY3MTOcib13REDxgC0TrA/640?wx_fmt=png)

检查该脚本，python2 运行的脚本，脚本中提示在导入 os 库....import os

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsK4hzZgEkssHX8kqmIYz7w7Cial1S9tvyxU6SnFC6tN11DbC1gqh6whSo4blM4syXXbiaMqP0ekLw/640?wx_fmt=png)

LinEnum 枚举也发现了该库的权限，以 root 执行着...

www 权限的外壳还是不能修改该内容....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsK4hzZgEkssHX8kqmIYz7PTSrFMPfsRzQubJs0NgX81ddbxYz6CZdLPQJTibJq06pvKsoCiboDvsg/640?wx_fmt=png)

继续枚举，发现了 friend 用户的密码信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMsK4hzZgEkssHX8kqmIYz74VSen4icomLJJCcsd8ZVktUb0tCqcLZgxHWOrlvZFLYkyrdqllGkukg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/icYFMPSTAVGsOwJoPKxictMlC2FumZZOA0zX1Xshuq1pPERMVUJibHgX4YuCjGFOGq6FCSPVeJCxUedQ5hzeAMYhA/640?wx_fmt=png)

通过 su 提升到 friend 用户后，简单的写入和赋予权限，获得了 root 权限，并获得了 root_flag 信息...

简单的一台靶机，smb 和 web_LFI 漏洞利用，脚本固定执行进程提权等等...

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台初级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_gif/Lg7ia5ZzL0MGorL3epErA3EvFsgZptTXt067VWjjPcQj8JKymne9dNxObiaSth48rEickBn9xRSOibEHCX9NLPaAlQ/640?wx_fmt=gif)

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