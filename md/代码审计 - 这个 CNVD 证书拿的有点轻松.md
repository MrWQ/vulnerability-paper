> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/iWQExIIU47HN522EX5E1WA)

**高质量的安全文章，安全 offer 面试经验分享**

**尽在 # 掌控安全 EDU #**

  

![](https://mmbiz.qpic.cn/mmbiz_png/siayVELeBkzWBXV8e57JJ4OyQuuMXTfadZCia0bN2sFBfdbTRlFx0S97kyKKjic5v6eaZ8cY4WQt0UEu4dkyowHYg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rl6daM2XiabyLSr7nSTyAzcoZqPAsfe5tOOrXX0aciaVAfibHeQk5NOfQTdESRsezCwstPF02LeE4RHaH6NBEB9Rw/640?wx_fmt=png)

作者：掌控安全 - 橙天

1. 首先我们找一个 EmpireCMS 做代码审计，利用 Seay 源代码审计系统工具  

2. 通过审计 EmpireCMS 找到了 e 目录里的 ViewImg 下的 index.html 文件，发现其中有一段代码存在漏洞, 代码大概的意思是通过 Request 函数获取 URL 参数，并作为 img 和 a 标签的 src 属性和 href 属性，然后通过 document.write 输出到页面。

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcr4ialag5Kicanv2PLiaEeDRcicxWcFiatgXD8rrSXYpCBFLnficEpAkDezQ3BpU9JuBEkMWlGnna4v8Cicw/640?wx_fmt=png)

3. 之后我们就查找 Request 函数流程，就是通过 window.location 获取当前地址，根据传入的 url 参数, 获取当前地址 url 参数起始位置和结束位置。 

例如我的地址是：

`javascript index.html?url=javascript:alert(/xss/)，`

`经过处理之后得到javascript:alert(/xss/)。`

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcr4ialag5Kicanv2PLiaEeDRcicRwICzQKcomKvYFFLfdFrKZyU9TnyXiaEZibB1vOyicUxNlsf8Y710grBA/640?wx_fmt=png)

4. 最后经过 document.write 函数输出到页面，并且 href 和 src 的值就是返回的 javascript:alert(/xss/)

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcr4ialag5Kicanv2PLiaEeDRcicqo7grzIHooR5A7JDbBoiaVic6EUkSDeD1t00ybkKvxpHxOCZCJfzeSvQ/640?wx_fmt=png)

5.（一）我们通过实例测试一下漏洞

https://www. 目标 1.com / 在网上找了一个帝国 cms 的网站，通过输入我们上面代码审计的路径之后回车。

出现这个页面之后点击那个图片实现弹框

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcqzEUWNxqJ7RY7gZY4F5lY8EHy7d2nl2SlAbIbtzWMJUDOD3icdpjlR3phNakiaylszw6AuyzoyUNeg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcr4ialag5Kicanv2PLiaEeDRcicyucbZ9iaydvB0neMwEPRmkwpKriayvTbjnfp72h1JZYfXCBfjJpgqG1A/640?wx_fmt=png)  
（二）我们在测试第二个实例  

https://www. 目标 2.com / 还是通过刚刚那种方法输入那个路径，之后发现他也能到这里 点击图片 弹框

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcqzEUWNxqJ7RY7gZY4F5lY8QxJFLD4eW5On397dGgYn19b5D5bb9jtpYLckLrZ63GsZ0lpVfan39Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcr4ialag5Kicanv2PLiaEeDRciczX4a83PpcgNwqtYDAeJMNAuSzicubibt1HVt2ebqpliamnSnA9FH0deYg/640?wx_fmt=png)  

（三）前两种都实现了 xss，我们在找一个实例

http://www. 目标 3.com / 还是通过上面的输入路径 发现这个网站也可以，点击图片发现也执行了

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcqzEUWNxqJ7RY7gZY4F5lY8VlcibKWVqDn0bibwYlcwfhaVibKHSLAnnjicqe45Te7Jz3DI9edVGZ1Fdw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcr4ialag5Kicanv2PLiaEeDRcicEaFmFOsgXMTZjM17QAbc4Bcbg9uWdk2roERy70CdDTwLyAlY7YZrbg/640?wx_fmt=png)  

经过网上找的几个帝国 CMS 测试发现可以实现通杀，之后我们提交 CNVD 获得证书（CNVD-2021-15824）

  

**回顾往期内容**

[实战纪实 | 一次护网中的漏洞渗透过程](http://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247488327&idx=1&sn=c6677ad2bc524802c79c91a8982c2423&chksm=fa686a36cd1fe3207916178ce750add0fe89e6e0b6bdae53f42429d71a259d53cb39db41a7f5&scene=21#wechat_redirect)

[面试分享 #哈啰 / 微步 / 斗象 / 深信服 / 四叶草](http://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247491501&idx=1&sn=70aae2e2f83d503ca6fad3c4f952bd6e&chksm=fa6866dccd1fefca9de95e8c4c42b81637de45b73319931fcd9e5fdc3752774ac306f76b53f6&scene=21#wechat_redirect)

[反杀黑客 — 还敢连 shell 吗？蚁剑 RCE 第二回合~](https://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247485574&idx=1&sn=d951b776d34bfed739eb5c6ce0b64d3b&chksm=fa6871f7cd1ff8e14ad7eef3de23e72c622ff5a374777c1c65053a83a49ace37523ac68d06a1&token=1892203713&lang=zh_CN&scene=21#wechat_redirect)
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[防溯源防水表—APT 渗透攻击红队行动保障](https://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247487533&idx=1&sn=30e8baddac59f7dc47ae87cf5db299e9&chksm=fa68695ccd1fe04af7877a2855883f4b08872366842841afdf5f506f872bab24ad7c0f30523c&token=1892203713&lang=zh_CN&scene=21#wechat_redirect)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[实战纪实 | 从编辑器漏洞到拿下域控 300 台权限](https://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247487476&idx=1&sn=ac9761d9cfa5d0e7682eb3cfd123059e&chksm=fa687685cd1fff93fcc5a8a761ec9919da82cdaa528a4a49e57d98f62fd629bbb86028d86792&token=1892203713&lang=zh_CN&scene=21#wechat_redirect)
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

![](https://mmbiz.qpic.cn/mmbiz_gif/BwqHlJ29vcqJvF3Qicdr3GR5xnNYic4wHWaCD3pqD9SSJ3YMhuahjm3anU6mlEJaepA8qOwm3C4GVIETQZT6uHGQ/640?wx_fmt=gif)

扫码白嫖视频 + 工具 + 进群 + 靶场等资料

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpx1Q3Jp9iazicHHqfQYT6J5613m7mUbljREbGolHHu6GXBfS2p4EZop2piaib8GgVdkYSPWaVcic6n5qg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcqJvF3Qicdr3GR5xnNYic4wHWFyt1RHHuwgcQ5iat5ZXkETlp2icotQrCMuQk8HSaE9gopITwNa8hfI7A/640?wx_fmt=png)

 **扫码白嫖****！**

 **还有****免费****的配套****靶场****、****交流群****哦！**