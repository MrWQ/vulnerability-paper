> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/wpjAmXjg1qMigdQ0W_H6RA)

**本文首发于****奇安信攻防社区**  

**社区有奖征稿**

· 基础稿费、额外激励、推荐作者、连载均有奖励，年度投稿 top3 还有神秘大奖！

· 将稿件提交至奇安信攻防社区（点击底部 阅读原文 ，加入社区）

[点击链接了解征稿详情](https://mp.weixin.qq.com/s?__biz=MzI2NzY5MDI3NQ==&mid=2247489051&idx=1&sn=0f4d1ba03debd5bbe4d7da69bc78f4f8&scene=21#wechat_redirect)

**背景**
------

在某次授权的攻防演练项目中遇到了目标使用 shuipfcms 系统，接着对 shuipfcms 进行本地搭建后代码审计，最终获取目标权限。

**思路介绍**
--------

1.  某一处泄露 Authcode
    
2.  利用 Authcode 加密 cloud_token
    
3.  thinkphp 缓存 getshell
    

**代码分析**
--------

**Authcode 泄露**

在 shuipf/Application/Attachment/Controller/AdminController.class.php:37

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6jfjC551L8gZxZ99NmZh1pqfEMOSl0NiaVeUAZOsulevaUyM9GicKMwiakZtPD1xww7yLtnIo8y4n6Q/640?wx_fmt=png)

swfupload 函数是不需要鉴权就可以直接访问到的，可以看到红色箭头处，当我们的密钥不对的时候，会直接打印出系统的 AuthCode。

如图所示：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6jfjC551L8gZxZ99NmZh1pRIXHsaJedNpysHlhnWiapZ3qSS1CMkvSxGJrVnzW3kpXLtA7FgzBKjQ/640?wx_fmt=png)

我们得到这个 AuthCode 后可以干什么呢？

**cloud_token 解密**

在 shuipf/Application/Api/Controller/IndexController.class.php:17

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6jfjC551L8gZxZ99NmZh1pNdpwTK1t0QibXBKuH6myorg7p0Jkcb9t9CBcCEyJzQQ4cAe9ZDv6rtg/640?wx_fmt=png)

这里我们 POST 进来一个 token，然后调用 authcode 函数进行解密：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6jfjC551L8gZxZ99NmZh1pUWfOeIoUgHcCDju9YGwOA6jap8Y7biaP1bZTtjibWRluyHrj9Wpbiblqw/640?wx_fmt=png)

当 key 为空的时候，就会用 authcode 来解密了。

而这个 CLOUD_USERNAME 默认是没设置的，属于云平台的配置选项，所以默认条件下，这个地方的解密是用 authcode 来解密的。

上文已经泄露了 authcode，所以这里解密后的内容也是我们可控的了。

然后看一下解密后的操作：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6jfjC551L8gZxZ99NmZh1psaEQZUlxgNnc2cCy2Vod0EKOQghZlia9KicI8s7hqd6XbuhXicUlnLEXA/640?wx_fmt=png)

调用了一个 S 函数，这个是 TP3 内置的缓存操作函数。这里的键值是 getTokenKey 函数的返回值，跟进一下：shuipf/Libs/System/Cloud.class.php:161

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6jfjC551L8gZxZ99NmZh1pstP8g11U6JN8JOpd4Z8NyCH3HjwgSvickkCZJBCXQXjXsZUYoreoD2Q/640?wx_fmt=png)

OK，这个值还是比较好计算的。

**thinkphp 缓存 getshell**

然后看一下缓存的处理：

shuipf/Core/Library/Think/Cache/Driver/File.class.php:120

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6jfjC551L8gZxZ99NmZh1pJpo5lz6khz4ZLeOZWrmns2tF6cfcodKjn3bj8QugBrPTg9LiaeqRSUg/640?wx_fmt=png)

首先是文件名的生成方式，第一个红色箭头处，跟进：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6jfjC551L8gZxZ99NmZh1p1eK9e308RPkKhFtEKFaSTM2iabRuK9n3nI3pgG8mpzUreickhyx0YmRA/640?wx_fmt=png)

这里的 DATA_CACHE_KEY 默认为空，不用管，但是 $this->options[‘prefix’] 是有的。看一下生成方式：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6jfjC551L8gZxZ99NmZh1pQDiatdKHp7f8Plw9YBibibBZGiaSlBNU54AtKfRKllaWe6r5PhaOexA6KA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6jfjC551L8gZxZ99NmZh1peiaWicKQ4RiazAAojPAN92OzaBzk5XcicnFVrU8FcPWFSLbuNxNVTxiatLA/640?wx_fmt=png)

就是三个长度的随机字母加一个下划线。这个就比较有难度了需要猜测和爆破了。

然后就是一个写入反序列化数据的操作。

我在本地测了一下，数据像这样：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6jfjC551L8gZxZ99NmZh1puJKJQ1ep7Aa98MYG2wo4spSAWSL1vgJdent4ibtbSsVEYJvOkictH4nQ/640?wx_fmt=png)

