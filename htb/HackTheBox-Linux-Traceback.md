> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/C0nT-T_9l_jcI_E-wnC4MQ)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **178** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/ZREXjsC2nJKx0JHGsC5rFpiaQjsk60OEibhDJ4vLJgUl7n0nCnGoCmtcS6TWpecmKRlG5IwNnyjGHau71NkOwyTw/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/233

靶机难度：初级（4.0/10）

靶机发布日期：2020 年 3 月 23 日

靶机描述：

Traceback is an easy difficulty machine that features an Apache web server. A PHP web shell uploaded by a hacker is accessible and can be used to gain command execution in the context of the webadmin user. This user has the privilege to run a tool called luvit , which executes Lua code as the sysadmin user. Finally, the Sysadmin user has write permissions to the update-motd file. This file is run as root every time someone connects to the machine through SSH. This is used to escalate privileges to root.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/9h3lBeicPhRCbL55vicQK1Qj4FqoebibNv9EhH20XgIRH3RZicuNRbKdZqdDr5c2JMCyJWH8zicp8cJH9gJCp0Zy8Qg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/ZrqZaezpWclmao6Vp2LSrkuD0NTO9TiclXmiaWSh0NibqeKL1xJ4qBoJbPODkzJ3g0OvTdUGll3Otz9978tOYib32Q/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMKT0U1dZviaK7LtKulDiaQA8WXyLU25EvicxJXv7sASuKia0so8BZNYonbcLXicdf7xatiaBBrUdIPxpTg/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.181...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMKT0U1dZviaK7LtKulDiaQA8yqyYgicFRqNQZSKvHKuAyAaqoMASrQRZjhq4sCBoVBo7dydHS27MjcQ/640?wx_fmt=png)

我这里利用 Masscan 快速的扫描出了 22，80 端口，在利用 nmap 详细的扫描了这些端口情况...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMKT0U1dZviaK7LtKulDiaQA8aPuxaNialPXComNMmeK3GR1Am0wPyLGjxbXQf5NdjtgEYjZFICibb0bQ/640?wx_fmt=png)

访问页面发现该网站已被黑客入侵，并且该消息指向存在后门...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMKT0U1dZviaK7LtKulDiaQA87bkpaA6KO2OuFNNpV9NicY23KvMz7ef9iaibqQhYJj9GFmWOU2mrMmeKQ/640?wx_fmt=png)

查看页面的前端源码可以看到以下注释，黑客似乎在网站上留下了 shell 外壳?

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMKT0U1dZviaK7LtKulDiaQA82HkcTPcCSm5mYgQcC8KUAXs1LP1SrfZPoYmj4wft1f4b8Pnr9ujx7g/640?wx_fmt=png)

直接上 google，发现了 github 上有存在的目录情况... 这里开局尝试用 gobuster 爆破未发现存在目录信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMKT0U1dZviaK7LtKulDiaQA82v7EGDwc6OytBEMbF1VyxYeOwAkBb7CweagYqjwlHql1yIotvghODg/640?wx_fmt=png)

把该文件全部尝试了，发现 smevk.php 是个登录页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMKT0U1dZviaK7LtKulDiaQA8aArRJjndOs1xm7wRNOhdnWcQdcO7LCazBl7e9wInEXOAOJYatOWZoQ/640?wx_fmt=png)

可看到该登录页面情况...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMKT0U1dZviaK7LtKulDiaQA8O9WuCwr4FDeyPctKKq5ibopmQ35DBcgX2ULmrsRcoJZjIVyiauJTrwrA/640?wx_fmt=png)

```
admin/admin
```

简单使用默认密码登录进入了页面...

该页面功能就是外壳功能，非常多的，文件上传呀，写入 shell 都可以，随意提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMKT0U1dZviaK7LtKulDiaQA8YXOnpF9n7ibvmGRpdEeyKHzkBias0RpPZ2zTsD2aicdExicSDkb5ZaNAjw/640?wx_fmt=png)

这里直接上传 shell 也可以，我尝试了几种方法都可行...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMKT0U1dZviaK7LtKulDiaQA8H7L3s6jAdFIibN2oQoyDOw3gDxoCdIb6eChuY6u0tGGhHYN8IEovWibg/640?wx_fmt=png)

最后直接找到 home 下的 webadmin 目录后，把 authorized_keys 写入到了 ssh 中....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMKT0U1dZviaK7LtKulDiaQA84zy3PJ3RzG1HWyU9Ecrm0kgSt2mEcR1hQiaCJjJEdAqn3VeefYUpZ4w/640?wx_fmt=png)

登录后 web 用户无法获得 user_flag 信息，需要提到 sysadmin...

sudo-l 发现了 luvit 程序提权... 这是最常见的提权了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMKT0U1dZviaK7LtKulDiaQA8HmaQP2Cs6ArZiaw3tZribIC7ejxxict1SwUYL3WpzEkvjMdYlm9bEuBMg/640?wx_fmt=png)

可看到 sudo 执行是 repl

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMKT0U1dZviaK7LtKulDiaQA8fibRO8rrmPXoLNKQuPoAhE2xYEgSf06yTcW9nUCYNP5bbgiawoIz27sA/640?wx_fmt=png)

```
https://gtfobins.github.io/gtfobins/lua/
```

 google 轻松找到了提权方法...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMKT0U1dZviaK7LtKulDiaQA8JTXIXdEG2knmt5dP4eic5BsIBDe33a058ywGRCk5iacwaBxMBf3VrlibA/640?wx_fmt=png)

写入 shell，然后 sudo luvit 执行该 shell 即可...

获得了 sysadmin，并读取 user_flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMKT0U1dZviaK7LtKulDiaQA8c3y8nZII0hAwWBCAF9jf9MBn86Xp56UohqECZj46NqOTODBicBpvXFg/640?wx_fmt=png)

直接上传 pspy32 进行进程监测...

发现 motd.d 显示每 30 秒在服务器上运行以下命令....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMKT0U1dZviaK7LtKulDiaQA80ruOFOS7Hu15pOicMbGliare2OuLBxo3SK9E8l7fJiatj0eicW92dZPvwg/640?wx_fmt=png)

该问题也是常见的了，记得以前遇到过，不多解释了，google 也很多解释...

这里截图是写入 00-header 文件信息后，会在登录 webadmin 时刻显示需要的信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMKT0U1dZviaK7LtKulDiaQA8KfOwJkv0hzW08KQhmas8NzTZnKZ0NSuXA9bIrZyKmoUZk1Uf1ZRtXQ/640?wx_fmt=png)

写入 root_flag 信息和 key 看看....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMKT0U1dZviaK7LtKulDiaQA8MYJbquRjjiaG77Wq9dTpy0n7Oq9ocuV309I11XknMTTJ2unKD2xeQJA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/ZREXjsC2nJKx0JHGsC5rFpiaQjsk60OEibhDJ4vLJgUl7n0nCnGoCmtcS6TWpecmKRlG5IwNnyjGHau71NkOwyTw/640?wx_fmt=png)

保存后登录 webadmin，成功获得了 root_flag 信息... 继续进一步获得 root 权限很简单了...

这里也可以利用 00-header 植入或者读取... 随意操作...

后面的靶机我就不多解释一些简单的原理了，快速过了...

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台初级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/9h3lBeicPhRCbL55vicQK1Qj4FqoebibNv9EhH20XgIRH3RZicuNRbKdZqdDr5c2JMCyJWH8zicp8cJH9gJCp0Zy8Qg/640?wx_fmt=png)

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