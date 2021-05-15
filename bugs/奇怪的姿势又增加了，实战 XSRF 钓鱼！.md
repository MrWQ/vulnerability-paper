> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/WSDcDioHOaZx451ENXAyng)

**高质量的安全文章，安全 offer 面试经验分享**

**尽在 # 掌控安全 EDU #**

  

![](https://mmbiz.qpic.cn/mmbiz_png/siayVELeBkzWBXV8e57JJ4OyQuuMXTfadZCia0bN2sFBfdbTRlFx0S97kyKKjic5v6eaZ8cY4WQt0UEu4dkyowHYg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rl6daM2XiabyLSr7nSTyAzcoZqPAsfe5tOOrXX0aciaVAfibHeQk5NOfQTdESRsezCwstPF02LeE4RHaH6NBEB9Rw/640?wx_fmt=png)

作者：掌控安全 - holic

前言  

-----

CSRF 感觉似乎很不值钱的样子，我前几天审计出了 3 个后台存储 xss+csrf

然后 cnvd 跟我说不收 csrf 和后台存储 xss，自此后台我从不找 xss 和 csrf

但是毕竟作为目前毕竟出名流行的一个漏洞，还是讲解一下，我会讲的很简单，ojbk

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcq8uEPVg3KkdX9vp3bm81pFbX4wAglYq5K7otRymyWEBMicM9y8Xc4f9ib7KYvylKjypBphtq10ALibw/640?wx_fmt=png)

0x01 CSRF 介绍
------------

CSRF 的全名为 Cross-site request forgery，它的中文名为 跨站请求伪造

CSRF 是一种夹持用户在已经登陆的 web 应用程序上执行非本意的操作的攻击方式。

1).CSRF 是利用了系统对页面浏览器的信任

  
2).XSS 则利用了系统对用户的信任。

**原理：**

攻击者盗用了你的身份，以你的名义发送恶意请求

CSRF 能够做的事情有：

  
以你的名义发送邮件、发消息、盗取你的账号，甚至于购买商品，虚拟货币转账

0x02. 本地靶场演示 csrf
-----------------

这个 cms 是我找的，提交 cnvd 不收，我就拿出来讲 QAQ

cms 下载地址：http://down.chinaz.com/soft/39546.htm

