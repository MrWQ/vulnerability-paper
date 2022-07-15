> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/kSSxoTw8sXufDdUKE6u4RQ)

![](https://mmbiz.qpic.cn/mmbiz_gif/3xxicXNlTXLicwgPqvK8QgwnCr09iaSllrsXJLMkThiaHibEntZKkJiaicEd4ibWQxyn3gtAWbyGqtHVb0qqsHFC9jW3oQ/640?wx_fmt=gif)  

> **文章来****源：****web 安全工具库**

一、访问上传的木马文件

http://192.168.1.104/1.asp

![](https://mmbiz.qpic.cn/mmbiz_png/8H1dCzib3UibuLo68RGLwmOfz7mTKsGs2qfBlAGArb6HEicftVurNNG6KbWjTVtVBLKRqezRsdtHxzKOeSCxicm5aQ/640?wx_fmt=png)

二、点击 F12，打开谷歌自带的开发人员工具，点击 network

![](https://mmbiz.qpic.cn/mmbiz_png/8H1dCzib3UibuLo68RGLwmOfz7mTKsGs2qTIliayftniaZiakqdYK2Ddu65AVKWNwANASmJawh41o3v8gUu97ogpGMg/640?wx_fmt=png)

三、输入密码，看看抓包情况，该木马会自动向某网站上传木马路径和密码

![](https://mmbiz.qpic.cn/mmbiz_png/8H1dCzib3UibuLo68RGLwmOfz7mTKsGs2qNxnlP9oM3YtRhR4WCgPibyyApWbqsHibPud2WOHeYIGhvlHXwsnRlMpA/640?wx_fmt=png)

四、查看木马源文件，然后搜索该网址，随便修改为一个无效地址，该木马用的是反转加密，所以我们搜索不到，有时候是其他加密，需要解密才可以修改

![](https://mmbiz.qpic.cn/mmbiz_png/8H1dCzib3UibuLo68RGLwmOfz7mTKsGs2qGDsL8o4KfibShDKjbIb11aYoZXdbOLd3T50P9nm3iau0ZWOXkOMIKT6A/640?wx_fmt=png)

注意：抓包的时候，有的后门不是一登录就发送的，也有可能停一段时间才发送，甚至当你退出的时候才发送

**禁止非法，后果自负**

**如侵权请私聊公众号删文**

![](https://mmbiz.qpic.cn/mmbiz_jpg/3xxicXNlTXLicjiasf4mjVyxw4RbQt9odm9nxs9434icI9TG8AXHjS3Btc6nTWgSPGkvvXMb7jzFUTbWP7TKu6EJ6g/640?wx_fmt=jpeg)

推荐文章 ++++

![](https://mmbiz.qpic.cn/mmbiz_jpg/US10Gcd0tQFGib3mCxJr4oMx1yp1ExzTETemWvK6Zkd7tVl23CVBppz63sRECqYNkQsonScb65VaG9yU2YJibxNA/640?wx_fmt=jpeg)

*[Pystinger - 使用 Webshell 绕过防火墙进行流量转发](http://mp.weixin.qq.com/s?__biz=MzAxMjE3ODU3MQ==&mid=2650511856&idx=3&sn=034d78d93d69df6291e9b250ac2c7180&chksm=83bafc14b4cd750275467f20483ed8a97db76583434d6aa325435d0716145803de84bcb855e3&scene=21#wechat_redirect)

*[WEBshell 与文件上传漏洞](http://mp.weixin.qq.com/s?__biz=MzAxMjE3ODU3MQ==&mid=2650509750&idx=2&sn=33eaf4781af33c3da07888d4a3588d1b&chksm=83baf452b4cd7d445f96ae68f5fad1fabd46ada5347d762e2d4801f8712e1262c2827ab1955d&scene=21#wechat_redirect)

* [一次服务器被传 webshell 事件溯源](http://mp.weixin.qq.com/s?__biz=MzAxMjE3ODU3MQ==&mid=2650490432&idx=3&sn=30777692202b543f53e47f49eda9eb4b&chksm=83ba23a4b4cdaab26416ce1962f83eaf4b1d0b5b659db227d24a1c7038e2a20b799a945d8074&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_png/3xxicXNlTXLib0FWIDRa9Kwh52ibXkf9AAkntMYBpLvaibEiaVibzNO1jiaVV7eSibPuMU3mZfCK8fWz6LicAAzHOM8bZUw/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_gif/NZycfjXibQzlug4f7dWSUNbmSAia9VeEY0umcbm5fPmqdHj2d12xlsic4wefHeHYJsxjlaMSJKHAJxHnr1S24t5DQ/640?wx_fmt=gif)