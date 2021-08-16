> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/JpzfWlB1_kB-8uak6xN7vg)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=other)

  

  

大家好，这里是 **大余安全** 的第 **123** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/sGWlDp8sFCl67vCmcZr3JtQP0jB8suQiaKaKCVYPOezloiaicS8xMkAriaAQd3dTOPXicBTVStlX66kEffEWJOiczUTA/640?wx_fmt=other)

靶机地址：https://www.hackthebox.eu/home/machines/profile/126

靶机难度：中级（4.8/10）

靶机发布日期：2018 年 7 月 21 日

靶机描述：

Aragog is not overly challenging, however it touches on several common real-world vulnerabilities, techniques and misconfigurations.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/o62ddIpxjBd0kv6p3zb6uf1GiaCo9PiaF12hWQQSurxFPuVIDtsNTgUpjjvmib7GxKXNePVMAwJfzuib52MWoORPYg/640?wx_fmt=other)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/Clq0o4fE5u6X5A1maTmqcvtEibdrsDO41kZPibRCHsX3Koj69GFK2qOyPwdcrgcDkHklrdJzBCiaQPuMVe11oSYHA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTpab7hxqQPkicCfkRoT3JqibHrVSgHXGnuMHuZK4Q2yrSPsuA5XsWVfBAb1icS98niaQKgh8bJDZs4g/640?wx_fmt=png)  

可以看到靶机的 IP 是 10.10.10.78....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTpab7hxqQPkicCfkRoT3Jq5ibA6DPAyTkQCjKicACC40So8sOByn8XXyFMHZVqUjoqUuibKxR19UpRA/640?wx_fmt=png)

Nmap 发现了 vsftpd（已启用匿名登录），并开启了 OpenSSH 和 Apache 服务器....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTpab7hxqQPkicCfkRoT3Jq4IhhS9087rNs47PGuJGZ5yHalODjuIMDMJ9z0iczrMgVgLAVTcQNc6A/640?wx_fmt=png)

直接匿名登录 ftp... 并发现了 test.txt 文件，下载...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTpab7hxqQPkicCfkRoT3JqicohacDKvvysPe5jlSr6MDHK6gYcj1YqokbjibCMNLGgs5hMgNUdlRTw/640?wx_fmt=png)

在内部，我们看到了一些 XML，估计要利用注入 sql 或者 XXS 等攻击行为...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTpab7hxqQPkicCfkRoT3JqIFHl0IpW3lgwcwiaXsnbdDSIC5oT5zQQgS1X2QAGxA2Gel7SWdT0RhA/640?wx_fmt=png)web 是个 apache2 页面..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTpab7hxqQPkicCfkRoT3Jq0oiac2uGAgkTYAaqtm1KrjqUhXicqibf4pxH9w6Jsd9ibjDKicpcpZGo4Eg/640?wx_fmt=png)

直接目录爆破仅发现了 hosts.php 页面....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTpab7hxqQPkicCfkRoT3JqTxemMJg6h5ESGz0HxDq4jzFaJGX6jSmXC11WLqXoOpU5LckRiczYhOQ/640?wx_fmt=png)

看到不完整的数字信息....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTpab7hxqQPkicCfkRoT3JqqmNuEvibgSAd0NPKdicphtEWddNsfCVia0vKx37P4xeVEhCY1Lnzl1eng/640?wx_fmt=png)

通过前面 XML 信息，可以将 XML 数据发布到页面并获得一些输出

是否可以利用 XML 外部实体（XXE）攻击起作用？并注入一些 XML 以在系统上读取文件？试试

首先，将 XML 文件修改为以下内容，以测试是否可以读取 / etc/passwd...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTpab7hxqQPkicCfkRoT3JqNjKg5ZXjO3f65yB1R23GeZf01U239oDKCSdoVXaicDr11fjfz9S2FmQ/640?wx_fmt=png)

```
https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20Injection
```

这里通过 github 找到了 XXE 攻击的利用方式....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTpab7hxqQPkicCfkRoT3JqrJwobmbFDYNZsrsLlVCKibqy41TibFgTfE9uiaFAe05ydN7glB3z7EJLA/640?wx_fmt=png)

果然，利用 xml 输入可以进行入站 XXE 攻击来读取文件信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTpab7hxqQPkicCfkRoT3JqibicDvYTZEQhQE92jc7M2lia40Gy4kwibEmwvshdGZsnrwzzSux2hBvm8Q/640?wx_fmt=png)

