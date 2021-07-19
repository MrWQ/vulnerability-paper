> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/hzoELeD1eNLmwVbMN2jFZw)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **97** 篇文章，本公众号会每日分享攻防渗透技术给大家。

靶机地址：https://www.hackthebox.eu/home/machines/profile/4

靶机难度：初级（3.7/10）

靶机发布日期：2017 年 10 月 16 日

靶机描述：

Tenten is a medium difficulty machine that requires some outside-the-box/CTF-style thinking to complete. It demonstrates the severity of using outdated Wordpress plugins, which is a major attack vector that exists in real life.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/U7IQUFmZG1bqzIhV5HZKbZgWPxEY5MWaGSyMqlAesy0wZeEHzCNMqpzBefwQjV0iaz2Gq8w8d1v4UsOdgJK0a6Q/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/a4ItSXeSn34KK6iaF0mInaXAJY0DKkhF28NjydHiauDm4iauOatMfIFxgh9L8ic23wb77htyqURBGSWK3yib68EZUQQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPSfLdicufnaoLTaicoZY8N9vPrjwsJbrzXYR8w4bwPS8Sxj3YfLuAKVjeGnibjsng8TicFeicQ549bsTQ/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.10....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPSfLdicufnaoLTaicoZY8N9vEZjPdw4WFtYYtXYiciaPTmgmO30oaKPMS5CGJBWtYWjjWMAy9G3dxgRg/640?wx_fmt=png)

Nmap 发现了 OpenSSH 和 Apache 服务器上运行的 Wordpress 博客...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPSfLdicufnaoLTaicoZY8N9vXOu5lmBmfsLqTkUGqGT8YopJAYPoqkzTicpAcs5iaLtPiaBL3yKnZqPsQ/640?wx_fmt=png)

登录进来发现... 又是非常熟悉的 wordpress 博客... 利用 wpscan 枚举即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPSfLdicufnaoLTaicoZY8N9viaF4Cyfx4QFfdBicAulAzribGEVxVibVqwP6yIgYbSXEmmX66qyp3alKpg/640?wx_fmt=png)

```
wpscan --url http://10.10.10.10/ --enumerate u vp
```

用以上命令可以扫描出用户名，可看到发现了 takis 用户信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPSfLdicufnaoLTaicoZY8N9vIwIExGaWWS8436QdADFuCsdt9RJuwufGyVScmSOibYhGucGiaEkicIGGw/640?wx_fmt=png)

登陆进来后往下翻有立即申请图标，进入发现页面信息 url 存在 ID？修改 ID 发现有各类的内容信息，有的可以上传文件，有的可以注册账号等等... 都存在各自不同的职位职称...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPSfLdicufnaoLTaicoZY8N9vsiahdTsDcvcFeOaXvAWGEicrogcsLQXKK0vHduRb8ibIzQciaVaaub4m0A/640?wx_fmt=png)

```
for i in $(seq 1 20); do echo -n "$i: "; curl -s http://10.10.10.10/index.php/jobs/apply/$i/ | grep '<title>'; done
```

利用 curl 枚举了所有 ID 的信息... 发现了 hack.... 值得关注....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPSfLdicufnaoLTaicoZY8N9vQV1HBkZgloJicXbezsPSDTYqLTQSmoBGLXmaErtQuvPxxAQHu99RGow/640?wx_fmt=png)

需要继续枚举目录底层信息... 这里利用了

```
[cve-2015-6668](https://vagmour.eu/cve-2015-6668-cv-filename-disclosure-on-job-manager-wordpress-plugin/)
```

去获得底层信息地址...  

因为前面利用 bp 拦截检查过上传文件，无法上传 php 文件提权... 只能是 jpg、png 等图片... 搜索发现底层存在 jpg 信息..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPSfLdicufnaoLTaicoZY8N9vOKOrHDxJkib2oqC1aYIxnGro9s2cMzUDWMuKIt5AIxvzw3OhDymib0VA/640?wx_fmt=png)

下载下来...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPSfLdicufnaoLTaicoZY8N9vMMKWyeyRicS38Ogj0a5QkFqGYBuRLVcADeduick1TpKEkuicZjwzjFicoA/640?wx_fmt=png)

```
steghide extract -sf HackerAccessGranted.jpg
```

通过 string 等工具分析... 视乎存在 hash 值...

利用 steghide 提取出了图片的 id_rsa 值信息... 这里的信息很久以前就演示过了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPSfLdicufnaoLTaicoZY8N9vInuyBBH3rjzUGlnQWP0wGuAUJVXscJvKVCmS6kNVT0fMzibXLQSetbQ/640?wx_fmt=png)

直接利用 ssh2john.py 脚本转换 rsa，然后利用开膛手爆破... 成功获得了密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPSfLdicufnaoLTaicoZY8N9vcbH5W27iclUF73MectqwgNuduzUdGvq2ibd76VnK8OTribFhavYqdbkoA/640?wx_fmt=png)

可知道 nmap 扫描发现 ssh 是开放着... 直接登陆... 获得 takis 用户权限... 提取了 user 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPSfLdicufnaoLTaicoZY8N9vArvnJhTklzdvTcDhRClpdVQ4L0lA8JkM8REqAG0icpNicia7X6HOz8CIQ/640?wx_fmt=png)

linux 直接 sudo 查看提权方法... 发现 fuckin 执行 root 权限... 直接提即可...

成功获得 root 权限提取 root 信息....

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台简单的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/U7IQUFmZG1bqzIhV5HZKbZgWPxEY5MWaGSyMqlAesy0wZeEHzCNMqpzBefwQjV0iaz2Gq8w8d1v4UsOdgJK0a6Q/640?wx_fmt=png)

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