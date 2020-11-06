\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/qWks8K-K-B5cFeVP8UlUCw)

  

**上方蓝色字体关注我们，一起学安全！**

**作者：零度安全攻防实验室**

**本文字数：1445**

**阅读时长：9～15min**

**声明：请勿用作违法用途，否则后果自负**

**前言**

这次我们团队里面的 Mix、阳光宅男、azeng 师傅有辛参加了这次南京 DEFCON GROUP 的线下技术沙龙，也结识很对大佬，跟大佬们面基。在最后还参加了这个渗透攻防挑战赛。

**现场黑阔云集**

![](https://mmbiz.qpic.cn/mmbiz_jpg/yaFib21icvRicBomWVL0g9UCRPphVibM6iadJLVglPHZDg2LLDFPNM0jQiaHCmB424YQ6AIZOb92N3rnIHGYHQiaDbCibw/640?wx_fmt=jpeg)    

**墨者学院的负责人 Image 给大家介绍这次对抗赛的网络拓扑环境:**  

![](https://mmbiz.qpic.cn/mmbiz_jpg/yaFib21icvRicC9ibdXEjSbxop9sBCjYPKD56Kcm9HnLfiawI7pP6iaHohibpOGAh6z2GvdhJmYXIf4pHrGJicicVUytTtw/640?wx_fmt=jpeg)

**正文**

   首先我们访问目标系统：

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAibV6GZibdbV8MLgpWrrEInibxIxZC8Bib9CFUehnMgzx7W9LhOPeCIfl3A/640?wx_fmt=png)

 **这里提示了：信息搜集的关键点**

        尝试爆破用户名密码：

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAQSicphJjQydQZDw3o6NZlHAfl2PAZlzzfIXRVHVYuWSXia2VNd41fPYg/640?wx_fmt=png)

        Admin 账号输入发现输入账号密码登陆并没有回显账号密码输入正确或否刚开始认为只是账号密码输入错误没有回显，但只要能密码对上可能兴许会 302 跳转，爆了两轮会想起开发的测试系统，于是决定尝试用 test 账户登陆。

        先随便输入了一个密码

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAQRMkodE7rhrN1sKhFibSGUKFu5cHhP1JvRriakuuVicwYvz6yd2YyibfBg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAibUHSU21SgwlddvHGJUiaXicfibIgfw0icnuZvMlV4OjGVwSFvJia22oqMoA/640?wx_fmt=png)

    发现有返回结果，于是用 burp 放字典进去爆破，这里就不阐述了！

    快进到爆破出账号密码 username:test password:123456

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uA1fVLd4CghnPRR4xicQ8VFBIFxYiaoiaNHpGz2zQC39R0ebA9Jk1ib3yuVQ/640?wx_fmt=png)

    在最下方拿到第一个 key

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAGQCwz8RuFlP3mqLlCTaYCbj8lZIwXcSQGqjDHWgAg0BSR2JKcFia7VA/640?wx_fmt=png)

    后又想到他之前的数据共享系统叫 DCNL-db 于是想去看看 github 有没有相关信息。

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uArfdNicKsVpufFdfo5Pia81opa53Y256E7D5zglic6k02pol3Viat7OZ0oA/640?wx_fmt=png)

    发现了一个近几天上传的代码，（肯定是他了）

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uA6fVsIlMN1B3R0tSW6kPvj4PsGdjKf9K9GXIwF6KKWpWib5pHjddBrBg/640?wx_fmt=png)

    打开 mxxn.py 发现了华为 obs 对象存储服务的 key 和 Secret

    通过翻阅资料找到了一个叫 obs browser 的工具，于是去了官网下载该工具。

    添加一个新的账号

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uA57EMKuqngoTS6Ac2aRojzkfAjMgRzEpSDpnZvFwZ0v2MkaSjYaoN0A/640?wx_fmt=png)

    在这里看到了很多存储桶，然后就可以继续往下深挖了

  ![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAEDbDC8C65ibymiasUXTmUDubabsZwZFMRbN6aujRYXXibCPwKrdfkb0ibg/640?wx_fmt=png)

    Dns 那个桶里面没有东西

    Eveloper 中存放了第二个 key

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAfUeQpUM0CrTV8xt8kYORPml3PKWDV4syc2u5CmgwITK8zVc4hshj0w/640?wx_fmt=png)

    并且发现 mysql\_tools.py 之后直接把 mysql\_tools 下载下来看，发现了 mysql 的连接账号和密码，直接拨 vpn 去连 mysql 就行了

    再晒上一个现场战况的照片  

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uA98nCpJbLcqPL7iacK1ywrM3WDiamSciaVZROdsv1NHhvic8TaO18gn0ic5w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uACAwy8bA33KGluqaxRwhABQgibwlUhNNl4QUKU9ibQYsbHwKAhtNXicbQQ/640?wx_fmt=png)  

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uA3GBynYYOLO9KkLup5XPzniaNemDviaZImDzfkHuF9VMWKNcwQ4oOeJZw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAericibOArIpHC8XCFsDM5bibdo73cDfumH7x58MPTF8G9xN8V97qZ7TWA/640?wx_fmt=png)  

    继续往下深入在一个叫 wangjun 的文件夹中发现了一个叫服务器. txt 的文本，发现了密码，但是并没有给 ip 和账户，问题不大后面应该能用到。

    但是其实这边应该就能猜到账户名有可能就叫 wangjun 或 root

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uATqRh4oJaSenK1CW51I2xeP5Hn4fyj1GrU5jE1qFOzou1fxhlHT3JbQ/640?wx_fmt=png)

    在 DB 文件夹中发现了网站的源码，发现并没有什么用，并且尝试了上传操作，显示并没有权限

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAKMX0dl2IZpbichYvCIwFSO6JgopHbicfpJDgsr0rouPe6rzYyI1u9tRQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uABPJngf7Er5BFXiaAg9ZVbcH3xROXGvjBiaaZia0KMQhwuyeQkMAHkdESA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAZRvWiaHhYLpE1Kc8rZiaud34CE1zrRiaj6HwQF0k2PYAeSHKmXf2XoCiaA/640?wx_fmt=png)

    再去到第三个桶翻看数据，并没有什么可利用的数据

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAENucUPwNngenNzssrgAIegSXL9BTaDjekTxXSVIh2fXDjicMbMlJ7jg/640?wx_fmt=png)

    外网信息搜集部分工作完成，接下来可对内网进行渗透，首先我们需要获取到靶机的操作权限，能够让我们执行命令运行程序。

    使用我们之前信息搜集在 mysql\_tools.py 泄漏出的账号和密码进行对 mysql 的连接，这里我使用的工具是 navicat

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uA3GBynYYOLO9KkLup5XPzniaNemDviaZImDzfkHuF9VMWKNcwQ4oOeJZw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAeERuGFRA1ib6RiaUOjv7mFnxV1Jdtc486nE3KxO7tKYzicqmIsIuJCzWQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAXw0S1tk7xvpT4RXf3WZs80Viau43Dw10M9CtKpfbR1BmdUqobn7WxEw/640?wx_fmt=png)

    拿到第三个 flag

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAqluGMy6taKGjRibiaGk6ib63FRX5mdVM5VNDo6cY0bKHKicww06x8K7d2g/640?wx_fmt=png)

    然后开始对这台机子的相关信息做搜集。

    使用 load\_file 函数对靶机的铭感路径进行尝试，获取到一些有用的铭感信息，但我们现在的主要目的是获取到网站的绝对路径从而写入 webshell，次要目的是搜集关于这台机器上的其他辅助信息。

    查看一下 mysql 的版本信息:

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAY2MrDH6wjKaPuqOqSlykqKquJ296gqymzq9KEnNFG4UMgxOVJfyo5w/640?wx_fmt=png)

    Select load\_file(“/etc/my.cnf”);

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAPYOetEyTtFhBmlHkpvKqEDFDIEfEJUHib10CyIe3InYibBnFJgWymuuw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAuJIrMP8UH7RMMrOJywSN8oqpSj2LaK6U4gjsMc6RkkMriaGriaI3H67w/640?wx_fmt=png)   

