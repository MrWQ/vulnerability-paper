> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/x6R_o9ZHh4uMkE3BLwRFyA)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **27** 篇文章，本公众号会每日分享攻防渗透技术给大家。

靶机地址：https://www.vulnhub.com/entry/mr-robot-1,151/

靶机难度：中级（CTF）

靶机发布日期：2016 年 6 月 28 日

靶机描述：根据表演，机器人先生。

此 VM 具有隐藏在不同位置的三个键。您的目标是找到全部三个。每个密钥逐渐难以找到。

VM 不太困难。没有任何高级开发或逆向工程。该级别被认为是初学者 - 中级。

目标：得到 root 权限 & 找到 key1~3

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/xMkop2LgjnWJ2ibeqRr6ibJ0DACo8NUp2r61alcad7YrhtFnpOBUaD70nTfefkrffcx14CUeicLquAibJZ4rbwLmfQ/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8WjicaDiaWb3iceFUz9fj5LxUcUjibumty9OLEkmiaqWHFXwbiaYV8C5RJPFg/640?wx_fmt=png)

我们在 VM 中需要确定攻击目标的 IP 地址，需要使用 nmap 获取目标 IP 地址：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8coMbcib7lpmqX4KtRYt9N5eKjqNORCxX9GRB2wvruUMryia227OGYOLg/640?wx_fmt=png)我们已经找到了此次 CTF 目标计算机 IP 地址：192.168.56.124

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8a8zL6dJ9gmuao7JDzuqnd6jPblzxw86PbvSGuE6I61uBjvZN66BibWg/640?wx_fmt=png)

扫到了 22、80 和 443 端口...22 去 root 不行... 直接访问 80...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8iaMTb8YS0sKyicrEyTqmPaHLoRm7vK4Zb3kPqiabhHO344GpnCupiar1Gw/640?wx_fmt=png)

直接访问 robots.txt 文件试试...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8GuDbGBxdWdPsicUmjqs2ibOMshlpA1jsGBA6ex5cndCE5jQSZSJ210NA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8SMzjbyDWAXUv7qxclUoBKBXs0Um0r86dfdjYVRv0TgKpzH1106fuHg/640?wx_fmt=png)

直接找到了第一个 key... 还有一个. dic 后缀的文件，一看这就是个字典文件

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8AOXC3bZhnnsicwp2FAL9AcakgicHic2e7lz7Vg4eB9rKZIRZjISIFa9TA/640?wx_fmt=png)

果然是字典，套路应该是密码字典... 这边爆破下网站获取更多信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8gKms3ZK7FfSkZrdj8rntW3Deib3ocKuZ4NlhF32rJU7JdFVxMUb4X1g/640?wx_fmt=png)

可以看到这是一个 WordPress 网站，以及发现了 / wp-login...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8d9AY5UwfMPdpP3TjpQxTaQ3FvyHEvSUwiaYkwdQO7bO1qBYDGgibfkoQ/640?wx_fmt=png)

登录 wordpress 的页面.... 找下用户名用这个试试...（admin 不成功）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8ibpzmIqYAyvYtfBRicZDjG0pGrVmuLDH0kDaLw537gW0HtDg1uc24TXw/640?wx_fmt=png)

发现随意输入用户密码都会回复这个... 错误：无效的用户名或电子邮件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8tBiaZhlzcvCgUKY5RlKlYYibibJlP0H0z3D8jYEmNoSxNNDmCd7XnuGuw/640?wx_fmt=png)

查看源代码，我这里可以找到正确得账号... 利用 robots.txt 里面获取得字典对账号进行爆破试试...

