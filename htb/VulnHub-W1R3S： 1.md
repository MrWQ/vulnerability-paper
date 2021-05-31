> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/cTnrq0e_ThNjSYOFs9D5QQ)

靶机地址：https://www.vulnhub.com/entry/w1r3s-101,220/

靶机难度：中级（CTF）

靶机发布日期：2018 年 2 月 5 日

靶机描述：You have been hired to do a penetration test on the W1R3S.inc individual server and report all findings. They have asked you to gain root access and find the flag (located in /root directory).

Difficulty to get a low privileged shell: Beginner/Intermediate

Difficulty to get privilege escalation: Beginner/Intermediate

About: This is a vulnerable Ubuntu box giving you somewhat of a real world scenario and reminds me of the **OSCP** labs.

目标：得到 root 权限 & 找到 flag.txt

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/F6V6Kvlib598cruI3TjHeqU9bptO6tyM1YBpvZb2sC6cvE3bAx0NcT1N38JjgQCsp3MsiaOIOia0kayJoW1Y1Emnw/640?wx_fmt=png)

  

一、信息收集

我们在 VM 中需要确定攻击目标的 IP 地址，需要使用 nmap 获取目标 IP 地址：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM0b8o45Y0zoMnA9RlSuVdia0VfibuosnAlEADxAic3wibviaCQvTWcghS02xj9NEeVzGMelvvH2asbPCw/640?wx_fmt=png)

我们已经找到了此次 CTF 目标计算机 IP 地址：192.168.182.145

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM0b8o45Y0zoMnA9RlSuVdia3sOcG5WU5npOGwcLL4iaI4icV0ouJmh0eic36RWia2nc6BTHzfeYYVA1Tw/640?wx_fmt=png)

这是靶机的界面

我们开始探索机器，第一步是找出目标计算机上可用的开放端口和一些服务

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM0b8o45Y0zoMnA9RlSuVdiaryXJDjOQggsib7WRkMExGbmPvrg2pdXfHjoBVQuPXyBpztWsSCxwh4w/640?wx_fmt=png)

命令：nmap -sS -sV -T5 -A -p- 192.168.182.145

开放了 21,22,80,3306 端口，这边我直接 web 渗透收集信息（喜爱 80 端口）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM0b8o45Y0zoMnA9RlSuVdiaRDzrKaAyhhzd26p8IFiacbibYia4IzB9z5R4TWXeP0OnENbb8Lm4geEfA/640?wx_fmt=png)

找了一会，没发现有用信息.....

我使用 dirb 工具攻击目录

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM0b8o45Y0zoMnA9RlSuVdiaHAwIUTF9Ooeqia5d2qDNMQ6MseXIRFWvH4vRiaDMsOW4fzQUkg4pSGsA/640?wx_fmt=png)

找到了几个重要的目录，/administrator、/installation  和  /wordpress /

直接访问 http://192.168.182.145/administrator/installation/ 

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM0b8o45Y0zoMnA9RlSuVdiafswNRKuulIgNCU7mOic04KSTP3ZsFJ7VohdKACM8DbfHL64x0mYc3CQ/640?wx_fmt=png)

该 administrator 目录原来是 Cuppa CMS 的安装设置（内容管理信息系统）

谷歌查询（这里需要阶梯出去）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM0b8o45Y0zoMnA9RlSuVdiaexzMzUsKiaTH2Nz1JgqibQQEXrnmCCqxNlua6FY02NpneLU7c2ib8Zjlg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM0b8o45Y0zoMnA9RlSuVdiaRSZloIghBm09icyBUzwa8PmP1iba5lLiaQib4S4JtMiaB6hljBHW8oby0KA/640?wx_fmt=png)

地址：https://www.exploit-db.com/exploits/25971

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM0b8o45Y0zoMnA9RlSuVdiawiaaoSVjnvSx39BbdiaPcKoRIvSqDm0wicgGoA7Ss55DvIibQALq9vyosA/640?wx_fmt=png)

这边每一篇文章都有一个新的 exploit 希望大家能一个一个记住，记住上百个可以随意攻破一台服务器！！

  

二、权限提升

这边我们发现 25971.c 里面 exploit 里介绍 “Moreover, We could access Configuration.php source code via PHPStream”（此外，我们可以通过 PHPStream 访问 Configuration.php 源代码）