成功写入了 webshell。但是实战中的前缀需要爆破, win 不区分大小写，会很快，linux 则稍微麻烦一点。比如我本地是 rDe_。

### **利用过程**

首先我们发送报文获取 authcode:

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6jfjC551L8gZxZ99NmZh1pRIXHsaJedNpysHlhnWiapZ3qSS1CMkvSxGJrVnzW3kpXLtA7FgzBKjQ/640?wx_fmt=png)

然后我们生成 token 发送：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6jfjC551L8gZxZ99NmZh1p8Sfw0FUIR6SedrKWp7uyNlictUQ1TAaeYBK19FZB7RZVddbFd1sNTbA/640?wx_fmt=png)

响应报文中有验证通过就证明成功了。然后我们就需要找到我们的缓存文件了。  
这次比较幸运，目标有列目录的漏洞。

然后我们访问缓存文件即可成功 getshell。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6jfjC551L8gZxZ99NmZh1p7o78X38r7vTYC9SGDHv16Zpw2LicT7elCYShjqLC5FRrrOb8Tia5HvaA/640?wx_fmt=png)

**注: zc.com 解析为 127.0.0.1 为本地环境**

END

  

【版权说明】本作品著作权归带头大哥所有，授权补天漏洞响应平台独家享有信息网络传播权，任何第三方未经授权，不得转载。

  

  

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/WdbaA7b2IE6jfjC551L8gZxZ99NmZh1pWncsiabq0u6h2eNyazDDEMTv0Xe3ErEyTtFibXfb2uiaNjdUCuhS4AZHg/640?wx_fmt=jpeg)

**带头大哥**

  

一个神秘而优秀的补天白帽子

**敲黑****板！转发≠学会，课代表给你们划重点了**

**复习列表**

  

  

  

  

  

[某客户关系管理系统代码审计](http://mp.weixin.qq.com/s?__biz=MzI2NzY5MDI3NQ==&mid=2247491025&idx=1&sn=5771a9d4e07021484ad26fe18e827dfe&chksm=eafa559ddd8ddc8b5189ba07f8ef2895d6afec242c205c8ac3c405cb3659cd41b22245cdebc1&scene=21#wechat_redirect)

  

[硬核黑客笔记 - 不聪明的蓝牙锁](http://mp.weixin.qq.com/s?__biz=MzI2NzY5MDI3NQ==&mid=2247490689&idx=1&sn=f99858d495c68c20cf84f03adb4be35b&chksm=eafa54cddd8ddddb22050aec101a7a5a49932dc866b5fd8d0d99331f65529f2a64540e34bc40&scene=21#wechat_redirect)

  

[Celery Redis 未授权访问利用](http://mp.weixin.qq.com/s?__biz=MzI2NzY5MDI3NQ==&mid=2247490558&idx=1&sn=18e3c2d0dd8b1ed48f3b383088c205c0&chksm=eafa53b2dd8ddaa44b0b7a136c476ee928f21b88564e9a59cd8314aa4f73f9447bd13a8e430a&scene=21#wechat_redirect)

  

[漏洞验证框架的构思与实现](http://mp.weixin.qq.com/s?__biz=MzI2NzY5MDI3NQ==&mid=2247490729&idx=1&sn=a41331e9589d134fe1c8a7373ed5ad4d&chksm=eafa54e5dd8dddf3956b6c07003296e017956607c6fc03993821d62fd07d4b360df96cdb9065&scene=21#wechat_redirect)

  

[施耐德 PLC 认证绕过漏洞分析](http://mp.weixin.qq.com/s?__biz=MzI2NzY5MDI3NQ==&mid=2247490855&idx=1&sn=7eed7a6cc5d3a3ca523a2da3cd2fa648&chksm=eafa556bdd8ddc7d9c0685df72ec0cde7af04bcdb510f176f9b8ff3754987db8267deb5aadf7&scene=21#wechat_redirect)

  

[Chromium issue 1187403 分析](http://mp.weixin.qq.com/s?__biz=MzI2NzY5MDI3NQ==&mid=2247490908&idx=1&sn=e75a3033ef0cdf0892cc48af6315c362&chksm=eafa5510dd8ddc067d053af40ea5e9a159bd5e01179c57d00b178ffca95c55571e57c3cd09af&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/WdbaA7b2IE6D8InhXuGX2q6Cbw7zhMJLFcmlcnz38EApnEkFiaISicklcwbo3gnI17t54PqyYOE8LV4yczIfjdqw/640?wx_fmt=png)  

  

分享、点赞、在看，一键三连，yyds。

![](https://mmbiz.qpic.cn/mmbiz_gif/FIBZec7ucChYUNicUaqntiamEgZ1ZJYzLRasq5S6zvgt10NKsVZhejol3iakHl3ItlFWYc8ZAkDa2lzDc5SHxmqjw/640?wx_fmt=gif)

  

点击阅读原文，加入社区，获取更多技术干货！