![](https://mmbiz.qpic.cn/mmbiz_jpg/BwqHlJ29vcq8uEPVg3KkdX9vp3bm81pFO3tm5cvE8Jr6zddcgXU6BYfIq3tPLjTFpfIgA1bVZBE2wzTic8Ubiayw/640?wx_fmt=jpeg)  
因为存在 csrf 和 xss，然后刚好想到这里友链有 csrf 和 xss

那我们就直接制作一个 poc

![](https://mmbiz.qpic.cn/mmbiz_jpg/BwqHlJ29vcq8uEPVg3KkdX9vp3bm81pFDNXTuLloMgd5ZS2Y2W0M3KxbbxDckuJq67AkcYMN0iaIMyf0z4oFqsA/640?wx_fmt=jpeg)  

copy 一下，然后复制到 html 中，我们再用火狐打开

![](https://mmbiz.qpic.cn/mmbiz_jpg/BwqHlJ29vcq8uEPVg3KkdX9vp3bm81pFkphTicVdJiaEwQ5ib048JFMJqTBCt82sGzeticy7sHMpbWVCvIia5dcFzPg/640?wx_fmt=jpeg)

上面看到了友链是没有链接的，然后我们点击我们的 poc

![](https://mmbiz.qpic.cn/mmbiz_jpg/BwqHlJ29vcq8uEPVg3KkdX9vp3bm81pFJJBwTRfqdEZ02v1cftHMNBYBjBxsnRbtntwKWXzOhxK0C5M5mhHmeA/640?wx_fmt=jpeg)

然后发现 success 成功了，我们去前台刷新，看会不会跳 xss 弹窗

![](https://mmbiz.qpic.cn/mmbiz_jpg/BwqHlJ29vcq8uEPVg3KkdX9vp3bm81pFwzM70Yuw2aLrXMz6tb5niclNybRWSpefZjFIkjauZ69QBExeslpLpdQ/640?wx_fmt=jpeg)  
成功的弹窗了，我第一时间想到就是蠕虫，哈哈哈

![](https://mmbiz.qpic.cn/mmbiz_jpg/BwqHlJ29vcq8uEPVg3KkdX9vp3bm81pFvW2S530eGlibZAjz4BLO5AJeCttMmAYlThxfnRicsibPc8Zxxbaib5xUTQ/640?wx_fmt=jpeg)  
然后我们再去后台看下是否添加了

![](https://mmbiz.qpic.cn/mmbiz_jpg/BwqHlJ29vcq8uEPVg3KkdX9vp3bm81pFnJBcnviaAA9IUw7GXPibUtqn3ZpKibJb64p74bJKhCWy1Jy1V0fawYWPA/640?wx_fmt=jpeg)  
没错，添加好了。

如果要细节的话可以这样写 https://www.baidu.com <script>alert(1)</script>

因为后面那串代码会被拼接到站点去执行，

所以是看不见的，只会看到 baidu 的 url，这就是出其不意

0x03 剖析 CSRF 漏洞原理
-----------------

下面友链简称 a 页面

  
csrf.html（也就是 burp 生成 poc）简称 b 页面

a 页面需要管理员登录的情况下，然后诱惑管理员点击 b 页面，这时候因为 b 页面有我们的恶意代码，他会借用 a 页面中的管理员，去执行 b 页面中的恶意 payload

为什么会执行 b 页面的内容呢？

  
因为 a 页面管理员登录的情况下，是会有个 cookie

  
然后你再打开一下其他页面，就不需要再次登录，

而 csrf 就是借用管理员的 cookie，去执行我们编辑友链的表单，于是乎就打出了 csrf

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcq8uEPVg3KkdX9vp3bm81pF7arov93fV9I1c6BpAooeKjluQWNO4ckWvyPtY8cfX677Q8f54vBibAg/640?wx_fmt=png)

核心代码在这个地方  

  
第一个 if 是给变量赋值，然后以 POST 传参形式的

  
第二个 if 判断 title 不能为空

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcq8uEPVg3KkdX9vp3bm81pFFZDCAHiceclQanApgTCyhAxZCjoic2vEPb0lklzcGJCTHE64QPatrRyw/640?wx_fmt=png)

  
然后就执行第二个 if，发现 getrs 不知道是什么函数，去定位一下

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcq8uEPVg3KkdX9vp3bm81pF89g98YmnIVuc3a2wpQEsHV2WxyHxicozqUsiagiblsdPRQpK3UticYz1iaQ/640?wx_fmt=png)  
  

发现这里是 $conn 就是连接数据库，不用去看也猜得到的

  
然后是执行 mysqli_query，$conn 连接数据库，

接着 value 就是执行的 sql 语句

`if(getrs("select * from sl_link where L_title='$L_title' and L_del=0","L_id")==""){`

这句就是查询数据库，看是否存在，不存在的时候才会执行下一步的，这时候我们再去插入数据库

  
接下来就是回显内容，回显内容就不说了

从这边可以看见，这边没有 token，也没有二次校验

  
导致可以造成 xss，插入数据库的时候也没有对其进行使用 htmlspecialchars() 去过滤

这时候即存在 xss，又存在 csrf，本来还想测测是不是存在注入，由于我比较懒，写的文章是关于 csrf 的，我就不继续测试了

所以就造成了 xss+csrf

![](https://mmbiz.qpic.cn/mmbiz_jpg/BwqHlJ29vcq8uEPVg3KkdX9vp3bm81pFhAibsv9X4H09mDQgibZNLia9TibSSibEPRzQooOFD3xIL66VbwjtbBPic41w/640?wx_fmt=jpeg)  
这边提到 xss 了，我也提一下。

关于 xss 的审计小知识，应该大佬都知道，我就简单的讲讲。

存储型 xss 是在第二步的时候会进行过滤，如果②没过滤的话，基本就存在 xss 了  
（除非 config.php 这种配置文件有过滤 QAQ）

关于过滤这方面的话百度一下就可以了，我不多废话。

可以进行二次校验，或者校验 token，或者判断 refer 头是从哪里来

一些小思考，这个 cms 可以 csrf 添加超级管理员

  
csrf 危害有时候也挺大的，比如后台 getshell，这时候可以尝试配合 csrf，哈哈哈

总结
--

本篇文章讲的简单易懂，如果懂了，那就懂了，不懂可以问问

这边其实还有个添加管理员的漏洞，可以使用这个洞去添加管理员。

这样更方便，具体可以留给新来的同学研究。

这里的利用思路也很简单。

这边先是利用 csrf 中去添加友链，然后再添加友链的地方做个手脚，打个存储型 xss

  
（你以为这样就完了吗，不）

  
记得 flash 钓鱼吗，这配合起来就会一直提示 flash 版本过低，就会跳转到我们自己搭建的 flash 页面上（前提是得免杀）

  
然后去下载我们伪造的木马，这不就很好的打了一波配合

我们先看下前端底部的友链

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcq8uEPVg3KkdX9vp3bm81pFpDZczb0gic8kMXWbE1iacXxs9dWYE7Zic7ZGosJibduKMBCepZgZSYs4iaQ/640?wx_fmt=png)  
  

然后我们在后端这边稍微偷偷的改一下

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcq8uEPVg3KkdX9vp3bm81pFv4DlNu68STyHvzeXDI6rJrSEUN3ktB9r36MIE8zb3VolehvG3UxJlg/640?wx_fmt=png)  

这时候你就发现有弹窗了

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcq8uEPVg3KkdX9vp3bm81pFpuEGlYrlpRaElia2wcibUibT7nOAGF13oM2uG9AYUqqlJC5HJVMonZribw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcq8uEPVg3KkdX9vp3bm81pF6Afy1c5e0mblXYVGSqHOxtWtmoq2L7ibuAUL7zfORIOX6jQMdMHsXSg/640?wx_fmt=png)  
  

然后看下友链，你会发现一点破绽都没有，简直是躺着 吊肉鸡

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcq8uEPVg3KkdX9vp3bm81pFTGBEHBrHHkyLn5XTonvA7wBicqSib28ia17pSDbxTaFRVOITAyOX9HO2w/640?wx_fmt=png)  
只有当你看源代码的时候才会发现这玩意，嘿嘿

这时候我们 flash 钓鱼，就得去 GITHub 上面找一下页面源码

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcq8uEPVg3KkdX9vp3bm81pFb2NsrasQ0Wu16v0poCOhlYvRZAwdnk4RXMY1BhmbwWI2ssqHkxribtA/640?wx_fmt=png)  
  

