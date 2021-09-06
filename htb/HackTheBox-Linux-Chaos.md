> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/UUbfWZDzuPDQ8D6lFMEFuQ)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **146** 篇文章，本公众号会每日分享攻防渗透技术给大家。

靶机地址：https://www.hackthebox.eu/home/machines/profile/167

靶机难度：中级（5.0/10）

靶机发布日期：2019 年 4 月 25 日

靶机描述：

Chaos is a “medium” difficulty box which provides an array of challenges to deal with. It requires a fair amount enumeration of the web server as well as enumerating vhosts which leads to a wordpress site which provides a file containing credentials for an IMAP server. The drafts folder contained sensitive information which needed cryptographical knowledge to decipher. The decrypted information leads to a page hosting a vulnerable Latex application which helps to gain a foothold. Password reuse helps to land a shell as a user but in a restricted shell which can be bypassed by abusing a GTFObin. Escaping the shell gives access to the user’s firefox folder containing saved logins which on decrypting gives access to a webadmin console and the root shell.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/Fms1OiaYewPh3x0qgfYJc4OlyqAM94frFbPucnlNicbAEfQBUiadH22Tjm93pUGLZzhvficphibRkFOYZicvTkMPePyQ/640?wx_fmt=png)

  

  

  

一、信息收集

  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPEOX8eLxVUH8s8y8f8wvfQFxibNs8KBwWhxmUE8y09c69ViaYkiagYibc1Fg/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.120...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPECI8icliaEhOCqXnY5fpPGWIicxcW3h6DWIhnjZvVWNhN9zaX9Csmvuwbg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPErN5sia7JsuHPVCUd4EbsNhfPruwMHj1wh1knTO9DZ7CicoT2Xv9ibluGQ/640?wx_fmt=png)

最近 nmap 扫描 HTB 端口，速度效率太慢了... 吐血...

这里使用了 Masscan 进行扫描... 发现开放了挺多端口...

在利用 nmap 指定端口进行了扫描...

端口 80 上运行 Apache，端口 10000 上运行 IMAP 和 POP3 服务器的两个实例，以及 webmin 控制台....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPE3mfsMDk6aetM8KJaFTw0mghSSTg7orjcjGveX59CVjc1gVDc1MwwgA/640?wx_fmt=png)

不允许通过服务器的 IP 地址 10.10.10.120 访问该站点... 必须通过其域名访问该站点... 添加 hosts

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPEY8WIAwEa4GOTTRZSmfDgJIwJbHXkESf0WhmshmHQXX4QgLP0SBcWPA/640?wx_fmt=png)

简单爆破了下，发现了 wp 页面，wordpress 页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPE464CMocSibib0z9rTtJI30aJibaUd0v9evz1SenCo7MANLM8gA3elogkg/640?wx_fmt=png)

果然... 这里提示需要密码才能查看信息...

直接上 wpscan... 枚举

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPELevLibbcic4YYqolkvRZIbrQjfnpgx6jPa84vjfxWhK2iceQkaSnguhRA/640?wx_fmt=png)

枚举发现了用户名：human

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPEazPpQo6tFACKvInxOpVMh6icexzqZpP0E1rKDQ2UPPY8x7GWDBQcKrA/640?wx_fmt=png)

在 passwd 框中输入了用户名 human 成功进入...

获得了 ayush 用户的密码... 这里信息收集告一段落...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPEvhwwGxtEsJLllFic0KiaibJaD1wF7OmVFcE9JuSXN9IUDWPkWDcKwP1ibQ/640?wx_fmt=png)

nmap 可以看到系统正在使用开源 IMAP 和 POP3 电子邮件服务器 Dovecot 在端口 143、993 和 995 上运行着... 需要利用 openssl 工具，可以监听该服务下的信息内容...

https://wiki.dovecot.org/TestInstallation

这里有一篇文章专门讲述了该页面的命令解释... 作为利用需要简单了解阅读下...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPEU84OKVA8nQMIRHyJlN6VKFrU7DkbATENkG0aOCaGicPlTic1X6xJb63g/640?wx_fmt=png)

