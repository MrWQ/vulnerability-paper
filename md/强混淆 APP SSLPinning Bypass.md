> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/sxTOMjBuBmAXLnVfuE4WLw)

![](https://mmbiz.qpic.cn/mmbiz_png/rTicZ9Hibb6RXu3bXekvbOVFvAicpfFJwIOcQOuakZ6jTmyNoeraLFgI4cibKrDRiaPAljUry4dy4e2zK8lUMyKfkGg/640?wx_fmt=png)

**前言**

遇见 App 存在证书绑定时，一般会采用工具一把梭，比较熟悉的有 justrustme 模块；以及使用 objection 将 SSLpinning 给 disable 掉；还有就是某些大佬自己集成的十多种绕过证书绑定的框架如 DroidSSLUnpinning、FridaContainer。使用这些工具基本上可以绕过 90% 以上的证书绑定，但有些 APP 做了混淆后上面这些工具就失效了，通过学习肉师傅传授的思路，可实现混淆 APP SSLPinning Bypass。

**正文**

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RWg5rbKnPw74dRapPz5VTibR5NSVmXgpcSp05guBr2UbZ8tqqnibEvIFkP8Hdf1hx2IoqXqCSIsYjLA/640?wx_fmt=jpeg)

首先从开发角度来了解证书绑定如何实现，从下面代码中可以看出针对该网址 www.tetsukay.app 从系统里取出文件，取出文件之后计算 sha256，然后与该值`YLh1dUR9y6Kja30RrAn7JKnbQG/uEtLMkBgFF2Fuihg=`进行比对。

```
https://www.anquanke.com/post/id/197657
https://zhuanlan.zhihu.com/p/58204817
https://qiita.com/tetsukay/items/ad6cf55c740a57050cd3
```

所以我们可以从框架层的两个地方进行分析

1、取出文件

2、计算 sha256

打开文件时，hook 构造函数 java.io.File，然后从构造函数的重载中发现 java.lang.String 会被反复调用进行打开证书文件。

通过分析得出，打开的文件中包含该 cacert 证书的路径，然后调用栈中包含该函数

X509TrustManagerExtensions.checkServerTrusted

满足这两个条件，把消息和调用栈传出去，也就定位到哪个函数执行了 ssl 证书绑定。

```
Java.use("java.io.File").$init.overload('java.io.File', 'java.lang.String').implementation = function (file, cert) {
      var result = this.$init(file, cert)
      var stack = Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new());
      if (file.getPath().indexOf("cacert") >= 0 && stack.indexOf("X509TrustManagerExtensions.checkServerTrusted") >= 0) {
        var message = {};
        message["function"] = "SSLpinning position locator" + file.getPath() + " " + cert;
        message["stack"] = stack;
        var data = Memory.alloc(1);
        send(message, Memory.readByteArray(data, 1))
      }
      return result;
    }
```

我们运行该脚本后在 APP 登录处输入账号密码，然后在保存生成的文件中搜索 SSLpinning，可以很明显的发现该混淆后的类 z1.g.a(CertificatePinner.java:13)。

python r0capture.py -U -f cn.xxx.xxx -v >>xxx.txt

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RWg5rbKnPw74dRapPz5VTibRTrN0GJEicmQej5hWnTeRnia0uT4vicsHl9XVBxia6xaOGPw3riaicZPofjKA/640?wx_fmt=jpeg)  

当然也可以搜索

X509TrustManagerExtensions.checkServerTrusted

同样也能定位到该混淆后的类。

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RWg5rbKnPw74dRapPz5VTibRoocMfKibLRuY7wTzOQfwByLaXeE8ic1Wicic0NRQX6q4J4586wSGQ4JtsA/640?wx_fmt=jpeg)

找出该类后，我们的做法就是 hook 该类，将`.a`返回值置空，以此达到校验失效的目的来实现绕过。

```
setImmediate(function(){
    Java.perform(function(){
        console.log("Bypassing")
        Java.use("z1.g").a.implementation = function(){
            console.log("called here")
            return;
        }
    })
})
```

编写好 hook 代码，使用 frida 加载绕过。

frida -U -f cn.xxx.xxx -l bypassPinning.js --no-pause

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RWg5rbKnPw74dRapPz5VTibROoEKEsakSibGFWaIRuKmtzeKJSoBgVTEbsjhHuWmb2gMNM535DfKP7w/640?wx_fmt=jpeg)

结果展示，如下

![](https://mmbiz.qpic.cn/mmbiz_jpg/rTicZ9Hibb6RWg5rbKnPw74dRapPz5VTibRia6rHpm8HukRuo18ezmf6toyuCstujGA4apsTJ0s3HCWg4f6tVOV68Q/640?wx_fmt=jpeg)

参考链接：

```
https://www.anquanke.com/post/id/197657
https://zhuanlan.zhihu.com/p/58204817
https://qiita.com/tetsukay/items/ad6cf55c740a57050cd3
```

E

N

D

**关**

**于**

**我**

**们**

Tide 安全团队正式成立于 2019 年 1 月，是新潮信息旗下以互联网攻防技术研究为目标的安全团队，团队致力于分享高质量原创文章、开源安全工具、交流安全技术，研究方向覆盖网络攻防、系统安全、Web 安全、移动终端、安全开发、物联网 / 工控安全 / AI 安全等多个领域。

团队作为 “省级等保关键技术实验室” 先后与哈工大、齐鲁银行、聊城大学、交通学院等多个高校名企建立联合技术实验室，近三年来在网络安全技术方面开展研发项目 60 余项，获得各类自主知识产权 30 余项，省市级科技项目立项 20 余项，研究成果应用于产品核心技术研究、国家重点科技项目攻关、专业安全服务等。对安全感兴趣的小伙伴可以加入或关注我们。

![](https://mmbiz.qpic.cn/mmbiz_gif/rTicZ9Hibb6RX4MU7S4WB8R6vF3JbUjA7K0ZtOPxqGSo1HGPhTDicQibOro93UYNBOwRPd4EFseGTDsl1tan0ZXcmw/640?wx_fmt=gif)