于是我们尝试写入一句话，发现没有权限

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uArAlyh0FicOmsHxbTVemOO0egaD5IopebYcbh3WicUXr5GZuqr7DibEKlw/640?wx_fmt=png)

    那就说明很有可能路径并不是这个，那问题来了不是 apache 的服务，那是什么，难道 ngnix？我怎么确定他是 ngnix ，于是通过.bash\_history 发现了一些信息并确定是 ngnix

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uATS6yxJwZlsbsudSTDQxon6h7p8Dphkh6nWQVTmsDHsSYSCibZztPsoQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAIU158ukSI72ibGklMYA1Wy81rFT90QngibtoeQ2JdTbNs59Nicu3ETmLQ/640?wx_fmt=png)

        直接通过 load\_file 读取 ngnix 的配置文件, 总算找到了 web 路径 /dcnl/db/html  

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAwjAuZtBlF32reKqpe9ibNcUOUwldqv4apicAo9I3arx5PicGlYSX1FFQA/640?wx_fmt=png)

    通过 mysql into outfile 在 web 路径下写入一句话

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAkurnHVoOwpN25JlmMicMneETnUEpuSjBibUc06xwTJK54SsOibCL7d7Rw/640?wx_fmt=png)

    通过蚁剑连接

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAfoUOPWlW26PIWFUrz0jkkvsSXreuY5eB5p662RyVb1sFuj1iaPKILwQ/640?wx_fmt=png)

    拿到第三个 key

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uA4ygvkzQbk7ibuZyicLhVNHA7pefAE3mIpYv61s7WF4FeYbBJOrbNldNw/640?wx_fmt=png)

    继续信息搜集，这里我上传了 LinEnu 信息搜集的脚本

    内核信息

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uALCUIiaYic8KxoV9j1AI6XSSGIjXrLXf3LZxrEzncbCvuiamY5sp0Wh1icw/640?wx_fmt=png)

    系统版本

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAtZMaLwx37PJGiapqhmAdt5iblic1GyQnIRWoLMHYmvAZwyMqRxsSQaMhA/640?wx_fmt=png)

    这里看到了一个 adm 的账户，但是他并没有登陆的权限，所以之前的密码应该用不到这里

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uA72SYO8lsTK7aVBMoOjSuBkrtmb6nM5mT5uMyRO2QKOSibuJbIre8BiaA/640?wx_fmt=png)

    通过用反弹 shell 的方式尝试用 root 账户登陆

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAibZrre8OmX2wSRHdLABwqwsjDhJnPXpJm5W0cqMap1X11e5zDYf97bw/640?wx_fmt=png)

    貌似并不行，继续往下信息搜集，发现他是 sudo 的 1.8.23

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAg8UYfRib2CTHekia6cN1mrxKmdHqWfOuMwAbUH6FG3fDFhZRAUv8CPiaA/640?wx_fmt=png)

    好吧想起那个 sudo 的洞，可是然并软 要改配置 / etc/sudoer 没权限

    在搜集一下网络信息差不多就这台机子的信息就摸遍了

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAuVQhOXYp1O23EzEiaYRFwjYAE88lLjkyicAl9sE178BY8mb9t847aWLg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAicWRl0OwiaOOE02AjaKBuImD0APtWibFhB1x3WiavBWjo42ibeLARvcCRNA/640?wx_fmt=png)

    获取一下相邻主机的 ip

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uATGdibjNNrEicykc5L9icuFdL2Wib6u9S9StYsVHfx2XfKPQFNrHicmjE0UQ/640?wx_fmt=png)

    相邻机子有点不想摸了，直接看能不能到 192，直接打 192

    扫描了一下 192 段的信息发现开了 22，8080

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAGzZSsMFuYd8frJjeryFITO26Ria5xtd73lFtsib2LicHegibIic0XZGZNsg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uA8iaEzibmq2zB8gnSBUwUvERsRAp5D2Mtiaf1p7bj1Fc0VeH9ZLxw8HdPw/640?wx_fmt=png)

    这里有一点就很神奇，之前泄漏出来的配置文件里面是 192.168.0.39 但是 192 段只有 37 这一台机子，挂了 socks5 连接 39 也连不上。

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAoFpyYvIZslTuAxZPLJKsoZd28JA9icMe7CuBKBhXK0dPrObvHjvqALA/640?wx_fmt=png)

    于是用 php 脚本扫描 192.168.0.37tcp 端口开放情况

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAich7ZR5ymynaVjc3hYQasdr1pHtGVo4JP6aYGaS9qvZYZujSkMKzdSQ/640?wx_fmt=png)

    用之前的密码尝试能否登陆，得到的结果是直接 timeout 换了 n 多种方法都不行就卡这里了

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAwLItQL9YOkCdzqLN2QpOdv3eGx1fkpxmsPm8w44c97exCkFlKDXEsQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/eqGGHicCG3MayjHf0ib4almO7w8zLXk6uAp28hzIBQxPb77ib8Zrhb84SKg6vlOTNYkiaQ742MzlssJE1t9p6ArTgw/640?wx_fmt=png)

    罪恶的渗透之旅就卡在了 dmz 很扎心，有好主意的小伙伴可以来联系我，我们可以探讨交流看我们哪一步忽略了！！！！

 **有想法想要交流探讨的朋友，可以在公众号回复你的微信号我加你们一起交流！！**  

![](https://mmbiz.qpic.cn/mmbiz_png/VfLUYJEMVsiaASAShFz46a4AgLIIYWJQKpGAnMJxQ4dugNhW5W8ia0SwhReTlse0vygkJ209LibhNVd93fGib77pNQ/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/eqGGHicCG3MaM6jPic7CE6ib8esib9oj7R2tibNwPiaiauYJ7o3iaaVAsqodoXvtibm0q6FJfNykgonVku5AI4j97Yfm7KQ/640?wx_fmt=jpeg)

点赞、关注、转发、走一波  

零度安全攻防实验室

安全路上，与你并肩前行