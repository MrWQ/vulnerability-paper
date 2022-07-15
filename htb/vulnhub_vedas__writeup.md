> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/HAkPiAcHuFN_6ULSh0wcdQ)

首先通过网络发现，得知目标机器的 ip 为 10.10.20.138

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VYLkiax1bH3oYkSqqoicutomJdIw9qA224wNSyIfU86xJKPEsnAp6UdHnfwlGlFB9rLKIHNtJlK1NQ/640?wx_fmt=png)

下面进行基本的信息收集，发现目标开启了 22(ssh), 与 80(http):

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VYLkiax1bH3oYkSqqoicutomAciaugj1PpD7mr8diaOXDLiaEtlAD5eZkZTEfq7OklUCcrIwBTATDJecA/640?wx_fmt=png)

Udp 开放了 163(snmp)

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VYLkiax1bH3oYkSqqoicutomuXsvIHen2HoJ19CiaNXx9LLdtGHbOswh769tXe6UuQyYmfTUlibsUZpA/640?wx_fmt=png)

使用 msf 进行 snmp 枚举，获的部分信息，留存备用。

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VYLkiax1bH3oYkSqqoicutomOGIB7gicBibFYV96Tjqk5tWK6F1ujxwGKSAH6iaYemUw4tCevtuG8rxLw/640?wx_fmt=png)

获的 flag1:RigVeda: {0e87105d070afcb11c7264cc13f2e86b}

然后转战 web

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VYLkiax1bH3oYkSqqoicutomPV3k3HBSoLibRKucy5ictjq0U1xkiaGicETmhB3AiaXTptmv9W8ECpDusMA/640?wx_fmt=png)

随便点点没啥东西，就只能先爬一下目录了，先使用 cewl 生成一个目录字典

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VYLkiax1bH3oYkSqqoicutomxyEAAahDnNyZicoA0oxaN20Z91FohnDOqw8DdoE2CHH1Y3BzzczlxlQ/640?wx_fmt=png)

获得目录

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VYLkiax1bH3oYkSqqoicutomkfodQKpNeaiaeggA4odPPqjwfGRp1QotYRyy2Ge0zaWRnTMFWKfiaQXw/640?wx_fmt=png)

Cms 识别得到是 cms made simple

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VYLkiax1bH3oYkSqqoicutom5Co5FF0K1ppkF2kZOSHEibAxFIXQicRUGZvGicQ8uPAbKbB1zPG6YVfeQ/640?wx_fmt=png)

网上找到了 sql 注入的 exp

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VYLkiax1bH3oYkSqqoicutom5cHib4HgNqIWQM417a8p6rg3TIPka9hDMRrwfsT7KGn08u0geOxibCDA/640?wx_fmt=png)

利用之，得到账户密码

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VYLkiax1bH3oYkSqqoicutomdlthHBXEiaqdzrwBo2nqa0wibw5m75Mr1GiaMRdibA4Q31XtND2WXF8DOg/640?wx_fmt=png)

然后登录后台

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VYLkiax1bH3oYkSqqoicutom3Mib8m8SicJgvKTNlNYhPMvpOBEzYrot7clkL1gobiczlqoZibdXBqyMlA/640?wx_fmt=png)

找到第二个 flag

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VYLkiax1bH3oYkSqqoicutom70I8x3ZK47UViaibbRouvrGMXPiayOaBiaFb94meibBZh8DKQMnmTnA64Xg/640?wx_fmt=png)

使用得到的帐号密码进行 ssh 登录

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VYLkiax1bH3oYkSqqoicutom5gUQR45xichZpXicZbIZeanojiaGojZ5tIaHxmoO3S9cIeD53Pt1vIPQg/640?wx_fmt=png)

然后我们可以使用 -u 参数去获取一个 meterpter 的 shell

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VYLkiax1bH3oYkSqqoicutomUuibxF6fsnxoOYl16bsQEmsicP92F47Pj8Akkn8OgzmyV9pneX1N7zVA/640?wx_fmt=png)

查看网络链接，发现目标开启了 5000,3306, 因为 sql 注入我们已经利用过了，所以这里我们尝试转发 5000, 看看有没有什么收获

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VYLkiax1bH3oYkSqqoicutomGysRpa6JF58n56xOtjXcZBUOkyB9OLMvfgGxSN7Fyib5LuSX61QxXFw/640?wx_fmt=png)

进行端口转发

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VYLkiax1bH3oYkSqqoicutomGHgmibFOfKhSjKmzZLv96khzaZELOP8gWCTHpbGJXb84DYLfiaMhC3HQ/640?wx_fmt=png)

获的第三个 flag，。那么接下来怎么办呢？突然发现每一个 flag 后面都带有 to root，那么把这些东西都连接起来，搜索看看

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VYLkiax1bH3oYkSqqoicutom8uTzxtvlLZl8WPUw0oH3SKqH2ibaDsugfxJEoznWbH7iaKzMIF9XaC2Q/640?wx_fmt=png)

是 md5 的值。可能就是我们 root 的密码，先登录已经获取的账户

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VYLkiax1bH3oYkSqqoicutomEjCsWs1kXHt3l72CCgcynicNXVTev9OlIKqNcpTUGoHIIZ3dsRQgia8w/640?wx_fmt=png)

然后查看 home 得到所有的账户，使用刚才 md5 的内容，切换到另一个账户，发现是我们所需要的高权限账户

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VYLkiax1bH3oYkSqqoicutomSWYYw56yMt38kLlebRvQ8acuN8L2RVOkicS0lYs7NBC5xxMkq9EUsBA/640?wx_fmt=png)

然后就是切换终端，拿 flag 了

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VYLkiax1bH3oYkSqqoicutomz8sOA6oKqOQQx5XzmeXQkTQZyWaReK1SCowmJZfhPoTVX2EMuOiaglQ/640?wx_fmt=png)

     ▼

更多精彩推荐，请关注我们

▼

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08XZjHeWkA6jN4ScHYyWRlpHPPgib1gYwMYGnDWRCQLbibiabBTc7Nch96m7jwN4PO4178phshVicWjiaeA/640?wx_fmt=png)