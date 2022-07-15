> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/3mO2tJeU8qyWJnyARX960w)

![](https://mmbiz.qpic.cn/mmbiz_gif/3RhuVysG9Lenf7an2sf098pVucEcKNqIrmiaEpqDdT2yYibEbtIsQeOqJOiapQtSOtiaFyndgtZRHPj6mXcgJXspLg/640?wx_fmt=gif)

喜欢就关注我吧，订阅更多最新消息

  

```
文章字数1539
预计阅读时长7分钟
```

  
涉及知识点实操练习 - VulnHub 渗透测试实战靶场 Node 1.0  

https://www.hetianlab.com/expc.do?ec=ECIDdb58-4b9d-427b-b7b3-8382c7e0a7f5&pk_campaign=weixin-wemedia         

Node 1.0 是一个难度为中等的 Boot2root/CTF 挑战，靶场环境最初由 HackTheBox 创建，实验目的是获取两个 flag

靶机地址：http://www.vulnhub.com/entry/five86-1,417/

技术点
===

*   `opennetadmin v18.1.1`RCE
    

*   `searchsploit`
    
*   github 搜索 exp
    

*   破解 Linux 中经过 HASH 加密的密码
    

*   `crunch`生成字典
    
*   `john`和`hashcat`破解密码
    
*   `hash-identifier`查看 HASH 类型
    

*   SSH 免密登陆
    

*   公钥复制为`authorized_keys`
    

*   Linux 查看当前用户权限可读文件和可执行命令
    

*   查看当前用户权限可读文件`find / -type f -user www-data`
    
*   可执行命令`sudo -l`
    

目标发现
====

nmap -sP 参数使用 ping 扫描局域网主机，目的地址为 192.168.56.5

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY4wPlNQlGsfn7R4zj44icHGshNxPEEBwicHuJ0V4xBnWUz28YpIPicZI0EA/640?wx_fmt=png)

nmap -sS -A -v 192.168.56.5 看一下详细的扫描结果 -sS 是半开放扫描，-A 是进行操作系统指纹和版本检测，-v 输出详细情况

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY4BqSubFHsAb8S7g2prLdX56PXXTw5MUfNocEEpDgLa12AXFGSI0lz5A/640?wx_fmt=png)image-20210110233307631

可以看到开放了 22、80、10000 三个端口，并且 80 端口存在 `robots.txt` 和路径 `/ona`

漏洞发现与利用
=======

访问 http://192.168.56.5 是个空白页面，然后去访问 /ona，可以看到是 `opennetadmin` 的管理页面，并且版本是 `18.1.1`

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY4MenAibqlNusZAM7oq3j5xcpggcT9DQ0w1bu7QqH6wN2puswUocIr7yQ/640?wx_fmt=png)image-20210110234925936![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY4pmKxf061f85RAkZxLVQA7FCgibMDbqzYiclCUGcbu8eIJvO1vTHRZycw/640?wx_fmt=png)image-20210110235509936

`v18.1.1`的`opennetadmin`是存在 RCE 漏洞的，在 github 找个 exp 打过去就可以，https://github.com/amriunix/ona-rce

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY4XRaMTr4lP5cqOQW0DXaoOzoxmLA5wtCgicgp6n4tVSsqdJSrxrB5FIw/640?wx_fmt=png)image-20210111000006420

或者是使用 `searchsploit` ，不过这里有个坑点，就是要对这个 bash 脚本进行转换格式，否则会报错，使用`dos2unix 47691.sh`这个命令，而且这里的 shell 不能转成 TTY

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY4cQLIYNr0KLibUfNuStgMTPFVP6F9kcB4MtVqaqr2HwNdBcaJEbzvQibw/640?wx_fmt=png)image-20210111000238886![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY46JluLP5ta0L0G7Awb0ntibrbWDEA7C3UClfbn4Wz5UHVR2gBostaMiaw/640?wx_fmt=png)image-20210111000505227

下面的问题就是如何进行提权了，经过一番测试，发现这里无法执行的命令是没有回显的，并且不能执行`cd`命令，但是可以使用`ls`和`cat`命令

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY4VuUtXuctu1UlhnLd6FAlS2h9DJDcjFRmG04g4jWJ1NQibg683dyaPrw/640?wx_fmt=png)image-20210111001159331![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY4RKpwZXFSz992gGHicML0xH5hPuoFtFpEQLXSWmcFuciadU5sk9FIJ2kw/640?wx_fmt=png)image-20210111001246590

