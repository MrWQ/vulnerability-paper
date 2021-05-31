> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/oQmmnPmCzY13XTu96pnMlw)

大余安全  

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **36** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/Q6e43UC3v1HiaBRGY9kMxh3tLO1aBBkGyOkLibppRwafQGLWpwuJO8ejicFmygc0xEug5gKuge6miasNIBiaIaiak0iaQ/640?wx_fmt=png)

靶机地址：https://www.vulnhub.com/entry/dc-6,315/

靶机难度：中级（CTF）

靶机发布日期：2019 年 4 月 26 日

靶机描述：

DC-6 是基于 Debian 64 位构建的 VirtualBox VM，但是在大多数 PC 上运行它应该没有任何问题。

我已经在 VMWare Player 上对此进行了测试，但是如果在 VMware 中运行此 VM 时遇到任何问题，请通读此书。

当前已将其配置为桥接网络，但是，可以根据您的要求进行更改。为 DHCP 配置了网络。

安装非常简单 - 下载它，解压缩，然后将其导入 VirtualBox 或 VMWare，然后就可以使用了。

注意：您将需要在渗透测试设备上编辑主机文件，以使其读取如下内容：

192.168.0.142 wordy

注意：我以 192.168.0.142 为例。您需要使用常规方法确定 VM 的 IP 地址，并进行相应的调整。

这个非常重要。

是的，这是另一个基于 WordPress 的 VM（尽管只有我的第二个）

目标：得到 root 权限 & 找到 flag.txt

请注意：对于所有这些计算机，我已经使用 VMware 运行下载的计算机。我将使用 Kali Linux 作为解决该 CTF 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/TLAfQEhpjHSPbp8RvqloqZfhr9oq4s6WqbTll9md0ZdsSxQCd5OvTakCISlraZ8vylH1cV3xQ3X6wE358HPuFQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/6DdW6admPmWicucEOicwONQBeMWRA7Pq57A9xCTGbIWomiboqObS0bEetoo2qW2hHk2E5GOcuQYUqSlQT5BKsDqRQ/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/M39rvicGKTibrmYlY2VW5XChia77yhteBC7iarNdYSwicq64NZrCHeSZqRpsFRTZkpfgclSWaibqftONNMWLkz6QjyoQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNDMYGwspIwkvqb9ibiceZ9ypC8GWWiaJam5OncHmhX1fJMjjbQ7fNLlXA1G3O0dfypZJXyrDia7ffiaYw/640?wx_fmt=png)

我们在 VM 中需要确定攻击目标的 IP 地址，需要使用 nmap 获取目标 IP 地址：

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNDMYGwspIwkvqb9ibiceZ9ypj6OUnFkRnNUCL1wiaXclMrCM5FwNJJMYe9ibPibQ52qwgfia5B5iaKX1nxg/640?wx_fmt=png)我们已经找到了此次 CTF 目标计算机 IP 地址：

```
192.168.56.132
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNDMYGwspIwkvqb9ibiceZ9ypKbuBSian1aLNtqiboR2qhyymG99tric1Q4Xtb6mOgBVBj1jDyhusuAlgw/640?wx_fmt=png)

nmap 扫描到了 22 和 80 端口开放着...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNDMYGwspIwkvqb9ibiceZ9ypCM2dec5sqM7bBXGKyu2RLzTHbJKXB1Gr50OBJZQ37IyB7vK4HjibibCQ/640?wx_fmt=png)

按照作者要求，添加 wordy 做重定向...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNDMYGwspIwkvqb9ibiceZ9ypxEVzvgAf25gzvTAzH0DXRIibgcO4aewsnQdIRnOXtfrKjCFH15PN9Og/640?wx_fmt=png)

这是 wordpress 框架... 基于 WordPress CMS 架构...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNDMYGwspIwkvqb9ibiceZ9ypkXMJYYgT7Hqk5HW0EibP6ZcnmCS9IRtnw26BPicqPibgYlUzicdpvichY5w/640?wx_fmt=png)

```
wpscan --url http://wordy --enumerate
```

由于是 wordperss 架构直接 wpscan 进行爆破... 这边发现了五个用户名... 用户名都放入文本中...

看过前几章或者了解 wordpress 框架的都知道 http://wordy/wp-login.php 存在这个登陆页面...

这边下一步需要知道用户名的密码... 回到介绍你可以看到，作者给了提示...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNDMYGwspIwkvqb9ibiceZ9ypEpsq2CAompgAzyqNAomKloPzZcgerIHpsntkk2rRaLTqeYCpBECnDA/640?wx_fmt=png)

意思就是减少我们爆破密码的时间... 缩小范围...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNDMYGwspIwkvqb9ibiceZ9yphiaqHf3JEpukAnOqPqMh3KldCqt7KRA7ASsIKLFnh6IOib2N4VwHNnPw/640?wx_fmt=png)

```
cat /usr/share/wordlists/rockyou.txt | grep k01 > passwords.txt
```

（按照作者要求操作）

```
wc -l passwords.txt
```

 （目前字典数量 2668 个）  

因为 rockyou.txt 单词列表包含 14344392 个单词，将其减少到 2668 个单词的事实可节省大量时间，这边直接使用压缩后的字典爆破即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNDMYGwspIwkvqb9ibiceZ9ypx4LqgcARw760VdFQaLmOvLPnam0bHGXEFBKbSwVOJiaTmSwo6GnaSvg/640?wx_fmt=png)

```
wpscan --url http://wordy -U mark -P passwd.txt
```

扫描发现就 mark 用户可以成功登陆

```
密码：helpdesk01
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNDMYGwspIwkvqb9ibiceZ9ypVhNRr5fibIrNdXB8SDMfRo7UMHoqeicxm2ichEG509v2Erb7zB5MW6icrA/640?wx_fmt=png)

