\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/l7\_WKig-TAVgCoD7gwDd6w)

渗透攻击红队

一个专注于红队攻击的公众号

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDoZibS8XU01CtEtSbwM3VGr3qskOmA1VkccY0mwKTCq6u2ia1xYRwBn3A/640?wx_fmt=jpeg)

  

  

大家好，这里是 **渗透攻击红队** 的第 **22** 篇文章，本公众号会记录一些我学习红队攻击的复现笔记（由浅到深），不出意外每天一更

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC4T65TNkYZsPg2BJ2VwibZicuBhV9DGqxlsxwG0n2ibhLuBsiamU7S0SqvAp6p33ucxPkuiaDiaKD6ibJGaQ/640?wx_fmt=gif)

Windows 权限简介

在 Windwos 中，权限大概分为四种，分别是 Users、Administrator、System、TrustedInstaller。在这四种权限中，我们经常接收到的是前三种，下面我们对这几种权限进行分析：

*   Users：普通用户权限，是系统中最安全的权限 (因为分配给该组的默认权限不允许成员修改操作系统的设置或用户资料)。
    
*   Administrator：管理员权限，可以利用 Windows 的机制将自己提升为 System 权限，以便操作 SAM 文件等。
    
*   System：系统权限，可以对 SAM 等敏感文件进行读取，往往需要将 Administrator 权限提升到 System 权限才可以对散列值进行 Dump 操作。
    
*   TrustedInstaller：Windows 中的最高权限，对系统文件，即使拥有 System 权限也无法修改，只有拥有 TrustedInstaller 权限才可以修改系统文件。
    

当我们权限较低的时候，我们就可以通过权限提升来提权，在提权前需要对目标主机信息收集，查看可以利用那些提权方法。

**Windows 快速找到提权 EXP**

**Windows Exploit Suggester**

* * *

该工具可以将系统中已经安装的补丁程序与微软漏洞数据库进行比较，并可以识别可能导致权限提升的漏洞，而其只需要的只有目标系统的信息。

下载地址：https://github.com/GDSSecurity/Windows-Exploit-Suggester

首先在目标主机上运行命令：

```
systeminfo > exploit.txt
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLJFSHsqQIy6FHHLpmmFaMziaum6D9EYlicFlXL6ff6h9vqboq1Cyk35oV4f0ghB1OefkWDROU9fzeA/640?wx_fmt=png)

接下来我们从微软官方网站自动下载安全公告数据库，下载的文件会自动在当前目录下以 Excel 电子表格的形式保存：

```
python windows-exploit-suggester.py --update
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLJFSHsqQIy6FHHLpmmFaMzawTvqRqBKBjgRnouAKhicM9FMWyEaABd7cCrqxTEAl218mwkzeTkYvw/640?wx_fmt=png)

然后使用 Windows-Exploit-Suggester 工具进行检查系统中存在未修复的漏洞：

```
python windows-exploit-suggester.py -d 2020-11-04-mssb.xls -i exploit.txt
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLJFSHsqQIy6FHHLpmmFaMzwgqhKaH3YSTfqtDW5xES6QlMe9Zkg29s19Ot2C67M3Twev5BHtX2Bw/640?wx_fmt=png)

如果报错的话是因为没有安装 xlrd 模块：

```
pip install xlrd --upgrade
```

* * *

**Powershell Sherlock**

通过 Powershell 中的 Sherlock 脚本，可以快速查找可能用于本地权限提升的漏洞。

下载地址：https://github.com/rasta-mouse/Sherlock

首先在目标系统 Powershell 环境导入 Sherlock 脚本：

```
Import-Module .\\Sherlock.ps1
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLJFSHsqQIy6FHHLpmmFaMz39h6keBPcqAcXl9CGnAIIN907iaEfa2pcjeEO5J7qnLJO64a8n1cW8A/640?wx_fmt=png)

之后就可以调用 Powershell 脚本，搜索所有未安装的补丁的漏洞：

```
Find-AllVulns
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLJFSHsqQIy6FHHLpmmFaMzRjw9U5pagicKgmkrJKdAYgIEqwZ7icBl3fEjNQpzswib3m4FVwEaD0hAA/640?wx_fmt=png)

* * *

**通过 CMD 命令查找 EXP**

```
systeminfo>saul.txt&(for %i in ( KB4013389 KB3199135 KB3186973 KB3178466 KB3164038 KB3143145 KB3143141 KB3136041 K3134228 KB3089656 KB3067505 KB3077657 KB3057839 KB3057191 KB3031432 KB3036220 KB3023266 KB2989935 KB3011780 KB3000061 KB2992611 KB2975684 KB2914368 KB2850851 KB2840221 KB2778930 KB2972621 KB2671387 KB2592799 KB2566454 KB2503665 KB2393802 KB2305420 KB2267960 KB982799 KB2160329 KB977165 KB971468 KB975517 KB970483 KB959454 KB957097 KB958644 KB956803 KB941693 KB921883 KB899588 KB823980 ) do @type saul.txt|@find /i "%i"|| @echo %i is Yes)&del /f /q /a saul.txt
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LLJFSHsqQIy6FHHLpmmFaMzO82fWIoWiap76I3jYpMAAiaWhcm3auyddI9Lxzibo1FMrQRzavY4WcNZQ/640?wx_fmt=png)

从上图得知，有很多补丁没有打，那么就可以根据这些补丁号来选择对应的 EXP。

* * *

渗透攻击红队 发起了一个读者讨论 快来发表你的评论吧！ 精选讨论内容

参考文章：

http://www.saulgoodman.cn/RedTeaming-4.html

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

渗透攻击红队

一个专注于渗透红队攻击的公众号

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDdjBqfzUWVgkVA7dFfxUAATDhZQicc1ibtgzSVq7sln6r9kEtTTicvZmcw/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDY9HXLCT5WoDFzKP1Dw8FZyt3ecOVF0zSDogBTzgN2wicJlRDygN7bfQ/640?wx_fmt=png)

点分享

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDRwPQ2H3KRtgzicHGD2bGf1Dtqr86B5mspl4gARTicQUaVr6N0rY1GgKQ/640?wx_fmt=png)

点点赞

![](https://mmbiz.qpic.cn/sz_mmbiz_png/dzeEUCA16LKwvIuOmsoicpffk7N0cVibfDgRo5uRP3s5pLrlJym85cYvUZRJDlqbTXHYVGXEZqD67ia9jNmwbNgxg/640?wx_fmt=png)

点在看