```
a LOGIN ayush jiujitsu
b select inbox
c list "" *
d select Drafts
e FETCH 1 BODY[TEXT]
```

验证用户密码登陆成功 -- 显示出可用邮箱 --select 与邮箱进行交互 --FETCH 查看邮箱内容....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPEbL9xxJH3hNDpjIxoRh4pNbYRconk4BXdjeBHFTU4ytcx5j4tRHibuKw/640?wx_fmt=png)

发现了两段 hash 值... 都复制到本地看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPEmWRdCnkrhwtXsGTicYxnPDhKqoQHaK9niasD0ZfY93TMQSuyGv8A102Q/640?wx_fmt=png)

可以看到前一段是加密的，通过邮件提醒，另外一段是解密前面一段的密匙...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPEGiaXcRPiccibIYvV8WEGMfPIO4bXuLwZx1Yof8UjTdtHg7e44gurt4PsA/640?wx_fmt=png)

通过代码可以了解到一些内容：

该 filesize 变量解释是该变量的长度为 16 个字节... 例如：一个 39 字节大小的文件将导致 filesize 变量为 0000000000000039

该 IV 变量用作数据加密的初始化向量... 它的值将是第 16 个字节的文件对象...

该 encryptor 变量表明在 CBC 模式下使用了 AES 加密，解密期间应使用相同的内容...

该 with open(outputFile, 'wb') as outfile: 和下面的显示，两行 filesize 变量（16 个字节）和 IV 变量（也 16 字节）被写入到输出文件中（即，enim_msg.txt 之前的任何加密的数据）被写入... 由于 IV 在 encryptor 变量中使用了，因此 IV 在解密期间也需要使用...

通过以上解释，编写了简单 python 脚本...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPEPr7xJicTuYZKrCcj9CmtRRVjkbYuubPVsPVSXKv9KzZ6AuiaUC8CxqGw/640?wx_fmt=png)

获得了一串 base64 值... 转储后读取，获得了域名地址...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPEHOx9sXiaZ50nujAQMFLyWQDx8kVIWJ88bCticjH7HDNrEeiaxK4cO38Fg/640?wx_fmt=png)

通过前面的 base64 值转储后的文件提示，这是由 Chaos Inc 创建的自定义 PDF 应用程序...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPE1SqWVZ9GwffVRMIthb6WhTY1dWl6rsc07SmgmTt7dx7FZD7XYfAqjQ/640?wx_fmt=png)

bp 拦截测试，发现这是 Latexpdf.... 找下 EXP 试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPE77iaaibFLDicqdKPs1UDSHrng3ibOF6chAjvgIxqs1wzMZmU281COVIkLQ/640?wx_fmt=png)

google 搜索，挺多的文章...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPEowriccgrxicRElxbKqpN19b26xPsRacXHut0xtcMNuxfMxWlwoT08zcw/640?wx_fmt=png)

发现存在注入... 试试利用

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPEDibeblroNPh6hYbyBiayBudE6UBC8TialObTFCLQalBMrdKAcsZqdtSiag/640?wx_fmt=png)

通过简单 shell 替换写入...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPEnNaXjVDH3Dk6egPxwLmnwUFjWvsGic2cwy4H3cv97dE7QEQYiaRBicqIA/640?wx_fmt=png)

获得了反向外壳 www 权限... 检查发现除了 tar 命令外，基本都不能使用，应该是在黑名单或者规则限制中...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPEsSNWWOs4a8D6VKcC6cr8UbExJbiargvF94tCAGwbGBI506PeGMibaPkQ/640?wx_fmt=png)

由于前面 wordpress 就发现了 ayush 用户名和密码...su 进入了 ayush 用户权限外壳中...

但是使用命令还是不行，还在 rbash 环境下，需要绕过 rbash，根据报错提示...

设置正确的 PATH 环境变量后，正常可以使用了，获得了 user_flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPE8s2CugEYQiccGEZVDCHoqzljHqvaPNdamIyiceKbKgIB28fujqDjH6IQ/640?wx_fmt=png)

