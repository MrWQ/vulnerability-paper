> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzI2NDQyNzg1OA==&mid=2247485443&idx=1&sn=d81e2cb97b1fa114346b7d44967f2ee9&chksm=eaad883eddda0128b30ba28324637bdee11eb9804dc386465c0d142a4fee31e8e12ca2c53067&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2enaicZag8Tibicxc5Wp6wicN3yVvOCjQVY9hCOibNrHZt5qvibia4dtPJkfxf5QicYwTz3xCYKGOKTOumkag/640?wx_fmt=gif)

介绍

  

        ServerChan 是一款 程序员 和 服务器 之间的通信软件，也就是从服务器推送报警和日志信息到手机的工具。

网站地址：http://sc.ftqq.com/3.version

获取 SCKEY

        用 Github 账号登录 http://sc.ftqq.com/3.version ，点击发送消息，获取 SCKEY

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2enaicZag8Tibicxc5Wp6wicN3yj8fYGEsea5yLSVOzomwbnzmYlQqzsnhCTR96BxVU3d4vAuiaEIwKVow/640?wx_fmt=png)

绑定微信

用微信绑定 ServerChan

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2enaicZag8Tibicxc5Wp6wicN3yc0kTMdywzYEPu4wBHPkjnhUBPZzVVH8g1Ria3zVEX0libqR5lp8kicQIw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2enaicZag8Tibicxc5Wp6wicN3y2jfUuCwgayWHMRFjPRyETDqRUnia7ViatzcuLZNutG31EQS1T9ePHQXg/640?wx_fmt=png)

插件安装  

下载 http_ftqq.cna 文件，修改 24 行的 SreverChan 链接为刚刚获取的 SCKEY

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2enaicZag8Tibicxc5Wp6wicN3yDE64bYAshzX8Eql1hfzmS8gib2oXRQchJ6ase8e184fv2O5XHWFJtxQ/640?wx_fmt=png)

然后在 CobaltStrike 脚本管理器中加载该脚本即可

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2enaicZag8Tibicxc5Wp6wicN3ysfWfqcd29PYHuBicRnD9cGW3gujyicEEDt7X5iamSZ5yuDINkOJAibLibnw/640?wx_fmt=png)

功能测试

用虚拟机测试上线，微信成功收到通知。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2enaicZag8Tibicxc5Wp6wicN3yUertGHibs9pviaQmzATK8TFBY912CWvwqbJgy8Rg2Lzge3FqvPiaib1VIQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2enaicZag8Tibicxc5Wp6wicN3yR5sSnDk7G8gHH3SYsqj3hRF5KpempM1Yl66TiaQOPvEmibec2k8Me31w/640?wx_fmt=png)

但是在客户端加载插件，当客户端没连接上服务端的时候，是不提醒的。所以，我们需要在服务端运行该插件。

关于如何在服务端运行 cna 插件，传送门：[CobaltStrike 加载插件](http://mp.weixin.qq.com/s?__biz=MzI2NDQyNzg1OA==&mid=2247485377&idx=1&sn=1e93b38971c0c3c4e1cdfdaa7625ec9e&chksm=eaad87fcddda0eea6469afd46a059b6ebff47e1dfa0a5d5fc8ca22722f5db61141580ea12c9f&scene=21#wechat_redirect)

参考文章：

http://www.nmd5.com/?p=567&from=timeline&isappinstalled=0

来源：谢公子博客

责编：浮夸

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2edCjiaG0xjojnN3pdR8wTrKhibQ3xVUhjlJEVqibQStgROJqic7fBuw2cJ2CQ3Muw9DTQqkgthIjZf7Q/640?wx_fmt=png)

如果文中有错误的地方，欢迎指出。有想转载的，可以留言我加白名单。

最后，欢迎加入谢公子的小黑屋（安全交流群）(QQ 群：783820465)

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SjCxEtGic0gSRL5ibeQyZWEGNKLmnd6Um2Vua5GK4DaxsSq08ZuH4Avew/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)