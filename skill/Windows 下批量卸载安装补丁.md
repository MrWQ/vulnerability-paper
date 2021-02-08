> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/uHN7CRjSuhbBcHm0uil8mA)

![](https://mmbiz.qpic.cn/mmbiz_gif/3xxicXNlTXLicNjoNVg3ssI3Y0DyakuNiaRcPHnJ2bcEJ1xEKMcWJVCMkGtgKPreu5mettSVS63YYVSzCTiaLWWnOw/640?wx_fmt=gif)  

1. 以管理员的身份运行 cmd，输入命令：wmic qfe get hotfixid >> c:\list.txt

![](https://mmbiz.qpic.cn/mmbiz_png/3xxicXNlTXL8zHfJNsJ4zibI6rKgHGnA9wnHxxeHfcj99TrH2LCOkLdicA1jrTDBNQyialSVMq8RJIkMHl1cqUWSpg/640?wx_fmt=png)

2. 打开 C 盘下的 list.txt

![](https://mmbiz.qpic.cn/mmbiz_png/3xxicXNlTXL8zHfJNsJ4zibI6rKgHGnA9wsX1tHS7UciaaT1suDqJas8fqWynnxY2hCL5sl5cLMUq4l0vJSCk1V4A/640?wx_fmt=png)

3. 将第一行的内容删除后保存

![](https://mmbiz.qpic.cn/mmbiz_png/3xxicXNlTXL8zHfJNsJ4zibI6rKgHGnA9wuYuTBicgyqkZYc3KBJeb5KtrU35nxU3FKpq28ddVaPreVL9GWMaAXSQ/640?wx_fmt=png)

4. 回到 cmd，输入命令：for /f %i in ('type c:\list.txt') do echo wusa /uninstall /kb:%i /quiet /norestart >> c:\uninstall.cmd

![](https://mmbiz.qpic.cn/mmbiz_png/3xxicXNlTXL8zHfJNsJ4zibI6rKgHGnA9wGXkJbtYlxXmjECPk4WM8pm05sGcDFJM976d5LnOeQaPtXCgaxIQqUw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/3xxicXNlTXL8zHfJNsJ4zibI6rKgHGnA9wFibiaguXk1vPwvicwHfwrgYRjRbUxRHAjGmXNPLDxHprBZoia3NjyKvDQw/640?wx_fmt=png)

5. 选择 uninstall 文件右键 “编辑”

6. 打开文档之后，需要将 kb:KB 全部替换成 KB：

![](https://mmbiz.qpic.cn/mmbiz_png/3xxicXNlTXL8zHfJNsJ4zibI6rKgHGnA9wic3BeOa47boQol1GKhJzdRwHeUf8x0QNMhTibichoJW0b9XVn93lzFMBg/640?wx_fmt=png)

7. 单击文本窗口上的【编辑】，选择【替换】，替换完成后保存

![](https://mmbiz.qpic.cn/mmbiz_png/3xxicXNlTXL8zHfJNsJ4zibI6rKgHGnA9wfoYYwGXwQfv593ESGW2C59klUiak1gFxBmibJ3CPdia4gFBibY0yL8QRpQ/640?wx_fmt=png)

8. 双击运行 uninstall.cmd，等待运行结束，重启计算机就可以了

![](https://mmbiz.qpic.cn/mmbiz_png/3xxicXNlTXL8zHfJNsJ4zibI6rKgHGnA9w0VE2yDG2QiarHNmRGOk0yyQzHQbmic8ef4whvI5VE7ZVwCZXViag4LTNg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_jpg/3xxicXNlTXLicjiasf4mjVyxw4RbQt9odm9nxs9434icI9TG8AXHjS3Btc6nTWgSPGkvvXMb7jzFUTbWP7TKu6EJ6g/640?wx_fmt=jpeg)

推荐文章 ++++

![](https://mmbiz.qpic.cn/mmbiz_jpg/US10Gcd0tQFGib3mCxJr4oMx1yp1ExzTETemWvK6Zkd7tVl23CVBppz63sRECqYNkQsonScb65VaG9yU2YJibxNA/640?)

*[Windows LPE 攻击（CVE-2018-8120）](http://mp.weixin.qq.com/s?__biz=MzAxMjE3ODU3MQ==&mid=2650460994&idx=3&sn=3b40620b1906b3f73c8c32becae5da82&chksm=83bbb6a6b4cc3fb05d23dae6b16b5667e80ed1dc2d7fa4be64009261f0cbdee01d80f666341e&scene=21#wechat_redirect)  

*[Windows 远程桌面服务漏洞（CVE-2019-0708）复现测试](http://mp.weixin.qq.com/s?__biz=MzAxMjE3ODU3MQ==&mid=2650460988&idx=3&sn=15486923d1da8656ea256d13739e3311&chksm=83bbb6d8b4cc3fce9ae5a328c32c0a24cbba183252da93ee253c38de098d12474198d0f0865d&scene=21#wechat_redirect)

* [利用 msfvenom 与 metasploit 入侵 windows](http://mp.weixin.qq.com/s?__biz=MzAxMjE3ODU3MQ==&mid=2650460656&idx=3&sn=1f45cd2e497185255779bc3c2d9e0b6d&chksm=83bbb414b4cc3d021b0932bccf310ca0f46760679544304f220e93fc0fdef5e660b3240bbb7a&scene=21#wechat_redirect)[](http://mp.weixin.qq.com/s?__biz=MzAxMjE3ODU3MQ==&mid=2650448610&idx=1&sn=8056fa278081890adc388d4490f33695&chksm=83bbc706b4cc4e105f26110dfc5403ba821486e34554440d5bbbb29ced857f11fb0125d602eb&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_png/3xxicXNlTXLib0FWIDRa9Kwh52ibXkf9AAkntMYBpLvaibEiaVibzNO1jiaVV7eSibPuMU3mZfCK8fWz6LicAAzHOM8bZUw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/NZycfjXibQzlug4f7dWSUNbmSAia9VeEY0umcbm5fPmqdHj2d12xlsic4wefHeHYJsxjlaMSJKHAJxHnr1S24t5DQ/640?wx_fmt=gif)