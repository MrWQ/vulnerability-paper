> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/JJlPrr8uJ_8fcTqiYWe40g)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **137** 篇文章，本公众号会每日分享攻防渗透技术给大家。

靶机地址：https://www.hackthebox.eu/home/machines/profile/161

靶机难度：中级（4.0/10）

靶机发布日期：2019 年 4 月 3 日

靶机描述：

Vault is medium to hard difficulty machine, which requires bypassing host and file upload restrictions, tunneling, creating malicious OpenVPN configuration files and PGP decryption.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/mOcxDEIvrQXjKq4u8WBtxHcSvTMPpTEKv2hGbMbxR5ic3iapf3RFeETmwkrHdGnMqZdZ8cFHBpyOsEgvx1QnJRpw/640?wx_fmt=png)

  

一、信息收集

  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88pnbBvfrkrQKmqzThT8ayiaeyXpodfsa6QF4sbAkVLBzRKn7lXAGXBFw/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.109..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88XlvLUOpWkoRe9WJL1RvibCo0sqwMUW5GImqOgjYicVWlZe6KmvCGMuuw/640?wx_fmt=png)

nmap 仅发现开放了 apache 和 ssh 服务...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88jGFE1RtJhowBbc6gjXryJib0BWeoibFpLF6eNQwYIWQopYbBeibmKlmaQ/640?wx_fmt=png)

这里提示了 Sparklays 信息... 我猜测是目录或者用户名...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88jB8lzzjSvqKIAEicUBYYbGD1QyYW4aPSesh7ARibuP5UWlNicsicqnZRLA/640?wx_fmt=png)

尝试爆破发现是目录信息... 存在 / desig 等目录信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88fPwLU5iba9h9L5r1TsE0OHHoUIIQ6grmgOV14IIe6BxXIdcNlwmaTZg/640?wx_fmt=png)

根据爆破获得的信息，正常访问

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88wBG6vmVxq93V9oOy93dWEsWFktYJ8Sibezd3am8HYtwlOD94J191JHg/640?wx_fmt=png)

点击进去后，这是个文件上传的页面... 文件上传漏洞利用

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88nzEPJHfnILy3m6D1pciaiaicWGbsmZC4UTSH2xUPefUvMLO57EZIxXFaQ/640?wx_fmt=png)

随意上传个简单的 php_shell 发现格式名称不对...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88giaQcXcibLAcuEibwuGUUKr3x67XBzP4gzQOiclpCVXnabhAtkLeKeyXuw/640?wx_fmt=png)

经过多次尝试，需要. php5 后缀名称才可成功上传....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88lHBmf6443oTFWMNh8Rka07siaicJkPZAOgzu3A9UWccdFwTsw15jV1bg/640?wx_fmt=png)

通过简单的 shell，获得了反向外壳...

这里提示下，文件上传是其中爆破出来的一个目录，还有另外的登录用户的页面和别的页面，都存在兔子洞，坑是挺多的....

进来后发现 dave 用户桌面下存放着三个文件.... 都是重要信息，两个密码... 一个服务存在的现状 IP...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88icnRgRqgZulGniabr162mnO3jicRtn3EhA8QpLf6eJgLnDUcnuGbjmMNg/640?wx_fmt=png)

查看了 ssh 密码，登录即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88FJYmFYoZsRpxfJHQGtY1hKtHwqic0YkEAlpwxmLkCtoibsoLGF0TicW6g/640?wx_fmt=png)

ssh 登录进来后，发现存在虚拟网桥接口...192.168.122.1

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88R60qfkYv2Uj1q77DYPTcqRuiceJPC6lyZibAdBndPz7r2En00FngVn5g/640?wx_fmt=png)

查看本地存在的一些端口，是虚拟网桥开放的 22 和 80 端口...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88umz3z0YV68LwJicUawakeDKHjmCibLTgU94Yz8N0CiaicicsZbQWbgYfuGw/640?wx_fmt=png)

这里熟悉的技术，利用 SSH 把流量转发到本地即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88Aju3kxsO5gYEfr2YE5zwRmEkXm0SQvI0zzjAxxahutLDRD24wqg9zQ/640?wx_fmt=png)

然后通过本地访问网桥 IP 开放的 web 服务...DNS 和 VPN，这里存在 DNS 设备和 VPN 链接情况...

DNS 访问 404 报错...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88zjdl6FUU11AT3Sia58JeHZIFxEeia3P7qLgvvLfD6xTcicZibBW4aaEBWg/640?wx_fmt=png)

