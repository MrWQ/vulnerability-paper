> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/dwj_3oDzpub1uqxwzot5jw)

前言
--

拖更了快一周的**不一样的 Burpsuite 扩展武装篇系列**终于写出了第一篇，本系列宗旨是一个 BurpSuite 挖 SRC 打通关无需运行很多别的工具去辅助，作者根据类型分出了三个方向主动，被动，效率扩展去武装自己的 Burpsuite，这篇文章仅仅是不一样的 Burpsuite 扩展武装篇系列的第一篇后面应该还会有几篇，一篇文章写不了那么多的扩展推荐。下文推了很多不错的小众或是大众的 Burpsuite 扩展，或许其中有一个会对你挖 SRC 带来很大帮助。给你开拓新的思路!

主动扫描篇
-----

### FastjsonScan

一个简单的 Fastjson 反序列化检测 burp 插件

使用方法也很简单，就像使用 repeater 一样，你可以在 burp 的任何地方选中一个请求右键选择【Send to FastjsonScan】将这个请求发送到 Fastjson Scan，然后就只需要等待扫描结束🌶 。如果扫描的目标存在漏洞，在窗口下面的 Request 窗口会展示使用的 payload, 如果没有漏洞，则会展示原始的请求与响应

> ps: 由于反序列化检测利用了 dnslog，所以检测会稍微慢一点，在等待结果期间你还可以继续看其他请求，真的是相当方便呢

地址：https://github.com/Maskhe/FastjsonScan.git

### rexsser

这是一个 burp 插件 (python)，它使用 regexes 从响应中提取关键字，并测试目标范围内的 XSS 反射。有效的参数会被反射，易受攻击的参数会显示在 rexsser 扩展选项卡的结果中。

地址：https://github.com/profmoriarity/rexsser.git

### Struts2-RCE

一个用于检查 struts 2 RCE 漏洞的 Burp 扩展器。

这个 Burp 扩展可以检测到以下 18 个远程代码执行漏洞，它们是

•S2-001•S2-007•S2-008•S2-012•S2-013•S2-014•S2-015•S2-016•S2-019•S2-029•S2-032•S2-033•S2-037•S2-045•S2-048•S2-053•S2-057•S2-DevMode

地址：https://github.com/prakharathreya/Struts2-RCE.git

被动扫描篇
-----

### Passive Scan Client and Sendto

Passive Scan Client and Sendto | Burp 被动扫描流量自动转发和手动重发插件

基于 @c0ny1 师傅的被动扫描流量自动转发的基础上添加右键手动重发的功能

地址：https://github.com/Conanjun/passive-scan-client-and-sendto

### burp_find_shiro

1、通过 burp 代理流量寻找 shiro 站点，加载模块

2、开启代理，访问网站

3、如果网站使用的是 shiro，则在模块输出和 “Dashboard” 提示

地址：https://github.com/Jumbo-WJB/burp_find_shiro.git

### BurpShiroPassiveScan

一款基于 BurpSuite 的被动式 shiro 检测插件

BurpShiroPassiveScan 一个希望能节省一些渗透时间好进行划水的扫描插件

该插件会对 BurpSuite 传进来的每个不同的域名 + 端口的流量进行一次 shiro 检测

目前的功能如下

•shiro 框架指纹检测 •shiro 加密 key 检测

地址：https://github.com/pmiaowu/BurpShiroPassiveScan.git

### burp_jspath

获取 js 文件路径

获取 html 脚本标签路径

筛选资产内容

效果如下：

地址：https://github.com/j1anFen/burp_jspath.git

