\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/T0xeXKnUuEZKsO9PQqGaCw)

**Java 作为企业主流开发语言已流行多年，各种 java 安全编码规范也层出不穷，本文将从实践角度出发，整合工作中遇到过的多种常见安全漏洞，给出不同场景下的安全编码方式。**

本文漏洞复现的基础环境信息：jdk 版本：1.8 ，框架：springboot1.5，数据库：mysql5.6 和 mongodb3.6，个别漏洞使用到不同的开发框架会特别标注。

安全编码实践
------

### Sql 注入防范

常见安全编码方法：预编译 + 输入验证

预编译适用于大多数对数据库进行操作的场景，但预编译并不是万能的，涉及到查询参数里需要使用表名、字段名的场景时 (如 order by、limit、group by 等)，不能使用预编译，因为会产生语法错误。常见的预编译写法如下

jdbc：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09pLxVNNV5ezLZB83145rJLmvnBYyRNAdLG8RibFDV3XfmXtyupVMRPKA/640?wx_fmt=jpeg)

Hibernate

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv097uezcYHJKSMSrjic3bBhsEuLFxxa6E972a5yw8mIL3THA863omoictnA/640?wx_fmt=jpeg)

Ibatis

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09FgmVHIVHlbyaSD9cQfjuMJsJoK2xqib7JwHMibIpko7SkRjhoxVoO47Q/640?wx_fmt=jpeg)

Mybatis

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09HVia1ymEIFj2xfRib5XKqnh7JicuZ0XshxqXibLlDlZGRVqIaLjpNtGMHg/640?wx_fmt=jpeg)

在无法使用预编译的场景，可以使用数据校验的方式来拦截非法参数，数据校验推荐使用白名单方式。

错误写法：不能使用预编译的场景（直接拼接用户的查询条件）

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09bD37zXmdrvqWVCqedb284qw7AyOuWsq5XNkccoMdyPocibCHqDzmCLQ/640?wx_fmt=jpeg)

漏洞利用验证：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09iby9b5zRvDqzBtGrG7vMZDibDmhicpejlT5ibSWcPVO4teumgib4coKrA4Q/640?wx_fmt=jpeg)

不能使用预编译的正确写法（通过白名单验证用户输入）：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv095Jfb6jrlmwoyCzEESu6MM6eSXmWvLtvwW6Kd6ItKuZFcxdX5fxncFw/640?wx_fmt=jpeg)

漏洞修复验证：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09c065OPHcyjpEwEmKuXteZ4qlHiaicF0bskVwGgQK4MZs8nqksYPf30RQ/640?wx_fmt=jpeg)

### Nosql 注入防范

涉及到非关系型数据库 mongdb 在查询时不能使用拼接 sql 的方式，需要绑定参数进行查询，跟关系型数据库的预编译类似

错误写法 (拼接用户的查询条件)：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09G2ZtUVcxfY3iaylmY0U6JQuoD5U3xVrs9skRWKib8OkxImANkUKoE1OQ/640?wx_fmt=jpeg)

漏洞利用验证：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09F88yhJNF7LgVwIIR0ibvJX315zia3prRO7D6b3TkQ9w5ue3r8kiaicvnZw/640?wx_fmt=jpeg)

正确写法 (参数绑定)：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv094RjZicPpEOP0NmmQSCffN02cTWX8aHtte7Pd4yicKsJia4ahPT0iaTuJicw/640?wx_fmt=jpeg)

漏洞修复验证：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09U6frgVSyuVL7d84Ev1fxfygE7F2YNfPH1MpuCn4eToosYQE8DgDozw/640?wx_fmt=jpeg)

### Xss 防范

> 白名单校验
> 
> 适用于纯数字、纯文本等地方，如用户名
> 
> Esapi
> 
> 适用于常规的输入输出，如用户评论

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09wOGhGIqicHicLGibqMR0Mxk9qv1GBiaywOIdbMpQmzUhl3JQXLiaTC1FGeQ/640?wx_fmt=jpeg)

