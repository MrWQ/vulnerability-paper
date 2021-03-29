> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/bWkr-LUrkxSu642NtWCaJA)

  

网安引领时代，弥天点亮未来   

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDCVZx96ZMibcJI8GEwNnAyx4yiavy2qelCaTeSAibEeFrVtpyibBCicjbzwDkmBJDj9xBWJ6ff10OTQ2w/640?wx_fmt=png)

  

**0x00 具体操作**  

  

**1.fofa.so 最近出了一个识别蜜罐的功能。**

**2. 此方案就是为了应对被识别出来是蜜罐, 可以使用 nginx 代理功能快速复制线上系统并且改造成蜜罐, 并且这样是没有蜜罐的特征的。**

**3. 例如我要复制 freebuf，并且改造成蜜罐。**

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hC4lokVJ5E8Yg4Nj1hbiadiaA4h4hAProXXT0al0QxONDaOzRrd9iansqCRAFO4r3Wx5cO8S9pia8HsEw/640?wx_fmt=png)

**4. 在自己的服务器上配置 nginx 代理到 freebuf**

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hC4lokVJ5E8Yg4Nj1hbiadiaA8YzY5RqU3jxy1ICm26VAqGWxCQwScQuSibIFPjYVoKy1yUw01HibQThQ/640?wx_fmt=png)

**5. 这样打开我的网站就会代理到 freebuf 了**

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hC4lokVJ5E8Yg4Nj1hbiadiaAkQsViaBPXgYTl2WIH279T2FiceR6OJZ3XytRgo0xQMr9c2pbbGHTQNqw/640?wx_fmt=png)

**6. 网站复制完了，接下来就是改造了，打开网络, 找个一个 js 文件.**

**7./freebuf/2.1.0.8047219fb6b712d64292.js**

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hC4lokVJ5E8Yg4Nj1hbiadiaAlNKpsYvBMOslibNUNw9T1iaclg40vXGdicjCqgyk9DT2YFHlPsmJRtLnw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hC4lokVJ5E8Yg4Nj1hbiadiaA3lvU5MqPag774XClyGCHJlckDen00JEmZBowPPebibTItRzDQmqbc5g/640?wx_fmt=png)

**8. 并且 nginx 配置文件改成下面这样, 意思就是上面这个 js 文件不代理到 freebuf 由我本地进行处理, 所以这个 js 文件在清除缓存之后提示 404 了。**

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hC4lokVJ5E8Yg4Nj1hbiadiaAjjVbbyoQzxyiabPXUMOoYRKcyvpiaicHyicGJ2htSbkfAdJqFYh81UEXEQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hC4lokVJ5E8Yg4Nj1hbiadiaAgIWpfFfWEQedBNjuVgzRia5Bfqe6t8xKggk9abCvuK2jUG0psLpkiaNQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hC4lokVJ5E8Yg4Nj1hbiadiaABYjHdSwicqYEHmQrSOQ0mmFd8Cy6jkdoaiarnjialy39szmntO62ku6kQ/640?wx_fmt=png)

**9. 然后在我服务器上创建对应的目录和对应的文件名**

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hC4lokVJ5E8Yg4Nj1hbiadiaAcMqCnECJtacAbtoYmOb8LlqlicsKC3hbpz5ToZ0uutsPxib29WyIicytw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDeibLqJxh4YEHfciaZQlXA276yC37Pa7T1eeAT1YbiaEnHKOGRbxY8hrP88zE4J5UyH6rPzOFuGUQYQ/640?wx_fmt=png)

**10. 然后在 js 文件开头增加一个自己的 js 代码就行了**

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDeibLqJxh4YEHfciaZQlXA27upYwlvk7e95ODMgZLzb16UJ3ZuSRkXq1yKjWaj1ABgTibn6Kkgq0sTg/640?wx_fmt=png)

**11. 最后清除缓存, 刷新页面, 可以看见刚才那个提示 404 的 js 已经响应 200, 并且已经增加了自己的代码了**

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDeibLqJxh4YEHfciaZQlXA27DdkbWhk7Qzsy1kqKmpAHkSjVJLYvUsPpdrVpqwAuV4lUL4FONVGGow/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDeibLqJxh4YEHfciaZQlXA27PfR1EoQNga3EJ39hVAZ2LX5JmdHc9v7uh4AX59N2wYGnCopXNzk9IA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDeibLqJxh4YEHfciaZQlXA27m0jFbuJlEmlqGpgLEqAX1H4usR1p8KWMKPIWvy4zB17ShmfVurUQow/640?wx_fmt=png)

**12. 这样快速构建的蜜罐, 是没有蜜罐特征的, 一般的蜜罐识别插件也无法识别出来。**

**13. 文章就是抛砖引玉, 可以自由发挥, 例如把一些接口弄到本地来。**

**14. 作者简介: 以前是个渗透仔, 现在连 burpsuite 都懒得打开的小伙子。**

![](https://mmbiz.qpic.cn/mmbiz_gif/b96CibCt70iaaqjXT4YxgHVARD1NNv0RvKtiaAvXhmruVqgavPY3stwrfvLKetGycKUfxIq3Xc6F6dhU7eb4oh2gg/640?wx_fmt=gif) 

知识分享完了

喜欢别忘了关注我们哦~  

学海浩茫，

予以风动，

必降弥天之润！

   弥  天

安全实验室  

![](https://mmbiz.qpic.cn/mmbiz_jpg/MjmKb3ap0hDyTJAqicycpl7ZakwfehdOgvOqd7bOUjVTdwxpfudPLOJcLiaSZnMC7pDDdlIF4TWBWWYnD04wX7uA/640?wx_fmt=jpeg)