> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/kmRe_1Ao3nM4V0SGCUSsgw)
| 

**声明：**该公众号大部分文章来自作者日常学习笔记，也有少部分文章是经过原作者授权和其他公众号白名单转载，未经授权，严禁转载，如需转载，联系开白。

请勿利用文章内的相关技术从事非法测试，如因此产生的一切不良后果与文章作者和本公众号无关。

 |

**0x01 前言**

这种提权方式在 2020 年 8-9 月时 @sailay1996 在他的 Github 就放出了 EXP，当时测试这个 EXP 时发现只能用于本地测试，无法在实战场景中应用（能力有限，不会编写），网上的复现文章也都是在本地测试的。

昨天好友 @Arenid 给我投稿了这种提权方式的复现文章，又花了点时间重新看了一遍，根据他的文章补充了在实战场景中的应用。

**0x02 RpcSs 服务简介**

**服务名称：**RpcSs；

**显示名称：**Remote Procedure Call (RPC)；

**启动类型：**默认为自动开启状态；

**服务描述：**RPCSS 服务是 COM 和 DCOM 服务器的服务控制管理器。它执行 COM 和 DCOM 服务器的对象激活请求、对象导出程序解析和分布式垃圾回收。如果此服务被停用或禁用，则使用 COM 或 DCOM 的程序将无法正常工作。强烈建议你运行 RPCSS 服务。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcXuxB8bU8WTic5Oy1MkU2caRSLKFicP37jPtm088le7GicgGDedibiatV4qmsib0WwaDuMevic8D9p7ISvA/640?wx_fmt=png)

****0x03 EXP 本地测试****

这个提权 EXP 可以将当前 Network Service/Administrator 权限提升为 SYSTEM 权限。

将下载 EXP 里的 exe 和 dll 文件放在同一目录下执行即可，exe 会加载 dll 中的 payload 进行攻击得到 SYSTEM。  

**EXP 下载地址：**

```
https://github.com/sailay1996/RpcSsImpersonator
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcXuxB8bU8WTic5Oy1MkU2caBy75AY98zEEN2MP2XrAcsKBoTnQSZnMrkVtV58IuhAQeEuSEKsHX7g/640?wx_fmt=png)

这个 EXP 在实战中无法直接利用，因为在 Network Service 的 Webshell 下执行这个 EXP 时是没有任何回显的，也并不是交互的问题，尝试了在交互式 cmd/powershell 执行，结果都是一样的。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcXuxB8bU8WTic5Oy1MkU2caRunMXXDr89ZW2TehbqFkQpibHs5IvGnsEiaE60h738pPiakYOPJSaX4vw/640?wx_fmt=png)

**0x04 实战场景应用**

通过谷歌搜索相关资料得知 Metasploit 已将 @sailay1996 提到的 RpcSsImpersonator 权限提升技术移植到了 getsystem 命令中，具体详情可查看底部的参考链接。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcXuxB8bU8WTic5Oy1MkU2cah9ib3JeH53soAGXsGNia4OHoCVt6ojvl4OeKYSWNrbgczuWFGxy01G8Q/640?wx_fmt=png)

```
0 : All techniques available                  //所有可用技术
1 : Named Pipe Impersonation(In Memory/Admin) //命名管道模拟（在内存/管理员中）
2 : Named Pipe Impersonation(Dropper/Admin)   //命名管道模拟（Dropper/Admin）
3 : Token Duplication(In Memory/Admin)        //令牌复制（在内存/管理员中）
4 : Named Pipe Impersonation(RPCSS variant)   //命名管道模拟（RPCSS变体）
```

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcXuxB8bU8WTic5Oy1MkU2caZ8G9t9EKf30yA26iax0dxKXJMgsx3qrAF54XWyuRJ90aU9jdoSfCthQ/640?wx_fmt=png)

由于利用过程过于简单就不再详细写了，大致测试环境和权限如下：

*   测试系统：Windows Server 2012/2016
    
*   当前权限：nt authority\network service
    

首先我们先利用 Metasploit 攻击载荷得到 network service 权限会话，然后直接执行 getsystem 命令即可得到 SYSTEM 权限。

![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOcXuxB8bU8WTic5Oy1MkU2caibXyiaHsjUJWiaCRy8gyR4J3LicgKI2a9sIsaCDKyJ6XbzQOZLqzziby9AA/640?wx_fmt=png)

**0x05 参考链接**

http://batcmd.com/windows/10/services/rpcss/

https://github.com/rapid7/metasploit-payloads/pull/431

https://github.com/rapid7/metasploit-framework/pull/14030

只需关注公众号并回复 “9527” 即可获取一套 HTB 靶场学习文档和视频，“1120” 获取安全参考等安全杂志 PDF 电子版，“1208” 获取个人常用高效爆破字典，“0221” 获取 2020 年酒仙桥文章打包，还在等什么？赶紧关注学习吧！

公众号

* * *

**推 荐 阅 读**

  

  

  

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf8eyzKWPF5pVok5vsp74xong5AN4sVjsv6p71ice1qcHHQZJIZ09xK3lQgJquhqTLfoa9qcQ7cVYw/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247486401&idx=1&sn=1104aa3e7f2974e647d924dfde83e6af&chksm=cfa6afd2f8d126c47d81afd02f112daea41bce45305636e3bba9a67fbdcf6dbd0e88ff786254&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOf8eyzKWPF5pVok5vsp74xolhlyLt6UPab7jQddW6ywSs7ibSeMAiae8TXWjHyej0rmzO5iaZCYicSgxg/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247486327&idx=1&sn=71fc57dc96c7e3b1806993ad0a12794a&chksm=cfa6af64f8d1267259efd56edab4ad3cd43331ec53d3e029311bae1da987b2319a3cb9c0970e&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/XOPdGZ2MYOfUDrsHTbibHAhlaWGRoY4yMzOsSHefUAVibW0icEMD8jum4JprzicX3QbT6icvA6vDcyicDlBI4BTKQauA/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg4NTUwMzM1Ng==&mid=2247484585&idx=1&sn=28a90949e019f9059cf9b48f4d888b2d&chksm=cfa6a0baf8d129ac29061ecee4f459fa8a13d35e68e4d799d5667b1f87dcc76f5bf1604fe5c5&scene=21#wechat_redirect)

**欢 迎 私 下 骚 扰**

  

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/XOPdGZ2MYOdSMdwH23ehXbQrbUlOvt6Y0G8fqI9wh7f3J29AHLwmxjIicpxcjiaF2icmzsFu0QYcteUg93sgeWGpA/640?wx_fmt=jpeg)