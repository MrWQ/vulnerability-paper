> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [www.secpulse.com](https://www.secpulse.com/archives/124527.html)

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-1583303682.jpg)

BurpSuite 是我心中最强大的 Web 渗透工具，没有之一！它也是日常中用得最多的工具，它有一些强大的插件可以帮忙我们减少大量的工作量以及更好地挖掘漏洞，今天分享下我常用的一些 burp 插件。  

**Autorize —— 强大的越权自动化测试工具**

如果你在测试越权的时候，还是手动把 URL 复制到另一个浏览器的低权限账号中来打开，你就 out 了！  

Autorize 是一个测试权限问题的插件，可以在插件中设置一个低权限账号的  cookie ，然后使用高权限的账号去浏览所有功能，Autorize 会自动用低权限账号的 cookie 重放请求，同时也会发一个不带 cookie 的请求来测试是否可以在未登录状态下访问。

该插件可以直接在 Bapp Store 安装。

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-1583303683.jpg)  

如果结果中的 Authorization Enforce 列是绿色，那么就可以确定该请求两个账号都可以访问了。

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-15833036831.jpg)

**Turbo Intruder —— 短时间发送大量请求**

如果你还在用 burp 的 intruder 功能来爆破密码，测试并发，爆破目录那你就 out 了！

Turbo Intruder 是 Intruder 的增强， 它可以在短时间内发送大量的 http 请求，具体速度取决于你的网速，即使在比较差的公共网络下，它也能每秒发送几百个请求。

使用 Turbo Intruder 我们可以在几分钟内爆破完百万级的密码字典和目录字典，也可以在一瞬间发送几十个并发请求来测试并发漏洞。  

该插件可以直接在 Bapp Store 安装。

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-1583303684.jpg)

在要插入 payload 的地方加个 %s ，然后在下面窗口添加自定义的处理脚本即可开始爆破。

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-15833036841.jpg)

下图是爆破完目录的截图，可以看到 23 万的字典，只用了 105 秒，每秒发送了 2224 个请求。  

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-1583303685.jpg)

**Software Vulnerability Scanner —— 自动根据版本号查找 CVE**

Software Vulnerability Scanner 是一个扫描器增强插件，它会检查网站的一些软件版本信息，然后通过 vulners.com 上的漏洞数据库来查询相应的 CVE 编号，找到的结果会显示在漏洞面板上，不用我们自己手动去查找某个版本的 CVE 。

该插件可以直接在 Bapp Store 安装。

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-15833036851.jpg)

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-1583303686.jpg)

**Scan Check Builder —— 自定义扫描 payload**

Scan Check Builder 就是 Burp Bounty ，它提供了十分的简单的方式去为 burp 的扫描功能添加自定义的扫描 payload 。 这样我们可以对一些 burp 没有覆盖到的漏洞添加 payload，并生成相应的漏洞扫描结果。

该插件可以直接在 Bapp Store 安装。

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-1583303687.jpg)

只需要设置下请求的 payload 值， payload 插入的位置， 响应中如何判断存在漏洞，就可以快速添加一个自定义的漏洞类型了。  

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-15833036871.jpg)

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-1583303688.jpg)  

**Logger++ —— 更强大的请求历史查看器**  

Logger++ 可以查看所有工具发出的请求，如 repeater, intruder, scanner, 插件等。这样我们可以查看到扫描时的一些 payload，以及在扫描时监控网站后台的响应情况。

该插件可以直接在 Bapp Store 安装。

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-15833036881.jpg)

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-1583303689.jpg)

**Brida —— 连接 frida 与 burpsuite**  

Brida 是我很喜欢的一个插件，它可以连接 frida 与 burpsuite ，hook 神器 frida 在移动 APP 的渗透上发挥着很重要的作用，如绕过 ssl pinning ， 自动加解密 APP 的请求内容等。我们可以把一些常用的 frida 脚本放在 Brida 的脚本上，然后通过 Brida 启动 APP 来进行渗透。后续可能会写一篇文章来介绍怎样使用 Brida。

该插件可以直接在 Bapp Store 安装。

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-15833036891.jpg)

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-1583303690.jpg)

**J2EEScan —— 强大的 J2EE 后台扫描插件**

J2EEScan 是一个扫描器增强插件，可以通过该插件扫描 J2EE 漏洞，如 weblogic、struts2 、 jboss 等漏洞。唯一不足是停止更新了，只有 17 年的漏洞

该插件可以直接在 Bapp Store 安装。

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-15833036901.jpg)

**sqlmap4burp++ —— 连接 burpsuite 与 sqlmap**

sqlmap4burp++ 是一款兼容 Windows，mac，linux 多个系统平台的 Burp 与 sqlmap 联动插件。可以方便地对请求调用 sqlmap 来扫描。

该插件地址如下：

https://github.com/c0ny1/sqlmap4burp-plus-plus

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-1583303691.jpg)

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-15833036911.jpg)

**Knife ——  工具箱、自定义 payload** 

Knife 插件的主要的目的是对 burp 做一些小的改进，更加方便使用。个人比较喜欢它的 dissmiss 功能和 hackbar ++ 功能， dissmiss 可以方便让 burp 不拦截某个域名的请求，而 hackbar++ 有很多 payload ，可以方便地在 repeater 中插入 payload， 而且可以添加自定义的插入 payload。

插件的地址是：

https://github.com/bit4woo/knife

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-1583303692.jpg)

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-15833036921.jpg)

**CSRF Token Tracker —— 绕过 CSRF 限制进行暴力破解**

CSRF Token Tracker 可以自动获取 csrf 的 token，对于一些有 csrf 限制的请求，它可以绕过该限制，如暴力破解具有 csrf token 的登录请求。

该插件可以直接在 Bapp Store 安装。

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-1583303693.png)

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-1583303693.jpg)

**JSON Beautifier ——  格式化查看 json**

JSON Beautifier 可以使 json 格式的数据更加好看，也就是格式化查看，在查看 json 请求时十分好用。

该插件可以直接在 Bapp Store 安装。

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-1583303694.png)

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-15833036941.png)

**Decompressor  —— 自动解码和修改 gzip 压缩包**

Decompressor 可以自动解码和修改使用 gzip 压缩过的请求数据。有时候网站发送的数据是使用 gzip 压缩过的，使我们在 burp 上看到的请求是乱码，并且无法修改请求数据，Decompressor 可以帮我们自动解码来查看，并且可以以未压缩的方式修改数据，然后再自动进行压缩。

该插件可以直接在 Bapp Store 安装。

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-1583303695.jpg)

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-1583303696.jpg)

**Wsdler —— 测试 WSDL 请求**  

Wsdler 可以解析 WSDL 请求，以便使用 repeater 和 scanner 对 WSDL 请求进行测试。  

该插件可以直接在 Bapp Store 安装。

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-15833036961.jpg)

![](https://secpulseoss.oss-cn-shanghai.aliyuncs.com/wp-content/uploads/1970/01/beepress-image-124527-1583303697.jpg)

Burp 插件的推荐就介绍到这里了，如果大家有发现一些好用的插件，欢迎推荐！

**本文作者：[timeshatter](https://www.secpulse.com/archives/newpage/author?author_id=18416)**

**本文为安全脉搏专栏作者发布，转载请注明：**[**https://www.secpulse.com/archives/124527.html**](https://www.secpulse.com/archives/124527.html)