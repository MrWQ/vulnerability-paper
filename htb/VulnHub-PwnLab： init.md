> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/SL0AHSidQ6gJ7KiAfjFwww)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **23** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/gBSJuVtWXPZE73MPxL1VoDjO3DFaxJA2MQpSSibwsXKVf4VIHh8S9fZXT8pq1ALE3hWEN22AaniaghxGrJqjEsxw/640?wx_fmt=png)

靶机地址：https://www.vulnhub.com/entry/pwnlab-init,158/

靶机难度：中级（CTF）

靶机发布日期：2016 年 8 月 1 日

靶机描述：Wellcome to "PwnLab: init", my first Boot2Root virtual machine. Meant to be easy, I hope you enjoy it and maybe learn something. The purpose of this CTF is to get root and read de flag.

目标：得到 root 权限 & 找到 flag.txt

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/ymNhlIRQRwIDdqQDCiblECK9VN2KquqTzJXM7etEnDcIpDdITqzFuiapav9TDnIiaGgf1e4sP9IO6B5NEtEyg2t5w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/eGDabDaNAhQ72wHWRToOUZR31X9kamiak0wrpr3lxKHpuoTpia329Xu6T0OTYlZic9XeEyQ4twasnibb924VBgIt1g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/6DdW6admPmWicucEOicwONQBeMWRA7Pq57A9xCTGbIWomiboqObS0bEetoo2qW2hHk2E5GOcuQYUqSlQT5BKsDqRQ/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/M39rvicGKTibrmYlY2VW5XChia77yhteBC7iarNdYSwicq64NZrCHeSZqRpsFRTZkpfgclSWaibqftONNMWLkz6QjyoQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8tu4ckDRAHz6FDGQSk3WU6JLBj9Uib9fG4c0wWicr1H1ULX3M1zNiaiaHSWg/640?wx_fmt=png)

我们在 VM 中需要确定攻击目标的 IP 地址，需要使用 nmap 获取目标 IP 地址：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8tDsEqaNErft67dX9rhEcwRWVTgZwkMtqgBWJRs7fYjPujqdIwjc67DQ/640?wx_fmt=png)

我们已经找到了此次 CTF 目标计算机 IP 地址：192.168.56.112

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8tJV6pzqyysmypj6KkLZ6gAZMqxssWiaKBg8rYJsFQbq3uaWu4FPibInVA/640?wx_fmt=png)

```
80、111、3306、34632端口................
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8tDPvzMiaKmoYrNBhHGHmMia1s0w9A1qVUsfFXZbwNTFMlEQfEPv8L5KEA/640?wx_fmt=png)

通过 nikto 对 web 服务器中隐藏或配置错误的目录或文件进行扫描...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8tDM9VZsovCrjzx090E9H8wHvVgPBktaOpQdFzUBic4DdGAEkorco1Fyg/640?wx_fmt=png)

config.php 包含 mysql 或登录表单的凭据... 还有登录页面和 images 目录等

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8t2cy4EjgtMRhFK5gQBQF4AHupoP7wacJxugCLLDoSDMX2ur7h5XwSGw/640?wx_fmt=png)

先访问 web 服务器看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8t3AThiasPA4wUjvPGQgx1hkzibewld5WKo1BfeiaeoXqxzaCJgsq5S1bNA/640?wx_fmt=png)

可以看出存在 LFI 漏洞利用...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8tRwWV83fLYvLNe7x3nTSEhmzZcY9NeOiakgGTP6nlFBzbQrM8kRTbnuQ/640?wx_fmt=png)

直接按照意思输出访问即可找到 base64 值...（借鉴学习前辈经验，记住到脑子就是好的）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8t9UYbQKz9aGfjG1MsZSp5ia1tibaHteyfFmAl6jB4zvZSRqUAVIyvOnMw/640?wx_fmt=png)

```
PD9waHANCiRzZXJ2ZXIJICA9ICJsb2NhbGhvc3QiOw0KJHVzZXJuYW1lID0gInJvb3QiOw0KJHBhc3N3b3JkID0gIkg0dSVRSl9IOTkiOw0KJGRhdGFiYXNlID0gIlVzZXJzIjsNCj8+
```

kali 上解码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8tia8pIAL59X5TMKwwBicBjS38l2UDWhS1C38DJyGHBUeJ0lTiaKcib5vXkw/640?wx_fmt=png)

```
H4u%QJ_H99
```

知道密码后登陆他（config.php 是数据库的信息...）  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8t4OkHsBzqp3FSGPEgmhEjspkK0vR4hZUEblAtzrPfTusIUgCicsIH8DA/640?wx_fmt=png)

成功进入 mysql... 用之前章节教给大家的命令开始收集信息把...GO

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8tWTicaRro11liaFe03sphcf7u9xJATljsKWrkibAFUmq3N2fibUp6ahRayQ/640?wx_fmt=png)

一路收集下去，发现三个用户密码，解码把...

```
| user | pass             |
| kent | Sld6WHVCSkpOeQ== |
| mike | U0lmZHNURW42SQ== |
| kane | aVN2NVltMkdSbw== |
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8tzeZqRPGibw7jiavkLqPfoWDFzNXRmmKeCXeRxlWbBD95pRyOSyVoSHew/640?wx_fmt=png)

