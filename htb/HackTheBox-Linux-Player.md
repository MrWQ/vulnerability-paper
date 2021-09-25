> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/k2XCq8pKMrCucFTql3X9gQ)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **161** 篇文章，本公众号会每日分享攻防渗透技术给大家。

靶机地址：https://www.hackthebox.eu/home/machines/profile/196

靶机难度：高级（4.6/10）

靶机发布日期：2019 年 11 月 5 日

靶机描述：

Player is a Hard difficulty Linux box featuring multiple vhosts and a vulnerable SSH server. Sensitive information gained from a chat can be leveraged to find source code. This is used to gain access to an internal application vulnerable to LFI through FFMPEG, leading to credential disclosure. The vulnerable SSH server is exploited to login to a Codiad instance, which can be used to gain a foothold. Process enumeration reveals a cron job which executes a script that is vulnerable to PHP deserialization. The script is exploited to write files and gain a shell as root.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/YK9e7vHy9IQATwibKVicOpXZibX8VOvBrnF8UXRGvcibFy79c4NzQ5qiaZYAialtVicUHCxUcIPzXM0K4aziaQHEPjTDIw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/cr0TTE2QLx3xBmEgU6pOvE8icSG4mNiaNpN7pAPCkEzHe6jKcGMJKUSTPuib5nT7XWwliazst9VfJHD6hSEQ3ibbiauw/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPqD6RFzj0SqQ6ic9yqnmZTBHQK14GOxYXWdMG9XSeYZxiacyR8aXm0wrA/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.145...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPcu6LswDcQ5rLrjNyoondBSeRe0F6K5ZSUHO2QDDxicnK1QGa0cvkIyw/640?wx_fmt=png)

我这里利用 Masscan 快速的扫描出了 22，80，6686 端口，在利用 nmap 详细的扫描了三个端口信息，6686 是 ssh 服务等...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPB1xNECSt57z8UaSae9vhZPkA6HrgFJb00NbKWrtvicuibeibHqZkW69sA/640?wx_fmt=png)

访问 http 服务发现 404...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQP5a8dC3LejPdMrZIk4lD6X0cicb3CQK7gBJq1tZ7g0BViaGjauzNKBOUQ/640?wx_fmt=png)

爆破目录发现了 launcher 目录存在...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPUmxWiaial9gRWXS6NfbMTU8W9NWVLsp2bFJicunLTIZJ3RIrv6Sic4WcHw/640?wx_fmt=png)

访问发现该页面左边像是源代码的样式，是泄露还是提示？

右边是倒计时...email 可填入...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPcVhMIDzo9yxtl3wyr8iaXibKYNep810ngUiaqiadKa7pSIEljiatqFlicxkg/640?wx_fmt=png)

直接通过 burp suit 进行拦截分析...

