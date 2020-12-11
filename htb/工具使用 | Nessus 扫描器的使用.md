> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzI2NDQyNzg1OA==&mid=2247483887&idx=1&sn=f269efcd56c8681e800f3c5c93c23da5&chksm=eaad81d2ddda08c4f66cbc77dcf2ecd93d2d1954d04203aab20bf2b5d896c86bbaf0905c27cd&scene=21#wechat_redirect)

  

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2fkFTpkFY7gmpvKmZia33W1frUUooYP502FbS1Z6diawYToibXEuKeRQhvIHV3YZEUQ6xeNbjVGLNMnA/640?wx_fmt=gif)

  

**目录**

Nessus

Scans

Settings

一个基本扫描的建立

自定义扫描策略

Nessus 的高级扫描方法

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2fkFTpkFY7gmpvKmZia33W1fDVrtaR3icdeUqz7vc35mQqWFKrGZYOJOQysXeo1vBZP9iahL65rCxvHQ/640?wx_fmt=png)

Nessus

Nessus 号称是世界上最流行的漏洞扫描程序，全世界有超过 75000 个组织在使用它。该工具提供完整的电脑漏洞扫描服务，并随时更新其漏洞数据库。Nessus 不同于传统的漏洞扫描软件，Nessus 可同时在本机或远端上遥控，进行系统的漏洞分析扫描。对应渗透测试人员来说，Nessus 是必不可少的工具之一。它不仅免费而且更新极快。安全扫描器的功能是对指定网络进行安全检查，找出该网络是否存在有导致黑客攻击的安全漏洞。该系统被设计为 client/sever 模式，服务器端负责进行安全检查，客户端用来配置管理服务器端。在服务端还采用 了 plugin 的体系，允许用户加入执行特定功能的插件，这插件可以进行更快速和更复杂的安全检查。在 Nessus 中还采用了一个共享的信息接口，称为 知识库，其中保存了前面进行检查的结果。检查的结果可以 HTML、纯文本、LaTeX（一种文本文件格式）等几种格式保存。

Nessus 不仅可以扫描网站，还可以扫描主机。

它由一个执行任务的服务端，和一个分配任务的客户端组成。

它使用 8834 端口作为后台，你在本地输入 https://localhost:8834 即可转到登录后台页面，然后输入账户名和密码即可登录。

它有两个大的选择按钮：Scans 和 Settings

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2fkFTpkFY7gmpvKmZia33W1fzKyXmGnz9rbruuUFFQBKXvIjEg7KJLEJdrrTpp9Ptvop2jEC13QCrQ/640?wx_fmt=png)

### Scans

Scans 按钮下面是我们的扫描的一些选项，分别有 My Scans、All Scans、Trash、Policies、Plugin Rules 和 Scanners

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2fkFTpkFY7gmpvKmZia33W1f8syJicw6wWKkrGCB2Beq1JTjPn6VziabOthbrMAksFFibuwtOqSibmOLFg/640?wx_fmt=png)

*   My Scans 就是你的一些扫描的站点
    
*   All Scans 就是你曾经所有的扫描。
    
*   Trash 就是垃圾桶
    
*   Polices 就是策略，策略允许您创建自定义模板，定义在扫描期间执行的操作。创建之后，可以从扫描模板列表中选择它们。从这个页面，您可以查看、创建、导入、下载、编辑和删除策略。
    
*   Plugin Rules 是插件规则，插件规则允许您隐藏或更改任何给定插件的严重性。此外，规则可以限制在特定的主机或特定的时间范围内。从此页面，您可以查看、创建、编辑和删除规则。
    
*   Scanners 扫描，远程扫描仪可以通过升级链接到 Nessus。一旦链接，就可以在本地管理它们，并在配置扫描时选择它们。从此页面，您可以查看扫描仪的当前状态，并向下钻取以控制所有正在运行的扫描。
    

### Settings

Settings 按钮下面是软件的一些基本设置，分别有 About，Advanced，Proxy Server，SMTP Server，Custom CA，Password Mgmt，My account，Users

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2fkFTpkFY7gmpvKmZia33W1fmfw9M8uxuFxvMvvlp44ytce0MrCdrsA09FYv8U6cLhLeAEQl9PR9rA/640?wx_fmt=png)

*   About 就是一些关于软件的版本等信息
    
*   Advanced 是高级设置，高级设置允许手动配置全局设置。为了使这些设置生效，可能需要重新启动 Nessus 服务或服务器。注意：在扫描或策略中配置的设置将覆盖这些值。
    
*   Proxy Server 就是代理服务器，如果你要通过代理扫描网站的话，就需要在这里配置信息
    
