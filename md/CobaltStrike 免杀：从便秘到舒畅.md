> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/FhcGJl4_vdpDiEAjHl5cmw)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADe5a0d1wrESSwdwNL7sgxwE8vMg9JfaDuHN4dP3ze8uj5wZtLTQ10c1GwM477H2eI7u6K5lnwa6g/640?wx_fmt=png)

CobaltStrike 免杀：从便秘到舒畅

1

概述

有老哥看了前几天发的便秘帖子后，说鸡哥不讲武德，shellcode 没发出来，卡巴都没有过，帖子就这样结束了。这次一起奉上，CS 通杀所有常见杀软上线运行，相关文件以上传到：

https://github.com/mai1zhi2/CobaltstrikeSource/

2

效果展示

#### **2.1 火绒**

执行 shellcode 部分：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADe5a0d1wrESSwdwNL7sgxwvG8Foibnc8ibQT6QAAg1lyGx9e3fJomHkhD1tQPN63Xj9Jo3rpKy8gmg/640?wx_fmt=png)

执行到反射 dll:

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADe5a0d1wrESSwdwNL7sgxwy5FiaFNKcZbG0Cp7uXX4k3xibgqlJxtMP0rwPNZTae5pOh2ibtt9Mf7oA/640?wx_fmt=png)

运行上线：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADe5a0d1wrESSwdwNL7sgxwbQWNGhhmWpiaer2ibcj3onibxcPZcUeEkBQ3SVUGrCddmqichuibTiaclaGA/640?wx_fmt=png)

火绒沦为摆设：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADe5a0d1wrESSwdwNL7sgxwNWlicdLlTGVNagDvsX7mzETCQAHx2wicPBdjAqopyb113VlW8b9MzxfQ/640?wx_fmt=png)

#### **2.2 360**

执行 shellcode 部分：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADe5a0d1wrESSwdwNL7sgxwUzIF4dNIJicWricVF3zr1dP59Qh0gxyLQpicZmRhtrdw9ohIH1D22D2qw/640?wx_fmt=png)

执行到反射 dll:

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADe5a0d1wrESSwdwNL7sgxwIIKShBjCplQdarOo9SJ5fibB2l29rDKtxHEc4BZf4Sde4z5b7UGIicZw/640?wx_fmt=png)

运行上线：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADe5a0d1wrESSwdwNL7sgxwyqgdILXMgicazWMLLbrvLVchzjYeXPdTniaoNgDCEbcRz5jERWzWtXVA/640?wx_fmt=png)

360 沦为摆设：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADe5a0d1wrESSwdwNL7sgxwj48L4EmsWBJYtyPNPMcWoPCEKqs3mtHU975XEtGzx2uex9o870HkOw/640?wx_fmt=png)

#### **2.3 腾讯管家**

执行 shellcode 部分：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADe5a0d1wrESSwdwNL7sgxww04pox5icXqMibn3MicSOYqg0bEohujnlbmKCPia7Pvj9lbib9KVKqva7NA/640?wx_fmt=png)

执行到反射 dll:

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADe5a0d1wrESSwdwNL7sgxwSVBFylibY2RdeTx4tcWHn6L4IsyOjxOQmeVTiaQL2SVNjuSR1YqHDMMw/640?wx_fmt=png)

运行上线：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADe5a0d1wrESSwdwNL7sgxwGeUEPOeF2iaeaicSr72jd5rRDLIc0EsB7I9iaAYqZzEkCBOYvoxdCJDOg/640?wx_fmt=png)

软件管家沦为摆设：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADe5a0d1wrESSwdwNL7sgxwEuVrIqNMgyBEWHaFf7F057wtt0ufMaCVPv7KZmv36oJEcRddbXzlHQ/640?wx_fmt=png)

#### **2.4 卡巴**

