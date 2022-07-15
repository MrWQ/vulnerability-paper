> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/mDtQeoyCs-KbsvCQgqKdkA)

推文开头，先学习一下中华人民共和国网络安全法，大家要做一名合法的白帽子，不要搞事情。

```
https://www.cto.ac.cn/thread-106.htm
```

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/khmibjLuVibFAUdnHOIkkz7lxuSSmdDAgnrhg238LjAKFCoamn2ick3uPzTlFibTXPdQns8KNAIiakSfpc0M5hEU6GQ/640?wx_fmt=jpeg)

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/khmibjLuVibFAUdnHOIkkz7lxuSSmdDAgn9KCtNqV7fpbyKk9UviaMnHV74CkEKBywWmL1WJStQpibUz9V3N5dZrhQ/640?wx_fmt=jpeg)

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/khmibjLuVibFAUdnHOIkkz7lxuSSmdDAgn4e9QAM4Zk0Mq0DJWrjibL2icf4jSkAInkzFibibC7tRNef61sJ0txibJTZQ/640?wx_fmt=jpeg)

本推文仅用于信息防御技术教学，切勿用于其他用途，有侵权或者存在危害性，请联系我进行删除。

> 某些原因我们这边拿到了一个 bc 站，搜集了一下信息找到的他的一个分站。
> 
>   

信息收集
----

是一个 bc 的分站只有等级查询功能，使用的是 ThinkPHP 框架.

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC594GBAIpQTZBagxO5iaGN2NKRhgaWb1Ty34PImLAxsBTwFdNU28JrG1kEgTSxvAGic8nicQZKlIGmA/640?wx_fmt=png)

开启了 debug 模式可以直接通过报错知道网站路径

![](https://mmbiz.qpic.cn/mmbiz_jpg/khmibjLuVibFC594GBAIpQTZBagxO5iaGN2XmEX9NQrVl2aatQXQkZSAbBNXTzGOcjtAdzQ8zzUicyuLwibQPh9JXVQ/640?wx_fmt=jpeg)

查看网站资产，发现有个 phpmyadmin，尝试爆破弱口令并不存在弱口令

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC594GBAIpQTZBagxO5iaGN2K0trRa9A6SYp1XYFDDgfPR4nKTCnvjwNjQdcI0SlsJlsrMFUguo2Zw/640?wx_fmt=png)

sql 注入 getshell
---------------

只有一个查询等级功能尝试 sql 注入

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC594GBAIpQTZBagxO5iaGN2eic8iaw5XAC3X9xL9Fe0ZicNw51FUgQVvyzyHZl7nKrS3hTFeXncenTuQ/640?wx_fmt=png)

DBA 权限，尝试获取 osshell，不知道什么原因拿不了，还可以 sqlshell，因为之前扫到了 999 端口的 phpmyadmin，sqlmap 跑不出密码想到添加用户登录 phpmyadmin。

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC594GBAIpQTZBagxO5iaGN26hUb8CkqZ2rlXcznDKF80ibtAxiclNYqGV4w1OQZhT0gcTU8q2psywmQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_jpg/khmibjLuVibFC594GBAIpQTZBagxO5iaGN2r85gPqtMKo0SqMuYd0R61oRU5IY5IUwpTnlaw6icJyLoxo5G5rdS5cw/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC594GBAIpQTZBagxO5iaGN25RZ2nAyLNZv4rnIsyTKbSglPRLVKFPTzibyaeickepwkZX7AZxbtc5nA/640?wx_fmt=png)

哦吼先进入 phpmyadmin 脱裤有好几个站的数据库，之后使用日志写 shell 拿到一个站点的 webshell，但是禁用了执行命令的函数绕不过，然后到了 9 点网站关了只能访问 phpmyadmin，想到不同站点用的 php 版本不同可能有没禁用函数的，尝试 phpmyadmin 写，可以直接执行系统命令。

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC594GBAIpQTZBagxO5iaGN2EuJ0ibZ019x7ANkoiaAYY0lIufic3n4Po5YziaRQwp0DWIzeR6tJ1hzicGg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC594GBAIpQTZBagxO5iaGN2B6YZGylODLYCB6VYEKaxrVaXGFvFFPRRBf3xKpFhpNfntoNuWZicAzg/640?wx_fmt=png)

哦吼直接 system 权限，都不用提权了

RDP 登录
------

system 权限直接给他加个隐藏用户上去看看

![](https://mmbiz.qpic.cn/mmbiz_png/khmibjLuVibFC594GBAIpQTZBagxO5iaGN2DOEia5HicULJxewqoNKpvVhpbJmhq2QHwWy8cmegCtpUhiaaq6iavq4EDA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_jpg/khmibjLuVibFC594GBAIpQTZBagxO5iaGN2xVxmZ1bY3ibuZIaM1NySjGicnOiazL4DnOe8cDAaoI9RHS0UN4EWoRkPg/640?wx_fmt=jpeg)

这里也有许多干货喔  
  

**↓↓↓**

公众号

**↑↑↑**  

欢迎关注（排名不分先后）