VPN 页面可以输入，google 看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88DmBnMfJ1460A6lnqYhf0Wzud8dozuvMe6zgmmXlS2ibH1BQYISeicRPQ/640?wx_fmt=png)

google openvpn reverse shell 发现一些 shell 提权的文章，利用看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88GYMbcOIzPfC4z0mpP9672ptrjInjLsudZxUNVmZ9vUriblc9IcCicICA/640?wx_fmt=png)

修改后... 靶机监听即可

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88RpRrrl4QxwyiboE6Qb9J3SLOten0AV4z15CgXF0BGwhkW2kKibIIzS5A/640?wx_fmt=png)

通过 openvpn shell 成功进入了 root_DNS 用户权限下... 查看根目录发现了一些文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88JxPSniaa03dDq8LKibic3lb0QficqB7o2tF2pTDmLPOnn1wyqlZcEXquGA/640?wx_fmt=png)

获得了 user_flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88WZKgOm7ZMEz5RVhnavgBWWTJTVPLiapI3iaOWVcbeSiazyQ5q6ulFgHmg/640?wx_fmt=png)

这里可以知道本环境 IP192.168.122.4...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88icOBPeiba4dcFEeMRlxtyzQVkJcppsbvLZ4pBaa6EI8t1dQHqZ3LrgPg/640?wx_fmt=png)

回看下前面发现的三个文件中 servers 网络情况... 里面标注了，DNS 是. 4 的 IP，还存在防火墙是. 5 的 IP，说明. 1 的 IP 到. 4 的 IP 之间有台防火墙串联着，IP 是. 5....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88EA4Fg5WLduh3fzgnCgC7u9ywkp1Wa7PBFoYXh9D3aIXHyXZyE9FjCQ/640?wx_fmt=png)

继续查看路由情况，是添加了条 192.168.5.0 的路由...

看看本地域名... 存在 Vault 域名：192.168.5.2...

发现此环境安装了 nmap，对 192.168.5.2 扫描了端口情况... 存在 53 和 4444 的潜在端口...

重新理清下思路...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88sxo3eibjfDN67BbZUvem3tJwb8XksJ1DzuOdfuJozyhWJICyHria5WmA/640?wx_fmt=png)

情况是这样的，看图即可...

需要绕过 FW 进入 5.2 环境... 还是需要 SSH 或者流量等转发技术...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma888JZicf9lYXyZP9QicfFyRfW5RMYgk7tOm7HneVKNVCZgWrKcNhpJ7Buw/640?wx_fmt=png)

将 4444 作为源端口，利用 nmap 绕过防火墙并找到另一个开放端口...987

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88wH3S0iaz1VuHD7p3S4dcsIFzYP0rkozD1eO1FmKhXwPptKicstXVqt0Q/640?wx_fmt=png)

当然，在查看历史记录日志里，也发现了该操作... 他是利用 ncat 生成侦听器进行连接...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88jvTTIVCIpC3krn7HG5wgGYvsBZrqlc2eWQhjSASf7EpOYVpUcQMjDA/640?wx_fmt=png)

我们也利用 ncat 侦听器进行生成，该侦听器在更改源端口时重定向到端口 987...

然后利用 ssh 成功登录... 并查看到了 root.txt.pgp 文件...pgp 格式下，在 5.2 环境里无法查看...

查看了三个环境下，在最初的 dave@ubuntu：10.10.10.109 环境下，可以使用 gpg... 当然本地也可以...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88yCibM2jflc1CfiaWxBscnFYQQkVyZunY4w8Szwib7xerZs1wHQ6M1Fm5A/640?wx_fmt=png)

由于 5.2 环境无法使用 base64... 这里利用 scp 将文件传回到 DNS 环境....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88DXwicoz2XLyiaGzQArM8ABOSVejFnH6FiasXOiadM2f4y0KzOricpUEUaBA/640?wx_fmt=png)

通过 base64 进行复制文件即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma889Ea4OmUECDXFKiaIGe6w3L4v23DAicEYGicnpqpyBQ3ePBibYDQhVPqfPg/640?wx_fmt=png)

转储....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNNofd1fveBQ9Nc17F6Ma88kUibuYLU0lQLVaQQ8HrkZqYjAasianJzTexRQfJqB9gv0LYD2BKibtWqA/640?wx_fmt=png)

放回 dave@ubuntu：10.10.10.109 环境下后，利用 gpg -d 成功获得了 root_flag 信息...

目录爆破 -- 文件上传 --ssh 流量转发 --openvpn 漏洞利用 --nmap 绕过防火墙扫描 --ncat 端口转发 --scp 文件传输和 base64 文件传输 --gpg 获得 root_flag

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