在枚举 ayush 目录下发现了隐藏文件. mozilla/firefox/bzo7sjt1.default... 这是 firefox 浏览器的配置文件信息...

在读取 logins.json 后，发现了这是 10000 端口的浏览器登陆配置文件...

文件还包含 encryptedUsername 和 encryptedPassword....

其中还有 key4.db 文件，这是密钥数据库文件，主要存放加密密钥和主密码的...

方法 1：

利用 firefox_decrypt 工具读取用户名密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPE34ib2xc2r4bKI4Gy8vD0gWAgWVgSL23RDtWRDQsyaJvNicELWffmxEww/640?wx_fmt=png)

```
sudo git clone https://github.com/unode/firefox_decrypt
```

我先将整个隐藏文件都拷贝到了本地 kali 进行操作... 这里读取需要密码，密码就是 ayush 的密码...

通过下载 firefox_decrypt，然后直接对整个目录进行了读取，输出了 root 用户名密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPEw2gw4icX3hbEnc585fGlQnD9ejJlTgdZQzytWO3MCn0DZJT37lkcLLw/640?wx_fmt=png)

然后直接提权 root... 并获得了 root_flag 信息...

这里是有先人帮助写好了工具... 直接简洁获得了需要的信息... 很快速

方法 2：

利用 firefox 原始方法覆盖密匙数据库，直接登陆 root....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPEDvruvBUtk4SWsUHZY6qUXe3CF15lPlxblMPCYjhTUAu1ia4iabecXqeQ/640?wx_fmt=png)

首先输入 firefox -no-remote -ProfileManager，界面会和下图一样，create Pro... 创建新的用户数据库... 我命名为靶机名字...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPEibOnfulOvRZNmX3nECy1MFwVWJhQRpTZqoGQ9d9F7UbtibiaUTm4N9jibw/640?wx_fmt=png)

然后直接点下一步即可... 创建好后会出现该选择框...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPEjNC2IKqRibvuWbMjzpeHLCKzQoicTWhic6umSwsPHVNjrzrRicaicQKGFeQ/640?wx_fmt=png)

```
sudo cp logins.json key4.db /home/dayu/.mozilla/firefox/0buqx7yf.Chaos/
```

然后会在 firefox 本地目录下出现乱码 + Chaos 的文件夹... 进入后是不是很熟悉，和靶机拷出的一样文件信息...

这里需要将靶机上的 logins.json 和 key4.db 两个文件拷到新创建的 Chaos 目录下... 进行覆盖

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPENXfgrDDt715ibt4c7ypHWjl1oOGs0VxznvjvLfYl6xH6WTWk43icqAJQ/640?wx_fmt=png)

然后输入 firefox -no-remote -ProfileManager，选择前面创建好的 Chaos，选择双击后会打开新的浏览器页面...

输入域名 + 10000 端口访问即可...

过了一会，会弹出需要输入密码... 和前面工具读取信息一样需要输入的密码一致...

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200624221704951.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0ODAxNzQ1,size_16,color_FFFFFF,t_70)

输入密码后，会直接跳转到登陆页面.. 自动输入好了 root 用户名和密码信息... 直接 Sign in 登陆即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPpP2kd1hJ1BXqSgO3wbkPE786MiaFMnwqbdwPm9fvMxTMY5rSR273bdTpcS8clZIyQBbYvKib4ibUzQ/640?wx_fmt=png)

登陆进来后直接是 root 权限了... 这里随意发挥操作了，最直接的就是在左下角可以修改当前用户名密码...

这思路是看到一篇文章知道的... 非常感觉大佬分享的思路...

这篇靶机也学到很多东西...

HTB 真的非常好，每一台靶机都是不同的环境，每个环境虽然个别环节使用的方法一致，但是过程肯定是不一样的，例如都是文件上传，然后上传有的限制了文件名称，有的是环节上需要另类操作，都是卡时间点的地方，加油~~

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台中级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/Fms1OiaYewPh3x0qgfYJc4OlyqAM94frFbPucnlNicbAEfQBUiadH22Tjm93pUGLZzhvficphibRkFOYZicvTkMPePyQ/640?wx_fmt=png)

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