\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/V0cTKJrzMPgC6xyueUSx7g)

说明：Vulnhub 是一个渗透测试实战网站，提供了许多带有漏洞的渗透测试靶机下载。适合初学者学习，实践。DC-2 是该系列第二版，以下内容是自身复现的过程，总结记录下来，如有不足请多多指教。

下载地址：

Download (Mirror): https://download.vulnhub.com/dc/DC-2.zip

目标机 IP 地址：192.168.5.138  
攻击机 kali IP 地址：192.168.5.135

同网段信息收集与 DC-1 相同，不做过多的叙述。

**\*falg1**  

1、arp-scan  -l

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9tWyXxBVnBlKJj7lwObVRDOoY3QhzCPcFMCP9zTciaHJhibW6iax4vJ5Bw/640?wx_fmt=png)

2、扫描该主机开放的端口，发现开放 80 端口，尝试访问。访问失败，本地无法对该域名进行解析，修改 host 文件。

nmap -sV -p- 192.168.5.138

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9njH0KwB1uTwic9gq0l9GXarpAt2wqFMkJicVpQquibQfEnu2a2So2QR9Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9EJs8jMyv0V1sVjHS57U75oCPtmPctiaHAn53IibUsqzAqp6YbqyQu5Ww/640?wx_fmt=png)

3、host 文件修改

        vim  /etc/hosts   添加内容为：192.168.5.138    dc-2  修改后再次访问，即可。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9P9JFB1NNsmhdPfRNyo8S88ZvmhKgL1a11ZdD5SCVZHqAN7Uz1XrPug/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9slBQSicOwG4YaGwJrIHMofeBPM9sY0vWgUamHDc7ibSZMkcQicRicNodibg/640?wx_fmt=png)

ji![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9MEOYYqdspvBr1w2k26zIz81QzyqGyZ1RnIYkPTdurworYOK8rAjgMA/640?wx_fmt=png)

进入后发现该站点为 WordPress（WordPress 是使用 PHP 语言开发的博客平台，用户可以在支持 PHP 和 MySQL 数据库的服务器上架设属于自己的网站。也可以把 WordPress 当作一个内容管理系统（CMS）来使用。--- 选自百度百科）以及 flag1。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9icEdHrCkdBeZJUex82Tibucc7guDACgCEZNjLLdlc58iaTHiax4oVZ5iawQ/640?wx_fmt=png)

**\*flag2**  

根据 flag1 的关键字（如：cewl，password）等。

cewl 介绍（Cewl 是一款采用 Ruby 开发的应用程序，你可以给它的爬虫指定 URL 地址和爬取深度，还可以添额外的外部链接，接下来 Cewl 会给你返回一个字典文件，你可以把字典用到类似 John the Ripper 这样的密码破解工具中。除此之外，Cewl 还提供了命令行工具。）

命令 cewl -h  查看 cewl 的用法。

根据提示使用 cewl 来爬取密码。

cewl -w DcPassword.txt http://dc-2  

收集 238 条密码。  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9qgqT38DmYdt5EMdnUNSG1JMuJKE8jxhMvVgf1H2pknRc2ibdcM8tmpQ/640?wx_fmt=png)

目录遍历，找到后台登陆页面。  

python3.8 dirsearch.py -u "http://dc-2" -e\*

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9moBt7icYjPSPIeRUUQnpj8ib4PlNPClqtgAzsjZQneCIksnVCLeibG2ibQ/640?wx_fmt=png)

访问登陆页面。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9DTVBCEPYVKjzrUFaYHdGlKObn78Qy35CVrtQEJLicvKUKtlamibohZwQ/640?wx_fmt=png)

使用 WPScan 工具扫描网站，并对用户名进行扫描。

WPScan：WPScan 是 Kali Linux 默认自带的一款漏洞扫描工具，它采用 Ruby 编写，能够扫描 WordPress 网站中的多种安全漏洞，其中包括 WordPress 本身的漏洞、插件漏洞和主题漏洞。最新版本 WPScan 的数据库中包含超过 18000 种插件漏洞和 2600 种主题漏洞，并且支持最新版本的 WordPress。值得注意的是，它不仅能够扫描类似 robots.txt 这样的敏感文件，而且还能够检测当前已启用的插件和其他功能。

wpscan --url http://dc-2/ -e u 

爆出 3 位用户，admin，jerry，tom  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9wSeCv9FgEIm2XBLqYolyACgkOdCIpyGI6ZtTgmThasmKcs0xWQCYXw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9VTkB4MiabezbRqUT8MAKleSGMk0fIJy6VJMZslYGclzaxwFrM3DrdSQ/640?wx_fmt=png)

