> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/rL-y3n8NdUao8Ai_3CI1_A)

0x01、前言  

在某次授权红队行动中，客户给定目标外网资产很少

经过各种挖掘，各种尝试，久久没有结果，注意到某系统为通用系统。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE7rnB4H8UtQtEKO0115FtvjsQB6RQRGw8AHnVXvpoKpV3W2kH31L2xn6W78SKzgagqd68vAC9WB5A/640?wx_fmt=png)

于是开始了下面的故事。

0x02、寻找源码到 getshell
-------------------

### 查找源码

1、网盘泄露：这套系统并不开源，各种网盘泄露网站一顿查找，无果

2、Github、gitlab 泄露：尝试了多个关键词，均无果

3、Fofa 找同类型的站：用 favicon.ico，或是用 title 来搜，并且将这些资产采集起来，最终在某个站发现`web.rar`，成功获得源码

### 代码审计

查看代码目录结构如下

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE7rnB4H8UtQtEKO0115FtvjxLqzEd2cF6lCEtPLXKCKiaxdaibCv7WkcYagEfRKibGaczslpiakcaw5Fw/640?wx_fmt=png)

首先看 web.xml，注意到这个过滤器`filter.PurFilter`

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE7rnB4H8UtQtEKO0115FtvjYSAkCLia0wJXPnPFVT1ATCxQpicdul241eQ9UNCfwTUfXIWGBibtQpRQw/640?wx_fmt=png)

跟进去看下

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE7rnB4H8UtQtEKO0115FtvjRrkPHch6xAR43cBcHduoKc2k7Z3qVBtB9msicDY4tsZicibCGQF8etibQA/640?wx_fmt=png)

此处定义几个数组  
![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE7rnB4H8UtQtEKO0115FtvjsiahTPIia5gJ7lk4P9ibPKozuJL2z6mqFGbHCeIfnAsE93OuslEDt75cw/640?wx_fmt=png)

使用 getRequestURI() 获取 url，查找 url 中最后一个点的位置，然后获取后缀转小写

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE7rnB4H8UtQtEKO0115FtvjbnHg89RbiaBsibZicg5CPpZ2CdDPaYADp8xENE087W0QQggUIicMJ0Btlw/640?wx_fmt=png)

这个过滤器实际上是一个权限校验的工作，如果用户没登录的话是只能访问数组里的路径，或者后缀数组的特定后缀的文件。但是此处使用  
getRequestURI() 获取 url，我们注意到

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE7rnB4H8UtQtEKO0115FtvjPvt3EOCRr70gVgrdOOBSSicQcaoeUuZ0jmsbaylt9OY8GbOGicrhrS5A/640?wx_fmt=png)

只要我们的`strSuffix为`后缀数组中的就能过了这个验证。

我们首先了解一下`getRequestURI()`这个方法  
当我们请求`/test/1.jsp;aaa`时`getRequestURI()`取到的结果也是`/test/1.jsp;aaa`  
那么此时想到构造请求`/test/1.jsp;1.jpg`就能绕过这个权限校验

绕过权限校验以后开始寻找可 getshell 的漏洞点，直接全局搜索 multipart，寻找上传功能

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE7rnB4H8UtQtEKO0115Ftvjvt9EkIAafSLllbOuAk053ViaSJUCptKKxcHu5kiapibFBTP6OdLgk4tmA/640?wx_fmt=png)

看到第二个的时候成功发现一处任意文件上传

### 获得权限

按照代码分析，直接构造包上传 shell，成功 getshell

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE7rnB4H8UtQtEKO0115Ftvj7UC6heV7GMFr9RLYQ7ibW1OAma6lsAx41x5ucWBTLYYUjHJW9uV5EDg/640?wx_fmt=png)

0x03、拿下内网 edr
-------------

### 获取 edr 系统权限

通过 shell 执行 tasklist 发现此机器装了某 edr

扫描 c 段 443 端口发现 https://172.x.x.x 为某 edr web 管理界面

用 frp 开个代理

用已经公开的漏洞测了一遍发现，存在一处命令执行漏洞没修

利用公开的脚本直接弹了一个 shell 回来

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE7rnB4H8UtQtEKO0115Ftvjy1A52I9CKZ6Nc9y7pMyEpDZDzBj8InnXIeU6mDXXhRWT2j5DWMiczXQ/640?wx_fmt=png)

此次的目的不是获取这个 edr 的服务器权限，而是可以进到 web 管理界面可以做到给终端下发后门。所以目标为的登录 web 管理界面

首先的想法是找数据库账号密码然后登录进后台。

之前也没搞过，先看下进程  
![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE7rnB4H8UtQtEKO0115FtvjVcfmZQ2uG4m1zNXWW70UmJJxwiaKt3caXhthDt8tVUaxiaicJabMT8RgQ/640?wx_fmt=png)  
好像是 mongodb，使用以下命令查数据库密码

```
find /ac -type f -name "*.php"| xargs grep "password"
```

太多了发现密码名字好像叫 mongodb_password，再次查找.

```
find /ac -type f -name "*.php"| xargs grep "mongodb_password"
```

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE7rnB4H8UtQtEKO0115FtvjibRiaw6GDJzvibdQ1u4VI8P8YX47xV7Vzcs9eibct7MyqPZkcianWOicBPUg/640?wx_fmt=png)

查的过程中感觉就算找到数据库连上了密码也很难解密

于是想到之前的未授权任意用户登录，漏洞文件在`/ui/login.php`

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE7rnB4H8UtQtEKO0115FtvjatwbdZ0OuvPd0y5y2Gfj1jpkSnA2jmoQlPtibpKskVibicneIBiac2GrZw/640?wx_fmt=png)

于是先备份文件，然后将此处的 if 改为`if(1==1)`

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE7rnB4H8UtQtEKO0115FtvjRO1SMQl1NsF5fxXAP0ygp7rl3ibZQa9pKUusricTsmqlz68KPkGQhtHw/640?wx_fmt=png)

使用`/ui/login.php?user=admin`登录成功

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE7rnB4H8UtQtEKO0115FtvjzhbsibQp4byicMayxNIZG94Y8oiaibWn2fWZrlQ3GUdnaOAgZiaM5Gbib8cA/640?wx_fmt=png)

然后就可以加白名单批量下发马执行上线了。

0x04、技术总计
---------

1、想办法获取外网系统源码

2、代码审计获取外网 shell

3、历史漏洞获取 edr 系统权限

4、修改文件进而任意登录到 web 管理端

转载于补天平台。

公众号

如文章对你有帮助，请支持点下 “赞”“在看”