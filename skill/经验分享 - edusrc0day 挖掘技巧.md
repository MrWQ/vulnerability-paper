> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/1LEN5rYhDrH7qGRIWuTlUA)

**![](https://mmbiz.qpic.cn/mmbiz_png/OBLmObCsZtRhFM3KeDj0QMtHtS04jFyCfsXLsRytlX5oAxgTNL5dYAAe5swJaOREVqksBqdUW8nzibErssPRu5w/640?wx_fmt=png)**

**前言  
**

**“**

**申明：本次测试只作为学习用处，请勿未授权进行渗透测试，切勿用于其它用途！  
**

**本篇文章由团队师傅钟北山师傅创作。  
**

**本篇文章涉及到的所有站点均已提交至 edusrc！**

**涉及站点均修复此漏洞，发出来仅是作为分享学习。**

**”**

**![](https://mmbiz.qpic.cn/mmbiz_png/OBLmObCsZtRhFM3KeDj0QMtHtS04jFyCfsXLsRytlX5oAxgTNL5dYAAe5swJaOREVqksBqdUW8nzibErssPRu5w/640?wx_fmt=png)**

******Part 1 经验分享******

  

**“**

**PS：作为在 edusrc 的小白，经常看见大师傅们的刷屏，我也很向往能像大师们一样有一次刷屏的机会，于是有了这一次的渗透之旅。**

**思路：要想刷屏上分，就得找系统来挖掘，对于不会审计的我来说只有做一些黑盒测试（会审计大佬可以忽略这一点）**

**首先我们利用 fofa 找一些与 edu 有关的系统**

**语法：**

```
"系统" && org="China Education and Research Network Center"
```

**![](https://mmbiz.qpic.cn/mmbiz_jpg/EWF7rQrfibGZqnIort6QdIKib7MDuqkaKEEFkZRG4szEyeuHNx4YOUaEo3IvjLcrXf62r0ibU5octY7DXOFZkoiaOw/640?wx_fmt=jpeg)****其中可以在前面加一些：阅卷系统、评分系统、直播系统、录播系统。（我们需要找的是弱口令能进去的系统）**

**此次渗透我使用的是：**

```
"点播系统" && org="China Education and Research Network Center"
```

**![](https://mmbiz.qpic.cn/mmbiz_jpg/EWF7rQrfibGZqnIort6QdIKib7MDuqkaKE9ydGpHiaqXgbMBL7bdowxqOr3nxxMtH8SGHUOibyjjs6ngnICjpMiamvg/640?wx_fmt=jpeg)**

**当确定系统后，我们就开始寻找目标站点，能通过弱口令进入的系统是最好的（admin\admin admin\123456)**

**![](https://mmbiz.qpic.cn/mmbiz_jpg/EWF7rQrfibGZqnIort6QdIKib7MDuqkaKEIibano1KicJZDRP33xGaUx5YlCv0biaCQpk9XI8a8hrpjK30bxPac8Z5A/640?wx_fmt=jpeg)**

**通过上述的弱口令测试并没有进入后台，此时肯定会有爆破密码的想法，但是爆破成功的可能性太小了，于是我思考是否能通过找到操作手册发现默认密码，观察页面有关键字：网瑞达和 WRD 视频直播点播系统**

**于是使用谷歌查找：WRD 视频直播点播系统操作手册**

**![](https://mmbiz.qpic.cn/mmbiz_jpg/EWF7rQrfibGZqnIort6QdIKib7MDuqkaKEKia9Qhic08yWpzjicCTGaK1RYoEJ4wHsJiaicGXw7XWxhVs4xnUdI8YDsJg/640?wx_fmt=jpeg)**

**点进去看看能否找到默认密码, 运气还是好，碰巧发现了默认密码：默认管理端用户名『****admin****』 密码为『****Wrd123!@#****』。**

**![](https://mmbiz.qpic.cn/mmbiz_jpg/EWF7rQrfibGZqnIort6QdIKib7MDuqkaKEwzrzJYqWt5eYTOZ1BbicNezdiapX6icgYA2PuX1iaT1EhyY8LZzouQ3FWw/640?wx_fmt=jpeg)**

**发现 WRD 视频直播点播系统默认密码后，继续使用 fofa 构造语句查找能进入的系统（如果大多数都是默认密码，此处就是一个弱口令通杀）**

**语法：**

```
"WRD视频直播点播系统" && org="China Education and Research Network Center"
```

**![](https://mmbiz.qpic.cn/mmbiz_jpg/EWF7rQrfibGZqnIort6QdIKib7MDuqkaKE9FQhOhgdSj1GB7aDcR8pp5xrDDdo2TDzpazw5W0xXL3ksialtQOyo7g/640?wx_fmt=jpeg)**

  
**运气还是有点倒霉的，这么多站点只有一个通过默认密码进入了系统：http://223.99.203.174:8081/login（已修复），测试完后，心里很复杂，这么多站点，就一个弱口令，看见有相关公司，于是在 fofa 一次公司名称，看看有没有别的站点：**

**语法：**

```
"网瑞达" && org="China Education and Research Network Center"
```

**![](https://mmbiz.qpic.cn/mmbiz_jpg/EWF7rQrfibGZqnIort6QdIKib7MDuqkaKEN0v6l7XBOibc098BT0rMDdo3B2qEEFeNONxdRNfW860lrYaQW3v779Q/640?wx_fmt=jpeg)**

**发现这个公司的系统产品挺多的然后继续进行默认密码测试，在 1063 个站点下，大约测试出了 10 多个站点，全部已经提交平台并且修复：**

**![](https://mmbiz.qpic.cn/mmbiz_jpg/EWF7rQrfibGZqnIort6QdIKib7MDuqkaKESMa5XrKtueMyn5YOicCZ9OfhiaFoic0z2FfEib7AiaZgR3PM4hQPTB3xotw/640?wx_fmt=jpeg)**

**看着这么多站点 ，却只有一点点能通过默认密码进入，心里非常的失落，于是有了能不能越权登录的想法：**

**首先在登录框抓登录的返回包看见 false, 顺手修改为 true, 放包：**

**![](https://mmbiz.qpic.cn/mmbiz_jpg/EWF7rQrfibGZqnIort6QdIKib7MDuqkaKE8F3LuhkvU9UhzzwRGwAuXiaQlfq21jSFb0BNcSFNJNKLvOJufLR4VNQ/640?wx_fmt=jpeg)**

**![](https://mmbiz.qpic.cn/mmbiz_jpg/EWF7rQrfibGZqnIort6QdIKib7MDuqkaKEArPm2CpKWExB4bwMvjdsohKMsERBYlvy8dvia0knp14nrhusN1zhnKw/640?wx_fmt=jpeg)**

**发现这样修改数据包，在放包时无任何反应，于是我思考，能不能用默认密码进入的站点的返回包放入不能登录的站点测试：**

**（通过测试，寻找到辅助站点：http://211.64.117.58:9080/signin 获取到返回登录数据包：**

```
HTTP/1.1 200 OK
Server:
Content-Type: application/json
Connection: close
Cache-Control: no-cache, private
Date: Tue, 27 Apr 2021 03:00:35 GMT
Set-Cookie: laravel_session=eyJpdiI6IllsZ3EzYTMxVnpKeGdtMnA0dmNXcnc9PSIsInZhbHVlIjoiREJQQ2VIbVNhXC9VVE1hWEZ2NTdpa1lralZ6dXRxT0JnNkwzd3JrSEJqMHBlZ001YXhzNFp0MGpvdE9TN0h1TkNQQW94YWFiWlFxbFNBOVpEVUVaVVBnPT0iLCJtYWMiOiI2MTRkYjYyNjA0YzRlNTk3MjczYjYwMzEzMDZiN2M1NDg5ZmY1MTAzODIxM2E3ZjM2NDc5Njc3ZWU4MTdmMDI5In0%3D; expires=Tue, 27-Apr-2021 05:00:35 GMT; Max-Age=7200; path=/; httponly
Content-Length: 291
{“success”:true,“data”:{“token”:“eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImlzcyI6Imh0dHA6Ly8yMTEuNjQuMTE3LjU4OjkwODAvYXBpL3NpZ25pbiIsImlhdCI6MTYxOTQ5MjQzNSwiZXhwIjoxNjE5NTA2ODM1LCJuYmYiOjE2MTk0OTI0MzUsImp0aSI6Ik5RUWtScEZOOUE4Y1d6bWEifQ.U2tsG3rqnt8Qe1lX9rHR1HmHBJlS5mOBOmKkInF_GaM”}}
```

**![](https://mmbiz.qpic.cn/mmbiz_jpg/EWF7rQrfibGZqnIort6QdIKib7MDuqkaKEib54IiathHcPsTUV6SW6j5SjsIT1BKiciaWf1ibKR3ZQxLasyBkHuD84boQ/640?wx_fmt=jpeg)**

**去访问目标站点：http://202.193.24.122:9080/signin，然后在登录处输入账号 admin 密码任意 ，抓返回，将包换为刚获取的成功登录包然后放包：**

**![](https://mmbiz.qpic.cn/mmbiz_jpg/EWF7rQrfibGZqnIort6QdIKib7MDuqkaKETPKdhCXmZ1PLYY67aeFTQjcQKj1Q4sJkNyLOMHjdDMQg62drae30rw/640?wx_fmt=jpeg)**

**然后点击放包，没想到全部的数据包放完后，就成功的进入到后台了**

**![](https://mmbiz.qpic.cn/mmbiz_jpg/EWF7rQrfibGZqnIort6QdIKib7MDuqkaKEAaEQsYAticjiben7qdK5n5Zx9BVt89I6LhXt751OiaF4Rwkps3icuzozYQ/640?wx_fmt=jpeg)**

**随后我任意选择了几个不同的学校进行了测试，都可以通过此方法进入后台，通过收集，一共有 400 所高校被日，当然我只选择了部分提交，完成我的刷屏梦想，**

**最后放一张我 edusrc 的个人资料，嘻嘻，欢迎关注 vx 公众号：F12sec ，喜欢我文章的也可点一个关注，之后经常分享我个人的渗透思想和技术，**

**厂商已经修复漏洞，故所有站点均未打码**

**![](https://mmbiz.qpic.cn/mmbiz_jpg/EWF7rQrfibGZqnIort6QdIKib7MDuqkaKEtPJlzS4F6mbPBI55sBMPrKvedILEpCuybxcUz73uFcBetdTu8UwZ3w/640?wx_fmt=jpeg)**

  

**如果对你有帮助的话  
那就长按二维码，关注我们吧！  
**

**![](https://mmbiz.qpic.cn/mmbiz_png/Qx4WrVJtMVKBxb9neP6JKNK0OicjoME4RvV4HnTL7ky0RhCNB0jrJ66pBDHlSpSBIeBOqCrOTaWZ2GNWv466WNg/640?wx_fmt=png)**

**![](https://mmbiz.qpic.cn/mmbiz_jpg/EWF7rQrfibGYIzeAryXG89shFicuMUhR5eYdoSEffib7WmrGvGmSPpdvYfpGIA7YGKFMoF1IrXutHXuD8tBBbAYJg/640?wx_fmt=jpeg)**

**![](https://mmbiz.qpic.cn/mmbiz_png/wKOZZiacmHTc9LIKRXddrzz6MosLdiaH4EQNQgzsrSXHObdAia8yeIlLz6MbK9FxNDr44G7FNb2DBufqkjpwiczAibA/640?wx_fmt=png)**

**![](https://mmbiz.qpic.cn/mmbiz_gif/b96CibCt70iaaJcib7FH02wTKvoHALAMw4fK0c7kH8Aa77gpMcYib3IVwvicSKgwrRupZFeUBUExiaYwOvagt09602icg/640?wx_fmt=gif)**  [实战 | 我的 SRC 挖掘 - 如何一个洞拿下百分 QAQ](http://mp.weixin.qq.com/s?__biz=Mzg5NjU3NzE3OQ==&mid=2247485758&idx=1&sn=cafc83acbfd9de667bdceb85c04b9d77&chksm=c07fb2caf7083bdc18f1beae464118405003a18aa47aa6edbf51929a7da1ff47042a8b2190ae&scene=21#wechat_redirect)

[](http://mp.weixin.qq.com/s?__biz=Mzg5NjU3NzE3OQ==&mid=2247485586&idx=1&sn=148764c1aab126a76b0c459ec67dc1f8&chksm=c07fb366f7083a70301714c87c8d09d3ee2c0dd2567360a46e87372c62a0f0415074ca06631a&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_gif/b96CibCt70iaaJcib7FH02wTKvoHALAMw4fK0c7kH8Aa77gpMcYib3IVwvicSKgwrRupZFeUBUExiaYwOvagt09602icg/640?wx_fmt=gif)  [实战 | 一次简单的信息收集到 getshell 的过程](http://mp.weixin.qq.com/s?__biz=Mzg5NjU3NzE3OQ==&mid=2247485252&idx=1&sn=88464e7c793a168d7f1c2506414c1695&chksm=c07fbcb0f70835a6a768376c3ee586e384b4e314d59aedaed0c04a2d6c9237e7314205e0f9dc&scene=21#wechat_redirect)  

**右下角求赞求好看，喵~**