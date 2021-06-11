> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/EHn4ScNOEr9lyda2bnGWPQ)

**描述**

  

PbootCMS 是全新内核且永久开源免费的 PHP 企业网站开发建设统，是一套高效、简洁、 强悍的可免费商用的 PHP CMS 源码，但存在 SQL 注入漏洞，攻击者可构造恶意语句进行获取敏感数据。

  

  

  

  

  

**影响范围**

  

PbootCMS 3.0.4  

  

  

  

  

  

**FOFA**

  

app="PBOOTCMS"

  

  

  

  

  

源码分析
----

漏洞代码位置：

```
apps\home\controller\ParserController.php
```

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCXOYYibX4iaQSVe1FxuzpCKJY7mxqVMOqPJ23ohehUII6O2EicoeibwLpzpiaxOXsBEglia2rhU9m9e6UA/640?wx_fmt=png)

当传递的参数 $where 是一个数组时就遍历数组，当 $where 是一个索引数组时则：$where_string.=$value。  

接下来找到 “$where” 函数中要传递的代码为索引数组时的代码：

```
pbootcms\static\backup\sql\0cb2353f8ea80b398754308f15d1121e_20200705235534_pbootcms.sql
```

在 “parserSearchLabel()” 方法中，传入的数据被分配到变量 “$receive” 进行遍历，“$key”被带入 “request()” 进行过滤。

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCXOYYibX4iaQSVe1FxuzpCKJImkibicicmCjgUZHHnFVApsQ3PYdhj3DcTgYia6YiaUw8FFHgn20aV8roYw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCXOYYibX4iaQSVe1FxuzpCKJR0g4UWfnFIp7mCicdyRJUIfqrzxm7XZjO8AGdZ7cicN4EicmhGltzx9LQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCXOYYibX4iaQSVe1FxuzpCKJNCP56XubunAVugClgC9Xgs7OrnWw60In3OGjazCmF6vSkHhk0FrdPA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCXOYYibX4iaQSVe1FxuzpCKJiaq9GXGUWpC8S8n3PibTp1jZl2oruw03SDd4Ho62ibBr22SyyyfRe0jYQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCXOYYibX4iaQSVe1FxuzpCKJ59G2qkN9sRwLJyuz9bhibBvge942aicjm8ITEjK5rMZaVicDqvj5njA1g/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCXOYYibX4iaQSVe1FxuzpCKJdLr57Uq0CgMdy6OWUcpsXCdiaSxjkatFzgUVkPwVQsoicEBwDvcIKJKQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCXOYYibX4iaQSVe1FxuzpCKJ4EI6OoUgc7hXLibeglsnFFCnKq8ueMAuiciaO3VzSib4qYPUicOnjs8Psfg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCXOYYibX4iaQSVe1FxuzpCKJBmDXTWvSeKeWfK7wmhbssyZFQpd2SHNeV5tibqY9LouiaichXibVmwDY9Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCXOYYibX4iaQSVe1FxuzpCKJibk0pZwjkApSpcge2JRd6Mdh5MmFy59M4YzQFFrGkcPv2aHjFKeqbZA/640?wx_fmt=png)

通过上述方法传入索引数组的值只能包含中文、字母、数字、水平线、点、逗号和空格！它由 “htmlspecialchars()” 和“addslashes()”编码。最后，它被传递到 “$where3”。  

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCXOYYibX4iaQSVe1FxuzpCKJwnItDwSKG3vMfcmdf1xpicVIcSuTGzdoXhFutxfiaA9g1T0vk5Ib1Uiaw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCXOYYibX4iaQSVe1FxuzpCKJM4b3dFRxXEg8LP0TwUyxEVFyWd7yiaI3Xq2zTHhic9Libu6kHjVG9DUZg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCXOYYibX4iaQSVe1FxuzpCKJvibTic6Prz7yGtdkYr0iaKibmiaDu8oGpNplMDZDvTeu01CNxgbR4y19HJw/640?wx_fmt=png)

“getlists()”中的 “$where3” 是可控的，它将以 “and” 的形式进入语句，所以最终造成了 SQL 注入。  

本地复现
----

默认数据库是 sqlite。为了测试方便，我们需要用 mysql 数据库替换默认数据库。mysql 数据库目录：

```
pbootcms\static\backup\sql\0cb2353f8ea80b398754308f15d1121e_20200705235534_pbootcms.sql
```

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCXOYYibX4iaQSVe1FxuzpCKJvaRxkRybzHLNa3YSjh3ZhOCCJJ6guSSPZBX6icDCHQueekJdEARL18A/640?wx_fmt=png)