```
JWzXuBJJNy
```

在 web 服务器登陆它查看下  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8tnEopag4MxrlMib2BTGiaWj9icdiaIzvpXBtzvxg1nichdOOFypKrsV9wPLg/640?wx_fmt=png)

好吧，文件上传...（又来了经典的文件上传漏洞...)

![](https://mmbiz.qpic.cn/mmbiz_png/6DdW6admPmWicucEOicwONQBeMWRA7Pq57A9xCTGbIWomiboqObS0bEetoo2qW2hHk2E5GOcuQYUqSlQT5BKsDqRQ/640?wx_fmt=png)

二、提权

![](https://mmbiz.qpic.cn/mmbiz_png/M39rvicGKTibrmYlY2VW5XChia77yhteBC7iarNdYSwicq64NZrCHeSZqRpsFRTZkpfgclSWaibqftONNMWLkz6QjyoQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8t2uYluAboYDliagiaZib7auYYvjXwybxk1XA8fCicbbgJrmCBVXJCQcODOA/640?wx_fmt=png)

我这边随意上传了 txt 文件，告诉我说只能上传图片... 那就是 gif 格式吧

这边教大家另外一种快速提权的方法，kali 里面有太多太多编程的木马代码，只要你感兴趣，有 N 种方法能拿到你 root，不使用 MSF 来试试！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8tBCkNg3ZTso7F10eUrVibjQ567neHRtiaZIq93rw1e3IljXfpa5aZMicxQ/640?wx_fmt=png)

这是一个 php 的 shell，固定写好了的，简单修改下即可用

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8tyDPKHVOhcenKBhR7LrGsD6hLhNGQbFRib1Dj9A0ZL3OLt0PrS935QVA/640?wx_fmt=png)

加 GIF，方便加壳

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8tibypkEa2vUMwTRkwa6iczOF3ZUA2IgpIicPCsfbEZwfyac1QHdgo7UEGA/640?wx_fmt=png)

修改本地 IP 即可（提醒，这边要用 nano 去编辑，否则会出错的...)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8tXvY9BE7FUmZssBiaic8e8OkO5PCWydiaFRGmS4vWSK6ghQK23ibSc4iaUow/640?wx_fmt=png)

加个壳，然后上传

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8tekeXib0B1icwW2V0wDe3icUOibKFcOXGMGQEqccibQRGGWdticjKYa7mvzDw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8tKO7wpJnrt3CA3vcahibbmRicKd7icmaH8zD4A4uZTJp42lbtjlHgd2XNg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8tYbZLIfdo9kicictxPOongiahGOhtCIVrVt5JFPCrNficJIia873MKk3UjFA/640?wx_fmt=png)

上传成功，显示了很多数值的 gif.... 这边需要触发 gif，才能反弹 shell 拿到权限

