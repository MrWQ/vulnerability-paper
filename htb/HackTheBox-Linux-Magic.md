> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/wRKU05-ce4bxfJ6HtqA7Mg)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **193** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_gif/ldWFh337rbjfApaRGicR1GGwHDCYPhsKZ9euLodKu0upoCBupGzffThUrZlyL2I0qu4OzmzGg3YQ4JPhJ2UZ18A/640?wx_fmt=gif)

靶机地址：https://www.hackthebox.eu/home/machines/profile/241

靶机难度：中级（4.6/10）

靶机发布日期：2020 年 8 月 22 日

靶机描述：

Magic has two common steps, a SQLI to bypass login, and a webshell upload with a double extension to bypass filtering. From there I can get a shell, and find creds in the database to switch to user. To get root, there’s a binary that calls popen without a full path, which makes it vulnerable to a path hijack attack. In Beyond Root, I’ll look at the Apache config that led to execution of a .php.png file, the PHP code that filtered uploads, and the source for the suid binary.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/ibQV91UPVPA0YraLBxG6SF7hBIMGETWZCPmdut5HSvsfqQz6CtfmOScRtJFM8gtn5LKRiav4DhT1Cxk6YPiaEHZvQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/dphnm0BKfwKLtib9vQ1APuIAKeJtunpQ9t0U2bFm604pdiagpiavfaicU0LSsYk60Ugh838nnFVzywH0z19gB2VMOQ/640?wx_fmt=gif)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/7phYCjicsxExcHT6Dnz0PPkUycARhia5vV64je93lrrZSxlz64jyGCuicicUC0jAZx4rsG4qsfMwymvib1zwhibQRdaw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMh3fzBfWBYvdbyU9Ug93g3Nhn2WRA2VcMrrYzLz4u6vYzhXJFEj7jaj6iaGdhySibdAHnsLWaySv5w/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.185...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMh3fzBfWBYvdbyU9Ug93g34sqpQLklAYPlialoSibrxYVxjRbE8hcVt0icnaeDq1U3xia9MSMPnn8zpQ/640?wx_fmt=png)

我这里利用 Masscan 快速的扫描出了 22，80 端口，在利用 nmap 详细的扫描了这些端口情况...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMh3fzBfWBYvdbyU9Ug93g3eBm0xZfFh9h7KuK4u1y122xEfia3o0NGojiaU5FThCL0YSm7ULzM9rLg/640?wx_fmt=png)

web 页面包含了很多图片，左下角点击 login 进入了登录页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMh3fzBfWBYvdbyU9Ug93g3B8Mfqpj0XAwNta24ibpECwTmgcehOv6GmmIRGAJJQv7TmLOK097feOw/640?wx_fmt=png)

简单的 sql 注入... 成功登录...（

这里不多说了，遇到几十次了... 一模一样的注入）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMh3fzBfWBYvdbyU9Ug93g3ZibEXM3sZ67F3OAqXcmMDQhx0smhKo9yHuOdmY4WicI6WGr6oafSLXYA/640?wx_fmt=png)

登录后是文件上传页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMh3fzBfWBYvdbyU9Ug93g3pxYGI7lckuQfLjgd1ZKSiaPtZsTopYoaLtulf4QQXEDfNBfr6qYiclQg/640?wx_fmt=png)

点击 upload image 返回... 必须使文件具有与 jpg，jpeg 或 png 类型的文件才可上传...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMh3fzBfWBYvdbyU9Ug93g3zt1QyjNocsjBrqD900fD2MDInMWxFibUh8ehy3SX7WSpQw3cLO6ibNEw/640?wx_fmt=png)

```
exiftool -Comment='<?php system($_REQUEST['cmd']); ?>' sample.png
https://medium.com/@sebnemK/find-flag-in-image-file-upload-c9bc4975f595
```

google 很多文章写了如何 webshell php png 方法...

随意在 kali 上搜索 png，然后随意利用一张图，注入 webshell 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMh3fzBfWBYvdbyU9Ug93g3mgbfL06mYzkgnwPCNX9GSF4vHNe4kia0ANZZFzLkCFeiaVZ56elcgEPw/640?wx_fmt=png)

成功上传...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMh3fzBfWBYvdbyU9Ug93g3YFjryib0KYkKz5gFvf8NibekhFsH6m3btOv5TTptwDpvz8eh0Nklm35A/640?wx_fmt=png)