接下来，我们以 POST 的形式发送索引数组，还记得源码里数组中的值要以 “and” 的形式进入 “where” 条件：

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCXOYYibX4iaQSVe1FxuzpCKJvaRxkRybzHLNa3YSjh3ZhOCCJJ6guSSPZBX6icDCHQueekJdEARL18A/640?wx_fmt=png)

当条件为真时：  

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCXOYYibX4iaQSVe1FxuzpCKJHjAPnHUiazydEWAsOL9WR3bfXg2se3xtuflboBBnK4V3Jndl9fnR7sg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCXOYYibX4iaQSVe1FxuzpCKJ0D7ZDWAezbIS51L1ic7bXEj6cNOoLLEmf9pIfMz0zdCVbtVtG91iaVJw/640?wx_fmt=png)

当条件为假时：

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCXOYYibX4iaQSVe1FxuzpCKJD8Izn5vS8CBQQAH5oz6vKuicIFAEqSibsIOEOLYeLN7WibX3BxGNsFmbQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCXOYYibX4iaQSVe1FxuzpCKJZL7zTdVIOb3N5sCy2IxQUJmAdWxQtYJP8sByt6nqrcIKtd3zUIkS7g/640?wx_fmt=png)

有效载荷：由于数据经过过滤，因此只能使用 “正则表达式” 进行常规匹配。例如：“用户名 = 管理员”可以表示为 “用户名 regepx 0x5E612E2A”，其中“5E612E2A” 是“^ a”的十六进制代码。  

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCXOYYibX4iaQSVe1FxuzpCKJFicpvx4nOPgMSzvhxKGtnKkjG5icOBsEtRPIVJ7iaLEzHxXG8pI3wn1hg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibCXOYYibX4iaQSVe1FxuzpCKJaVUzoKlett2SDiak4zYTMGRxX3Z6wH2KIJkmPLbshazVsNZnEervmNQ/640?wx_fmt=png)

就可以获得管理员的账号密码了。

公众号  

wiki.xypbk.com 已经添加授权访问

获取授权方式为后台回复：文库授权  

    本站开设的起因是因为某一次 HW，查漏洞真的太麻烦了，就想起来做了一个站点，本意就是自己用来快速检索漏洞详情的，为了方便大家就公开了，但是这样就又会被不法份子利用，和影响一些大佬的权益。

    为防止黑产份子的非法利用漏洞，不给国家安全添麻烦，本站从此开启授权访问，形式以每人单独授权发放，限量 1000 人，小圈子查阅，请勿分享您获取的账号密码，账号密码具都采用随机生成的 32 位 MD5，还请牢记。

    如若因漏洞利用产生重大影响，会根据登录 IP、请求内容、申请授权等信息进行查证，查证后将对号主进行追责，故不要分享账号，终害己身。  

    虽然比较麻烦了些，但会稍微对黑产份子有一些限制，保证了本站安全，也保证国家安全。同时有些敏感东西也能第一时间放出来了，还请大家谅解。

    同时本站承诺永远不会出现买卖账号等利益相关的事情，本站永不割韭菜，永久免费检索，坚决抵制安全圈的歪风邪气。

    最后，若大家对此有意见请后台留言，本站将及时改正，若内容有侵犯您的权益，请及时提出，进行删除处理。  

    本站能坚持多久全看大家是否滥用，内容若更新较慢也请谅解，本人有工作有生活，会尽量坚持更新的。

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/nMQkaGYuOibDavXvuud5F09Tjl7NMvU8Yzhia63knJ4QJFvO4WBfd6KQazjtuPC7uqNBt5gE06ia7GjOVn2RFOicNA/640?wx_fmt=jpeg)

扫取二维码获取

更多精彩

![](https://mmbiz.qpic.cn/mmbiz_png/TlgiajQKAFPtOYY6tXbF7PrWicaKzENbNF71FLc4vO5nrH2oxBYwErfAHKg2fD520niaCfYbRnPU6teczcpiaH5DKA/640?wx_fmt=png)

Qingy 之安全  

![](https://mmbiz.qpic.cn/mmbiz_png/Y8TRQVNlpCW6icC4vu5Pl5JWXPyWdYvGAyfVstVJJvibaT4gWn3Mc0yqMQtWpmzrxibqciazAr5Yuibwib5wILBINfuQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/3pKe8enqDsSibzOy1GzZBhppv9xkibfYXeOiaiaA8qRV6QNITSsAebXibwSVQnwRib6a2T4M8Xfn3MTwTv1PNnsWKoaw/640?wx_fmt=png)

点个在看你最好看