错误写法（对用户输入内容不做处理）：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09LhCHVZF5td7rvbHMZz8ibJ25icNV37AYUkDGgRCANCnicN5LGAdnBPm1w/640?wx_fmt=jpeg)

正确写法（通过 esapi 的黑白名单配置来实现富文本 xss 的过滤）：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09lXnfLicjVI0DaKic6rKe0Lgx0Z6M4xjlcQ3mgnuiaz4ehgAVnlo8tyGEw/640?wx_fmt=jpeg)

漏洞利用及修复验证：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09yZicBVBG4QdwfJ291JgOzsgU12h9LicBwMMb7KypochUWYMgPbRicRyTw/640?wx_fmt=jpeg)

### XXE 注入防范

为了避免 XXE injections，应为 XML 代理、解析器或读取器设置下面的属性：

> factory.setFeature(“http://xml.org/sax/features/external-general-entities“,false);
> 
> factory.setFeature(“http://xml.org/sax/features/external-parameter-entities“,false);

如果不需要 inline DOCTYPE 声明，可使用以下属性将其完全禁用：

> factory.setFeature(“http://apache.org/xml/features/disallow-doctype-decl“,true);

错误写法 (以 xmlReader 为例，允许解析外部实体)：

> XMLReaderxmlReader = XMLReaderFactory.createXMLReader();
> 
> xmlReader.parse(newInputSource(newStringReader(body)));

漏洞利用验证：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09A0pIcj1lN3Oz0vAW0oiaqPN72w2CBTFIh7ENdibibZgfMEfjSx4zIicGNA/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09KaP9rMp3DGSsOWNC9cPPG3JjvuAHTLtVoPlIQa6Q8o4qfEEyg0yl2g/640?wx_fmt=jpeg)

正确写法（禁止解析部实体）：

```
XMLReaderxmlReader = XMLReaderFactory.createXMLReader();
xmlReader.setFeature("\[http://xml.org/sax/features/external-general-entities\](http://xml.org/sax/features/external-general-entities)",false);
xmlReader.setFeature("\[http://xml.org/sax/features/external-parameter-entities\](http://xml.org/sax/features/external-parameter-entities)",false);
xmlReader.parse(newInputSource(newStringReader(body)));
```

### 文件上传漏洞  

文件名随机，防止被猜解上传路径

限制上传文件大小，防止磁盘空间被恶意占用

限制上传文件类型，防止上传可执行文件

正确写法（限制文件类型大小，通过 uuid 生成随机文件名保存）：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09fCwHZooSxjFHdg3Gc4EEmyDxx9wIVzdfwrmoUsgQRNSENOwDnTUricw/640?wx_fmt=jpeg)

漏洞利用验证

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09ZYicPy57UDoq643kiby3voC5KQGMVfg6nfWB9LgyHf98clnBiaJANDRDw/640?wx_fmt=jpeg)

漏洞修复验证：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09ga4p1UObaSb5XtxhmF3myexGjr2V71QFh09DLicnFV3envUa2euN5Qw/640?wx_fmt=jpeg)

### 文件包含

限制文件在指定目录，逻辑名称绑定文件路径，跟文件上传的处理类似，通过文件 id 读取对应资源文件

错误写法（直接请求用户设置的资源）：

```
String returnURL = request.getParameter("returnURL");
returnnew ModelAndView(returnURL);
```

漏洞利用验证：  

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv095LFKZrVmojRxq8X5kV7Yn61tvSibp2d6KdcBDxcYDnknrTEoWKxFQYw/640?wx_fmt=jpeg)

正确写法（通过文件 id 和真实路径的映射设置白名单）：

```
if(SecurityUtil.checkid(file\_id) ==null) {
return"资源文件不存在！";
}
returnget\_file(SecurityUtil.find\_path(file\_id));
}
```

文件上传后对应的路径会存储在数据库里，表结构如下：  

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09fJFWTo8AYqjEZoLJZnyZd5oY91YcgBDRMq6IU2lCGAgtK7EspX4CaA/640?wx_fmt=jpeg)

漏洞修复验证

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09jDTYCUs74a88ZDoZjTp90NoCicmbEXmSYWUTA32DMxBYmL5j5Lnsc4Q/640?wx_fmt=jpeg)

