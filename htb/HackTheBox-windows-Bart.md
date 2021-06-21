> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/c0OGxjRT9ngAlWrwVIIakw)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **68** 篇文章，本公众号会每日分享攻防渗透技术给大家。

  

靶机地址：https://www.hackthebox.eu/home/machines/profile/128

靶机难度：初级（3.7/10）

靶机发布日期：2017 年 12 月 20 日

靶机描述：

Bart is a fairly realistic machine, mainly focusing on proper enumeration techniques. There are several security policies in place which can increase the difficulty for those who are not familiar with Windows environments.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

  

  

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sPwoBgoqXC44Y49bsFnVq5nZtwWCm8UUYyppJQTcs9DCZszzXiarvQLtA/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.81.....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sPHiaGtLow0CgU8gaI2BFib0H1WmK7deRDziaQIFVwdqknOoD3OhvUNZUUA/640?wx_fmt=png)

Nmap 仅显示在目标上运行的 IIS 服务器...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sPB8Sup1jEfNEia8bF9ALAp5TtZYYfFO0DGK22ZFfe7AKUCoFTnwFVvnw/640?wx_fmt=png)

可以看到访问 10.10.10.81 重定向到了 forum.bart.htb，nmap 也发现了

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sPsWnyh68ocXsXZlQnzgIIKeBT8Lh2ibM7abpafUulgslpoNibR85TBJ5g/640?wx_fmt=png)

在 / etc/hosts 文件中添加了一个 DNS 条目，将 10.10.10.81 指向 bart.htb 和 forum.bart.htb...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sPhmicc0IKYvKK4TCVgsM9WzxJmGiatT0alKkTkp6cMG2N0e3mQxdrD8ZA/640?wx_fmt=png)

可以看到正常访问了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sPqtX0G5lIEvent6w0F3HR7BDaj6zYBY5au2Xm4WXOS9Q4NER7zukhdg/640?wx_fmt=png)

利用 dirb 对 bart.htb 进行爆破发现了 monitor... 是个登录页面

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sP7tWnCZDvJ41l5qwnUra3RpPU2b3Qia8XFkJmktiauHyAsVAYBlFjF9WA/640?wx_fmt=png)

经过在 forum.bart.htb 前段源码中找到了很多用户名，一个一个尝试...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sPj3yqTejNzhAwKj4WTeo1MmdxLTxsMX8ut1RjxGNQZJwWNx4ia3B8pjQ/640?wx_fmt=png)

尝试用户名发现 Harvey 是存在此用户的，那进行密码爆破...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sPaYaooo0yVLHZbzwOJxXpXZMfEQbTtZagFunDFmHh8DGGD3X1licticsA/640?wx_fmt=png)

```
cewl forum.bart.htb -w bart-dic.txt
```

由于我这几天链接 HTB 太卡了... 我就创建词典爆破，不然等一天都没结果...

经过爆破密码就是 potter... 这不就是在前源端源码找到的吗... 这里浪费了我 1 个小时，太卡了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sPgDxUq2nxzSdZGgUh7bicfqHib9UTpKgianzCaibVuia7zuic7P0QZ9FVDCww/640?wx_fmt=png)

尝试登陆，发现又跳到了另外的 DNS，继续添加试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sPIpPn6biaicPzoIHMEJicq24lIzJMprQUX90p8atcx1ESHuicEwiaNnPpNibw/640?wx_fmt=png)

添加完后，成功登陆...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sPHWzTHFkFaARhXkuXrC3Z96IjWEibrA9iaHHXc3iaYUvZpC528vMEbOEXw/640?wx_fmt=png)

可以发现，还有 DNS，继续添加到 hosts 去...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sP1Uh7ia4ibnM0A3bIz3lUmwJDghMdn91JQjibZKCp5s7Bic8NZPcj8HKXAA/640?wx_fmt=png)

访问发现又是一个登陆界面... 一环扣一环

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sP5Dap3QVkzrA4bFglArtFjTahVicjh2Ehq1Rg97L9v6zicd85iaQc1MFrQ/640?wx_fmt=png)

我使用 harvey/potter 登陆提示进不去，还有信息就是密码长度最小为 8 个字符...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sPk4EVFcyosIibSv6VoACqoRhy2rIA7ulFexZ0YprTpY6jMsduyr2IFLw/640?wx_fmt=png)

通过爆破尝试，用户名密码是