```
1、该页面存在/launcher/dee8dc8a47256c64630d803a4c40786e.php文件信息...
2、存在cookie值...像base64值...
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPyXuDvApp2LEd9oK9SRefes8fcsTIawzqrlhxrDY6EVSMI6Np1dyicpA/640?wx_fmt=png)

base64 转储后，还是一串数值...

google 说这 cookie 是标准的 JWT 格式，分为三个部分...

第一部分 base64 转储后获得了 C0B..... 还需要用于签名的密钥继续收集信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPgKaAoDvXbQRwf1mz23Fe1PMXRgksI0EyDkyVv0qsH6wkXsq6rn9PLw/640?wx_fmt=png)

我这里通过 burpsuit 继续爆破子 DNS 域名信息...

同时也利用 Wfuzz 进行枚举，发现 wfuzz 超级快就找到了...

chat、dev... 加入 hosts

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQP2Xbv3JqOhprbNrUO1jlqyjTlz24hfqJM6CrkhVtwJUicAavTgdM4a3g/640?wx_fmt=png)

dev 是一个登陆页面表单...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPN0T1TfwIch7tzPUF29BFWiahibDYPrkRdlGpjiaBGJ2D8cfeIs8xwrsNA/640?wx_fmt=png)

查看源代码发现 components 目录下存在 js 信息文件... 继续查看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPwTJcYl97tfMAgSkzCSibSpPnEDibX21IzbnVlibmp8wSE6v7E7wYhEkmA/640?wx_fmt=png)

服务器正在运行 Codiad，google 上可以找到相关的漏洞...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPsd50wKHJwuLxnOhx2Q3ibnbC05DKLsSSg5OreKMia7qustK5w1yQuB7A/640?wx_fmt=png)

可以在此处找到利用 PoC。但是，由于它是经过身份验证的 RCE，因此必须先查找凭据，先放放... 这是其中思路之一..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPhaZrFthvw7ibSQdsA1LOb7X5icWnkBEAt1Qzo6b4glGMt5JrkbPQZgBQ/640?wx_fmt=png)

由于没有枚举到用户名密码信息...

我转到了注入这块方向去专研... 随意输入用户名密码，拦截的目录是 / components/user/controller.php...

Codiad 是一个库，我需要去找到源代码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPNvZW0YZ34y7jsK2xgib74icUjmREqEq6eGR6G0z67rkCRauAOKtYdw4A/640?wx_fmt=png)

```
https://github.com/Codiad/Codiad
```

通过 google 简单搜索就在 github 上发现了 codiad 的库信息...

存在很多目录，该靶机上也是都存在的... 开始找下看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPuq6dicEL5oXf5gY910f1nzLY7pibkvPXyyAKP0pNlT9UDsgia5AcXUOhw/640?wx_fmt=png)

发现了 process.php 好像存在 sql 注入点... 试试...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQP5QgHwUmh0BjZ1Tnfvx80GmRysrOVLiaFa7CczBiaFkgm8iaPnQMMsQibyA/640?wx_fmt=png)

首先把 / components/user/controller.php 改为 process.php 信息... 然后很简单的测试，输入了 shell 创建文件... 出现了 Unable to create Absolute Path... 说明是存在注入点的... 肯定的

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPvSWRmicLIBnCXNoFAnDiardSt5ETibFx5s1rFEkx5ULS1hK0G2qJOp8sw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPf9ygm2bdAIrklE3HjAO89mRfj0rlrRRc93iaFNGR7BTsd9gtUmESIrw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPoMtgOib0icI1KGvfhiaBHic7Yv25FN5iamnnyBEgqsDHLEJoiaic2xMWyU95A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPKJHmb8KEgyWXxURspMQzxATia73zOkDKIicfBaYfZicu0ao2Jb2fSHQbQ/640?wx_fmt=png)

一顿操作，利用 burpsuit 枚举了用户目录信息... 发现 launcher 的 length 长度不一样，很可能可利用该点进行注入...

还是不行，这里浪费了很多时间... 第二条思路... 跳过...

```
1、codiad漏洞利用；
2、dev.player.htb注入利用；
```

先放着.... 继续枚举

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPrr8vDos5iaBspoicLLiaL4oD8pp2efuUqcsL5z57wcgNlEbltSjDYclqA/640?wx_fmt=png)

进入 chat.player.htb 这是对话聊天页面...

通过对话知道 staging 也是域名之一...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPQxrl4JD56gHENhHwyrRFrA49gSVeIQCBicH1IKJqhdBtrjRDiao7BTlw/640?wx_fmt=png)

可看到挂着的 burpsuit 枚举也发现了 staging... 添加到 hosts...

在 chat 页面没有更多有用的信息了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPEBtT75vtpaPbYFtaLFG57aDmb10rAkpNf4d2zVcxbvRibBmX3e5Svmw/640?wx_fmt=png)

跳转到 staging.player.htb 中...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQP6Icrgfuyjlh9vLNj4qwSbtgC9aCnSvLV3h5OoEFSPyG3xdZC6Lj0jQ/640?wx_fmt=png)

在 contact core team 中是个电子邮件 IP 输入页面... 是否存在注入呢...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPcic6kLDmuf5WOoGz9RibMJNRgZWibntPD38DqA9ZVDibsSKcj4yvOxK9Mw/640?wx_fmt=png)

存在 contact.php、fix.php 目录信息，Peter、Glenn、Cleveland 用户名信息... 目录信息都在 / var/www 下... 还是无思路... 玩得很开心

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPckHTYvUXYSicibnTpEjZ5N1xUOcrjjm1bbKANfUH3BicK4z7zFnibogGNA/640?wx_fmt=png)

我回头继续对 player.htb 进行查看，开始发现....40768C.php 信息... 我添加了后缀进行测试... 发现成功进入另外页面...

该页面是查看页面后的前端代码页面... 找到了...

这是 JWT 需要的凭证和密匙信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPBYQHXkiblQLhIEDhnjP6NAE6LvicTGF1243kM02ibWxds50UBRYYBAOvg/640?wx_fmt=png)

登录 jwt.io，可看到通过刚获得的凭证和密匙信息，勾选 base64 选项后，更改了新的 cookie 值... 直接通过 burpsuit 更改 cookie 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPDO33X4h0UjnzaRF0F0r9ibNxib9vwuRjia0Par1zibpaoBDDKZWpclBpPw/640?wx_fmt=png)

Send 后，发现产生了 location 值，这是目录... 登录试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPrShAVNavictWKIOicwFU3RjBgOnpOY6lSHsRI4nO4wEO55wCOUrTIibcQ/640?wx_fmt=png)

可看到重定向到了文件上传页面.. 没有任何提示可上传文件限制... 测试看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPKF5a5A56TAaQuSEe9PWeorYZDd9hoGEYibwezk0NvRjXYY05x27ZJVA/640?wx_fmt=png)

简单写了个 txt 文本，成功上传，没报错... 出现了 media，页面，url 后缀会自动生成...。AVI 的文件...

意思就是上传目录，会通过 avi_media 传输出来显示...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPYcQRNJfD9whduxkz72nmXuynRZyicF3RxdIt01vibB3kCeAnYo74MtpQ/640?wx_fmt=png)

可看到...avi

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQP2ibsXP68OGRUnU8K83jEtWrP4G3icHfswXnh7DhBicWLq7ch5gAnYZAUQ/640?wx_fmt=png)

通过 url，我通过 google 搜索了一番...

发现了存在 CVE 可利用...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQP25hIibTiaibjdv2amGYKRF9lkJ4dRzs3ECFfeEoXTtu7uaCkIbSbuhQPg/640?wx_fmt=png)

FFmpeg HLS 漏洞利用任意文件读取.... 下载 avi.py...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPye3K702QFAdAJIJmZX5DPnPVIMIicjYDBTzFUdn3JyLUHPMicCQkYhrw/640?wx_fmt=png)

下载执行，通过帮助执行了脚本...

我简单测试了 passwd 生成情况... 获得了 avi...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPYCgic6sWIedkergnibsXX5XD2LCZIdyZsxrNGyicE0wPZycC2Laj8SQ8Q/640?wx_fmt=png)

然后利用脚本生成的 AVI 文件上传到靶机...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPicDmlDTlMicfuzLaw9VicCR2s77usvjibiaDuV9h7wnMGgg43A45SvdpJcg/640?wx_fmt=png)

靶机回复了一个 vlc 的 avi 视频文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPiboQ9sAVDoV6ECLJKCnaOsoLK9deMTzKs1DVE3A14raG3MQEKU8dejQ/640?wx_fmt=png)

查看后，果然获得了靶机上 etc/passwd 的信息，通过视频展示的... 那么，我们可以通过此方式获得想要的东西...

那么需要获得什么呢？？

通过回看笔记，前面获得了很多 / var/www/html 的目录 php 文件信息... 可以通过 avi 来展示出其中这些信息的内容... 开始

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPcgyJs5ibcpgFyicI98m6IL8BmEV16j29rtVibP8HMIicTFVofDrUsLQpTw/640?wx_fmt=png)

利用脚本输出 avi

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPGXaLNnBXafreuxXDiaIf5bfuz2w2ibRj2aP2Arjic0AyEZzbSUBpgTDLw/640?wx_fmt=png)

上传获得 avi 查看后，发现了 telegen 用户名密码... 这里还查看了很多 php 信息，省略不截图了... 方法一致

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPExibzcicjlkIy6Dps8YDa50AC6KNxHME9aRlDXdWUgxMUNteyPq4sIgw/640?wx_fmt=png)

通过 nmap 枚举的 ssh 新端口，登录了 telegen 用户...

发现权限贼低...telegen 还存在 lshell 权限执行...

由于权限很低，我查看了 ssh 版本，7.2...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQP2FxrXibvxc5hbhiaSu27piaS1xga505ATqcxF0lOBIX3kqvySIYIENjibA/640?wx_fmt=png)

本地搜索，发现了可利用 CVE-2016-3115，39569EXP....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPfN9zgafE0JWctlOSScGgO2UYKHOJf9NJO5jsf2zHmc9xicaH9jiaEUJg/640?wx_fmt=png)

通过 EXP 提示，成功登录... 通过. readfile 阅读获得了 user_flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQP5zuKJOgOTqMNXz6cHKdkyMTYVGMWGMCaoSgunxaUibibiaXHuzO6YNhWQ/640?wx_fmt=png)

继续查看 fix.php 信息... 发现了 peter 用户名密码？？该目录是前面 burpsuit 枚举发现的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPia41M9icwNl6tIGAdwQZFvicicoBib7QR8zJ8JbKUibxLZzaKWH3A3A0BRZw/640?wx_fmt=png)

通过 peter 成功登录 dev.player.htb 表单页面... 首先证明了 peter 是 codiad 的页面用户名密码...

这里有两个思路可以提权了...

```
1、利用前面的codiad的POC进行提权即可...
2、直接在该页面写shell提权...
```

第一种方法很简单，EXP 下载查看 h 后，按照提权即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPRdbOR8Az7Kice769F3wAWexiaaf90vq5NMej741LZ7wvgZztLAx1sluQ/640?wx_fmt=png)

我尝试了第二种思路提权... 首先创建目录... 提示报错，demo/home 下才能生成目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPTh1coFQGvXHI0KxXQkZ95huPZDAvD3avicDlGWw4iaicDDXq23ialf1IbQ/640?wx_fmt=png)

重新写入...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPFkMreic28NlC2BJOLUOsrDqYHoolZ3uHE5bOQZ2PGzwRBcjFrMU4d8A/640?wx_fmt=png)

写入后，创建 shell 文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPYd9sKOVDn3OAgRexNfRCd6gpa3Um8okQejaVfcTfgwflXptYTWrMcg/640?wx_fmt=png)

创建了 dayu.php 文件后，复制了 php-rever-....shell 进入...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPdBoAzDHXjcBToXK8vg9nRzEwIytg1xwYqCsic2ibquDW3ibHQvxojsFrg/640?wx_fmt=png)

获得了反向外壳...

这里 su 登陆了前面 Avi 获取的 telegen 用户...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPiammNHnbJ7GPiaQxF5ichHB4FekLHwSDACkVJqyWuCLWuXnkcLuB4icHlg/640?wx_fmt=png)

继续枚举信息提权 root

上传 pspy32 监测进程....

发现了 buff.php 一直以 root 权限进行着...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQP4ibgKgcicpeJLaUyj5wmAicMMFMeuvgq7xSGxAZu1dUkXRQZFr0OljTNw/640?wx_fmt=png)

查看后发现了熟悉的面孔... 一串数字加 php 文件... 这不是前面就获取过么...

简单解释下该脚本：

该脚本创建一个 playBuff 类的对象，然后对其进行序列化并将结果存储在变量中，然后将文件 merge.log 的内容读入 $ data，以 $ data 作为参数调用反序列化方法，根据数字 PHP 文档，未序列化的方法将序列化的字符串作为输入，并尝试调用__wakeup（）函数... 等等等

简单读懂后，直接修改数字 php，写入 shell 即可... 先查看下内容吧

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPXG90kJZyciawiaR5AI7LkYn0LulQ9OicAkaTianNqQdMy335nxNhL6FGGg/640?wx_fmt=png)

这就简单的脚本... 当然，下面的代码是我测试写入的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPgH83muvtC2FOGngSGhHQPCAzbvd2ImQAG7YFh0Hfe8jenpia9gqq86suxfH0tdJyJFjde3w6nIpQ/640?wx_fmt=png)

通过测试，echo 直接写入 shell 覆盖数字 php 所有内容即可... 直接获得了反向外壳...

获得了 root_flag 信息...

这里还没结束....

因为中途 dev.player.htb 中枚举到的 process.php 思路，肯定有注入存在... 还没解决...

经过两个小时的测试测试... 我已经头晕了，一直回复 can't open file...

我会在回来的.... 估计是 process.php 脚本通读还是不够透彻... 在笔记上记住这里有个问题，等我成大佬了回来研究... 加油...

目录域名爆破 --Codiad 漏洞利用 --burpsuit 注入枚举 --JWT 信息枚举转换 --FFmpeg HLS AVI 文件上传漏洞利用 --SSH 的 CVE-2016-3115 漏洞利用 -- 文件写入 shell 提权 -- 进程枚举 -- 通读 php 脚本写入 shell 获得 root 权限...

全程离不开 burpsuit 神器... 让我进一步熟悉了 burpsuit 使用... 这台靶机挺爽的打起来...

这里我全程没有写任何命令，全在图里，到了这地步，以后会很少写命令出来了，该懂的前面都懂了，不懂的也别跳跃学习了... 巩固下基础

这台靶机我给了高级，是因为思路很多，很舒服...

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台高级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/pAKQibdZxLPFVjp9K5Pbx0gGWhXGIT5Y2ia1H4pSEP9CRUwCRRq8xl1ZxMiaeALB35QAJQce6DlTktLVBXhucFkQg/640?wx_fmt=png)

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