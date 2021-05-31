> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/E4kUDJrslOW1uecyDeu5Bw)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **19** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/gBSJuVtWXPZE73MPxL1VoDjO3DFaxJA2MQpSSibwsXKVf4VIHh8S9fZXT8pq1ALE3hWEN22AaniaghxGrJqjEsxw/640?wx_fmt=png)

靶机地址：https://www.vulnhub.com/entry/vulnos-2,147/

靶机难度：初级（CTF）

靶机发布日期：2016 年 5 月 17 日

靶机描述：VulnOS 是打包为虚拟映像的一系列易受攻击的操作系统，以增强渗透测试技

由于时间并不总是在我身边，因此花了很长时间创建另一个 VulnOS。但是我喜欢创建它们。该映像是使用 VBOX 构建的。解压缩文件并将其添加到虚拟化软件中。

目标：得到 root 权限 & 找到 flag.txt

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/ymNhlIRQRwIDdqQDCiblECK9VN2KquqTzJXM7etEnDcIpDdITqzFuiapav9TDnIiaGgf1e4sP9IO6B5NEtEyg2t5w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/eGDabDaNAhQ72wHWRToOUZR31X9kamiak0wrpr3lxKHpuoTpia329Xu6T0OTYlZic9XeEyQ4twasnibb924VBgIt1g/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/Fe5xibS5DJUDA9AxD1uS147czicCck7HYbZicgVXFrlsLXntEaOVcLzGJyhWwL2kicQgia6VkPsFqK3Qsh4kRPHetlA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhuAfUtrQTyAhvCSjOtVPz8aicHvNPeaR2156QCxPZssDUfzvj9rfpiayg/640?wx_fmt=png)

我们在 VM 中需要确定攻击目标的 IP 地址，需要使用 nmap 获取目标 IP 地址：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhjpLLAtibmY0qVmCbQ5l6gwbNH9zmHsojmibMhZhjRxtPvxhaQFerV9iaQ/640?wx_fmt=png)

我们已经找到了此次 CTF 目标计算机 IP 地址：192.168.56.111

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYheUrciaP1GDDcE7n5CnHW1ABvDqk7IOlIgq5MNAXcI9iaS1Rn5JXTXLibw/640?wx_fmt=png)

```
nmap -sS -sV -T5 -A -p- 192.168.56.111
```

只开了 22、80 和 6667 端口，分别是 ssh，Web 服务器和 IRC 服务器...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhIpBYwmDhqzaicibDWom5xRar9aqBjsRR6v0whNjPwPwMpEzK5Th9fPFQ/640?wx_fmt=png)

访问看 80 页面，发现另外一个链接，继续浏览

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYh2NV1douHk6ytTibVlkSDFv8LB1h0iaGZEVwHhA2ctrqVxzB0IOvj3KPQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhcWEkEntgegsQPRRnU2lZpEmc3nXmJNMicQx7QmeFGB3WZosvENU2bnQ/640?wx_fmt=png)

四个模块都找了一遍，都没啥信息...

二、web 渗透

![](https://mmbiz.qpic.cn/mmbiz_png/Fe5xibS5DJUDA9AxD1uS147czicCck7HYbZicgVXFrlsLXntEaOVcLzGJyhWwL2kicQgia6VkPsFqK3Qsh4kRPHetlA/640?wx_fmt=png)

在最后 Documentation 无意间发现... 真坑爹的隐藏了字面

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYheZibCO2dFyqg6tTN3lSzSibPf5xYeHKWw7ictTbubc0ibaiaK6ojOjiaXdGQ/640?wx_fmt=png)

原画面是这样的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhslecrnDMLJR7EIdPVRDia5QnfA1Hgswtialljjvo34gmhVmtau6qIxGw/640?wx_fmt=png)

全选字眼后.... 还有内容... 发现了新的目录 / jabcd0cs/

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhlZjhaibnRrrJeqEpVe53k12GaGsDhPTmU4ReEhicjS4d8xibhEYjULLibg/640?wx_fmt=png)

OpenDocMan 1.2.7... 版本 2013 年...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhWN4LaSM094LqUMDQicWV6Vctgaic97yib3TRVKtWSWNghU4uXD8I1UhuQ/640?wx_fmt=png)

直接用 exploit：32075，我们进去看看里面的内容...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhW3pM0mSdA9Eo7h6rtMWI1icSTxoLYsCgZ6WhTV61xkTrOpaziayrfYQQ/640?wx_fmt=png)

发现有 sql 注入攻击，正是我想要的...

先打开看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhMjzvWP5YJb8Zttw3QwOscaUaiaXNawHHYRd4HloNzcfdz3Gvz3jrURg/640?wx_fmt=png)