使用 WPScan 进行爆破。

Username: jerry, Password: adipiscing

Username: tom, Password: parturient

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9F6Qk5eiawjuO12GFzFzkQtkYKAVc3VQdTvJDwy7G5q3RoextgfRuqKw/640?wx_fmt=png)

登陆后台在 Pages 里找到 flag2

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9jv6QR0JPcTxUDa9uJpZ4dYDia3Xia7ibqMicSqlkHOAibDrMZVKuEqadIog/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9Dibk1gkHM4LRQuRUDjBgCJM2SWtXia4kTpnZ0iaLWS9xqVs17Wnplc53g/640?wx_fmt=png)

\*flag3  

flag2 提示要换一个入口，在扫描时发现对方的 ssh 服务正在开启中，端口为 7744 尝试连接。尝试连接，

ssh tom@192.168.5.138 -p 7744 指定端口连接，用户为 tom（名字好记）。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9BFOfgmLoRRuepF4ytjxyGtT3D5GeaHOte4LsoeKJdsoOsGHeFvGzibQ/640?wx_fmt=png)

当登陆成功找到 flag3。  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9clDqqNZnVqpG0dXicVzMYDd03bdibooayZzAzXUuK1ibkWwAx8OqssLog/640?wx_fmt=png)

发现无法执行命令，命令执行受限制。  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9qUg0DxoMsPg7m9L7Mibet3mia3o0y4DZiaIOfZfQXXzXZSyD661qz17qg/640?wx_fmt=png)

rbash 受限 百度一下解释如下：rbash 就是受限制的 bash，一般管理员会限制很多命令，例如 whoami cd cat 等很多常用的命令，不过肯定会有命令可以使用，我们可以查看 $PATH 有哪些，或者自己挨个试。

    1、echo $PATH #查看自己可以使用的命令

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9DSJmM7iaOb3JovmopUrcLxD7rHPx7ofial9zza3ibp1zwib3GqkKDvyI5A/640?wx_fmt=png)

        2、echo /home/tom/usr/bin/\* # 查看可执行的命令

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9miao6RicVUfo4DqWhZarQ2QggwD58aEtQ8f4qaBFSt1mJWJJGEpobESg/640?wx_fmt=png)

vi 对 flag3 文件进行查看。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9wgox8a4zq0xERkFgj6rzucuLEWRRVc8ibvtqH0y6PDGV2xjOZQsP8ibg/640?wx_fmt=png)

注：对 "rbash" 逃逸有兴趣了解，可以共同探讨。

**\*flag4**

flag3 提示我们要切换用户 Jerry，下一步对 jerry 进行切换。开启新的 shell 发起连接，发现无法连接，还是要进行 rbash 逃逸噗噗噗，不太明白这东西的原理那就百度好了。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9TFiaRKKiaLuD5icE692AgIxibWCxqFMIqc7asMxWfiaeHicFGSJBFfq1icCmg/640?wx_fmt=png)

BASH\_CMDS\[a\]=/bin/sh;a  

    /bin/bash

export PATH=$PATH:/bin

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9fQBsEsjTINyl4vItpDgq5dKOe7uaCTh1jslFTpDt3XvJ2GVO25wR1g/640?wx_fmt=png)

成功逃逸。

切换用户，连接成功。切换到 jerry 的家目录发现 flag4

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9t933icibWNGlpAJukDSMCfyNGSMTCrZiaClcnHF6gQW6LyCsdS4oKRFUg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9OT4ibwE0XXsl4mNSnOEujjSVHxYxTKaibYoYd7tbEzO3NweI7F8U4Vdg/640?wx_fmt=png)

flag4 提示我们还没有结束，提示关键字有 git，git 是一个开源分布式的控制系统。  

sudo 用来以其他身份来执行命令，预设的身份是 root。

sudo -l  # 列出目前用户可执行与无法执行的指令。该用户不需要 root 密码，以 root 权限来执行 git。

通过 git 缓冲区漏洞进行提权。  
git -h 选项中 有一项`-p | --paginate`这个 - p 的意思就是以分页的形式展示 git 的帮助信息，但是这里他会默认调用 more 来进行展示。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9ggtGwP2cGaIgsBtfWAMcficaQK00ViaibPibwcUrBiaNeE1RrUlibErUMhVw/640?wx_fmt=png)

sudo git -p --help

!/bin/bash 提权成功。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/zg4ibGYrEa24BvNcvIBhyg95tlHLwW4G9ZM6nVoMag6lZTeJlCXvphicCGtQeLjMLJP6Wan5HkYyOicXZrPqoxUVA/640?wx_fmt=png)  

参考链接：https://www.bilibili.com/read/cv7955909/

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