通过枚举，直接读取靶机的 id_rsa 信息，获得了密匙...（因为靶机 ssh 开启了服务肯定是 rsa 登录）

二、提权

![](https://mmbiz.qpic.cn/mmbiz_png/Clq0o4fE5u6X5A1maTmqcvtEibdrsDO41kZPibRCHsX3Koj69GFK2qOyPwdcrgcDkHklrdJzBCiaQPuMVe11oSYHA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTpab7hxqQPkicCfkRoT3JqJUgX0IjpVddXfib1saFZ69ia8DDpAVxl1xqUt6yrdZKfaVXceVKOIic3w/640?wx_fmt=png)

直接利用 rsa 成功登录，获得了 user_flag 信息....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTpab7hxqQPkicCfkRoT3JqKoLoicdMB97axnYz0RNbzw9Mt9baPmlD3YW5pbcD3nJGOic2AY3IHY0g/640?wx_fmt=png)

在 www/html 页面发现隐藏页面信息.... 很多内容....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTpab7hxqQPkicCfkRoT3Jq65ib2ibTQJia7vmRlHPnOJ5hsmClGSN14NWEibpNV6BmNo53yhEeBQKthg/640?wx_fmt=png)

直接访问发现存在问题，页面无法读取... 应该是域名问题...

直接将 aragog aragog.htb 添加到 hosts 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTpab7hxqQPkicCfkRoT3Jq35uuLD1LZy1O0hF5psnhcEKFpZtxlVLibnDIOcbkCXzm2aBeu51U2Sg/640?wx_fmt=png)

cliff 告诉我们两件事，他经常登录该页面，并且该站点也正在恢复.... 仔细检查

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTpab7hxqQPkicCfkRoT3JqhOwA4JfCb6I2ztiaK0JfF1csiaNgcbqMFPzkyIbicibibXkRzlpX82rquhw/640?wx_fmt=png)

我通过访问 admin.php 直接进入了登录页面，但是页面 url 跳转到了 wp-login.php 文件下...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTpab7hxqQPkicCfkRoT3JqziaYTcCx5pxIrhwibHic2Bqz59jPF8WbJ47aEOmdHMibfDF7kgjPfvaltQ/640?wx_fmt=png)

利用 pspy32 监听了靶机内所有进程情况，等待了 5~7 分钟，发现了一个规律，wp-login.php 为 UID = 1001 在调用，然后每一分钟准时调用一次....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTpab7hxqQPkicCfkRoT3Jq63mJ8xMeKka5ckNtGGeU1icC8psT3yQjxKkaSdqBia7RjxbJoha8Joiaw/640?wx_fmt=png)

```
https://stackoverflow.com/questions/3718307/php-script-to-log-the-raw-data-of-post
```

如何利用 wp-login.php 获取 admin-php 页面的登录密码？在 google 看到了这篇调用文章....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTpab7hxqQPkicCfkRoT3JqVrlx0yOHX3yXCHeEhxEYw0icDQKE0dsYnicLqnwjW7iaXOUTgNlpgnrRw/640?wx_fmt=png)

直接删除掉该文件，重新创建个，将文章方法添加入测试....

等待一分钟后，成功获得了 administrator 密码....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTpab7hxqQPkicCfkRoT3JqmiaxgGSpHOcfqTr7ticT46ywfCY67VDu0E0cibsDBnPQfZ8tBMLYLNwzQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/sGWlDp8sFCl67vCmcZr3JtQP0jB8suQiaKaKCVYPOezloiaicS8xMkAriaAQd3dTOPXicBTVStlX66kEffEWJOiczUTA/640?wx_fmt=png)

由于前面知道这是 UI=1001 在调用的，以为该密码是 cliff 用户的登录密码... 但是无权登录...

尝试 su_root 直接成功登录获得了 root 权限用户外壳....

成功获得了 root_flag 信息....

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台中级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/o62ddIpxjBd0kv6p3zb6uf1GiaCo9PiaF12hWQQSurxFPuVIDtsNTgUpjjvmib7GxKXNePVMAwJfzuib52MWoORPYg/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=other)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=other)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

随缘收徒中~~ **随缘收徒中~~** **随缘收徒中~~**

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)