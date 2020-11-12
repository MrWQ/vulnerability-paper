\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[www.uedbox.com\](https://www.uedbox.com/post/59017/)

在很多[反向代理](https://www.uedbox.com/post/tag/%e5%8f%8d%e5%90%91%e4%bb%a3%e7%90%86/)场景，或是[爬虫](https://www.uedbox.com/post/tag/%E7%88%AC%E8%99%AB/)中我们都会使用脚本程序提取搜索结果而不是使用[谷歌镜像](https://www.uedbox.com/post/54776/)。但谷歌搜索（google）的[反爬虫](https://www.uedbox.com/post/tag/%e5%8f%8d%e7%88%ac%e8%99%ab/)及异常流量标准会给我们带来很多麻烦，一旦出现验证码 **reCAPTCHA**，就基本中断了数据。今天[体验盒子](https://www.uedbox.com/)介绍一个方法可以绕开**谷歌搜索**永远不出现验证码的方案。

绕开谷歌搜索验证码 reCAPTCHA
-------------------

Facebook 有一个[调试工具](https://developers.facebook.com/tools/debug/echo/?q=https://example.com)。有趣的是，[Google](https://www.uedbox.com/post/tag/google/) 不会限制此调试程序发出的请求（列入白名单？），因此可以用来绕开 Google 搜索结果而不会**被验证码**阻止。由于涉及 facebook，每个请求都必须向库提供一个 facebook 会话 `Cookie`。

方案已经有了，下面只要实现它就行了，这里分享一个现成的谷歌搜索结果提取脚本，并且就是基于该方法绕开验证码的。

goop
----

谷歌搜索脚本，基于 Python，

### 安装

![](https://www.uedbox.com/wp-content/uploads/2019/08/goop.png)

至此，已经完整走过一遍绕开谷歌搜索结果验证码的流程，你可以将该方法融入到任何项目中。

> 但也要注意，故意绕开谷歌搜索验证码及使用 facebook 调试方法进行目的的操作都是不可取及不长久的。仅限用于概念验证而非非法使用。