Csrf

常见的框架已经自带了防范 csrf 的功能，只需要正确的配置启用即可

### struts2

JSP 使用标签，在 struts 配置文件中增加 token 拦截器

页面代码：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09DiaEUC5g1w01sjNGUoLz4qYPj0rRQuNCuJRHialmo1441zKePhE0NJ7A/640?wx_fmt=jpeg)

漏洞修复验证：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv097icdf9GSmKSOJBRkicY1tepWff8K3516AwHNu5QL1ka8P73yNG5kvvSw/640?wx_fmt=jpeg)

### Spring

正确写法：使用 spring-security

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09Rhnz2H79jlI5ppLX1S9jFY5VspPibgKxwpvC4SicRGZss7iaBVqdRhQEw/640?wx_fmt=jpeg)

漏洞修复验证

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09fb0sFHtWcCeAr5NiaWtE1mkb6jbiaFkibnLWU0icE0ia9rZ9q4p9ibQN6zug/640?wx_fmt=jpeg)

### 越权

Java 通用权限框架 (shiro)

进行增删改查操作时采用无法遍历的序号

对于敏感信息，应该进行掩码设置屏蔽关键信息。

垂直越权

角色权限矩阵

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09PPUYmicOdHtf0ZuFYahtqDYGJysZ7xfvhlTfPElpWKbnicy18jUQbndw/640?wx_fmt=jpeg)

限制匿名用户和低权限用户，执行操作前检查用户登录状态和权限清单

正确写法（判断用户权限清单是否包含请求的权限）：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09NjBdre0POMqqTwsZupFK2NWeGIIdqSVic4S7a1XtUssvc2MQwdy82Xw/640?wx_fmt=jpeg)

漏洞修复验证

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09yb3Jvibj69DtbLBhibCYWsGRmZ505kWLByZt9eFkLbDUZlUab1oDsFgg/640?wx_fmt=jpeg)

水平越权：

操作前判断下当前用户是否有对应数据权限，修复后修复前两次验证，通过返回长度不同可看到水平越权问题已解决。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09q7Sp7E8xBotn7TjZia2VtzJpGF5ZcMAI7kicSqdlyu4sycg1tnQZEdYA/640?wx_fmt=jpeg)

### url 重定向 & ssrf

url 重定向

对于白名单内的地址，用户可无感知跳转，不在白名单内的地址给用户风险提示，用户选择是否跳转

正确写法：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv090EGT9XWEqRGk7icarn5jxxAfrZLFaIRDhfYJIkFjMEUPRDXCHSwBlSw/640?wx_fmt=jpeg)

漏洞修复验证

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09G8v5ZkK2nbmy5jKApOYV6HtnwfmicTmicWXV9gbSibFNx7riaKfO8FDFEA/640?wx_fmt=jpeg)

Ssrf

漏洞利用验证：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09VMK5ScPzbXlHonReiaOm17Z9NkmQXrSSVicNceGJr6hrfIYahia7BFwaQ/640?wx_fmt=jpeg)

正确写法（限制请求协议，设置白名单域名，避免内网地址探测）：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09eMDBoegiceZibZbGpdZhtic0CF3SstZE5zFgms9oUTmiak1b53ADhUcPow/640?wx_fmt=jpeg)

漏洞修复验证

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09P97sialo5pDibdVFuP15dDDSn1IIBzn5MLwDGhWWZNGDNCYiby7bv5nTw/640?wx_fmt=jpeg)

### 拒绝服务

正则表达式拒绝服务，这种漏洞需要通过白盒审计发现，黑盒测试比较难发现。

错误写法（正则匹配时未考虑极端情况的资源消耗）

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09EvIgiczEemZ3zwlMG4hF2syl7afxfRdwd9OrZSIIs7GsLy1eRaITopA/640?wx_fmt=jpeg)

漏洞利用验证，随着字符长度增加，响应时间会越来越长，cpu 满负荷运转

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09rsEW9vbT2RQrrfm2y7gicH0iaQUtln6gnMibFT3Aic3JKhYRF4d7bVohWA/640?wx_fmt=jpeg)