先 dirb 爆破下 web 服务器

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8tIbS1rh9ZsJuEuNWPtvgRA0aiciaqKy4VCTy7rEyibIueqepb4SuDCpFXQ/640?wx_fmt=png)

这边发现 index 有个 php 文件.... 继续前车之鉴...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8tJa4oUhQBByZYZSLenicKiaJwbTpUvJf23keHGhDScC9fJqsJTTopZTfw/640?wx_fmt=png)

很顺利获得 php 文件的 base64 值，继续解

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8tRiaxcASu3YZj1dq6hNcg0lobI0R9DqLSJz0Eu7bkhfQb8UsZM04Z16w/640?wx_fmt=png)

解开 PHP 文件，可以看出 include("lang/".$_COOKIE['lang']);... 意思是使用 lang 可以打开会话...

这边用 curl 打开 cookie，引出打开 gif 文件...go

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8twHUHoanYyyn9WfUynGPhxNmVvZGSDtNdOkuicTqEnGgevfNdvaWKdwg/640?wx_fmt=png)

```
curl -v --cookie "lang=../upload/450619c0f9b99fca3f46d28787bc55c5.gif" http://192.168.56.112/index.php
```

因 lang 是在 index.php 解析中得到的，也得用它来访问 gif

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8tHmZTfQY9IdPiaoGk3ngpwvR2odo1zSzQIuTCBAY78sk62WCJDBicQ5kQ/640?wx_fmt=png)

另一端开启 nc，运行 curl 成功提得低权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8tZXOGhPkxzcvaUE9XnCpd487FXCYbpmQvRZ1YdeTLPtTPZDWCAzeNdw/640?wx_fmt=png)

这边使用 su 提权，提示：身份认证失败... 更换另外两个用户试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8tVGvdr48CB2PtHqVWdmibEtAybs3rGmFNApZKysVPpGPp9lgk8GRhD2Q/640?wx_fmt=png)

```
SIfdsTEn6I、iSv5Ym2GRo
```

获得两个密码...  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8tt2XwmGfzE3C3iah2MNNY9Np1WSmDaMFRlvyvsNUiavaHuXBPDOttqO5Q/640?wx_fmt=png)

一样身份认证失败...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8tL4mqaUyGTR2sy9qJgOJdeWgYAIQufLP1icuAyU8U3coTFWPHRFUG3JA/640?wx_fmt=png)

可以看出 kane 是可以用 su 提的... 进入 kane 目录发现有个 mike 权限使用的 msgmike 文件...

执行后…… 看起来该程序的作者试图在 cat 不提供完整路径的情况下运行了命令... 我在运行 Bash 程序 cat 的 / tmp 目录中创建了一个文件 shell，并将其添加到 $PATH 环境变量的开头，系统先 cat 在 / tmp 目录中查找二进制文件，并将执行我们的 shell...（多理解下就可以了）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8te2W6Uz5hQdEvEryhIxgWLUGicPJ1Kwk2yav8KCJcyAz7lpdOvRyLATw/640?wx_fmt=png)

看到 Mike 用户在 mikeand 和 kane 组中... 设置了 SUID 位... 进入了 mike 用户...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNwnUmBaY4LoFYXdRA9gx8tmthq4NI35koGtM43320Ss6HjCYlyVKmE16fWoSj9zdODqDD5Aiau1qA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/gBSJuVtWXPZE73MPxL1VoDjO3DFaxJA2MQpSSibwsXKVf4VIHh8S9fZXT8pq1ALE3hWEN22AaniaghxGrJqjEsxw/640?wx_fmt=png)

在 mike 用户中，有 msg2root 文件能执行 root 权限，这边简单代码执行试试，成功进入部分目录执行 root 权限... 查看了 flag.txt，这算是伪 root 权限... 既然知道了 msg2root 可执行，可插入 shell，那就换句木马就能提权了...

例如在执行 msg2root 输入；chmod u+s /bin/sh，在输出 / bin/sh 可提 root 权等等...

由于我们已经成功得到 root 权限 & 找到 flag.txt，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

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