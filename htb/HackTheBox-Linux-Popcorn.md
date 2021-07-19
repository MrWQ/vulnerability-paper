> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/GhWIlk6KRahgBq1ZJRItQw)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **95** 篇文章，本公众号会每日分享攻防渗透技术给大家。

  

靶机地址：https://www.hackthebox.eu/home/machines/profile/4

靶机难度：初级（3.6/10）

靶机发布日期：2017 年 10 月 11 日

靶机描述：

Popcorn, while not overly complicated, contains quite a bit of content and it can be difficult for some users to locate the proper attack vector at first. This machine mainly focuses on different methods of web exploitation.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/gOGib2VkpLWkbtKmMsQqySMxAsrxHvBeChSJUKPDZTQH3Gde0ayHZZrpyZNH0ibCdnibeicWkNf9sQ9ldtYghV6EUA/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/VHdxGs4QuYyTh2Ph5K8FUYeMSJgG10R6UvAkBSAhsibgPr3lEDRbtNqZKEuMkIHTcB9sm1tjN38OW3gSoLFfDlA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljDjkRKLs2SmZ04b1WylYzoiaVpBQNuTvrO2ql0icib2LVjpph2V4HeLYAgA/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.6....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljD5rwIy9gIXxDcTbQxCDkcHibjlB2qJTD6rdwHTd33JmiaSeSVmBJf5ib2w/640?wx_fmt=png)

Nmap 只发现两个开放服务， OpenSSH 和 Apache... 

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljDmZxxQFHVSJIceK8icZqYwbrDVBo8RYh8Wrmiab6EdsmuibUN7vkhFrGTg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljDv7lg1kiaAAy53e1JqgtMR6zBzIo42ocOj2AXQVKnrHASCOIDibVh5XYA/640?wx_fmt=png)

访问 web 后，没任何信息，进行了页面目录爆破...

发现了 torrent 目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljDvNhPtusMPQhtGxgibvC71Jy8dHc0wqTPPjVSt6Vl6RTqxGZ3jg121fA/640?wx_fmt=png)

访问后这是可登录页面，进行注册个账号密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljDwbEUg0I5l9ZmSCpumQ0HgWOLWxexx9r8KicjkEr0wxKZD9dEj4p2kCA/640?wx_fmt=png)

进来后发现有 upload 上传功能...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljDRyCC3FYQO05ayIFpqhT4thKibcvPwnxEh9jcfbzMFCgogekYP6qZ5iaw/640?wx_fmt=png)

通过随意上传一个文件... 提示只能上传 torrent 类型的种子文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljDUO2SDGcfCP88wg9JQavaG3WwSyxGpoAian66PMxwKXiawzJ9lxmpMkWw/640?wx_fmt=png)

这里随意上传了种子文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljDDcvxj4xKa65jamuop4jajGxdJqk2ZvD7thj8MsHgE7mR6ZE6XEfyLw/640?wx_fmt=png)

上传完后提示成功并跳转到了此页面... 此页面存在 png 格式的文件... 存在 upload 目录底下...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljDu1GAm6icSbVLQJoWqic9uRx2vuQUxQMqkOzCX6LwhPCyGWjNRTM9wdGg/640?wx_fmt=png)

通过这里上传 php_shell，提示失败，不允许...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljDTeiaH3jWDIverJB8HGR0VH6kGT9M3YcGNjS0h98wRHy17uhGgt0QUEw/640?wx_fmt=png)

这里我编写了简单的 cmd_shell....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljDoxmy8AooriaZ502JDFJ9nlqk8criamtVnNGnicwBpXXMfgpSt4tUnvVOw/640?wx_fmt=png)

通过 BP 绕过了靶机上传的限定机制...

要绕过第二次检查，这里可以使用 Burp Suite 截获该请求并修改该请求内容，只需将 POST 数据中的 application / php 更改为 image / png 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljDYO0ajfNH6xIBx0yl78HRm7KlRMbJnYoULkOqLSToSweibwC5ZlRNhfQ/640?wx_fmt=png)

成功在 upload 上看到上传的文件... 他会以乱码的形式上传进去... 无关紧要

这里执行后发现是正常的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljDUicwxP8TjyUl9bWCNt5hE5YtjJknG1f8cu320TOTedZnh7qtqJCLXYg/640?wx_fmt=png)

通过靶机自带的 nc 反弹 shell 获得了 user 信息...（这就不多解释了）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljDP71CXhf7MFDshurxcoAKzI2C8HrjCXohr3C8kgO4GeUW6CsFI6oeyQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljDV13uZDZrDlVC4libVsxstqv4jtKy7yiamXgConENpJiaRanZkhWKXMSsw/640?wx_fmt=png)

使用 ls -lar /home/george 会在. cache 目录中显示一个不常见的文件 motd.legal... 还可以看到内核来自于 2009... 存在 1.1.0 的 CVE-2017-14339 漏洞... 这是个恶意漏洞会导致 box 崩溃... 具有文件篡改特权升级漏洞....

查看 exp 本身内容就是利用本地的根添加一个新用户提 root 权限...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljDOdvsMmibLWxRbVp1Yicp8wxmHnmt62LgSEoUVztW0UpDmHyDFcKURbxw/640?wx_fmt=png)

这里通过 copy 内容利用 Vi 创建 EXP 即可...

成功提到 root 权限...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljDVt47AibWdyl1WMwkP1xpF7DHSmLp5jeW2MRYE3RXjgrH7SlTNIUROkA/640?wx_fmt=png)

获得了 root 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KM2dgwuzs0iaPaMvv8kapljD8gnuEB3icRgpnfjaHPTEBBWt3eGzyKgOSOCgAOQia0lVLu2xNeLn1MdQ/640?wx_fmt=png)

这里还有几种漏洞可以利用，可以自己进行尝试.... 方法参考 EXP 内容即可... 都可提 root 权限...

  

这里没什么难度，文件上传机制绕过... 自身存在的各种漏洞挖掘即可... 然后利用漏洞 EXP 提权...

适合初学者学习.... 加油！！

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台简单的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

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