正确写法（运行超过 2 秒就中止匹配）：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv098hblVIpC5nUxn6tuGrUmuCRNia26XsOA8FFX6FyEXfYyic7ibsAZEelIg/640?wx_fmt=jpeg)

漏洞修复验证：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09ic3O1fPyFVQyXSicfzCK16BGy1z7buHibLZ5iaAygk9oGmfxibtA9buRxLA/640?wx_fmt=jpeg)

### 不安全的加密模式

需要通过白盒审计发现漏洞，直接黑盒测试比较难。

错误写法：使用 ECB 模式，相同明文生成相同密文

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09cph63Whvm00gb0t3hZ2JMJcT3FWydia7JA4tqtbXUkuR3AGLkRoQ7ibg/640?wx_fmt=jpeg)

漏洞利用验证（使用选定明文攻击从后向前按位猜解）：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv098ic0LicBDPia4vmqibCJUxmoUAB0x8L9eac7n7MqSe066Lnib2kLhdSIDIg/640?wx_fmt=jpeg)

正确写法：使用 CBC 模式，相同明文生成不同密文

```
Cipher cipher =Cipher.getInstance("AES/CBC/PKCS5Padding");
```

```
public voidlog\_forging(HttpServletRequest request,HttpServletResponse response)
throwsException {
logger.info("user: "+request.getParameter("name")+" received 100$;");
}
```

需要通过白盒审计发现漏洞，直接黑盒测试比较难。

错误写法：使用伪随机，相同种子生成相同随机数序列

漏洞利用验证：

需要通过 java 生成前后 2000 毫秒内的随机数，然后使用 python 调用这些随机数尝试暴破

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09iaYf6XOFYf0YSVcYFdYJcWjYhejdcD22dZUI8CmZWw8icM5KCZBbNozQ/640?wx_fmt=jpeg)

正确写法：使用 Securerandom

漏洞修复验证（Securerandom 不能指定 seed，避免伪随机）：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv098ibCooS1kBk13bX1nGaiaia3SUdhbwYInZy3QOdrvDQcuRX94HsqdK1NQ/640?wx_fmt=jpeg)

### 条件竞争

Servlet 的单例模式容易导致条件竞争，也是推荐白盒方式审计漏洞。

错误写法：初始积分 100 个，每天限制签到 1 次领取 1 积分

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09iaQY5MpOoIvtDxaYDAbDeS71VNuYFBEABEdDfFvibxrK7gSbYX03fQHA/640?wx_fmt=jpeg)

漏洞利用验证（10 个并发可实现多次签到，这里多并发跟业务功能复杂度和服务器性能有关，如果想必现漏洞，可以在读取签到次数和增加签到次数之间增加 2 秒延时，可以保证漏洞复现。）

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09h91nvgE9Vw10V83ZWbUfgiaib7GLmsUPsdwibyhQ3hHfvbKmgia7Jj9lfA/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09syHxfmibII8vzE9pqGgqoVG6l7UqXLwTiad0bewyu4uqCaTFhzyjibzcQ/640?wx_fmt=jpeg)

正确写法：使用线程同步

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09oJcAicKPl4bD24DE0VmhTbCFibQHPy9lOGmCFYASlruRkTYcVAyXznLA/640?wx_fmt=jpeg)

漏洞修复验证：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09iafsgTSFicJeXf4H5icgSfzeoN3xf1C34RibTaBcZLsEopDKoJMr8OTGUg/640?wx_fmt=jpeg)

修复后返回数据包速度明显变慢，不能再重复签到领积分

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09uBAesqqVqX2Oaet3icH7DDVPvGrYMwMxJyReXdBWHcTvCsOOlarHSpw/640?wx_fmt=jpeg)

### 日志伪造防范 / http 响应拆分防范

日志伪造黑盒测试无法发现，需要通过白盒审计发现漏洞。

错误写法（直接将用户的输入打印到日志文件）：

