> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/u40x4dU4x82LaL2VuHHnNg)

前言：最近一直有小伙伴问我，可否发一些渗透测试方面，挖 src 思路这些，那么我们接下来将主要分享这些。

今天将分享一些绕过 cdn 获取真实 ip 的方法  

1、是否有套 cdn  

首先我们拿到一个域名，比如 baidu.com  

可以用多地 ping 的方式，看一下是否是多个 ip  

http://ping.chinaz.com/baidu.com

![](https://mmbiz.qpic.cn/mmbiz_png/NOwiaSy3Kbv2TUW3IicCMgLhsAW8cEUB8FHULQ6PPjnDqTcqsMQo5mic6mA86iaWbia3ic1JZ49P5W2s0Qsm04K5ImiaA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/NOwiaSy3Kbv2TUW3IicCMgLhsAW8cEUB8FCFZpUAmjp4boElbYdGQ3Bxz6g0dwD3uHFAW6rLQyezS7moDbwM8skg/640?wx_fmt=png)

这里明显是套了 cdn，当然我们还可以使用 nslookup  

![](https://mmbiz.qpic.cn/mmbiz_png/NOwiaSy3Kbv2TUW3IicCMgLhsAW8cEUB8Fuu7ZTllZIZjibpo0iakT93uKMsn4X6jicTC468L0OhOSqVzUSBSbeRhTg/640?wx_fmt=png)

出现两个 ip 或两个 ip 以上，就明显是有 cdn 的  

2、套了 cdn，如果获取真实 ip  

这里就到了重点内容  

方法一

可以用邮箱获取真实 ip，正常在某个网站上注册时，人家都会发验证码给你的邮箱，进行邮箱注册。  

我们点一下那个双层的向下箭头  

![](https://mmbiz.qpic.cn/mmbiz_png/NOwiaSy3Kbv2TUW3IicCMgLhsAW8cEUB8F9gh29LouJcbWtpxFK2EtQAAl1icPxf9Q9ar264dBPy4UzOqkpeXy6gA/640?wx_fmt=png)

显示邮件原文  

![](https://mmbiz.qpic.cn/mmbiz_png/NOwiaSy3Kbv2TUW3IicCMgLhsAW8cEUB8FjwntBvz8RoxBxJrLfGCibagZTcjy3EiaWD78LibCOLINZtoGLm0iaDyLsw/640?wx_fmt=png)

这里就出现真实 ip 了  

![](https://mmbiz.qpic.cn/mmbiz_png/NOwiaSy3Kbv2TUW3IicCMgLhsAW8cEUB8FnmWJagyIOCpgQmeuzCMkjhiaZLj2aziasDWDyITKsoJx7icgPDJEGyZOw/640?wx_fmt=png)

方法二  

查询 DNS 历史记录

https://dnsdb.io/zh-cn/search?q=baidu.com

![](https://mmbiz.qpic.cn/mmbiz_png/NOwiaSy3Kbv2TUW3IicCMgLhsAW8cEUB8FkibXT6ciaTpSZ9erUQqb0ZfylJibWchs3LaCQWRL43tjhAzWvjOlXTn2g/640?wx_fmt=png)

当然这里我们推荐这个，会比较准确  

https://securitytrails.com/

![](https://mmbiz.qpic.cn/mmbiz_png/NOwiaSy3Kbv2TUW3IicCMgLhsAW8cEUB8FqVTvmT2VUicvo1CYvfibBjqlNCso5XAtuJCwNjql9KMJNEPMpy1EMVrw/640?wx_fmt=png)

方法三  

查询子域名，为什么查询子域名，因为有些时候一些企业只在主域名挂了 cdn，子域名却没有，所以可以从子域名先入手。

这里推荐 layer 子域名挖掘机  

![](https://mmbiz.qpic.cn/mmbiz_png/NOwiaSy3Kbv2TUW3IicCMgLhsAW8cEUB8F7ic8BWGrpaUoaM5C9Q0GHtWqkJe4P6v0Dj2Nem2z8Rh0c60Nnm6dxiag/640?wx_fmt=png)

可以到星球下载  

![](https://mmbiz.qpic.cn/mmbiz_png/NOwiaSy3Kbv2TUW3IicCMgLhsAW8cEUB8FBflhlIRYicPgxBJNCZwKLCj8KkKSia53ia4ib5ogmN4ZZmJNUTg3mCI6SA/640?wx_fmt=png)

方法四  

网络空间搜索引擎，可以查询到原始 ip

第一个 fofa

![](https://mmbiz.qpic.cn/mmbiz_png/NOwiaSy3Kbv2TUW3IicCMgLhsAW8cEUB8FK4IM8Ot5sIt2ZkNMhmth9up9BaPn5fGTvhoz34lQLYRickRYDmqlSaA/640?wx_fmt=png)

第二个 shodan  

![](https://mmbiz.qpic.cn/mmbiz_png/NOwiaSy3Kbv2TUW3IicCMgLhsAW8cEUB8FljZYf1fLtJAs7gKhtA7rwmXAuv7CL2EO1j8ribG50viaDwGTsPq4x8TQ/640?wx_fmt=png)

第三个钟馗之眼  

![](https://mmbiz.qpic.cn/mmbiz_png/NOwiaSy3Kbv2TUW3IicCMgLhsAW8cEUB8F79F5fNYkDclbia6ALzUPhibDem32gQL7c5MMUCbqloQicnAtyPhEaNzCQ/640?wx_fmt=png)

方法五  

利用 ssl 证书获取真实 ip  

https://censys.io/

当然还有一些其他方法，比如 phpinfo.php

还有一个是国内很多 CDN 厂商因为各种原因只做了国内的线路，而针对国外的线路可能几乎没有，此时我们使用国外的主机直接访问可能就能获取到真实 ip

到这里推荐一下 peiqi 师傅的公众号，干货满满，喜欢的可以关注

公众号

更多渗透测试，也可以到星球里学习

![](https://mmbiz.qpic.cn/mmbiz_png/NOwiaSy3Kbv2TUW3IicCMgLhsAW8cEUB8FKV3NktCRVJ7W14sblwk73stL4P86DViaCoG069BgrcIFVZShmW6ZbMA/640?wx_fmt=png)