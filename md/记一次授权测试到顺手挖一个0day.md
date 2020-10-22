\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/pD3ixjZJk-0vpFu3-e2x8Q)

这是 **酒仙桥六号部队** 的第 **93** 篇文章。

全文共计2986个字，预计阅读时长11分钟。

  

**前言**

记在一次授权的渗透测试过程中遇到了这样一个项目，开始对前台一顿fuzz，端口一顿扫描也并没有发现什么可利用的漏洞，哪怕挖一个xss也行啊，但是xss也并没有挖掘到，实在不行挖一个信息泄露也好啊，果然让我挖掘到了一个信息泄露，get到了程序的指纹。

![](https://mmbiz.qpic.cn/mmbiz_png/WTOrX1w0s56uuc3jfc41nKarQvA7BApsNRVkqlusKQ9EggrmS55yYelMfCXg8waAdB9hAlSVlT77iaRN4L4icbSQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

Pbootcms是一套开源网站系统，然后百度了下该程序所爆出来的漏洞进行了测试，发现都失败了，猜测应该是程序升级到了较新版本，造成了网上爆出来的漏洞都被修复了。既然没有捷径可走，那还是只有老老实实去官网下载一份源码回来审计测试。

  

**源码审计**

#### 1.数据获取

通过对程序源代码的审查发现该程序封装了自己的数据获取助手函数：get(),post(),request()等，获取流程如下: 用post()函数举例说明：post(‘name’,’vars’)。

![](https://mmbiz.qpic.cn/mmbiz_png/WTOrX1w0s56uuc3jfc41nKarQvA7BApsIF3OjLKgWf07MaicMS28JhCOM91ewQTsMwTkYCpGoDticyoAqAo0WkxQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

可以看到将我们的传入的数据再次传入到了filter函数中：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

在filter函数中，会对获取到的数据进行一系列的强过滤，例如我们这里的 vars，就只能传递中文，字母，数字，点，逗号，空格这些字符。（PS: 因为不能传递括号“(,)”，所以sql注入中的函数都没办法使用，也就导致了什么报错注入，盲注啥的都不能使用，只有联合查询这种可以使用）接着函数在最后还经过了处理。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

跟进escape\_string函数：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

对数据还进行了htmlspecialchars，addslashes 双处理。

数据获取流程图所示：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

现在我们对该程序的数据获取已经有了初步的了解，主要的数据获取都是通过post(),get(),request()三大助手函数来实现的。

#### 2.注入挖掘

在审计的过程中发现程序存在较多的如下所示的代码：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

这里我将目光放在了DB类库中封装的where方法上，代码如下：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

如果此处传入的$where变量是一个索引数组，那么就会进入红框代码这里，并对值进行拼接。

明确目标之后，我们就可以开始搜索目标了：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

一番搜索下来发现，要不数据不可控，要不数据会通过escape\_string函数，并有单引号保护，达到过滤效果。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

**3.峰回路转**

通过多次对where，select，update等关键字的搜索，但是并没有获取到什么突破性的进展，然后又尝试了对$_GET,$_POST等原生态数据的搜索：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

在apps\\home\\controller\\ParserController.php文件中的parserSearchLabel方法中发现了问题：由于该方法代码较长，所以仅截图了关键部分。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

可以看到首先遍历了$\_POST数组，然后将键当做了$where数组的键。（这是关键），不过这里我们需要验证一下，键值为1，这个1是整型，还是字符串型，因为我们要控制输入的是索引数组。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

是int类型，完全符合我们上面的需求。

到这里也就是说这个$where3数组的键，值我们都可以控制了，不过$key：只能是/^\[\\w-.\]+$/这些内容。$value: 只能是/^\[\\x{4e00}-\\x{9fa5}\\w-.,\\s\]+$/u 这些内容。

接着继续往下看代码：  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

这里的$page为true，因为默认值是true，并且在中途的重新赋值过程中，我们没办法控制它，所以这里必定会执行getLists方法。

Getlists方法代码如下：代码较长，只截图了关键部分。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

成功的将我们传递的$where3数组传递到了where方法里面。

接着执行了一个page方法：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

这里设置了一个sql属性，后面会用到。

然后执行了最终的select方法。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

其中的buildsql方法就是结合我们之前设置的属性值来进行拼接成完整的sql语句。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

这里直接将我们前面通过链式操作where,order,page等方法设置的属性进行了替换拼接，又因为我们前面分析的在where方法中，如果传递进去的是一个索引数组的话，是没有单引号保护的，所以看到这里就差不多明白了我们成功逃逸了单引号的保护。

总体流程图如下所示：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

整个流程几乎已经走完了，测试效果如下：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

可以看到我们输入的aaaaaa已经成功带入到了sql语句中去执行，需要注意的是 我们输入内容是在小括号()里面的。

结合上面的request助手函数的过滤，我们知道输入的数据只能是指定字符：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

常规的报错注入是不能成功的，如：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

页面并没有像上面一样报错，而是返回了正常的页面，因为检测到了小括号，直接将我们的数据置为空值了。

#### 4.绕过注入

因为我们可控的点在where后面，where后面是可以接子查询的，如图：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

所以我们的绕过思路就是通过子查询的方式来进行操作，因为子查询是可以不使用括号的，如：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

我们的注入payload并没有被过滤，成功带入到了sql语句中去，但是因为不能使用括号，所以类似substring, mid等截断函数都不能使用，而且还不能使用=,<,>等一些比较符，怎么获取到准确数据又成了一个问题？

这里的突破目标就放在了对sql语句的变形上，首先就需要了解下sql的执行顺序。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

可以看到where的执行是在select之前的，那这怎么利用呢？如下：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

可以看到即使是select一个常量，如果后面的where条件不成立，也是不会查询到数据的，我们就可以利用where比select来对比出数据。

因为不能使用=,<,>等比较符，所以我们就需要找一个东西来代替它，并且因为不能使用substr等截取函数，所以就没办法一个一个的对比数据，就必须要找到一个可以让我们一个一个来对比的方式。

找到利用regexp来完美代替，因为regexp后面能接正则表达式，并且**.**能代表任意字符，**\***代表任意个数，那不就刚好符合我们的要求么，利用方式如下：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

将我们需要查询的字段放在where处，通过where返回的内容来控制select出来的数据。

（注意请使用^限定开头。如：^ad.\*）

因为数据不能使用引号，所以我们需要将引号内的数据进行16进制编码，效果是一样的。

控制了select返回的内容，达成的效果如下：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

Sql语句中，子查询先执行，并且在整个父类SELECT语句中我们子查询的结果处于where语句中，并且使用了AND连接，也就是说我们子查询的结果，同时也控制着整个sql语句的结果，那么就可以用来准确的判断数据了。

#### 5.本地测试payload

正确的页面显示：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

错误的页面显示：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

我们的真实数据：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

将我们的正则payload经过16进制编码然后带入执行，通过页面返回内容就可以判断我们的数据是多少了，最终达到了绕过过滤进行出数据的目的。

最终总体流程图可分三步，如图所示：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

测试结果证明我们的注入漏洞成功利用，接下来就是将payload映射到项目网站上去，经过大量的fuzz后成功得到管理员账号密码：

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

  

**后台Getshell**

漏洞文件：core\\function\\file.php

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

后缀白名单来自于handle\_upload函数的第三个参数，寻找调用handle\_upload函数的地方。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

后缀白名单来自于upload函数的第二个参数，搜索upload函数的调用处。

触发文件：apps\\home\\controller\\MemberController.php

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

继续跟进config方法。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

Config方法就是返回对应的配置项，配置项内容通过self::loadconfig()加载。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

配置项的一部分来至于md5(config).php文件，只要我们控制了这个文件中的home\_upload\_ext选项，也就控制了允许上传的后缀白名单了。

修改配置文件的地方。

文件：apps\\admin\\controller\\system\\ConfigController.php

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

将$\_POST遍历出来的键传递进了$this->moddbconfig方法。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

程序会首先将我们修改的配置内容更新到ay\_config数据表中去，然后再将数据表中的内容写入到md5(config).php文件中，造成我们可以添加任何类型的后缀文件。

#### Getshell利用

登录后台->全局配置->配置参数->立刻提交，使用burp抓包。

在POST数据中添加一个：home\_upload\_ext=php 字段即可。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

成功将其写入到文件。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

设置好了允许的上传白名单后，我们就可以通过上传php达到getshell了。

上传文件exp：upload.html

```
`<!DOCTYPE html>``<html lang="en">``<head>` `<meta charset="UTF-8">` `<title>pbootcms文件上传</title>``</head>``<body>``<form action="http://xxxxx/?member/upload" method="post" enctype="multipart/form-data">` `<input type="file" >` `<input type="submit" >``</form>``</body>``</html>`
```

将exp保存到html文件，修改对应的域名直接上传即可，文件上传证明。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

在本地将流程成功走了一遍后，利用到项目网站上也很顺利，直接就getshell了，成功交差，又可以愉快的喝冰阔乐了。

  

**总结**

整个流程从网站获取到指纹，然后找到源码审计，在审计过程中还是花费了较多时间，主要在前台审计的入口点寻找，和绕过过滤注入出数据，当时一度认为没办法利用，还好当时没放弃，然后慢慢一步一步的啃，终于还是啃下来了。  

  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)