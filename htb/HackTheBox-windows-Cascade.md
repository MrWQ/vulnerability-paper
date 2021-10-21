> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/gB83rFfVqYX0SwuO2u06Bg)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **192** 篇文章，本公众号会每日分享攻防渗透技术给大家。

  

  

靶机地址：https://www.hackthebox.eu/home/machines/profile/235

靶机难度：中级（4.7/10）

靶机发布日期：2020 年 7 月 20 日

靶机描述：

Cascade is a medium difficulty Windows machine configured as a Domain Controller. LDAP anonymous binds are enabled, and enumeration yields the password for user r.thompson , which gives access to a TightVNC registry backup. The backup is decrypted to gain the password for s.smith . This user has access to a .NET executable, which after decompilation and source code analysis reveals the password for the ArkSvc account. This account belongs to the AD Recycle Bin group, and is able to view deleted Active Directory objects. One of the deleted user accounts is found to contain a hardcoded password, which can be reused to login as the primar domain administrator.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/KLoTw1Op24K7bYlV0ty3cYaXKEJ4LukvDSWzMiawENwjkzichAIcDuC1uBxuMfSj29gpevgLGPPeMeHCwKyGiaZ5w/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/u542j6DNZqibANrqyuqYq3KwXicNtAI4PkbTngiacTDG6oGIUU4zWbT9cCpyZc4VZdBTedLFLr1Xzw3kQE9cxkCqw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Ffv0EPcbq7gH6aqjOkn7TaxjIzicxxZAXyDZGpkmftnmsZr14yStPcqW8LTBdjqHBtJl0mehGp8Sldg3msrgvoQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOnGM2WhjibOKh0PPecN2963T4et5rrxC46YnGXjKIYbnoUpf6ic3UiczSPLxmVPDLuPycX1icuXUP6VQ/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.182...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOnGM2WhjibOKh0PPecN2963ibNVIcGiap3rnVkKrmcg2KSDdkv7LkFDJN2l83l1kOGWj2VSWllzcnicQ/640?wx_fmt=png)

nmap 扫描发现域为 cascade.local，另外开放的 LDAP（389），SMB（445）和 WinRM（5985）都可用... 开始

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOnGM2WhjibOKh0PPecN2963UPYKHES7mhH13USjjRTbZvwvA9luYplVFMx2R3BTY5hYUQsAoUqJRg/640?wx_fmt=png)

```
ldapsearch -x -h 10.10.10.182 -p 389 -b "dc=cascade,dc=local" > test.txt
```

enumdomusers 和 rpcclient 都枚举没什么信息...

利用 ldapsearch 枚举出了重要信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOnGM2WhjibOKh0PPecN2963n1CaVQ4ibBFcshTdVu1rKnPX4ygZFQPqsGyI5Tgn1qCEjaKiaJ43ORdA/640?wx_fmt=png)

信息量很大，我直接查找 pwd，password 等关键词... 发现了用户名和 base64 密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOnGM2WhjibOKh0PPecN2963GKWflF9DqSzqRbLS6juibrZIAoMXBF0t6hYscs4ab4qlPg104E2icqug/640?wx_fmt=png)

编译下即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOnGM2WhjibOKh0PPecN2963DClic0SZTtd0PhmbamD9VNs2tSm3icFRuTtmntL6LLdN8mbMWN52t2Xg/640?wx_fmt=png)

直接查看了 r.thompson 存在的共享目录...

进入 Data... 发现 Email Archives 文件夹包含 Meeting_Notes_June_2018.html，其中显示了一封电子邮件... 下载

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOnGM2WhjibOKh0PPecN2963QkKrloPr4beL99IZAs0ia0oj8pWfDcUU6x3GT4TqiaxiaUiaW7xlgkuyhw/640?wx_fmt=png)

电子邮件交换提示存在一个具有相同密码的 TempAdmin 帐户作为默认的管理员帐户... 非常重要的信息，只需要枚举出 TempAdmin 密码即可知道管理员密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOnGM2WhjibOKh0PPecN2963jC4kZ18HpzTPcYwLPYiad8hUyoSjyhlibr2YNkFsgSsib2qp8VRWJ6Jqw/640?wx_fmt=png)

还发现 Logs 文件夹包含 Ark AD Recycle Bin 和 DCs 文件夹，这些文件夹又包含分别为 ArkAdRecycleBin.log 和 dcdiag.log...

继续下载...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOnGM2WhjibOKh0PPecN2963aX2SGuUTiaDMBXiaXGuYiaRoCJ70W48C8GgRic1cnbMYNYDBg1rodvz8zQ/640?wx_fmt=png)

ArkAdRecycleBin.log 包含名为 ARK AD RECYCLE BIN MANAGER 的程序的文本日志...

该日志通知我们该程序正在 ArkSvc 的上下文中运行，并且 TempAdmin 帐户已移至回收站... 非常重要的信息！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOnGM2WhjibOKh0PPecN2963vcbV3xrf0cL0Vib6nqyEvxXKElhYknFIPwuwGwQxkMrvMZ5MFK8CFoQ/640?wx_fmt=png)

继续往下看 Temp 包含用户 r.thompson 和 s.smith 的文件夹信息，可以在 s.smith 的文件夹中找到 VNC Install.reg 文件... 下载

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOnGM2WhjibOKh0PPecN2963A7h3iaswKja6ibZicljeiaMURl3ZE0WH8vicXDxLyYhmf0rcAQf0siclX5lg/640?wx_fmt=png)

打开发现它似乎是注册表信息，桌面远程控制程序 TightVNC 的设置的信息等...