然后还得需要一个服务器和域名

（我只有服务器，没有域名，就不演示了）

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcq8uEPVg3KkdX9vp3bm81pFqAt6OQzw9O9m6AlNwgsKeWp1J2SJn81X6nwoziaQvofsR14nNOLpSPg/640?wx_fmt=png)  
就简单的直接打开看一下，然后就坐等 cs 上线肉鸡了

  
等我有空的时候我会本地搭建详细的去部署, 再会！

  

**回顾往期内容**

[公益 SRC 怎么挖 | SRC 上榜技巧](http://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247496984&idx=1&sn=ccf9cf7193235d4a6e189198a9f8359c&chksm=fa6b8c69cd1c057f605e587c8578eac81313039a754c285e731a89b374dcbc57c0cba4434e23&scene=21#wechat_redirect)

[实战纪实 | SQL 漏洞实战挖掘技巧](http://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247497717&idx=1&sn=34dc1d10fcf5f745306a29224c7c4008&chksm=fa6b8e84cd1c0792f0ec433310b24b4ccbe53354c11f334a1b0d5f853d214037bdba7ea00a9b&scene=21#wechat_redirect)

[上海长亭科技安全服务工程师面试经验分享](http://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247501917&idx=1&sn=f194da03379f55e1a79bd34b39ecdfc6&chksm=fa6bb12ccd1c383a30b798185114462798d1ac8363c2aabb7fdb2529891b5a0440f886d462f4&scene=21#wechat_redirect)

[实战纪实 | 从编辑器漏洞到拿下域控 300 台权限](https://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247487476&idx=1&sn=ac9761d9cfa5d0e7682eb3cfd123059e&chksm=fa687685cd1fff93fcc5a8a761ec9919da82cdaa528a4a49e57d98f62fd629bbb86028d86792&token=1892203713&lang=zh_CN&scene=21#wechat_redirect)
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[代理池工具撰写 | 只有无尽的跳转，没有封禁的 IP！](http://mp.weixin.qq.com/s?__biz=MzUyODkwNDIyMg==&mid=2247503462&idx=1&sn=0b696f0cabab0a046385599a1683dfb2&chksm=fa6bb717cd1c3e01afc0d6126ea141bb9a39bf3b4123462528d37fb00f74ea525b83e948bc80&scene=21#wechat_redirect)
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

![](https://mmbiz.qpic.cn/mmbiz_gif/BwqHlJ29vcqJvF3Qicdr3GR5xnNYic4wHWaCD3pqD9SSJ3YMhuahjm3anU6mlEJaepA8qOwm3C4GVIETQZT6uHGQ/640?wx_fmt=gif)

扫码白嫖视频 + 工具 + 进群 + 靶场等资料

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcpx1Q3Jp9iazicHHqfQYT6J5613m7mUbljREbGolHHu6GXBfS2p4EZop2piaib8GgVdkYSPWaVcic6n5qg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/BwqHlJ29vcqJvF3Qicdr3GR5xnNYic4wHWFyt1RHHuwgcQ5iat5ZXkETlp2icotQrCMuQk8HSaE9gopITwNa8hfI7A/640?wx_fmt=png)

 **扫码白嫖****！**

 **还有****免费****的配套****靶场****、****交流群****哦！**