这里可以看到 mysql 的版本号...

本来我想用 sqlmap 发现的，无奈怎么执行都报错...（这边先不管了，后面我在修复下...)

这边直接用最笨的方式 web 渗透...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYh2iaUOarkyNHO4iabu02jvFMOXG10xZJFdFyI1FlrEXJzZEtyo5qp1miaQ/640?wx_fmt=png)

可以看出 1~3 之间的是可变量，这边我们修改下试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYh17Fc1M1jPicZFKrHHIm3h5R17wicI8IQj0szZEetx0sCy2tIwD2qJrqQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYh0x1Rd6nDZkw1Bd3dywmr71FJ6LiaicnjZGUgVPcKMQUUYw71iaRicWlnAg/640?wx_fmt=png)

账号都能发现，那找出密码试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhWMPbXztXXBicFlaXJvnbq8DZRHviaZBhh2amIRsNQ5PicjLsSdnr00XPQ/640?wx_fmt=png)

发现是 md5 值，翻译

```
084e0343a0486ff05530df6c705c8bb4：guest
b78aae356709f8c31118ea613980954b：webmin1980
```

前面获得两个账号，guest 和 webmin

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhukaiaIevmTSpey4HTf5I9p5TcVvIWp3KEyfsVwvQHibDZiaHWpIGy4icSQ/640?wx_fmt=png)

用 webmin 成功登陆 ssh！！！继续查看 linux 内核

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYh1PdibunloBCjyt8mhV7UQ6rN3EMpVkgqDxYGHGtTPQMYFtYBMkEHKdw/640?wx_fmt=png)

```
Linux VulnOSv2 3.13.0-24
Description:  Ubuntu 14.04.4 
Linux 3.13.0
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhDrM0AXbs1EpPevbpVEAibwpM59DeBYbIhibk1LolWnsNvyspKM3TZGpg/640?wx_fmt=png)

三、提权

![](https://mmbiz.qpic.cn/mmbiz_png/Fe5xibS5DJUDA9AxD1uS147czicCck7HYbZicgVXFrlsLXntEaOVcLzGJyhWwL2kicQgia6VkPsFqK3Qsh4kRPHetlA/640?wx_fmt=png)

这边查找了一会，发现 Linux 3.13.0 中有利用的 EXP... 使用 37292.c 进行提权

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhU2VCjMic26ujFX6fiaqjG2kibZOHFkvdLAcOwewPPZBSnRTrllzp3Lzibw/640?wx_fmt=png)

下一步不多说，gcc 编译...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYh8nuq7nm5E3l3xZJlddXtDJPxEVrncKgdTZvUs2laccCIibkB79PicEeg/640?wx_fmt=png)

一步到位... 这边不多解释了... 基础知识... 不会的看前面章节！！

成功提权...

![](https://mmbiz.qpic.cn/mmbiz_png/gBSJuVtWXPZE73MPxL1VoDjO3DFaxJA2MQpSSibwsXKVf4VIHh8S9fZXT8pq1ALE3hWEN22AaniaghxGrJqjEsxw/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/gBSJuVtWXPZE73MPxL1VoDjO3DFaxJA2MQpSSibwsXKVf4VIHh8S9fZXT8pq1ALE3hWEN22AaniaghxGrJqjEsxw/640?wx_fmt=png)

Hello and welcome.

You successfully compromised the company "JABC" and the server completely !!

Congratulations !!!

Hope you enjoyed it.

What do you think of A.I.?

AI 牛逼，人工智能牛逼....

好吧，感觉最近越来越顺手了，渗透这些靶机越来越快了，估计是这个靶机比较简单吧....

继续加油！！！！

由于我们已经成功得到 root 权限 & 找到 flag.txt，因此完成了 CTF 靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

![](https://mmbiz.qpic.cn/mmbiz_png/ymNhlIRQRwIDdqQDCiblECK9VN2KquqTzJXM7etEnDcIpDdITqzFuiapav9TDnIiaGgf1e4sP9IO6B5NEtEyg2t5w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/eGDabDaNAhQ72wHWRToOUZR31X9kamiak0wrpr3lxKHpuoTpia329Xu6T0OTYlZic9XeEyQ4twasnibb924VBgIt1g/640?wx_fmt=png)

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/ymNhlIRQRwIDdqQDCiblECK9VN2KquqTzJXM7etEnDcIpDdITqzFuiapav9TDnIiaGgf1e4sP9IO6B5NEtEyg2t5w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/eGDabDaNAhQ72wHWRToOUZR31X9kamiak0wrpr3lxKHpuoTpia329Xu6T0OTYlZic9XeEyQ4twasnibb924VBgIt1g/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)