```
public voidlog\_forging\_sec(HttpServletRequestrequest, HttpServletResponse response)
throwsException {
Pattern p = Pattern.compile("\\\\s\*|\\t|\\r|\\n");
Matcher m =p.matcher(request.getParameter("name"));
String );
logger.info("user: "+name+" received 100$;");
}
```

漏洞利用验证（通过 %0d%0a 插入换行控制符，伪造日志记录）  

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09gDd2daOWtX1W3fmKUYjibgRbfBialsOthwacicPia8DbaKMpLvDb2RxRNA/640?wx_fmt=jpeg)

正确写法（过滤换行空格）：

```
@RequestMapping("/http\_splitting")
@ResponseBody
public voidhttp\_splitting(HttpServletRequest request,HttpServletResponse response)
throwsException {
Stringaddheader=request.getParameter("addheader");
response.addHeader("addheader", addheader);
}
```

漏洞修复验证  

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09Je4f49syfWkickwiaehibb8jhDfTcJz5rZd949oOJkmSW2VTyeCs2nshw/640?wx_fmt=jpeg)

http 响应拆分，只在低版本 web 服务器上出现，使用 tomcat9 未复现这个问题

错误写法

```
if(!cmd.equals("xxx")){
return"command "+cmd+" not allowed!";
}
```

漏洞修复验证 (新版本的 web 服务器可以自动处理 http 响应拆分)：  

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09lFKaFuzBW9C3fl5pn5Xea7sZsSIepl8icjBMq0oBaCY5KdCII8EA0tA/640?wx_fmt=jpeg)

动态代码执行
------

Runtime.exec

错误写法 (直接执行用户输入的命令)：

Process p = run.exec(cmd);

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09gciba2IMA2VdX7gxLLplFFxNqmte16pYOwwztv3wls8w3G2X8UKCobA/640?wx_fmt=jpeg)

正确写法：

1\. 输入净化

2.Switch-case 命令映射

```
endpoints.jmx.enabled=false
management.endpoints.jmx.exposure.exclude=\*
```

3\. 使用语言标准 api 获取系统信息  

“当前用户:”+System.getProperty(“user.name”)

漏洞修复验证

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09Xust8zA74Fe4Qk3SmbCxLIgTYluxpDgicD52Gf0uJiaUGym7FnibyjnsQ/640?wx_fmt=jpeg)

### 反序列化

错误写法（对序列化的类未做限制）：

> Stringdata=request.getParameter(“data”);
> 
> byte\[\] decoded = java.util.Base64.getDecoder().decode(data);
> 
> ByteArrayInputStream bytes =newByteArrayInputStream(decoded);
> 
> ObjectInputStream in =newObjectInputStream(bytes);
> 
> in.readObject();
> 
> in.close();

漏洞利用验证

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09lRwDFib2t4gm9RicXMKqdia4oHcD1drlX4N2jokiaIEicy23TSGHjrfWslA/640?wx_fmt=jpeg)

正确写法 (使用 serialkiller，主要也是通过黑名单去过滤，可以防御大部分的攻击)

> String data =request.getParameter(“data”);
> 
> byte\[\] decoded = java.util.Base64.getDecoder().decode(data);
> 
> ByteArrayInputStream bytes =newByteArrayInputStream(decoded);
> 
> try{
> 
> ObjectInputStream in =newSerialKiller(bytes,”d:\\serialkiller.conf”);
> 
> in.readObject();
> 
> in.close();
> 
> }catch(InvalidClassException e){
> 
> response.getWriter().write(“class not allowed!”);
> 
> }

漏洞修复验证

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09jU6Th3cwZFriaopWfiaWfkUa2FBWNnHUxI2bffDkj98e2I9oyO7mxaOQ/640?wx_fmt=jpeg)

### 表达式注入

Spel 表达式注入

错误写法（直接解析表达式）：

> public voidspel\_injection(HttpServletRequest request,HttpServletResponse response)
> 
> throwsException {
> 
> A a=newA(“test”);
> 
> ExpressionParser parser =newSpelExpressionParser();
> 
> StandardEvaluationContext context =newStandardEvaluationContext();
> 
> parser.parseExpression(“Name = “+request.getParameter(“name”)).getValue(context, a);
> 
> response.getWriter().write(“usrname:”+a.getName());
> 
> }