执行 shellcode 部分：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADe5a0d1wrESSwdwNL7sgxwX3NNUfP3Lvf43otyiczQSAibdJymJIZg3bdGiaU1oWnFgentCRy0gVE1g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADe5a0d1wrESSwdwNL7sgxwA80Skc4wbzCyvhibYSyevy91xkgXMtVlBKobS6dJ8S127sBwIp9iaA7w/640?wx_fmt=png)

执行到反射 dll:

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADe5a0d1wrESSwdwNL7sgxwOQ3dAZLGTECL7N9kzCe98SzZQDwt1wtcxRO3rjlQdn9L9e4fBVD7Gw/640?wx_fmt=png)

运行上线：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADe5a0d1wrESSwdwNL7sgxw78Hia9jTfIfIze5KNzfY68ibS2cFLAmX5r4Za81RYf9j73GDjTmUSCLg/640?wx_fmt=png)

卡巴沦为摆设：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADe5a0d1wrESSwdwNL7sgxw17wJ8cZE9icOz1g2xDUhs6txGsQX5hIPajmEJVcDjoicuKlO8yVogY2Q/640?wx_fmt=png)

#### **2.5 麦咖啡**

执行 shellcode 部分：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADe5a0d1wrESSwdwNL7sgxwzZUF0KIFVmzztOCsaHfR4aQYbia6Hv0wNtclAjVxO5N6P7icX1OLjiacQ/640?wx_fmt=png)

执行到反射 dll:

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADe5a0d1wrESSwdwNL7sgxwNEd25w3xHuZVqcFJqUzcbibSSiclloJUMdjexnfUBXiaVEeMs4V7RSTeg/640?wx_fmt=png)

运行上线：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADe5a0d1wrESSwdwNL7sgxwa4Vdtt2V7Picjo6HP2VCDbsSNQuPd6xBiatiaxrgHb1LHcOTmFuIsHk8g/640?wx_fmt=png)

麦咖啡沦为摆设：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADe5a0d1wrESSwdwNL7sgxwo1Uhw4Y0znBT57xMymftJSkGiaibN1WlRCScl11nSTQtqOic9Wf3jnTqQ/640?wx_fmt=png)

3

总结

#### **3.1 为什么能免杀**

**1、Shellcode 的使用设置**

从 Shellcode 转 C 代码，再通过 c 还原的 Shellcode，最后所得的 shellcode 没有经过绕过混淆和加密也是一样妥妥的免杀，关于 c 代码到 shellcode 的生成可以参考之前所发 shellcode 框架的文章。

**2、Beacon 的免杀改进**

目前主要为这两个特征：

Default.profile 的特征：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADe5a0d1wrESSwdwNL7sgxwu2c2g4FsGrIcjm53GopbMkqz5sSa9eCnR0NOdMBKf02bcuo6yN46bQ/640?wx_fmt=png)

与导出函数 RefletiveLoader 名字，我在 common/Sclisten.java 的 export() 方法修改了导出函数的名称：

![](https://mmbiz.qpic.cn/mmbiz_png/Jvbbfg0s6ADe5a0d1wrESSwdwNL7sgxwoOdOsB5lGAZqeAYh27iaKJkx8lW0YfAicZY5mdibicRaKRU9FcA6BxuPeg/640?wx_fmt=png)

#### **3.2 注意事项**

1、请勿使用 stageless 模式，因为该模式的生成规则不相同。

2、请勿执行在该项目 mimikaz、bypassUAC 等敏感行为，因为项目中这些功能还没进行免杀处理的，以防止掉线。因此我们需要对这些功能进行重写并使其免杀。

3、项目只是修改了相应的文件，无留后门等非法行为，老哥们可以放心重打包使用，不放心也可以比对文件，最后，大家护网顺利。

---- 完，谢谢大家观看 ----

4

关注

本公众号 不定期更新 文章和视频 欢迎前来关注

![](https://mmbiz.qpic.cn/mmbiz_jpg/Jvbbfg0s6ADe5a0d1wrESSwdwNL7sgxwPmOcPTxgdn5FlkBCuyEX1M1hs5zwLfxiaA7PRGnkPs6r6KhU06kRniaw/640?wx_fmt=jpeg)