这边我们直接利用... 访问试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM0b8o45Y0zoMnA9RlSuVdiaub1J4F5iaBtOdJwKnSpPqx6a6GaADdLIME48wRCro2KGdchZmJq3Jjg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM0b8o45Y0zoMnA9RlSuVdia1C3xicd5ymZCIbBzEpTbTFpoOpglKo23KmlUqibd3leibfOVULNiaAuEicQ/640?wx_fmt=png)

没有任何信息!!!

在浏览器上浪费了大量时间后，我决定使用 curl 来利用 LFI 漏洞获取 etc / password 文件

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM0b8o45Y0zoMnA9RlSuVdiaJgoJTHy7US37Kv11fgWMEEIkQWafE8dCTxicSI2mKPkHuLQyT33ibgFg/640?wx_fmt=png)

命令：curl -s --data-urlencode urlConfig=../../../../../../../../../etc/passwd http://192.168.182.145/administrator/alerts/alertConfigField.php

当我执行上面命令浏览 etc / password 文件时，找到了第一个用户名 w1r3s

然后我再次执行以下命令，以使用相同的过程获取密码文件，继续 data-urlencode...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM0b8o45Y0zoMnA9RlSuVdiaqvKqVPjYqTKF5wwk5qYWOjicj68cjr1gviaFdzcXDQNDBAG0lgRmm7UQ/640?wx_fmt=png)

命令 curl -s --data-urlencode urlConfig=../../../../../../../../../etc/shadow http://192.168.182.145/administrator/alerts/alertConfigField.php

发现：w1r3s:$6$xe/eyoTx$gttdIYrxrstpJP97hWqttvc5cGzDNyMb0vSuppux4f2CcBv3FwOt2P1GFLjZdNqjwRuP3eUjkgb/io7x9q1iP.:17567:0:99999:7:::

找到了用户 w1r3s 的 salt 密码，我们用另外一个开膛手 john 破解此密码

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM0b8o45Y0zoMnA9RlSuVdiabUVmf3GjTlHK48wsepNycEgfDeT89YuAMBcbqwkHckTLb0tF7YptjQ/640?wx_fmt=png)

先把这些命令复制到 pass.txt 文档中

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM0b8o45Y0zoMnA9RlSuVdiaZqGe9KduSrcULklQNfeVPbwjnK2Pse3ebwL8SFmzXz51rMk8uoCdPA/640?wx_fmt=png)

用户名：w1r3s

密码：computer

前面 nmap 扫到开了 22 端口，我们直接进行 ssh 登陆

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM0b8o45Y0zoMnA9RlSuVdiaStbXHEvd1Axr7ciaT3jPibczO461xLGj3fquam0JtzrramquvbW91IqQ/640?wx_fmt=png)

查看下权限

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM0b8o45Y0zoMnA9RlSuVdiaxGaH3vUEl0Ra820KgQOicTz2XeUxiaT7nqsCBWXM4fl1OpEFFFcAOD8g/640?wx_fmt=png)

竟然能 sudo 提权，我还以为继续得用反弹 shell 提权呢....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM0b8o45Y0zoMnA9RlSuVdiaMgklGs4AnU5ZXhC9Z5tYPRxF8akFibLQJrJiaR7KHxwWY21Dww8LyzUQ/640?wx_fmt=png)

sudo 提权成功后查看 flag.txt

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM0b8o45Y0zoMnA9RlSuVdiaJ3wZaKnbPSzMsgGe3k5icE52VzvaSd8qbtwZu0icrhRvgMRqHZ5MhCSw/640?wx_fmt=png)

这台靶机还是比较简单，应该不是中级难度... 了解过密码爆破工具 john 会省很多很多时间进行破解。

由于我们已经成功得到 root 权限 & 找到 flag.txt，因此完成了 CTF 靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/F6V6Kvlib598cruI3TjHeqU9bptO6tyM1YBpvZb2sC6cvE3bAx0NcT1N38JjgQCsp3MsiaOIOia0kayJoW1Y1Emnw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM0b8o45Y0zoMnA9RlSuVdiaaiaNNZB6GSyiaMhjNq56BoQuAztiaiaZLIJiaZibQmhqtGPr5eGgwGNxLVGQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM0b8o45Y0zoMnA9RlSuVdiabGk1ejAVVRb5QwLg5EWv2Em4YplLEu3z41rfU8RMMFm3VtvLza2ZbQ/640?wx_fmt=png)