*   SMTP Server 就是邮件服务器，简单邮件传输协议 (SMTP) 是收发电子邮件的行业标准。一旦配置为 SMTP，扫描结果将通过电子邮件发送到扫描的 “电子邮件通知” 配置中指定的收件人列表。这些结果可以通过过滤器定制，并需要一个与 HTML 兼容的电子邮件客户端。
    
*   Custom CA 是自定义的证书颁发机构，在扫描期间，保存自定义证书颁发机构 (CA) 有助于减少来自插件 #51192(SSL 证书不能信任)的发现。
    
*   Password Mgmt 是密码管理，密码管理允许您设置密码参数，以及打开登录通知和设置会话超时。登录通知允许用户查看上次成功登录、最后一次失败的登录尝试 (日期、时间和 IP)，以及自上次成功登录以来是否发生了任何失败的登录尝试。更改将在软重新启动后生效。
    
*   My Account 就是管理员账号的一些信息，通过这里可以修改管理员账户的密码
    
*   Users 是用户，从此页面，您可以查看、创建、编辑和删除用户。一旦创建，用户将配置一个角色，该角色确定用户的扫描权限。此外，每个用户都可以生成一个自定义 API 密钥来使用 RESTAPI 进行身份验证。
    

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2fkFTpkFY7gmpvKmZia33W1fDVrtaR3icdeUqz7vc35mQqWFKrGZYOJOQysXeo1vBZP9iahL65rCxvHQ/640?wx_fmt=png)

一个基本扫描的建立

一般我们要扫描一个主机或者网站的话，点击 My Scans，然后 New Scan 新建一个扫描即可。扫描模板的话，如果我们要扫描的是一个网站，我们选择 Web Application Tests；如果是要扫描一个主机的话，我们选择 Advanced Scan

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2fkFTpkFY7gmpvKmZia33W1f6U0qRboFuwQ216oBn9khexvgdETYrzl9M0LHvv9glVIwgfQCBI7pkw/640?wx_fmt=png)

然后进入了下面的页面，Name 就是这次扫描的名字，随便写，但是最好不要写中文。Description 就是对这次扫描的描述，也可以随便写，Targets 就写目标网站的 ip 地址或者 域名都可以。然后点击 Save 保存好。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2fkFTpkFY7gmpvKmZia33W1fsYIBJP4LE7ByiaaRQYIibV4Y32zD1tlBrdSZyen11JC1nHC3EYs5b4ibQ/640?wx_fmt=png)

然后回到了 My Scans 页面，点击开始就开始扫描了。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2fkFTpkFY7gmpvKmZia33W1fNW2b3paDz5UH0HDJnYJnKCxSBica0iayBVacxF76ARqZwGDLZJHu1iayA/640?wx_fmt=png)

扫描完成的话，这里会有扫描的结构，漏洞分为 5 种程度，最高级别 Critical 最低级别 info。

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2fkFTpkFY7gmpvKmZia33W1fSPXEnhYgBTVmlPBt9adnPiaIV8PsZ4xy5ibksibGLfGLvVhqy7TQEz3CA/640?wx_fmt=png)

我们可以点进去看每个漏洞的具体描述信息，通过对漏洞的分析，我们可以更好地加固我们的系统

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2fkFTpkFY7gmpvKmZia33W1fibUiaVCESxN9OXvj9hWXEaQnTibBcjLdpWNmplnJVACdaTWHicNAWzcUBg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2fkFTpkFY7gmpvKmZia33W1fPU1VAzeSBFfEO0MFJaGzHnlHukr7F0XVCfaH08vtObpRoqiaZVfSIiag/640?wx_fmt=gif)  

自定义扫描策略
-------

Freebuf：Nessus 自定义扫描策略

Nessus 的高级扫描方法
--------------

Freebuf：Nessus 的高级扫描方法

来源：谢公子博客

责编：浮夸

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2edCjiaG0xjojnN3pdR8wTrKhibQ3xVUhjlJEVqibQStgROJqic7fBuw2cJ2CQ3Muw9DTQqkgthIjZf7Q/640?wx_fmt=png)

由于文章篇幅较长，请大家耐心。如果文中有错误的地方，欢迎指出。有想转载的，可以留言我加白名单。

最后，欢迎加入谢公子的小黑屋（安全交流群）(QQ 群：783820465)

![](https://mmbiz.qpic.cn/mmbiz_gif/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SjCxEtGic0gSRL5ibeQyZWEGNKLmnd6Um2Vua5GK4DaxsSq08ZuH4Avew/640?wx_fmt=gif)

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/rSyd2cclv2et9NHxRhN8exP4Ly6FKH9SFQtevncFtKIlfLdaxSwwqFxgkrUz1x12kPp3ueaJctagDUcyJDGJyA/640?wx_fmt=png)