登陆进来，我发现了两个信息... 一个可以上传个人信息... 一个是 activity monitor 插件，这存在一个很大的漏洞...

![](https://mmbiz.qpic.cn/mmbiz_png/6DdW6admPmWicucEOicwONQBeMWRA7Pq57A9xCTGbIWomiboqObS0bEetoo2qW2hHk2E5GOcuQYUqSlQT5BKsDqRQ/640?wx_fmt=png)

二、提权

![](https://mmbiz.qpic.cn/mmbiz_png/M39rvicGKTibrmYlY2VW5XChia77yhteBC7iarNdYSwicq64NZrCHeSZqRpsFRTZkpfgclSWaibqftONNMWLkz6QjyoQ/640?wx_fmt=png)

在谷歌上查询 activity monitor 如下...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNDMYGwspIwkvqb9ibiceZ9yprCDXe8Xp4xOJV884M4mFsn2ApTy5mR14EibwF02Ntk5RG9UrWoviciatQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNDMYGwspIwkvqb9ibiceZ9ypWRXLfmulshfCia5OaNv9lYN22iclMU6YSFLib8nhcw2ZXjQrexRoe44jA/640?wx_fmt=png)

下载放入本地后...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNDMYGwspIwkvqb9ibiceZ9ypRR54yYeLeU3E5p7Ag5NSLFnicMFvX7AmQbTEprXDwEX7Cg91Udl84zg/640?wx_fmt=png)

我修改了两处地方... 红框

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNDMYGwspIwkvqb9ibiceZ9ypftDoX0t1g9EdM0cZ5rG1b4Ybnux6oicWtxib1B3sXjtLkwaVNtM0eqiaw/640?wx_fmt=png)

执行 45274.html 获取反向 shell...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNDMYGwspIwkvqb9ibiceZ9ypP6nC4H1v7L3gFAXcS9kWBGqTwfMqRUH0dzPVwkK2HkSL2erKx3HHkQ/640?wx_fmt=png)

成功 netcat 获得了反向连接...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNDMYGwspIwkvqb9ibiceZ9ypGONBtLtE5hlxEu5qM7mQksJwZtMaxDibyQ1aCjichFlYhIelSVMXMKKA/640?wx_fmt=png)

遍历目录时候，我发现了四个用户，在 graham 用户发现了 backups.sh，mark 用户发现了 things-to-do.txt 文件，该文件存储了 graham 的密码？？GSo7isUM1D4

登陆试试...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNDMYGwspIwkvqb9ibiceZ9ypE6uFWibO5XaECb28gMahEapdLWYia9YTehjzwjxpicBhrDhtjicibIXkAOg/640?wx_fmt=png)

成功登陆...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNDMYGwspIwkvqb9ibiceZ9yp8N4ibV2T8Y8Vw5Xew57RicT4M7OfT8iaz6Eicmb9j34EYofC35UZFqOlfw/640?wx_fmt=png)

检查了 sudo 权限，发现 graham 用户可以在没有密码的情况下以 jens 用户身份执行 backup.sh...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNDMYGwspIwkvqb9ibiceZ9yprFPZG4PY33wiaoOvibGj8Kt85FLJo6TtGOI8eWibOPkNniajGTO8WUhUicA/640?wx_fmt=png)

查看 backup.sh，我添加了 / bin/bash 使用它来编辑该文件...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNDMYGwspIwkvqb9ibiceZ9ypun4vOckwSs5oNDDAILVrTzib2vcTTFfa7HP19My60pMGudLicIibOa9jg/640?wx_fmt=png)

```
sudo -u jens /home/jens/backups.sh
```

成功进入 jens 用户，使用 sudo 提权发现 namp 是 root 用户权限运行的...jens 可以 root 用户身份运行 nmap...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNDMYGwspIwkvqb9ibiceZ9ypEuGWcDNYhR1ItYlpo5JibicFibYRcKicjYPcubDYialQBmyPR8kDicnMy27A/640?wx_fmt=png)

```
https://gtfobins.github.io/gtfobins/nmap/#shell
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KNDMYGwspIwkvqb9ibiceZ9yptZNyo1b9CfVQvuvXBt2lLEllAWuHTicP9kNBS9FvY5bD24ZicDbZ56tg/640?wx_fmt=png)

意思是 os.execute("/bin/sh") 内容输入到 mktemp 文本中，然后 nmap --script = 运行即可...（这里一定要用 sudo 执行）

成功提权...

![](https://mmbiz.qpic.cn/mmbiz_png/Q6e43UC3v1HiaBRGY9kMxh3tLO1aBBkGyOkLibppRwafQGLWpwuJO8ejicFmygc0xEug5gKuge6miasNIBiaIaiak0iaQ/640?wx_fmt=png)

这台靶机是 wordpress CMS 结构，这边新知识是框架中具有 activity monitor 插件，利用该漏洞即可，后面提权直接是老方法了...

由于我们已经成功得到 root 权限，因此完成了简单靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/TLAfQEhpjHSPbp8RvqloqZfhr9oq4s6WqbTll9md0ZdsSxQCd5OvTakCISlraZ8vylH1cV3xQ3X6wE358HPuFQ/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)