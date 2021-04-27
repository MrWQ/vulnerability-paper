> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/-nkt5-VIyYV_XcjGdAIaTA)

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icldmVNyQI1jUlUr1pW87a2lzaI7kgMkibNdjvdtN9oT6UcyWz7jBEibg5Hh0iaOMS7VgqAplyJOK2TQQ/640?wx_fmt=png)

0x01 目的
-------

攻击者通过 CDN 节点将流量转发到真实的 C2 服务器，其中 CDN 节点 ip 通过识别请求的 Host 头进行流量转发，隐蔽自己的真实 IP, 从而实现绕过流量分析。

0x02 前期准备
---------

*   Cobalt Strike
    
*   公网 VPS 服务器
    
*   域名、CDN、HTTPS 证书 (高隐匿)
    

0x03 域名、CDN 申请
--------------

### 域名申请

这里推荐一个免费的域名申请站点 https://www.freenom.com/ 如果只是临时的话可以从这里注册一个，不需要实名～

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icldmVNyQI1jUlUr1pW87a2llTDNNT7OqyV7S1lATBkG0wygyDLybWbxB2APibK50ulxd6bFLicnu8DQ/640?wx_fmt=png)

域名申请

### CDN 代理设置

配置 CDN，这里使用腾讯云 CDN, 域名需备案（免备案 CDN 地址 https://dash.cloudflare.com/ 可以配合 freenom 站申请的域名使用）

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icldmVNyQI1jUlUr1pW87a2lEyH7kyJYhSHGrC46gmMWy7EVh9ibgtW8XONKL5icWBC2Q1ibZjeibZygOA/640?wx_fmt=png)

CDN 配置

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icldmVNyQI1jUlUr1pW87a2lBj5ULXfVchdBNIrs5JtzgyW9tbTsfWtnaOiclsPa73keX6qAziaGraXQ/640?wx_fmt=png)

CDN 配置 2

域名解析配置

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icldmVNyQI1jUlUr1pW87a2lN7RNcBBqiaKVM5lic6dtlYyiaaqc8ZgmPGPJKsdVfic537OibosmCcCdPyw/640?wx_fmt=png)

域名解析

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icldmVNyQI1jUlUr1pW87a2lIVW0Ra2chG65icpeibTULiavNss8fw0hrYhxxJicn6yFXhx6iczTXL6ES2g/640?wx_fmt=png)

DNS 配置

0x04 C2 配置、主机上线
---------------

### C2 服务端配置

从 https://github.com/rsmudge/Malleable-C2-Profiles/edit/master/normal/ 下载 profile 配置文件，自己也可以 diy 一个。

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icldmVNyQI1jUlUr1pW87a2lNKLuvnLK7C8RGUh3gSPu3ZoUWPg5HeJjJD9gWdoahic8e06Et1m9O6Q/640?wx_fmt=png)

C2 配置

配置好之后启动 C2 服务：./teamserver vpsip password xxxx.profile

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icldmVNyQI1jUlUr1pW87a2lWEh3zavibje6MMq1dovJzcKlsOg9JUV0Lu4HLCiaI1sNNpzC2BwRyWqg/640?wx_fmt=png)

启动服务

### 客户端配置

创建新的监听端口 (未被占用的即可)，http 协议创建后门文件，成功上线。

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icldmVNyQI1jUlUr1pW87a2lPgN9Do2kiazUpxQ24piaVpPl2NejwWSfdQ5NiaNbePvoslibE4ClkeZ5wg/640?wx_fmt=png)

客户端配置

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icldmVNyQI1jUlUr1pW87a2lzzuiak3w3yyvfLHLXDhaD6Rz10rBHuE9DJcqaiaNJibu6zpTPiaaaPjLqg/640?wx_fmt=png)

上线 - 1

winshark 抓包未看到自己 vps 服务器 ip, 受害主机外连 ip 均为 cdn IP 地址

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icldmVNyQI1jUlUr1pW87a2luuTBUick8DNn2JkkXbo3qbrQjvhEfppPpK6iaJlHgNwsIX2Wo3JntgXg/640?wx_fmt=png)

真实 IP

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icldmVNyQI1jUlUr1pW87a2l31rlyKq01auKgpzcCETGu25V1G7aKMCyyV0KMvoqxeKx9xvrEjwCYw/640?wx_fmt=png)

CDNIP

### SSL 证书加密上线

如果想要使用 ssl 加密上线, 可以在腾讯云或者其他平台申请一个证书，将证书导入到 CDN 配置中。

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icldmVNyQI1jUlUr1pW87a2lbbXVjySNTxrEYROxMuQtlFP561dN0ghPFPbIOvGxbhxHtichicYphuBg/640?wx_fmt=png)

创建 / 导入证书

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icldmVNyQI1jUlUr1pW87a2ldvnNxZSpowQyn5LexELxufs8WjVmeb2t5iavOl0NDaUlzbuWEMdqUicw/640?wx_fmt=png)

证书配置

https 协议创建后门, 成功上线。

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icldmVNyQI1jUlUr1pW87a2lB19UEVjgRj9h6FYDu4OP4CnZ4EQQ8Lv78iaW4MBMic4niaVm0zfGw3LXg/640?wx_fmt=png)

https

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icldmVNyQI1jUlUr1pW87a2l5MZEDdm5gIAE0ibP07Paye7LuCZA1kiaUYIGwLJwQRP92QWKwPepCD2A/640?wx_fmt=png)

上线

winshark 抓包未发现自己真是 ip, 均为 CDN IP, 并且全都是加密传输

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icldmVNyQI1jUlUr1pW87a2lOv0VqVWx9QtDaaRmy3WGiaR0YFYHdjnDoxQrwdrSvdzVNBC2uib14SDA/640?wx_fmt=png)

数据包

SSL+CDN 上线也可以参考此文章：https://blog.csdn.net/god_zzZ/article/details/109057803

本人转自：https://www.xffbk.cn/archives/8.html

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

整理之前师傅们的问题：无 pdf 教材、内容零散无规律、分享的工具文章几天就被淹没找不到了。

联合几位大佬一起创办了知识星球，定期会对技术文章、工具进行整理（包括 src、渗透技术、情报收集等）。

一律会员制，建设初期，前三天年费 80。  

![](https://mmbiz.qpic.cn/mmbiz_png/p5qELRDe5icldmVNyQI1jUlUr1pW87a2lice3gVfEgZPQBUWjfu4sm1YD20YoiaichXtNqjQDooV46ib3HDXT7FqEQQ/640?wx_fmt=png)