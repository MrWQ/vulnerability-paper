> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/8SNb86yrTzPbPIAfQvz-2A)

由于国内最开始分享文章作者使用的是 CS3.X 版本。导致后来的同学也按照之前的文章去做，其实新版本给我们带来了更多的惊喜。这里简单提两个非常实用的。
---------------------------------------------------------------------------

### **http\https host 设置**

由于 3x 版本不支持在监听器时候直接设置，所以需要在 profile 文件中指定该字段。不过 4x 版本已经可以直接在监听器里设置了。这点我在域前置那篇文章简单提了一下，今天细说（水）。

3x 截图：

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4Udh25xdss8uON3rj4Nkar7S2iaQHPia7VrAaUcZK8xDVKha7qMjcR2O9Xy2s0pnk3hPibjz1zia6Gq4tA/640?wx_fmt=png)

4x 截图：

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4Udh25xdss8uON3rj4Nkar7SUBkZslOKX0lmHoSkXPzEHow8pzNkvE9CsPErH0icRl7cfE3icnGGyDBA/640?wx_fmt=png)

所以现在我们已经有两个可以设置 http host 的地方了。那他们的优先级是怎样的？这里我通过简单的修改部分源码在关键点添加提示 + 实际测试的结果都可以进行说明。  

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4Udh25xdss8uON3rj4Nkar7SXF73ErEibGAvbcM3oFQLwpHI5KOliajp8n1GgfV8KOiblLwAFzka20eUQ/640?wx_fmt=png)

（这里是我修改过的版本，在关键处添加了提示。） 

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4Udh25xdss8uON3rj4Nkar7SRE4ia36JKB71Uxg7I5gu9JxUtlibgTgtI8hIEeKOhb8qNiaseMGNUwPow/640?wx_fmt=png)

所以在设置 host 字段方面，我们可以完全信任监听器的设置。不再去依靠 profile 文件（每次都要手动改文件后再重启，你不累么！）  

### **定义 C2 端与监听的不同端口**

#### **端口映射场景**

之前有一个项目客户给定了 CS 服务器，但是给出的端口是映射的。外网访问 188.88.88.88:80 实际访问到的是 10.88.88.88:8000。在 3x 版本中，我们可以建立两个监听器，一个监听 80 另一个监听 8000 以达到我们的目的。不过在 4x 版本有了更方便的做法。

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4Udh25xdss8uON3rj4Nkar7SarcW2BKCSHEQDQU6sZUjok7W4gp1ZeVxFFeB7voXfM7uy7op2xoyxg/640?wx_fmt=png)

绑定的端口可以直接指定！如果不填写的话 是默认与 C2 端口一样的。  

可以尽情的验证这种行为的可行性。

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4Udh25xdss8uON3rj4Nkar7SICicsUtfAd3EBHiceEMlr5s1M04rn4ffOGNibeWmw16CdIvacDozqOIDQ/640?wx_fmt=png)

#### **反向代理场景**

这点特性不光可以应用在端口映射、frp 等情景，也可以很好的与之前很火的云函数或者其他反向代理的场景结合起来。

假设我们已经有了一个监听在 80 的监听器。现在想要新增一个流量中转方案。所以只需要在新监听器的 bind 上写另一端口 (我这里以 8000 为例)，然后 C2 端口还是写 80。再通过你喜欢的手段去转发，例如这样：

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4Udh25xdss8uON3rj4Nkar7SdqohoXpF9SwguAB8DLwJicqmB2FDib3hlU3N5MJJT8MQ5RQ4h9UsKqvw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/B7aQ0TKN4Udh25xdss8uON3rj4Nkar7SHOumZtr8ic19xHicSJ065jDjIND72UunlxUwAn19lcY9kLp4ygBgxnAQ/640?wx_fmt=png)

岂不是节省了在一个监听器上改来改去的时间。  

**最后**

CS 新版本更新了很多内容（虽然 4x 现在也称不上新版本了）。但是国内流传广泛的文章还是 3X 的。导致很多非常方便的特性使用者很少。在使用一个工具时，我们应当去思考，去理解，而不是一成不变的照抄前人思路，纵使前人的文章在当时真的很优秀。

如果看的人多的话，会考虑变成一个系列。期待你的点赞、转发。