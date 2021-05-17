> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/2ituOhXtx0CXELxfqj_nqg)

最近研究了一下 API 安全，有一个叫 Inon Shkedy 的同学整理了自己在 API 安全测试中的 31 个 tips。我觉得质量不错，翻译了一下，再加上了一些自己的理解，会分成 3 篇发出来。

项目：31-days-of-API-Security-Tips

地址：

https://github.com/inonshk/31-days-of-API-Security-Tips

**tip1:**
---------

旧的 API 版本通常会包含更多的安全漏洞，他们缺乏一些安全机制。我们可以使用 REST API 的可预测性来预测是否存在旧的 API 版本。比如当前有一个 API 被命名为 / api/v3/login ，我们可以检查 / api/v1/login 是否存在 。

比如:

http://api.example.com/v3/login

可以把 v3 换成 v2,v1 等等，其实如果想探测到更多的版本，可以探测一些大范围比如 v0-10 等等，还有存在一些 v2.1 这种小版本的可能。

http://api.example.com/v2.1/login

**tip2:**
---------

永远不要认为只有一种方法，用来验证 API 的身份。现代的应用程序有很多 API 接口用于认证: 

```
/api/mobile/login

```

```
/api/v3/login

```

```
/api/magic_link

```

等等。找出他们并测试所有的授权认证问题。

认证的接口确实很多，可以分为不同的应用，不同的平台，不同的版本等等。

这种是需要去做侦查，比如发现一些二级域名，再加上 login 之类的接口，或者公司的一些其他接口也是可以登录，这个在官方文档上可能有发现。

OAuth 的认证机制，需要学习一下。很多大公司的 OAuth 的接口如下：

<table width="665"><tbody><tr><td>在线服务</td><td>接口端点</td></tr><tr><td>RFC 6749</td><td>/token</td></tr><tr><td>Twitter</td><td>/oauth2/token</td></tr><tr><td>Dropbox</td><td>/oauth2/authorize</td></tr><tr><td>Facebook</td><td>/oauth/access_token</td></tr><tr><td>Google</td><td>/o/oauth/token</td></tr><tr><td>Github</td><td>/login/oauth/access_token</td></tr><tr><td>instagram</td><td>/oauth/authorize</td></tr><tr><td>tumblr</td><td>/oauth/token</td></tr></tbody></table>

做认证的时候，公开 API 一般为：

https://api.example.com/v1/oauth2/token  

**tip3:**
---------

还记得 5-10 年前 SQL 注入是多么常见么？你几乎可以进入任意一家公司。BOLA(IDOR) 是 API 安全最新的流行病。作为一个渗透测试人员，如果你知道如何利用它，你的荣誉就得到了保证。

BOLA 参考信息：

https://medium.com/@inonst/a-deep-dive-on-the-most-critical-api-vulnerability-bola-1342224ec3f2

**tip4:**
---------

测试一个 Ruby on Rails App 的时候，注意一个包含 URL? 的 HTTP 参数。开发人员有的时候会使用”Kernel#open” 函数访问 urls== Game Over，只需要发送一个管道作为第一个字符，然后再发送一个 shell 命令 (通过设计的命令注入)

更多的参考函数文档：

https://apidock.com/ruby/Kernel/open

**tip5:**
---------

寻找 SSRF? 使用它来：

*   内部端口扫描
    
*   利用云服务
    
*   使用 http://webhook.site 网站来反查 IP 地址和 HTTP 库
    
*   下载大的文件 (7 层 DOS)
    
*   反射 SSRF，本地管理平台泄露
    

**tip6:**
---------

Mass Assignment(批量赋值) 是一个真实存在的。现在框架鼓励开发人员在不理解安全影响的情况下使用 MA。在开发过程中，不要猜测对象的属性名称，只需要找到一个返回所有属性的 GET 端口即可。

![](https://mmbiz.qpic.cn/mmbiz_jpg/OdOkDJXavoicbPg29BQibcqNwf0iczgicjibFsLGdRIaV1ibgVeCSybtWu5tt9wlEknbx1XYXiaJwhPXUM44Pnrk1iaJ9w/640?wx_fmt=jpeg)

**tip7:**
---------

一家公司向开发者公开了 API 接口，而且在移动端和 web 端使用了相同的 API 程序。我们需要分开测试它们，不要假设它们实现了相同的安全机制。

**tip8:**
---------

在进行测试 REST API 时，我们也应该检查一下 API 是否也支持 SOAP。将 content-type 更改为 “application/xml”，在请求主体中添加一个简单的 xml，并查看 API 如何处理它。

有时身份验证是在不同的组件中完成的。可能是在 REST 和 SOAP API 之间共享的，所以 SOAP API 可能支持 JWT。如果 API 返回带有 DUMPling 的 stack trace，那么它很可能是存在漏洞的。

**tip9:**
---------

试图找到 BOLA 的漏洞?

HTTP bodles/headers 中的 id 往往比 url 中的 id 更容易受到攻击，可以首先试着关注他们。

**tip10:**
----------

利用 REST 的特性来查找管理 API endpoints!

比如你看到一个 api 叫做 GET /api/v1/users/<id>，我们可以试着修改请求方法 POST/DELETE 来 create/delete users

其实这些 API 端口是很好猜的，而且设计规范的 API 也应该这样设计。

一个规范的设计：

https://api.example.com/v1/users/<id>

可以替换 URI 中的版本，二级目录，id ，还包括请求方法等等。这都是可以用遍历工具来验证的。