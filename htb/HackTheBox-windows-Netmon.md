> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/Xgmz50KjAjvmiF7PMhk9Mw)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **70** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/pPxbtaV6eew1LBicCIVu68QpfvtXIqcKjMYt0xItpUeKekt1QdZqLL3ShDRgb9WAILZ8GZSHGeDbBAicL8f7MstA/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/177

靶机难度：中级（4.7/10）

靶机发布日期：2019 年 5 月 18 日

靶机描述：

Netmon is an easy difficulty Windows box with simple enumeration and exploitation. PRTG is running, and an FTP server with anonymous access allows reading of PRTG Network Monitor configuration files. The version of PRTG is vulnerable to RCE which can be exploited to gain a SYSTEM shell.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

  

![](https://mmbiz.qpic.cn/mmbiz_gif/C8q1034zkwCRacW6WDFYukwzHB3qVce5SZJ3HfVZ4pffic5sdkg6g0I4v5dyFDGebxk1zN99ibwvV65kBsxBgDeQ/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_gif/yQJ56734ZYGfTXlb9EfkjcOm3QV6qvXC55Xmjs4Ratr9cy6KXiadaRnpjvY67FtHd8iaWsyNBAASVrJ6INp7lgcg/640?wx_fmt=gif)

  

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOicu8ibXApUeVg9m3YuR2MXGFicqn7fplzXXMXNLj89TjTVFWhrLAKz6iatWbibUv2iahRLUqaRQC8HDZw/640?wx_fmt=png)可以看到靶机的 IP 是 10.10.10.152.....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOicu8ibXApUeVg9m3YuR2MXGxJe6DIv72L6NykBv63LHmiaEJJvRSqu6LMT51bA3DPwnlnnFOsaLLRQ/640?wx_fmt=png)

nmap 查看到开放了很多端口...

主要看 80 端口运行着 PRTG，21 的 FTP 和 SMB 匿名允许访问...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOicu8ibXApUeVg9m3YuR2MXGNoRheTyoEw5trApR35iac5JUxYM7lP8fPrnOWc5OLC8Z1G804Caf2Hg/640?wx_fmt=png)

一进来不到一分钟就获得了 user.txt.... 额....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOicu8ibXApUeVg9m3YuR2MXGb9X9ibwmE8pMkEfYFcwj5jQgwk6oKOKN0IYOzLvXoic3wWrVNBVrT1CQ/640?wx_fmt=png)

访问 80 的 PRTG，这是 PRTG Network Monitor 的 web 应用程序，用一些默认的账号密码登陆，无法登陆...

思路是找到凭证，我回到 FTP 查看试试...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOicu8ibXApUeVg9m3YuR2MXGux20Gxr1bjDVib1AOEQ1Zjs9905CgsaLPYK03yy11oNc5MibyyxzgoZA/640?wx_fmt=png)

在目录下发现了配置文件... 下载到本地查看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOicu8ibXApUeVg9m3YuR2MXGichkTfOQDabHUUkt6hOKbNDNj2miaQVqKpebNwOnH2jMzBQQ2lF9Bu5w/640?wx_fmt=png)

在 old.bat 文件中发现了账号密码...

使用 prtgadmin，PrTg@dmin2018 还是无法登陆，我后面又查看了会，没发现信息了，看到 2018 我改成 2019 成功登陆进去了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOicu8ibXApUeVg9m3YuR2MXGJXe0DuNRIfia0OgI711OWQrU5Z8UeK4LM7J0Zuknb3Bia15jiaYPu8fHA/640?wx_fmt=png)

PRTG 是一种监视工具，支持一整套传感器，例如 ping，http，snmp 等。服务器本身已添加到设备列表中，因此可以可以向其中添加传感器...

![](https://mmbiz.qpic.cn/mmbiz_gif/yQJ56734ZYGfTXlb9EfkjcOm3QV6qvXC55Xmjs4Ratr9cy6KXiadaRnpjvY67FtHd8iaWsyNBAASVrJ6INp7lgcg/640?wx_fmt=gif)

  

二、提权

![](https://mmbiz.qpic.cn/mmbiz_gif/X9SaMyWcMHNxeXEFX95ictyus2sNOw3vyzFbziaHyehUfGQJMZ1eHYKkZ7haph6cAUzGTF0Cq317B52jnxeCbB8g/640?wx_fmt=gif)

方法 1：

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/lkClP1nMRFcOdV3wgl4RTQeP5eUwXyxvUsCRbYWhcvWpqAIiap0vy2vdtcVrIlE31dS5VeWUXk6onHQooLuttcw/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOicu8ibXApUeVg9m3YuR2MXGh9R7IicsYFeW2m9SobXQCFxWdE0AwzRZ8OibvO2jYXapeo9urbNRgvsw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOicu8ibXApUeVg9m3YuR2MXG1c2AOibAP1nBib6HicpsjqBFWZhwG0icGuJJV0NSazFcWv4pr0gAeAapicg/640?wx_fmt=png)

在 10.10.10.152 服务器上单击添加传感器，然后选择 EXE/Script sensor...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOicu8ibXApUeVg9m3YuR2MXGeTQOzHF3hwrEPNOFNico2xL1dzBjicoKBnWeTotTAqpVQkY12pFa03icg/640?wx_fmt=png)

