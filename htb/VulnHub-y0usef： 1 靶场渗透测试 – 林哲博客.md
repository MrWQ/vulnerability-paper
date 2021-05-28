> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [www.lz80.com](https://www.lz80.com/21015.html)

> 作者：ch4nge 时间：2021.1.19 靶场信息： 地址：https://www.vulnhub.com/entry/y0usef-1,624/ 发布日期：2020 年 12 月 10 日 难度：简单 目…......

作者：ch4nge  
时间：2021.1.19

靶场信息：

> 地址：https://www.vulnhub.com/entry/y0usef-1,624/  
> 发布日期：2020 年 12 月 10 日  
> 难度：简单  
> 目标：user.txt 和 root.txt  
> 运行：VirtualBox（网络桥接）

本次靶场使用 VirtualBox 进行搭建运行，通过 kali 系统进行渗透测试，步骤按照渗透测试的过程进行。找了比较新的一个 vulnhub 靶场，此次靶机渗透级别为简单，漏洞利用也很基础。文章有不对的地方欢迎师傅指正~

### 1. 获取靶机 ip

使用 nmap 获取目标 ip 地址为 192.168.31.43, 使用 grep 过滤

```
nmap -sP 192.168.1.0/24 | grep -B 2 -A 0 "VirtualBox"
```

![](https://image.3001.net/images/20210118/1610972693_60057e151c033915b69f7.png!small)

### 2. 扫描开启的端口和服务

```
nmap -sS -sV -T5 -A -p- 192.168.31.43
```

![](https://image.3001.net/images/20210118/1610972700_60057e1cda7ae66ab6453.png!small)

获得四个端口信息

```
PORT        STATE    SERVICE     VERSION
```

### 3. 网站信息搜集 & 漏洞探测

##### 3.1 访问 ip

Sorry , the site is under construction soon, it run  
对不起，网站正在建设中，正在运行  
![](https://image.3001.net/images/20210118/1610972907_60057eebcb1765b6e5fa9.png!small)

##### 3.2 扫描目录

使用 gobuster 扫描目录，指定 200,204,301,302,307,401 响应码进行显示  
[响应码解释](https://www.lz80.com/go?_=7703dae78aaHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2RkaHNlYS9hcnRpY2xlL2RldGFpbHMvNzk0MDU5OTY=)

```
22/tcp      open     ssh          OpenSSH 6.7p1 Debian 5+deb8u4 (protocol 2.0)
```

```
80/tcp      open     http         Apache httpd 2.4.10 ((Debian))
```

![](https://image.3001.net/images/20210118/1610973088_60057fa001a34378a9c45.png!small)  
扫描到 301 响应码的 / adminstration (Status: 301)  
访问这个页面显示  
Forbidden  
You don’t have permission to access on this folder  
![](https://image.3001.net/images/20210119/1611026932_600651f4725a4edd8c98b.png!small)  
我没有权限访问，先继续扫描该目录下的文件  
http://192.168.1.182/adminstration

```
111/tcp     open     rpcbind 2-4 (RPC #100000)
```

![](https://image.3001.net/images/20210118/1610973665_600581e1e5f48bfc2c3fd.png!small)

```
36274/tcp   open     status 1 (RPC #100024)
```

尝试添加指向本地的 X-Forwarded-For header 头进行 bypass  
使用 burpsuite 进行操作  
![](https://image.3001.net/images/20210119/1611027395_600653c390db73118f07d.png!small)  
成功了！是一个登录页面，后面为了方便，我将使用 firefox 浏览器的插件`X-Forwarded-For Header`对网页访问的过程添加有效的 X-Forwarded-For header 头  
只需要填写 127.0.0.1 并勾选 X-Forwarded-For 即可  
![](https://image.3001.net/images/20210119/1611027618_600654a2e01403c62966a.png!small)  
刷新一下，可以看到已经起作用了  
![](https://image.3001.net/images/20210119/1611027708_600654fcdc8a909fb7ff5.png!small)  
我们想办法爆破一下用户名和密码

### 1. 弱口令

经过几次尝试发现是很简单的一个弱口令，用户名与密码均是 admin  
![](https://image.3001.net/images/20210119/1611027878_600655a6c9363049c77d4.png!small)  
如果猜不到也没有关系，直接使用 burpsuite 进行对常用用户名爆破。

### 2. 文件上传

通过查看，发现网站有一个文件上传的位置  
![](https://image.3001.net/images/20210119/1611028006_60065626108be6204a41e.png!small)  
我们尝试 bypass 上传后门，首先进行信息搜集，看一下网站的语言、服务器信息  
![](https://image.3001.net/images/20210119/1611028103_6006568722a08ffefeb2b.png!small)

```
200   （成功）  服务器已成功处理了请求。通常，这表示服务器提供了请求的网页。
```

我先上传了一些正常的文件，发现 jpg 文件上传失败，png 与 gif 成功了  
![](https://image.3001.net/images/20210119/1611028293_60065745665be4945054a.png!small)  
![](https://image.3001.net/images/20210119/1611028367_6006578f1cf20e3d3ce37.png!small)  
判断存在 MIME 类型检查，使用 burpsuite 进行抓包分析测试 bypass  
查看到上传 jpg 文件时 Content-Type: image/jpeg，修改为 Content-Type: image/jpg 可以上传成功。  
直接上传 php webshell，绕 MIME 类型检查测试。将 Content-Type: application/octet-stream 修改为 Content-Type: image/jpg，filename=”phpgsl.php” 后缀名不变  
![](https://image.3001.net/images/20210119/1611031775_600664df14da3702a6424.png!small)  
上传成功！  
使用哥斯拉进行连接  
`http://192.168.1.182/adminstration/upload/files/1611031692phpgsl.php`

![](https://image.3001.net/images/20210119/1611031952_60066590d734850fa4dd3.png!small)

![](https://image.3001.net/images/20210119/1611036497_600677511cf6307d4d11d.png!small)

使用哥斯拉的`PMeterpreter`模块反弹 shell，在本地 kali 机器中使用 msfconsole 接收反弹 shell

```
204   （无内容）  服务器成功处理了请求，但没有返回任何内容。
```

设置好 msfconsole 之后，哥斯拉的`PMeterpreter`模块设置 host 为 kali ip192.168.1.187，端口 4444，点击 go  
![](https://image.3001.net/images/20210119/1611036879_600678cf485d47071012b.png!small)  
![](https://image.3001.net/images/20210119/1611036760_60067858a735d469ef63c.png!small)

看到 kali 已经接收到了 shell

使用 python 命令升级为交互式 shell

```
301   （永久移动）  请求的网页已永久移动到新位置。服务器返回此响应（对 GET 或 HEAD 请求的响应）时，会自动将请求者转到新位置。
```

![](https://image.3001.net/images/20210119/1611037423_60067aefa734b113eced1.png!small)  
查找 user.txt  
![](https://image.3001.net/images/20210119/1611037443_60067b0381f5f645f78f0.png!small)

```
302   （临时移动）  服务器目前从不同位置的网页响应请求，但请求者应继续使用原有位置来进行以后的请求。
```

看起来是 base64 编码，解密得到

```
307   （临时重定向）  服务器目前从不同位置的网页响应请求，但请求者应继续使用原有位置来进行以后的请求。
```

root 路径没有权限访问，这里先不登录这个 yousef 用户，因为我们已经有 shell 了，现在尝试提权到 root。

查看一下内核版本  
![](https://image.3001.net/images/20210119/1611037608_60067ba88395447bbb84b.png!small)

```
401   （未授权）请求要求身份验证。对于需要登录的网页，服务器可能返回此响应。
```

在 exploit-db 搜索该内核版本是否存在提权漏洞

```
gobuster dir -u 192.168.1.182 -w /usr/share/wordlists/seclists/Discovery/Web-Content/raft-large-words.txt -s 200,204,301,302,307,401
```

![](https://image.3001.net/images/20210119/1611037790_60067c5ee981894e6755e.png!small)

将 37292.c 拷贝到桌面，使用 python3 搭建 http 服务，为靶机 shell 提供下载

```
gobuster dir -u 192.168.1.182/adminstration -w /usr/share/wordlists/seclists/Discovery/Web-Content/raft-large-words.txt -s 200,204,301,302,307,401
```

![](https://image.3001.net/images/20210119/1611038123_60067dabce3487b3f003c.png!small)

在 shell 中进行 wget 下载脚本，使用 gcc 编译脚本，得到 root 权限，查找并读取 root.txt 文件

![](https://image.3001.net/images/20210119/1611038132_60067db4a7fd9fdcd3e6c.png!small)

base64 解码得到

```
/include (Status: 301)
```

游戏结束！

此次靶场比较简单，主要是信息搜集的时候要对目录搜集全面，整个过程涉及到的漏洞都很基础。