这里肯定是有权限控制的，可以使用`find / -type f -user www-data`命令查看这个用户可以读取的文件，除了`/proc` 就是`/var/www/html/reports/.htaccess`和`/var/log/ona.log`

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY4DQNWJ7mSOCwPpqIdPibosL4dibLUldcZMk93rhJSia2YN4E28zt1zTnaQ/640?wx_fmt=png)image-20210111001014915

读取`var/www/html/reports/.htaccess`可以找到`AuthUserFile`的路径`/var/www/.htpasswd`

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY4EvicuI15DaHHPhbWNKibZtIkBIFicKXQRXfiapiarNbfZlod3eoibP2hZhkg/640?wx_fmt=png)image-20210111001712462

读取这个文件如下，可以得到用户名`douglas`和 HASH 的密码`$apr1$9fgG/hiM$BtsL9qpNHUlylaLxk81qY1`，给的提示是`只包含aefhrt的十个字符`

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY49lY5456z67Yq1LZ3lzhdMBxR1omnaS0OTaKOfU4Ls49ogiaM0bfIcLQ/640?wx_fmt=png)image-20210111002020236

```
douglas:$apr1$9fgG/hiM$BtsL9qpNHUlylaLxk81qY1

# To make things slightly less painful (a standard dictionary will likely fail),
# use the following character set for this 10 character password: aefhrt 
```

先用`hash-identifier`看一下是哪个 HASH，结果 hash -type : [+] MD5(APR)

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY4ZfeaUGI0icgs3th9BG9jzKANSR5sceYb0icGnexSRrww0bhLtyK8vD0w/640?wx_fmt=png)image-20210111002610462

然后使用`crunch`生成对应的字典，命令格式`crunch <min-len> <max-len> [charset string] [options]`，这里生成只包含 aefhrt 的 10 个字符，就可以使用如下命令`crunch 10 10 aefhrt -o pass.txt`，更多的介绍可以看 Linux 下的字典生成工具 Crunch 和 crunch 命令详解

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY4ncSmxUMPCtXAHlfJreXlHibpX5xz9l1Mj8zPPqZCTU9OeH7qPfDQo6Q/640?wx_fmt=png)image-20210111003458350

最后就要用大名鼎鼎的`hashcat`去破解这个 HASH，命令格式`hashcat [options]... hash|hashfile|hccapxfile [dictionary|mask|directory]...`，这里使用的命令为`hashcat -m 1600 -a 0 -o res hash.txt pass.txt`

-m 是 HASH 类别，-a 是攻击方式，-o 是输出结果，更多的参数可以参考 Hashcat 密码破解攻略。这里在 kali 里面运行一直报错，就转移到 wsl2 里面了，命令`hashcat -m 1600 -a 0 -o res hash.txt pass.txt --force`

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY4v59xOpebM7ic72guicu9IarEiaPYY4nrxXwDt4wBla0Rfnfibnvib9WQBuQ/640?wx_fmt=png)image-20210111213409125![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY4Cgx47yaIGKuBktFlIMe2e8B8KibqicBf4G6fKuL3x4k4mRCo7Fbk2Lpw/640?wx_fmt=png)image-20210111213624969

最终密码为 `fatherrrrr`

或者这里也可以使用`john`来进行破解`john --wordlist=pass.txt hash.txt`，但是速度可能有丶问题

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY4cFibzd4lGGcbickcOTBtqkZYUATc2icod71OGJ2oXe3nkDaT8AiaAtJg4A/640?wx_fmt=png)image-20210111220754542

使用 ssh 连接`ssh douglas@192.168.56.5`

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY4Mud124xUZYpb68t7qqPCqWibzeDgVuiboChCkSnHavXoA5tdsWicV3jVg/640?wx_fmt=png)image-20210111010646094

这里是个 TTY，但还是存在权限控制，使用`sudo -l`看一下可以使用什么命令，结果是`(jen) NOPASSWD: /bin/cp`，这里就有点奇怪了，`douglas`可以用`jen`的身份运行`cp`命令

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY4Pp1icko1T5eUGCo79BSLGIibspyCibbsA52FQhCRUwFl9ibodgfJkMmreg/640?wx_fmt=png)image-20210111010947213