漏洞利用验证：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09ftN8sNay3hlmWN11llgCQueO8nYkvlBD873ibEnSPhnUbWkpEs5fJFg/640?wx_fmt=jpeg)

正确写法 (使用 SimpleEvluationContext，可解析白名单内的表达式)：

> public voidspel\_injection\_sec(HttpServletRequestrequest, HttpServletResponse response)
> 
> throwsException {
> 
> A a=newA(“test”);
> 
> ExpressionParser parser =newSpelExpressionParser();
> 
> EvaluationContext context =SimpleEvaluationContext.forReadWriteDataBinding().build();
> 
> parser.parseExpression(“Name = “+request.getParameter(“name”)).getValue(context, a);
> 
> response.getWriter().write(“usrname:”+a.getName());
> 
> }

漏洞修复验证

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09AjyuvcVNd2WMWYpWpYoVNPcoZAwaYnAWnibCWaxr59BIyhVwnBJwgqQ/640?wx_fmt=jpeg)

OGNL 表达式注入涉及到 struts 框架的安全配置，主要是禁用动态方法调用，不再继续展开验证。

### Spring-boot 安全配置

1.Spring Boot 应用程序配置为显式禁用 Shutdown Actuator：endpoints.shutdown.enabled=false 避免应用被非法停止

2\. 删除生产部署上的 spring-boot-devtoos 依赖关系。

3\. 不要远程暴露 mbean spring.application.admin.enabled=false

4\. 启用 html 自动转义

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09U2qMFzibx3vq2GS4TP467sfHJuWCUlDudm7JEoAMh7lEfVmib8lUMyGw/640?wx_fmt=jpeg)

5\. 使用默认 http 防火墙 StrictHttpFirewall

6.Spring Security 身份认证配置, 该配置默认为拒绝对之前不匹配请求的访问：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09Ghf18zaXMWsyUbPky7HNG8O9iaiaItusHEicxhlVrOrbriahflYHbG13vQ/640?wx_fmt=jpeg)

7\. 禁用 SpringBoot ActuatorJMX

```
management.security.enabled=false
```

8\. Spring Boot Actuator 开启 security 功能  

错误配置：

```
management.security.enabled=true
```

漏洞利用验证：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09feRqSWEttvGpkwUibpWEpjwNa86WF9dDes5eqZ9l9zvgpGK9pYkKznQ/640?wx_fmt=jpeg)

正确配置：

```
management.security.enabled=true
```

漏洞修复验证

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39NT6ib53ZKlkBBujY0Kqv09UyPA9sDtduKib68DDULewoHN9mPiau0I7oicB4XreVG2ymBCliaZul8duw/640?wx_fmt=jpeg)

总结
--

作为安全人员经常会被开发问如何修复漏洞，开发需要具体到某行代码如何改动，通过对常见漏洞的复现利用以及安全编码实践，可以加深安全人员对相关漏洞原理的理解，根据业务需要更具体地帮助开发人员写出健壮的代码，预防或修复安全漏洞。

参考资料
----

> https://github.com/JoyChou93/java-sec-code/ 前面的常见注入类漏洞参考了这里的代码。
> 
> https://vulncat.fortify.com/en 后面的不安全加密模式，不安全随机数等配置漏洞参考 fortify 官方的漏洞知识库。

****扫描关注乌云安全****  

![](https://mmbiz.qpic.cn/mmbiz_jpg/bMyibjv83iavz34wLFhdnrWgsQZPkEyKged4nfofK5RI5s6ibiaho43F432YZT9cU9e79aOCgoNStjmiaL7p29S5wdg/640?wx_fmt=jpeg)

**觉得不错点个 **“赞”**、“在看” 哦****![](https://mmbiz.qpic.cn/mmbiz_png/3k9IT3oQhT1YhlAJOGvAaVRV0ZSSnX46ibouOHe05icukBYibdJOiaOpO06ic5eb0EMW1yhjMNRe1ibu5HuNibCcrGsqw/640?wx_fmt=png)**