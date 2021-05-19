> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/xVIXGxMACM-n9iBu42KbMg)

**1、描述**

  

jeewms 是由灵鹿谷科技主导的开源项目，WMS 在经过多家公司上线运行后，为了降低物流仓储企业的信息化成本，决定全面开源，是基于 JAVA 的 web 后台。经过代码审计又发现了命令执行漏洞。

  

  

  

  

  

**2、影响范围**

  

JEEWMS 全版本  

  

  

  

  

  

**3、漏洞复现**

  

fofa 语句：body="plug-in/lhgDialog/lhgdialog.min.js?skin=metro" && body=" 仓 "

  

  

  

  

  

  

演示一下

一、权限绕过漏洞

1、漏洞代码位置

```
src/main/java/org/jeecgframework/web/system/pojo/base/DynamicDataSourceEntity.java
```

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCDtzBMvLolYIMwXwibmu2rupPYoX6oNK9apnBicobcWxvGcqVn0pxpuEgXZiaclLtxxR5vgtKiczjvvA/640?wx_fmt=png)

mysql 版本 <mysql.version>5.1.27</mysql.version>，可进行 jdbc 反序列化

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCDtzBMvLolYIMwXwibmu2rus2PpKRwO9tmSFcwGibzNEcicziaayrzfLzuMSeGM18nicWCW7LCNTGqfnw/640?wx_fmt=png)

1.  漏洞代码分析
    

src/main/java/org/jeecgframework/web/system/controller/core/DynamicDataSourceController.java

此控制器可传入数据库 jdbc url、用户名、密码，因此存在 jdbc 反序列化漏洞

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCDtzBMvLolYIMwXwibmu2rulMDcDibIBnwW4UicPUGfaopqHiarfneZgiaMvGmKN5aOKTGaaxeYCALJibg/640?wx_fmt=png)

DynamicDataSourceEntity 内容：

```
src/main/java/org/jeecgframework/web/system/pojo/base/DynamicDataSourceEntity.java
```

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCDtzBMvLolYIMwXwibmu2ruDfnAgF1dZLEZ88TyrrCXjPoZfykI0kicKtuNhkD7ADibGpJUVG8njUlg/640?wx_fmt=png)

已知 jdbc url 可控，存在 jdbc 反序列化漏洞，无害验证如下

启动虚假 mysql 服务器

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCDtzBMvLolYIMwXwibmu2rudwfk8Dia0YMgI1K8ENeUDAZmwXceOictRPtsvmkBwgbC7ibhmlkr8gCwQ/640?wx_fmt=png)

发送 payload：使用了前篇文章的未授权绕过漏洞

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCDtzBMvLolYIMwXwibmu2ruEdMkqdzOMTryVZOkuB5deNSjic6ExvMtahpc263um56Ljgwx7TfsLew/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCDtzBMvLolYIMwXwibmu2ruMzibBJ3ghwF9236Jst7iaGguONMt1a8J0yAunVpkgpTURpF3Y2eMoB1A/640?wx_fmt=png)

收到 dnslog 请求

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCDtzBMvLolYIMwXwibmu2rukumrtzuFXBWFfXk58wN83WzJVoS8fuFSDfFXEnZtibfh6icBLwY1H0iaA/640?wx_fmt=png)

公众号

最后再给大家介绍一下漏洞库，地址：wiki.xypbk.com  

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCDtzBMvLolYIMwXwibmu2ruC6mJg4KJiaTLnzne7w4qraaB6SO9iaCpBDufyKficZobmJolBlnFicWHpw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCDtzBMvLolYIMwXwibmu2rur7RMzhZOzp8XKibxMGTkJY5F2EBexNxIA3pibcAuYr24WYhfm2zQ46Og/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCDtzBMvLolYIMwXwibmu2ruib8N3ggtVKgjpxPP4kQrWDla13YBSeukib04BuFxhB7Q3UowJKI0iagicQ/640?wx_fmt=png)

漏洞库内容来源于互联网 && 零组文库 &&peiqi 文库 && 自挖漏洞 && 乐于分享的师傅，供大家方便检索，绝无任何利益。

由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，文章作者不为此承担任何责任。

若有愿意分享自挖漏洞的佬师傅请公众号后台留言，本站将把您供上，并在此署名，天天烧香那种！