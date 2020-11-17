\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/09iM8Y\_YDTrdcGhv9aJzSg)

0x01 前言
-------

在一次 MSSQL 注入过程中，目标 WEB 应用过滤了`substring()`且不能使用`AND、OR`语句。通过查询 SQL Server 官方手册，然后自己利用其它函数的组合，实现了一个新的字符串截取方法。

0x02 注入
-------

由于该注入点已经修复，所以无法复现，就简单复述一下前期的测试过程。

目标 WEB 程序过滤了一些常见的 SQL 注入关键字例如：SELECT、AND、CHAR() 等，但是目标 WEB 应用程序为了防止 XSS 攻击将`<`与`>`替换为空，所以利用`SEL<ECT`可以绕过关键字检测

![](https://mmbiz.qpic.cn/mmbiz_png/MZzibwD3j5oEicJib2tvvAWiauZyszND28hibvs4FGq8erNp39c2zPMt3sAcylmoWy3xq9w4IoSjxdMkhpicNoppMkRA/640?wx_fmt=png)

绕过了第一点继续进行测试的时候，发现`as<cii(x)`不管`x`的值是什么，它的结果都是`x`本身，被这个坑了挺久的。后来发现 WEB 应用还进行了二次替换，将`ascii、substr`等字符替换为空

![](https://mmbiz.qpic.cn/mmbiz_png/MZzibwD3j5oEicJib2tvvAWiauZyszND28hibhvduqM8aXF3voycSJwON3zL0kfzuDwLnRMiboN3ucdiacoloAJgnMUcQ/640?wx_fmt=png)

发现这点后心想，这个注入稳了，利用双写`asasciicii(subasciistring(user,1,1))`绕过 WEB 应用的检测，但是真正测试的时候并不是我想象得那么简单，WEB 报错了，换了很多种组合还是报错。仔细想一想可能是 WEB 应用还做了别处理，应该换一种方法了

0x03 新方法
--------

通过查阅 SQL SERVER 官方使用手册（https://docs.microsoft.com/zh-cn/sql/t-sql/functions/charindex-transact-sql?view=sql-server-ver15）发现了一个有用的函数 CHARINDEX()

![](https://mmbiz.qpic.cn/mmbiz_png/MZzibwD3j5oEicJib2tvvAWiauZyszND28hibicjpvicJ0cW1MicwkCicRbVUp405IeMGJwNm1k1BQmSZib9mdWW26bNwqrw/640?wx_fmt=png)

比如`SELECT CHARINDEX('o', 'root');`从`root`开头查找，显而易见第一个`o`在第二个位置所以返回的结果是`2`

![](https://mmbiz.qpic.cn/mmbiz_png/MZzibwD3j5oEicJib2tvvAWiauZyszND28hibtoIoPceAVK1QLcuxKoljJffm0M1ibmSIkSv2nwbt9S6SkFBUaJGEdOQ/640?wx_fmt=png)

```
SELECT CHARINDEX('o', 'root', 3);\`从\`root\`第\`3\`个字符开始查找，那么第一次出现\`o\`的位置就是\`3\`，所以这次的返回值是\`3
```

![](https://mmbiz.qpic.cn/mmbiz_png/MZzibwD3j5oEicJib2tvvAWiauZyszND28hibuwDb15y3HqzZicrQdQpHQPRiaiaeWpAEh7eVxlLyNwLvhQEAUj6dy5E0A/640?wx_fmt=png)

```
SELECT CHARINDEX('o', 'root', 4);\`从\`root\`第\`4\`个字符开始查找，从第\`4\`个字符串后面已经没有\`o\`了所以返回结果为\`0
```

![](https://mmbiz.qpic.cn/mmbiz_png/MZzibwD3j5oEicJib2tvvAWiauZyszND28hibuwe4ITO56cdcibWsUGP9vZeGB9ibsZccQzzRV7zma9IH8sp6U0AibQBDQ/640?wx_fmt=png)

CHARINDEX 的查找是从左至右的，通过 start\_location 递进，同时利用 LEFT() 函数递进截取字符串，实现 CHARINDEX 每次只查找一个字符，案例如下：

```
SELECT CHARINDEX('a', LEFT('root', 2) ,2);
```

分析一下语句

1.  通过`LEFT('root',2)`截取左边两个字符也就是`ro`
    
2.  `start_location=2`从`ro`第二个字符开始查找也就是去查找`o`
    
3.  最终分析下来就是`a`在与`o`就行对比
    

这里`a!=o`所以返回`0`

![](https://mmbiz.qpic.cn/mmbiz_png/MZzibwD3j5oEicJib2tvvAWiauZyszND28hib3jY4s6PzwPPGXAqibLGxcWZ79WOjvDH5D3kIbz5Y3lnZaViaibjvItURw/640?wx_fmt=png)

这里`o=o`所以返回`o`在字符串中的位置

![](https://mmbiz.qpic.cn/mmbiz_png/MZzibwD3j5oEicJib2tvvAWiauZyszND28hib3e8zUQovDcK3tvuYnib9DYMweBib18MmdPeXSNBYkMKmMkMq0Itqc9Pw/640?wx_fmt=png)

在进行优化一下`SELECT CHARINDEX('a', LEFT('root', 2) ,2) - 2;`

如果字符不匹配那么返回结果必然小于`0`

![](https://mmbiz.qpic.cn/mmbiz_png/MZzibwD3j5oEicJib2tvvAWiauZyszND28hibsc4QVpJbyWdyvSPk7NhNErw5ia54eBVTccgQv6dSgdIR3SnwzneFZibQ/640?wx_fmt=png)

如果字符匹配那么返回结果必然等于`0`，这就算利用 CHARINDEX 和 LEFT 函数实现了 SUBSTRING 的功能

![](https://mmbiz.qpic.cn/mmbiz_png/MZzibwD3j5oEicJib2tvvAWiauZyszND28hibANLmVF5caCKYrIb4BVsOIficvQ6Or5qWf1kMVGIsHPjU4lg4Iq2wDlw/640?wx_fmt=png)

Intruder 跑数据
------------

实现我上面所说的字符串截取的功能变量应该有 4 个，而且要保证 CHARINDEX 和 LEFT 以及减去的值一致

Intruder 模块可以这样设置

![](https://mmbiz.qpic.cn/mmbiz_png/MZzibwD3j5oEicJib2tvvAWiauZyszND28hibs5nhap5U081eUjLwKpeT9pQSKOic7yKKyHVG3XiaHLRQtqmhrPySy6ww/640?wx_fmt=png)

第一个 payload

![](https://mmbiz.qpic.cn/mmbiz_png/MZzibwD3j5oEicJib2tvvAWiauZyszND28hibicpEyJPch5ic6KLTNaNOVEKdGkouzwOHRIFU5Ss5hF4cbLqF9dZksfAA/640?wx_fmt=png)

第二个 payload

![](https://mmbiz.qpic.cn/mmbiz_png/MZzibwD3j5oEicJib2tvvAWiauZyszND28hib95gFzKicicPeRMdxcctyRvWzNdHvhre8sqP2gGzUBYeicIzegsXxlUibNQ/640?wx_fmt=png)

第 3-4 个 payload，意思就是复制 2 的 payload

![](https://mmbiz.qpic.cn/mmbiz_png/MZzibwD3j5oEicJib2tvvAWiauZyszND28hibomoA5n7E6LYRbwaZhOepyfxHAy4dKsIia03fCqWBTES2KianuQLsSzicg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/MZzibwD3j5oEicJib2tvvAWiauZyszND28hibHhtUZcm7GF75VwxibWnsib3fGstiaaD7RFurhQXpN9QJ4qcaNUXrVaFCw/640?wx_fmt=png)

最终我的注入也可以出数据了

![](https://mmbiz.qpic.cn/mmbiz_png/MZzibwD3j5oEicJib2tvvAWiauZyszND28hibQm4aTXic7hrb8CZwwlT2vzMMIVL5nJJvoXuGgpBoXbh7gNpIrIibTWGg/640?wx_fmt=png)