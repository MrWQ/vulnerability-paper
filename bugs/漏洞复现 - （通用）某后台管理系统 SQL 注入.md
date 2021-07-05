> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/zxxOWSYgzY-z8GbBxEP_TQ)

前言
==

**申明****：本次测试只作为学习用处，请勿未授权进行渗透测试，切勿用于其它用途！**

此通用由团队师傅 paida 李贡献，转载请注明来源

漏洞描述
====

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGbmtwfvcCnu8utzqO8jMxbIRDh8xDs2grJ63PH7rc9AS8uPso8QKYv1znWxEKk7pCRVqmAiciaiciaRPw/640?wx_fmt=png)

此系统存在默认弱口令，以及前台 sql 注入。

FoFa 语法
=======

```
"Content/images/login/logo.png" && "/Content/js/core/knockout-2.2.1.js"
```

漏洞复现
====

前台登录，用户名处存在 sql 注入，burp 联动在同户名加 *，一键 sqlmap

关于 burp 插件文章地址：http://www.0dayhack.net/index.php/817/![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGbmtwfvcCnu8utzqO8jMxbIDxf40Jcia2LuBnfl7bkjM6pjiaIDRfgZEib0FW4LRyz5mZCFB4hZDHyibQ/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGbmtwfvcCnu8utzqO8jMxbIibceCPOGJIYARibicHD4nm9rWS5k16ykFykVobpjOgI2pmSfW6ZINeWuA/640?wx_fmt=png) 存在弱口令，默认账号 super 密码 1234。

![](https://mmbiz.qpic.cn/mmbiz_png/EWF7rQrfibGbmtwfvcCnu8utzqO8jMxbIzBQrKKNaFsc8xBaiavqRVXvHlrBH418ut9x9oGL24N4eoFfTQ3n47icA/640?wx_fmt=png)

**如果对你有帮助的话  
那就长按二维码，关注我们吧！**  

![](https://mmbiz.qpic.cn/mmbiz_png/Qx4WrVJtMVKBxb9neP6JKNK0OicjoME4RvV4HnTL7ky0RhCNB0jrJ66pBDHlSpSBIeBOqCrOTaWZ2GNWv466WNg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_jpg/EWF7rQrfibGYIzeAryXG89shFicuMUhR5eYdoSEffib7WmrGvGmSPpdvYfpGIA7YGKFMoF1IrXutHXuD8tBBbAYJg/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_png/wKOZZiacmHTc9LIKRXddrzz6MosLdiaH4EQNQgzsrSXHObdAia8yeIlLz6MbK9FxNDr44G7FNb2DBufqkjpwiczAibA/640?wx_fmt=png)

**![](https://mmbiz.qpic.cn/mmbiz_gif/b96CibCt70iaaJcib7FH02wTKvoHALAMw4fK0c7kH8Aa77gpMcYib3IVwvicSKgwrRupZFeUBUExiaYwOvagt09602icg/640?wx_fmt=gif)**  [经验分享 | 渗透笔记之 Bypass WAF](http://mp.weixin.qq.com/s?__biz=Mzg5NjU3NzE3OQ==&mid=2247486210&idx=1&sn=5c0f6409e51c3c0cfb6bde43f2406409&chksm=c07fb0f6f70839e0e29f4ea9c8655d4ce7690c2a147aeeb74f2827aece58e3746f3f7c4ee562&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_gif/b96CibCt70iaaJcib7FH02wTKvoHALAMw4fK0c7kH8Aa77gpMcYib3IVwvicSKgwrRupZFeUBUExiaYwOvagt09602icg/640?wx_fmt=gif)  [什么是 HTTP 和 HTTPS](http://mp.weixin.qq.com/s?__biz=Mzg5NjU3NzE3OQ==&mid=2247486492&idx=3&sn=0a975b99a0351a95eef41d37813f7e5d&chksm=c07fb7e8f7083efe8054f864b5b25541fa3bf19ab311700f29254d03e45a4357069ee07c8802&scene=21#wechat_redirect)  

![](https://mmbiz.qpic.cn/mmbiz_gif/b96CibCt70iaaJcib7FH02wTKvoHALAMw4fK0c7kH8Aa77gpMcYib3IVwvicSKgwrRupZFeUBUExiaYwOvagt09602icg/640?wx_fmt=gif)  [实战 |  BYPASS 安全狗 - 我也很 “异或”](http://mp.weixin.qq.com/s?__biz=Mzg5NjU3NzE3OQ==&mid=2247486492&idx=1&sn=fbd4ca8ed69ba6cb3adbc6ac8561d825&chksm=c07fb7e8f7083efef437eb3d685cc5bd6ac489629c613b5f2ce9ced8a7f8fcd335b6f91821a8&scene=21#wechat_redirect)

右下角求赞求好看，喵~