```
hydra -L dayu.txt -p dayutest 192.168.56.124 http-post-form '/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In:F=Invalid username'
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8s0e14jQkyLCcsX2H693pUbDqkRpTPXxCVtbWbGV76mc51rk5BagfvQ/640?wx_fmt=png)

成功发现了账号...Elliot

下面我们来找找密码....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8VuvMDmEzfuQnBzTJFwFQAEq4ZtibpnfkpNOReZZu62zZYJa6ZoT5Svg/640?wx_fmt=png)

使用这个命令.... 去找到密码

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8LIOBeRWFf8AUqCV4edYMEorKV8S6QCIOGBhSXfwT4bCoziasyZH6jNg/640?wx_fmt=png)

```
wpscan -u 192.168.56.124 --username Elliot --wordlist /root//Desktop/dayurebot/dayu.txt
```

等待跑....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8mDmNXuMZOUeAMDzyw64c1kzF3xCpxic2GYHYkKXhY0RUEPqxgH0ArzQ/640?wx_fmt=png)

这里等待了 5 分钟扫完了发现不了，我把 Elliot 改成了 elliot 试试后，发现了密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8ic2TfRCQ8jMSOD3jk9xzXk7GibtoPxCU9mnjiczmEz6vbPm37ySLibbplw/640?wx_fmt=png)

成功登陆进来了....

二、提权

成功登录后，发现有文件上传的地方....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8O5UicyorL4n5CuRCRwVVWsjI3L8kNxVI794xHibIthBxs9pcLUicX4MOw/640?wx_fmt=png)

If you have a theme in a .zip format, you may install it by uploading it here.

上传文件，这里我以为只能上传 zip，两个都上传上去了....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8sa7pa5A5rRmLJMLjiajjwjnibdR6tm1UzUOVaPkAQ06OtBtVgV5Ojc0Q/640?wx_fmt=png)

在 media 素材里看到我们上传的文件... 打开它...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8jib6vD1FWVdMzINCSzQhhej1l6b2QxibA70KYj4dWWJmfexnBt1mXhug/640?wx_fmt=png)

我们现在必须得访问它执行它，才可以获得权限... 编辑查看更多的详细信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8XFjCDNX3qdCxs2ia5eX0riaI0VmTR3gXBia0ia4uppK0vKFIIU7nGoHNFA/640?wx_fmt=png)

查看到了 url 访问它... 在本地开启 NC...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8YibssPAYR3fl2cp3EhJ2pbR2ShAM9l1Sk4m5icYyEf2QoQ8J8EED4eAA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8h2aOx57hvYibTyu2ZicoBSS1HKtHkPy93fibvjktkc6vCOCRHI2MfbtCQ/640?wx_fmt=png)

获得低权限用户... 当然页面还有很多地方可以获得这个低权用户...

```
python -c 'import pty; pty.spawn("/bin/bash")'
```

进入 tty  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8EAEzacul0ic1tiat72TGYg4QK0rweFAbCQ4PIQrUw8LMjSeiaW6VUJbSQ/640?wx_fmt=png)

这边找到版本想用内核提权... 发现试了几次没成功...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8vmWSD0vKlhOicicfD00yzf8ELQB6Iy8nIBiaNxn8RSSKYiaHks4UKbS8CA/640?wx_fmt=png)

一个一个找文件夹，找到了 key2 看不了... 想想

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8GHyM6aM4kzZKUodDibMpnNY2hd2XVdH9gAsKzicyFictriaPgTAyuicBKdQ/640?wx_fmt=png)

找了半天就在原目录下一个 passwd 文件... 尴尬.... 查看试了后进不去发现是 md5 值，去解码后成功查看到 key2...

这边通过 robot 提到了 root 权限...find 直接查找 key3 试试....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8hwVzvhBzst9Do8dwGNwunaRBA1ktdVrmvjeeS7XpPYbL0zcvy7cCug/640?wx_fmt=png)

这是 root.... 这边查看下底层有那些文件... 搜索 setuid 二进制文件

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8sZW7YEuBFKw6oHjWFs8Kf1Fibrqq0BmxicH6WxcjLhkQSZxFPkff5QcA/640?wx_fmt=png)

```
find / -user root -perm -4000 2>/dev/null
```

竟然安装了 namp....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8ibibRXC0ic8iclS47jhbFOHme4qKFxWpv68Rroq6mpV1v9l8xh1BmMqMzQ/640?wx_fmt=png)

Nmap 不会有 setuid 位，版本也低.... 利用 priv 升级漏洞进行 bash 提权试试....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPV2pAbAZYeN9KSM3g52ibr8VLjnWlpIbib3PRUibWvh5K7l8jo1KKSWAcy07G7aJqIfUreANcjw58sQ/640?wx_fmt=png)

成功提到 root 权限... 找到 key1~3 值....

学习使我快乐~~ 加油！！！

由于我们已经成功得到 root 权限 & 找到 key1~3，因此完成了 CTF 靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/xMkop2LgjnWJ2ibeqRr6ibJ0DACo8NUp2r61alcad7YrhtFnpOBUaD70nTfefkrffcx14CUeicLquAibJZ4rbwLmfQ/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)