```
harvey/Password1
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sPQS2FPwCibOY0ELFbiaUZVnibsc6lhlXhAAJyASrrh1CwCBhlu6nMTPS1g/640?wx_fmt=png)

成功登陆了....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sPTEyGa4scW7abZ9iarcGewpGJJHjowabmVHFmL58xfEEIkFMfbTyt0ng/640?wx_fmt=png)

在前段源码中可以看到有趣的信息... 存在注入攻击...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sPc7gBAuMiaTCo9pERpbSqcSQ4cj1FDXe7iaQ8Gmbwia3l8QQFDibC08EGjQ/640?wx_fmt=png)

存在注入攻击，那就简单了，可以上传 txt，返回 username... 那就直接上传 shell 反向外壳就 OK...

![](https://mmbiz.qpic.cn/mmbiz_jpg/2iaOMskBibMM4mNsp9A5G4u3Ev6zqassh3abNdVibWQe9H3ugibS1g34X7kn0Nibp23jchf2sWCdR4aS9aXSMI4LJiaw/640?wx_fmt=jpeg)

方法 1

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sPHakLWxTn7Xm2nNuZWB77cS1uXtUjsbIy6sibHgO3A6595MAXOHOR36Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sPjWXOCHsbXlMibPbyaJrtzP4yg5HOX62ZcDL7GX2PibLj847Fs5OgyxZA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sPXuw7EoJB9FNUPMonHuhZvSJxgUOQBPqSiatbRJvYrSkWJm6skCwbmsw/640?wx_fmt=png)

可以看到成功提权....（这里不多解释了，前面文章写了很多...）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sPE4OXfXDAB5a5IVRpNVq9cicFLI1okfnPRCBd6XAibQND9YNubahJ7cXg/640?wx_fmt=png)

这又是一套最新版本的 windows10 系统...

这里我卡主了挺久，最近上班也没时间渗透这台靶机...

我还是晚上抽了点时间想完成...

![](https://mmbiz.qpic.cn/mmbiz_jpg/2iaOMskBibMM4mNsp9A5G4u3Ev6zqassh3abNdVibWQe9H3ugibS1g34X7kn0Nibp23jchf2sWCdR4aS9aXSMI4LJiaw/640?wx_fmt=jpeg)

方法 2：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sPrSWP2bdZXTfFM7QC2eCQZea96J0RGT1rOyAqnOjxawsvedYRUN9q9Q/640?wx_fmt=png)

这边使用的是 php/met... 然后进行提权...（这几天开始使用 2020 最新版 kali，非常舒服，很稳定，强力推荐）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sPPGIAQnFXicGfOIrQtYtcJZmhibQWtg1vTgkJetoD6oOLBoMiccLVf6v1Q/640?wx_fmt=png)

这里我利用 php 简单语言写入了 msf 生成的 shell 代码，写入到了 dayu.php 文件中...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sPt7aib7TBia9xgV1xC0SCqgwicDD3nCpTDQNXteRBmlWrt29v694Q8ibwdA/640?wx_fmt=png)

成功提权... 这过程很简单也很暴力...

  

二、提权

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sPknGQr2BSbHpUtLibJnnwAOJPZ7GSiaKkOlSfz7p6VV0BX40YE9WgBF2w/640?wx_fmt=png)

这里直接上传 nc 进行连接，因为直接提权的 shell 不稳定... 我试了几次...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sP6aPuLgmKLbkJHDsDviaD3ramIHXojR2IX8BxqcEWlUKsI0wOibvSGicJQ/640?wx_fmt=png)

成功利用 nc 进来了...

下面推荐：

```
https://sushant747.gitbooks.io/total-oscp-guide/privilege_escalation_windows.html
```

里面有很多 windows 渗透的技巧

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sPibqibeljNleY7Uy00JSibJWicXky0icvdKibVJkG53GSmrgLkic1920xFWY3w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sP09P8Z0AAlHDWgTkLuHePxVh6H3BACictZibkTBrbxNe35hoge8ibV8MVA/640?wx_fmt=png)

这里直接查看其中的注册表... 而在注册表中显示管理员自动登录凭据... 好东西...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPPlbNFa4ReflpT9n8Jz9sPZld4Uyk42BxG9R0pRYmmsicASX8ScuY4SdWobNANznNYORvGFU12xXg/640?wx_fmt=png)

直接通过注册表中的登陆凭证直接获得了 root 信息...

  

这里可以利用 MSF 去暴力获得权限、也可以通过数据库查看密匙后 smbclient 进行提权、也可以利用写个 shell 获得权限...

这台靶机挺有意思的，可以延伸很多方法... 我这里不列举了

以后我写文章会快速过，命令也不附上了，自己看图敲打！加油

由于我们已经成功得到 root 权限查看 user.txt 和 root.txt，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

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