发现还是判定此上传文件为 image... 我将 png 改为 php.png 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMh3fzBfWBYvdbyU9Ug93g3UWGHxr9tfwL8QAGIXL1rkqcOALCoDvBh7gaeZcnq0Z4xGmKYpyybrA/640?wx_fmt=png)

成功获得了 shell 特权... 开始提权即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMh3fzBfWBYvdbyU9Ug93g3D1IV4hj2CosXSPLibWvoyfzFTWN681u5gfYHchfDIRUwbfDA0C81weA/640?wx_fmt=png)

很多 shell，随意提... 获得了 www 低权外壳...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMh3fzBfWBYvdbyU9Ug93g3DQuibx2dZ4WKLSm84XAqHLzGdcLBKQibBoHyGWK1O2U05mVSrXyP6qSw/640?wx_fmt=png)

枚举发现存在 db 数据库信息... 查看 db.php5 获得了 theseus 数据库用户账号密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMh3fzBfWBYvdbyU9Ug93g3c5ommGibGTcL8IKs8icJX36PWD8ypTIocRpQkgGOKsA1ek8IialzPylJg/640?wx_fmt=png)

直接利用刚获得的用户密码，枚举数据库信息... 直接获得了 admin 用户密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMh3fzBfWBYvdbyU9Ug93g3HPgKq12eLMaLYGdeDPZl6m9VZoOQ4l8fr7wnQk98oKCCeU2t50oG9g/640?wx_fmt=png)

尝试成功登录 theseus 用户界面... 并获得了 user_flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMh3fzBfWBYvdbyU9Ug93g3uia3yia2ibYdE9LWfVrGuROITVSB3icLtdp85XpibX4ZJjdK0J36UUhpatg/640?wx_fmt=png)

为了方便利用 ssh 登录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMh3fzBfWBYvdbyU9Ug93g3ahBZvBsqYBrbuPFw50tOOJMibfU7LYP43cbV3pnibyuddEtfCmGhQ6gQ/640?wx_fmt=png)

上传 LinEnum.sh 枚举信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMh3fzBfWBYvdbyU9Ug93g3HuAuDk7XgOfbWKlBYXSOPM7icvst1DcCswKD0iclTClkuicvYHWmo9pVQ/640?wx_fmt=png)

/bin/sysinfo -x 权限很可疑... 查看下...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMh3fzBfWBYvdbyU9Ug93g3jsSqOEXjNrQWC8Wo9fZibqcyu61KgcZeU3WmThHutxUauia1yv1X6LVQ/640?wx_fmt=png)

是一个 64 位的 ELF...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMh3fzBfWBYvdbyU9Ug93g3eR9hvrjAapDomQcQxhuDGQU1MfD3vk9IPSlk4ia0wBDxibYYGXqBRUww/640?wx_fmt=png)

strings 枚举发现二进制程序可利用 lshw，fdisk，cat 和 free 命令，而无需他们的绝对路径... 那这里提权的方法很多了，快速获得 root，或者提权都行...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMh3fzBfWBYvdbyU9Ug93g3rbxUXrZhT3e09jJkzmZYbOGwupBiaUFy76yYrUnJ8cAbuBNuQGJuYOg/640?wx_fmt=png)

创建 shell... 简单操作了... 赋权

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMh3fzBfWBYvdbyU9Ug93g3iaK2s4bc5vtxETqQFar3JuvkLm4lckSUiazF1HPTq6gkALLcAznDlhgg/640?wx_fmt=png)

执行 sysinfo 后，执行了该 shell，这里尝试第二次需要改 fdisk 名称 shell...

![](https://mmbiz.qpic.cn/mmbiz_gif/ldWFh337rbjfApaRGicR1GGwHDCYPhsKZ9euLodKu0upoCBupGzffThUrZlyL2I0qu4OzmzGg3YQ4JPhJ2UZ18A/640?wx_fmt=gif)

成功获得了 root 权限和 root_flag 信息....

该靶机很适合入门的人尝试.... 非常好的入门靶机!

sql 注入 -- 文件上传 -- 注入 shell 利用程序漏洞提权...

这种靶机遇到太多了...

加油！！

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台中级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

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