![](https://mmbiz.qpic.cn/mmbiz_png/BibeFvVBkRA8YBNkgJ9Jx6nZz3La2Aztr4Acx9c6QLeongFqNmNZuibV7HLdB8OaFDxcBaDyDpeLdMenAzyHq7wA/640?wx_fmt=png)

### Burp Bounty - Scan Check Builder

这个 Burp Suite 扩展允许你以一种快速和简单的方式，通过一个非常直观的图形界面，通过个性化的规则来改进主动和被动的 Burpsuite 扫描仪。通过对模式的高级搜索和改进发送的有效载荷，我们可以在主动扫描器和被动扫描器中创建自己的问题配置文件。

这个插件很强，Burpsuite 官方插件商店可下，分免费版和收费版。

收费版有很多非公开的被动扫描规则价格好像是人民币 500 多一年，不过你们可以去 github 搜一些别人写好的开源到 github 上的规则一样用，或者你自己学习去写规则。

地址：

https://github.com/wagiro/BurpBounty.git 或者 burpsuite 官方商店

使用 demo 视频（请自备武当穿云梯）

https://www.youtube.com/channel/UCSq4R2o9_nGIMHWZ4H98GkQ/videos

免费的规则库：

https://github.com/Sy3Omda/burp-bounty.git

效率扩展篇
-----

### BurpCrypto

**在 Web 渗透测试中有一个关键的测试项：密码爆破。**

目前越来越多的网站系统在登录接口中加入各式各样的加密算法，依赖于 BurpSuite 中的那些编码方式、Hash 算法已经远远不够，这里给大家介绍一款支持 AES/RSA/DES 加密算法，甚至可以直接将加密算法的 Javascript 脚本运行与 BurpSuite 中的插件：**BurpCrypto**。

地址：https://github.com/whwlsfb/BurpCrypto/releases

使用教程：https://blog.wanghw.cn/security/burpcrypto-tutorial.html

### burpFakeIP

伪造随机 ip 爆破的先决条件可以伪造 ip 绕过服务器限制。

四个小功能

• 伪造指定 ip• 伪造本地 ip• 伪造随机 ip• 随机 ip 爆破

地址：https://github.com/TheKingOfDuck/BurpFakeIP

### burp-fofa

基于 BurpSuite 的一款 FOFA Pro 插件。

地址：https://github.com/0nise/burp-fofa.git

![](https://mmbiz.qpic.cn/mmbiz_png/BibeFvVBkRA8YBNkgJ9Jx6nZz3La2Aztrib1gR48k190hLHrFTyqVmnIhFU6ofmia9TgnHib95xkFicjuNbicCYc4JTw/640?wx_fmt=png)

### knife

插件的主要的目的是对 burp 做一些小的改进，更加方便使用。就像用一把**小刀**对其进行小小的雕刻。增加了一些右键菜单提升效率

地址：https://github.com/bit4woo/knife

使用视频教程：https://www.bilibili.com/video/bv1BC4y1s7nS

### HaE - Highlighter and Extractor

**HaE** 是基于 `BurpSuite` 插件 `JavaAPI` 开发的请求高亮标记与信息提取的辅助型插件。

该插件可以通过自定义正则的方式匹配**响应报文或请求报文**，可以自行决定符合该自定义正则匹配的相应请求是否需要高亮标记、信息提取。

**注**: `HaE`的使用，对测试人员来说需要基本的正则表达式基础，由于`Java`正则表达式的库并没有`Python`的优雅或方便，在使用正则的，HaE 要求使用者必须使用`()`将所需提取的表达式内容包含；例如你要匹配一个 **Shiro 应用**的响应报文，正常匹配规则为`rememberMe=delete`，如果你要提取这段内容的话就需要变成`(rememberMe=delete)`。

地址：https://github.com/gh0stkey/HaE、

共享一下作者自己整理收集的一些 Hae 规则吧  

```
{
    "azure_storage": {
        "loaded": true,
        "regex": "(https?://[\\w-\\.]\\.file.core.windows.net)",
        "color": "red",
        "engine": "nfa",
        "scope": "response",
        "action": "any"
    },
    "IPv6": {
        "loaded": true,
        "regex": "(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])) ",
        "color": "red",
        "engine": "nfa",
        "scope": "response",
        "action": "any"
    },
    "Ipone": {
        "loaded": true,
        "regex": "([^0-9]+(1[3-9]\\d{9})[^0-9]+)",
        "color": "red",
        "engine": "nfa",
        "scope": "response",
        "action": "any"
    },
    "AWS Client ID": {
        "loaded": false,
        "regex": "(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16} ",
        "color": "red",
        "engine": "nfa",
        "scope": "response",
        "action": "any"
    },
    "Facebook Client ID": {
        "loaded": false,
        "regex": "(?i)(facebook|fb)(.{0,20})?['\\\"][0-9]{13,17} ",
        "color": "red",
        "engine": "nfa",
        "scope": "response",
        "action": "any"
    },
    "IPv4": {
        "loaded": true,
        "regex": "\\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}\\b ",
        "color": "red",
        "engine": "nfa",
        "scope": "response",
        "action": "any"
    },
    "Facebook Secret Key": {
        "loaded": true,
        "regex": "(?i)(facebook|fb)(.{0,20})?(?-i)['\\\"][0-9a-f]{32} ",
        "color": "red",
        "engine": "nfa",
        "scope": "response",
        "action": "any"
    },
    "Cloudinary Basic Auth": {
        "loaded": true,
        "regex": "cloudinary:\\/\\/[0-9]{15}:[0-9A-Za-z]+@[a-z]+ ",
        "color": "red",
        "engine": "nfa",
        "scope": "response",
        "action": "any"
    },
    "secret_key": {
        "loaded": true,
        "regex": "[Ss](ecret|ECRET)_?[Kk](ey|EY)",
        "color": "red",
        "engine": "nfa",
        "scope": "response",
        "action": "any"
    },
    "Artifactory API Token": {
        "loaded": true,
        "regex": "(?:\\s|=|:|\"|^)AKC[a-zA-Z0-9]{10,}",
        "color": "red",
        "engine": "nfa",
        "scope": "response",
        "action": "any"
    },
    "aliyun_oss_url": {
        "loaded": true,
        "regex": "([\\w-.]\\.oss.aliyuncs.com)",
        "color": "red",
        "engine": "nfa",
        "scope": "response",
        "action": "any"
    },
    "URL Parameter": {
        "loaded": true,
        "regex": "(?<=\\?|\\&)[a-zA-Z0-9_]+(?=\\=) ",
        "color": "red",
        "engine": "nfa",
        "scope": "response",
        "action": "any"
    }
 }
```

点赞，转发，在看和关注公众号就是对我这个用爱发电的作者最大的支持。需要加交流微信群的可以平台私信我发加群二维码，没有关注公众号的请勿加入。  

![](https://mmbiz.qpic.cn/mmbiz_png/BibeFvVBkRA8QtFrQn6r5sy2TYlPPMPXETfZvWUBZ168UL1ToouLBxc2Ng37LuDe39lcXnkcjFeibGu9f7crXfAQ/640?wx_fmt=png)