先去访问一下`home`目录，发现`douglas`和`jen`这两个用户，但是只能用`jen`的`cp`命令，且没有`jen`的密码

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY4iaenJZnTficuREZLE9TKuHvnVwjUDZbhm4WCMQWzECCVwDonU8o5loog/640?wx_fmt=png)image-20210111011436573

值得注意的是，如果`jen`用户下的`/home/jen/.ssh/authorized_keys`包含`douglas`的公钥，那就可以用`douglas`的`id_rsa`文件登陆`jen`的 ssh，也即免密登陆`jen`的 ssh。这里复制到`/tmp`目录下是因为`jen`没有权限访问`douglas`目录下的文件

```
cp .ssh/id_rsa.pub /tmp/authorized_keys
chmod 777 /tmp/authorized_keys 
sudo -u jen /bin/cp /tmp/authorized_keys /home/jen/.ssh/
```

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY4B9huiaLvO3ziaZJ8OwFAvebND7c67ibGRPhXXafGqyVect6Y0JlibUDdXg/640?wx_fmt=png)image-20210111014200082

然后用 ssh 连接`ssh -i id_rsa jen@127.0.0.1`

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY4AC3zrm7qllFS51WL5XOQ3SSf7cibbxk9T6ttS83gWdQlF5mlubkn7iaw/640?wx_fmt=png)image-20210111014442540

成功登陆`jen`，看到提示`mail`，还是先执行`echo $(find / -type f -user jen) > 1.txt` 看一下，有一个`/var/mail/jen`的文件可以读取

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY4SpibnaEWvWgA1QJFbuB6IDzQSAdRNdbHMkh5s5Zm5MtvJZLWB6FpfcQ/640?wx_fmt=png)image-20210111014759768

或者这里直接输入`mail`的命令也可以看到

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY4cIYOCXb2qsYl7ugmAT9GPNTXMfySoVxUXLYKp1D3DwwRgQ273Qoiajg/640?wx_fmt=png)image-20210111015110156

读取一下，其内容如下

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY41qEYkQbmmzx38y4LoYrFibsicLh4iaSnTy7rhCiacPxjq3j6FbPcvSAHWw/640?wx_fmt=png)image-20210111014908700

关键词：`change Moss's password`、`his password is now Fire!Fire!`

接着 ssh 连接`moss`用户`ssh moss@127.0.0.1`

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY46D8vNXJwLyiaXu3aWdp3tIFGEheovMSUGlEpELl6XelISvRz2sZkb7w/640?wx_fmt=png)image-20210111015350428

在当前目录发现了一个隐藏目录`.games`，访问后发现一个`root`权限的二进制文件`upyourgame`

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY4htq2stKpkiakuiap5bVBCJOHYG6rDBwOyMicFXeqvfSYKqhzbqA6d0jeA/640?wx_fmt=png)image-20210111015852402

运行之后就发现自己神奇的变成 root 用户辣

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY40NU9Xg9Vpoq0FeicQPrjpoGxIS7TA2bicdXjJ5yI1xhuXibgnEzevTjhg/640?wx_fmt=png)image-20210111020013886

最后，flag 在`/root`中，为`8f3b38dd95eccf600593da4522251746`

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY4oZg3rCjG2LuTkdx2KtwwMMkFbs5J2tCwROwrIQjdpha6ycm9vbVibPQ/640?wx_fmt=png)image-20210111020132080

彩蛋时刻，其实在拿到`douglas`的密码之后就可以用虚拟机登陆，然后操作，这里是用的`moss`的账号密码，也是同样的效果

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9LcEqmy2TcF9UKj8rcGibXCY4OQwRQmnvUNU4Jl2pCesqXIxbma1uT3HwP614PzDQibNXqo467nQFLjg/640?wx_fmt=png)image-20210111020648136

**1/15**

欢迎投稿至邮箱：**EDU@antvsion.com**

有才能的你快来投稿吧！

![](https://mmbiz.qpic.cn/mmbiz_gif/3RhuVysG9LdRmpz4ibIY8GpicEiabmEOVuDH643dgKUQ7JK7bkJibUEk8bImjXrQgvtr4MZpMnfVuw7aT2KRkdFJrw/640?wx_fmt=gif)

快戳 “阅读原文” 做靶场练习