好像可以写入 shell... 测试看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOicu8ibXApUeVg9m3YuR2MXGg88kUibjAKo4Oyo5cHXHYZASiaU7FCTzObKP3FQ3ib9zhJbOOCPv1BY0g/640?wx_fmt=png)

经过写入 ping 测试，本地看到数据包传输了，说明可以写入 shell 提权...GO

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOicu8ibXApUeVg9m3YuR2MXGiaxpVf82qfbguTibRBelgQo7hMx14fEsvO69WFxfHjA645f6lLlxL7Pg/640?wx_fmt=png)

通过 powershell 上传成功了 shell，但是没反弹回来...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOicu8ibXApUeVg9m3YuR2MXGqGl0iasbbMjAWu2K1L4PFDT0eiaNbFv4AHxtooRXykTpdzX0eoubdajA/640?wx_fmt=png)

```
cat dayushell.ps1 | iconv -t UTF-16LE | base64 -w0 | xclip -selection clipboard  
--由于转换 出的数值过多，利用xcilp进行黏贴
```

Windows 和其它平台不同，它有悠久的历史包袱，和现代大多数操作系统对 Unicode 支持的共识不同，它的 API 不是基于 UTF-8 而是基于 UTF-16 的... 所以我这边进行了 UTF-16LE 的转换... 延申知识：

```
[参考](https://blog.codingnow.com/2019/05/windows_utf16.html)
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOicu8ibXApUeVg9m3YuR2MXGso1ibAuoQLOVb72wkWJnIIcax78K0XgTO9UBIKQT72sbrSKIxyfK8pQ/640?wx_fmt=png)

```
PleaseSubscribe | powershell -enc + 黏贴
```

利用 powershell 将 sp1 转换的 utf-16 值上传... 成功提权...

![](https://mmbiz.qpic.cn/mmbiz_gif/X9SaMyWcMHNxeXEFX95ictyus2sNOw3vyzFbziaHyehUfGQJMZ1eHYKkZ7haph6cAUzGTF0Cq317B52jnxeCbB8g/640?wx_fmt=gif)

方法 2：

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/lkClP1nMRFcOdV3wgl4RTQeP5eUwXyxvUsCRbYWhcvWpqAIiap0vy2vdtcVrIlE31dS5VeWUXk6onHQooLuttcw/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOicu8ibXApUeVg9m3YuR2MXGtyIVwfs6A1jnVMcXzI32iaS3fJxCCxUxRwzSvISwyxDJBXDZ8DXZatg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOicu8ibXApUeVg9m3YuR2MXGWicOaib4IjIcNfjW7RxEkTcJp0hbnw7o0CSKOW8N9RzlnSicAnwpMlVzg/640?wx_fmt=png)

可以看到，还是利用注入，在靶机创建了新的用户名和密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOicu8ibXApUeVg9m3YuR2MXGo0X1zhN3XPfRZrKJrClS3R1VXYuPS6fLkibt1MBQcX3v0XhQzmyVNNg/640?wx_fmt=png)

可以看到通过前面的方法利用 psexec 进行提权成功...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOicu8ibXApUeVg9m3YuR2MXGeXUatMWOC17JgUtUaMyqQBl568kH2MqSJySicBsB2J6u81CnGFeLhicw/640?wx_fmt=png)

当然这里也可以利用 PRTG 漏洞的 46527.sh 的 EXP 进行创建新的用户名密码...

![](https://mmbiz.qpic.cn/mmbiz_gif/X9SaMyWcMHNxeXEFX95ictyus2sNOw3vyzFbziaHyehUfGQJMZ1eHYKkZ7haph6cAUzGTF0Cq317B52jnxeCbB8g/640?wx_fmt=gif)

方法 3：

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/lkClP1nMRFcOdV3wgl4RTQeP5eUwXyxvUsCRbYWhcvWpqAIiap0vy2vdtcVrIlE31dS5VeWUXk6onHQooLuttcw/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOicu8ibXApUeVg9m3YuR2MXGBwzYanzT5f6HZO3RL91DxdiaSXrggjnoiaxZRksatg9GqeoeXdjvI3OA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/pPxbtaV6eew1LBicCIVu68QpfvtXIqcKjMYt0xItpUeKekt1QdZqLL3ShDRgb9WAILZ8GZSHGeDbBAicL8f7MstA/640?wx_fmt=png)

可以看到还有很多方式可以提权... 这里我就不说了，放在玄学方法 3 里给大家拓展，加油!!!

这台靶机也学到了很多东西，好好复习！！

由于我们已经成功得到 root 权限查看 user.txt 和 root.txt，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

  

![](https://mmbiz.qpic.cn/mmbiz_gif/C8q1034zkwCRacW6WDFYukwzHB3qVce5SZJ3HfVZ4pffic5sdkg6g0I4v5dyFDGebxk1zN99ibwvV65kBsxBgDeQ/640?wx_fmt=gif)

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