其中找到的注册表文件包含一个 Password 属性，十六进制的密码值...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOnGM2WhjibOKh0PPecN2963HcZ57gmPrce6mYaRyiaXSwNq3azabaEBSRoH1APlPMzbOoMB0shyb9g/640?wx_fmt=png)

```
https://github.com/frizb/PasswordDecrypts
```

google 搜索发现了 vncpasswd 和 MSF 来进行破解... 该文章很详细的解释了... 利用即可

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOnGM2WhjibOKh0PPecN2963qKFxe6gVyZND84IyVv0ShKibfibuSyQicoplVPaKiaXngicrHo5EuicKW4tQ/640?wx_fmt=png)

```
irb
fixedkey = "\x17\x52\x6b\x06\x23\x4e\x58\x07"
require 'rex/proto/rfb'
Rex::Proto::RFB::Cipher.decrypt ["6bcf2a4b6e5aca0f"].pack('H*'), fixedkey
```

可看到顺利 MSF 解密成功...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOnGM2WhjibOKh0PPecN29632dbCEfyiaTTFEAjXthXaOr7FQIHX36WQEDgkImtarAHn7XRjibtQEKpg/640?wx_fmt=png)

利用用户名密码登录，并获得了 user_flag 信息...（这里用户名很简单的就能知道... 当然如果用户非常多可以进行爆破枚举）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOnGM2WhjibOKh0PPecN2963ocKoq7XbnYVcsPKpLjUQibNZq7FUKVZLyauz43BtacH5ibztiawXic44zQ/640?wx_fmt=png)

该命令显示该用户是 “Audit Share” 组的成员，并且登录脚本 MapAuditDrive.vbs 已分配给该帐户，Active Directory 登录脚本默认情况下保存在 NETLOGON 共享中...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOnGM2WhjibOKh0PPecN2963AuicablzxS4iaiaF7G6BNkWVOtrye6HgunWdWzY9c83uZouthnsZjN8sA/640?wx_fmt=png)

枚举发现了 NETLOGON 共享中存在 MapAuditDrive.vbs 和 MapDataDrive.vbs 文件下载即可...

在 Audit$ 下 DB 共享中存在 Audit.db 库文件... 下载

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOnGM2WhjibOKh0PPecN2963Ffa3uYHmKZStE5xrZJPH4LpQDrp07kXozUpHllChVrGHPy3kPuZ4lw/640?wx_fmt=png)

这里两种方法都能获取密码 hash 值...

我这里利用 Audit.db 读取库内容获取... 这里我利用了 sqlite3，或者也可以使用 sqlitebrowser 都行...

然后读取了 Ldap 信息.. 包含了密码值...

这里提下另外一个需要在 win 上利用 dnSpy 分析两个 vbs 也能获得...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOnGM2WhjibOKh0PPecN29630B5vecIgxLMliciauNWH0j5WuxokNnsHnCZsSYqJbJ8CCYzu5D49qMfA/640?wx_fmt=png)

这里大部分编码是利用 dnSpy 解析 CascAudit.exe 和 CascCrypto.dll 程序写的例如 1tdyjCbY1Ix49842... 这里可以在 Audit 目录下就存在该程序，下载分析即可...

这里我直接把 hash 值复制到 google 出来的结果，应该是有人写好了，但是我分析了下...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOnGM2WhjibOKh0PPecN2963ElCkBjeSMYZwcHGZqeCgAdqJia1SpTe0o9osJkc1fTfVkHc92yJDUHg/640?wx_fmt=png)

目前知道了密码，枚举下存在的用户信息... 利用即可

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOnGM2WhjibOKh0PPecN2963RQCtI43m0aJiaAPeDgzLntEjjzgicH1F1l02Sic9oo8RjOKdW8gqJu75g/640?wx_fmt=png)

前面已经知道两个重要信息，一个是管理员用户和 TempAdmin 密码一致，另一个是 TempAdmin 被移到了回收站...

查看到该用户被标识为属于 AD 回收站组，Active Directory 回收站是用于恢复已删除的 Active Directory 对象，例如用户，组，OU 等，这些对象保留在 AD 回收站中，它们的所有属性均保持不变，从而可以在任何位置还原它们...

这里可以使用 Get-ADObject 枚举 AD 回收站中的对象，并过滤具有 isDeleted 属性的已删除对象即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOnGM2WhjibOKh0PPecN2963JicvTVLXYliccAheSWCpJy15wgpcngGpLiaZHkr7ddUkbthpiahIW6MIoQ/640?wx_fmt=png)

```
get-addomain | select DeletedObjectsContainer
Get-ADObject -filter 'isDeleted -eq $true -and name -ne "Deleted Objects"' -includeDeletedObjects -property *
```

首先确定使用了 ArkSvc 帐户将 TempAdmin 帐户移到回收站，然后利用 Get-ADObject 恢复...  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOnGM2WhjibOKh0PPecN2963rVq7fVJ3vmdOU0Yib8B5fKOVAvTeKsJf3cn8p5vpEAn6BGZSHgMsdjg/640?wx_fmt=png)

可看到恢复后的信息中存在 Pwd 信息... 这是 base64 值...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOnGM2WhjibOKh0PPecN29639fl1FsDVbX0eWYO2p84Buklrj2Kg2ULB3he3C4weZdj7RgCnjYY8cg/640?wx_fmt=png)

base64 -d 编译后获得密码...

然后 winrm 成功登录管理员权限界面... 获得了 root_flag 信息...

这台靶机都是一环扣一环，域信息很明显，最后 google 搜索了很久回收站的恢复命令... 又学到了... 加油

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台中级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

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