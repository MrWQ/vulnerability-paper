> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzI5MDE0MjQ1NQ==&mid=2247506886&idx=1&sn=150341f365dcce8a36b108f8b7f9a4e5&chksm=ec26fa5edb51734813850d9b2cac7b93661bcc01eef11645303badc0d7af534043bf4624be3a&mpshare=1&scene=1&srcid=0104d98zzzzdZ7xQ0HmGSQWS&sharer_sharetime=1609721547996&sharer_shareid=c051b65ce1b8b68c6869c6345bc45da1&key=aa37eea3a2616ab37d9e2251c224671ed8053aabfaa78bc3bc02ae425b6d0aa135dc6c2c1bb2e6b201e6c4215046eee101b91e121266c46d8b0a2780b4bdbd002ce2bcb4da26d1f465b9d79a33b11cbea314ac22a4f2c82e8458cda2fe8998e2901c3ca7d82260d04a99ef8fba37881e6f61c8e56ba5beed90d6547f24d3d3f1&ascene=1&uin=ODk4MDE0MDEy&devicetype=Windows+10+x64&version=63010029&lang=zh_CN&exportkey=AWJHYgoxGrjSLpJfkHPEKxg%3D&pass_ticket=yy556pu%2Bp4W4mbvK7Q3O6PIbolc7ebdCh%2F3poyqaL0RGTca9FUoYwlT9SUXPGlGT&wx_header=0&fontgear=2)

总结一下关于 php（拍 h 片）弱类型相关知识的梳理。  

![](https://mmbiz.qpic.cn/mmbiz_jpg/RXib24CCXQ0944wO6ibwauQwWakk0qNJf7FlQ1yykQ8rKrT8HKDy14eWlFdykcUzA6GWkM7CIPN6Y1NdeMXiaUmcQ/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_png/T5oTIrKiajIHJRr18iczX1Npb4iblBSBIgfRibnCQNEiccibqzGqsqEmpr4jaZpqLhaytialPP3AOBzkv9aSe3poXdibJA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/CvOqicPgTH0307aOFI1SickLEjaqCJwsvicPlYR2PJjjsYhhbRibVZN8pP7THGvofuKCjicibBgnaDYBSsBLgAFicPpGg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rEu21icic9rbZBXknnicnbOZntUS297gYoHt3I8tS6OQAZZoADXIJPCQYeuS8TeYKlyR1eajrfD8Pw9sBtWv5fH0A/640?wx_fmt=png)

前言

![](https://mmbiz.qpic.cn/mmbiz_png/P30WKINsw4Kd67h3Ogicicib3FBs6jviaiaGsUDID5jDcevIZWlDrvmATgEiaPqPMcpttJBQzXzkNXuOXYl2zXwXFs7w/640?wx_fmt=png)

php 有八种类型

标量类型：整数型 integer, 浮点型 float, 字符串类型 string, 布尔类型 boolen

复合类型：对象 object, 数组 array

特殊类型：空 null, 资源 resource

我们要知道 php 是一种弱类型的语言, 它不同于 C/Go/java 等。

那么首先, 说一下 php 中两个比较符号。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0944wO6ibwauQwWakk0qNJf7mXScUfFMNq6vbjdiatfJqqHfKpFfVORn2iaQO40cBNaYtBUdicnYkFJJA/640?wx_fmt=png)

在这里要说明一下,== 在这里是判断两边的值是否相等, 等号两边为相同的值的时候, 直接判断值是否相等, 如果**类型不一样, 则先转换为相同的类型**, 再判断转换后的值是否相等。

(**若是等号两边是数值和字符串比较, 则字符串会转换为数值, 字符串转为数值这里很有意思了, 大家可以用 var_dump 去尝试一下不同的类型转换)**

(**比如像这样多尝试尝试**)

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0944wO6ibwauQwWakk0qNJf74Mtho14L9bbzosyVtcUiaaZ49QuMZhmO6vvaibWErG28GMF0HweMWicMA/640?wx_fmt=png)

其中为什么第 11 行为 true 呢, 这里是 php 中的 hash 缺陷, 如果 hash 值是以 0e 开头的, 进行比较时候会变成 0 乘以 10 的多少次方, 结果还是为 0

(ps：**如果 MD5 运算后为 0e 开头的字符串, 是不是可以绕过强制 (string) 转换后的 MD5 比较呢**)

**提醒**：0,"0",null,false,array() 都是为空。

===, 则是判断的是否全等, 不仅要值相等, 而且类型也要一致。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0944wO6ibwauQwWakk0qNJf7J0wPKR7VVlTZVicNrr7iaHic9iajHAWcfDTwPGtk51876O3vBcBocN7MzA/640?wx_fmt=png)

而在有些语言中 (比如 Go), 要比较的两个变量类型须相等并且 Go 没有隐式类型转换, 要比较的两个变量必须类型完全一样, 类型别名都也不行。

这里便可以先从一个简单的题目入手 (**题目来自攻防世界**)。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0944wO6ibwauQwWakk0qNJf7xCZst1PLXFnt03wEENhlE5cWkzZicD1G12HqzCqAzpJ2icJ9zfsia8ZNQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/T5oTIrKiajIHJRr18iczX1Npb4iblBSBIgfRibnCQNEiccibqzGqsqEmpr4jaZpqLhaytialPP3AOBzkv9aSe3poXdibJA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/CvOqicPgTH0307aOFI1SickLEjaqCJwsvicPlYR2PJjjsYhhbRibVZN8pP7THGvofuKCjicibBgnaDYBSsBLgAFicPpGg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rEu21icic9rbZBXknnicnbOZntUS297gYoHt3I8tS6OQAZZoADXIJPCQYeuS8TeYKlyR1eajrfD8Pw9sBtWv5fH0A/640?wx_fmt=png)

**is_numeric()** 函数

用于检测变量是否为数字或数字字符串（感觉说明这个函数, 大家就没有生词了）。  

然后就是一个很简单的弱类型比较了, 大家随便输一下符合两个逻辑的就行了。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0944wO6ibwauQwWakk0qNJf7E9SgIbCrLNabpia1X2bribsEnl6eYjDVF64FPDgJJetRksM3AjkbdtJw/640?wx_fmt=png)

有了这些准备以后, 我们可以进阶的再看一个题目（**题目来自于 BUUCTF**）。

我们迈过第一关以后会看到这个页面,F12 得到了提示。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0944wO6ibwauQwWakk0qNJf7zA0CH6ViaHvdPDkJswvriany3IDArfUkydbdlLBAhAMShSmQicUQmI1Fw/640?wx_fmt=png)

```
$a = $GET['a'];
$b = $_GET['b'];
if($a != $b && md5($a) == md5($b)){
// wow, glzjin wants a girl friend.
```

![](https://mmbiz.qpic.cn/mmbiz_png/165jdibJnGcUAxqeh4b1mTZjIzBhOXg6t5AmDhsbbz9lACibgYGLvRc1EUqxXTUGePTNRouZsJrbwUdYGD4TdOWw/640?wx_fmt=png)

知识补充

```
md5( string $str   [, bool $raw_output = false  ] ) : string
```

计算字符串的 MD5 散列值,md5 函数告诉我们我们传入的参数应该是 string 类型的, 但如果我们传入一个数组, 它不会报错, 也不会解析其值, 导致两个数组的中无论什么值 MD5 都相同 (出同样的错误是不是也是一样的呢)。  

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0944wO6ibwauQwWakk0qNJf7icYIFJVOD8GVTrdibH23ichicdtTBwz8CNkyLeA57v7e3urLWVWpTtBgnw/640?wx_fmt=png)

然后我们便可以传入两个数组来进行绕过了。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0944wO6ibwauQwWakk0qNJf78gFQLbY0sibbmdFOFibJgWdxD6C7jXKibBF55NcibfUyc3HiaeUKTKkiaR2w/640?wx_fmt=png)

到了第三关, 便和第二关大同小异了。

如果我们遇到强制类型转换比如再传参的参数前面有一个（string）类型转换, 那怎么办, 那边要用的 MD5 强碰撞了（记得以前看过一个 cissp 的题目讲的也是碰撞出 MD5, 也解释 MD5 的不安全性）。

这里我们大多可能要用一下工具（**fastcoll**）

讲完了 MD5 我们再将另一个,sha(**题目来自于 bugku,web29 各种绕过**)。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0944wO6ibwauQwWakk0qNJf7UicZWjq06Zknp6wxia7IeicUegwibKGtSflXktsFSKRQJNAjxTeuEKmnaw/640?wx_fmt=png)

  

  

  

![](https://mmbiz.qpic.cn/mmbiz_png/165jdibJnGcUAxqeh4b1mTZjIzBhOXg6t5AmDhsbbz9lACibgYGLvRc1EUqxXTUGePTNRouZsJrbwUdYGD4TdOWw/640?wx_fmt=png)

知识补充

```
sha1( string $str   [, bool $raw_output = false  ] ) : string
```

——计算字符串的 sha1 散列值, 测试 sha1() 函数和 md5() 函数 "殊途同归"。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0944wO6ibwauQwWakk0qNJf7fuDwXc56gH6MMXna8Z7dibHc2am2dRiaA3keL59v0Mq0Diaa18qTgwmfg/640?wx_fmt=png)

这里还有很多可以利用的函数, 比如 json_decode() {传入 json 形式的数据, 类 Python 中的字典}, 不可否认的是任何函数的绕过都需要相关的逻辑判断。

{**json_decode() 把接送格式的字符串解码成了数组, 而通过相应的逻辑判断我们便可的绕过**}

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0944wO6ibwauQwWakk0qNJf7PoyQDlBF1LgY49Sd0F7Zic5ayMnAf9boJoCrjdpibEeFVBNx4ak4wIxQ/640?wx_fmt=png)

下面我们会介绍与弱类型相呼应的 php 函数。

  

![](https://mmbiz.qpic.cn/mmbiz_png/T5oTIrKiajIHJRr18iczX1Npb4iblBSBIgfRibnCQNEiccibqzGqsqEmpr4jaZpqLhaytialPP3AOBzkv9aSe3poXdibJA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/CvOqicPgTH0307aOFI1SickLEjaqCJwsvicPlYR2PJjjsYhhbRibVZN8pP7THGvofuKCjicibBgnaDYBSsBLgAFicPpGg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rEu21icic9rbZBXknnicnbOZntUS297gYoHt3I8tS6OQAZZoADXIJPCQYeuS8TeYKlyR1eajrfD8Pw9sBtWv5fH0A/640?wx_fmt=png)

unserialize 函数问题

![](https://mmbiz.qpic.cn/mmbiz_png/165jdibJnGcUAxqeh4b1mTZjIzBhOXg6t5AmDhsbbz9lACibgYGLvRc1EUqxXTUGePTNRouZsJrbwUdYGD4TdOWw/640?wx_fmt=png)

知识补充

对单一的已序列化的变量进行操作, 将其转换回 PHP 的值。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0944wO6ibwauQwWakk0qNJf7eUhn69xXAx4NwCA4KRDv71fcn9NTTvMj8ZPnCzwHTHxr4IkkeYxiauQ/640?wx_fmt=png)

key 和 value 是我们可以通过 POST 数据传入的值, 我们把它传入 bool 值, unserialize 函数解析为了数组, 下面又因为使用的是 ==, 根据 php 弱类型, bool 值跟任何字符串都相等。

故判断成立输出了 OK。

![](https://mmbiz.qpic.cn/mmbiz_png/T5oTIrKiajIHJRr18iczX1Npb4iblBSBIgfRibnCQNEiccibqzGqsqEmpr4jaZpqLhaytialPP3AOBzkv9aSe3poXdibJA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/CvOqicPgTH0307aOFI1SickLEjaqCJwsvicPlYR2PJjjsYhhbRibVZN8pP7THGvofuKCjicibBgnaDYBSsBLgAFicPpGg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rEu21icic9rbZBXknnicnbOZntUS297gYoHt3I8tS6OQAZZoADXIJPCQYeuS8TeYKlyR1eajrfD8Pw9sBtWv5fH0A/640?wx_fmt=png)

strpos 函数问题

![](https://mmbiz.qpic.cn/mmbiz_png/165jdibJnGcUAxqeh4b1mTZjIzBhOXg6t5AmDhsbbz9lACibgYGLvRc1EUqxXTUGePTNRouZsJrbwUdYGD4TdOWw/640?wx_fmt=png)

知识补充

```
strpos ( string $haystack , mixed $needle [, int $offset = 0 ] ) : int
```

返回 needle 在 haystack 中首次出现的数字位置。

**![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0944wO6ibwauQwWakk0qNJf7CamF8B4KsYFaGeia7yltoXR9IemcGapZia5ickH8bjkdWIEl7PutdEMCw/640?wx_fmt=png)**

问题的出现依然是出现了 0=="admin" 的弱类型比较的问题。

![](https://mmbiz.qpic.cn/mmbiz_png/T5oTIrKiajIHJRr18iczX1Npb4iblBSBIgfRibnCQNEiccibqzGqsqEmpr4jaZpqLhaytialPP3AOBzkv9aSe3poXdibJA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/CvOqicPgTH0307aOFI1SickLEjaqCJwsvicPlYR2PJjjsYhhbRibVZN8pP7THGvofuKCjicibBgnaDYBSsBLgAFicPpGg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rEu21icic9rbZBXknnicnbOZntUS297gYoHt3I8tS6OQAZZoADXIJPCQYeuS8TeYKlyR1eajrfD8Pw9sBtWv5fH0A/640?wx_fmt=png)

php 中的哲学问题

![](https://mmbiz.qpic.cn/mmbiz_jpg/RXib24CCXQ0944wO6ibwauQwWakk0qNJf75fH1D4JpTpFMKoEHKm7XnvZOIWz9eUIC4C6jq48FKj9JReoc7kdM8A/640?wx_fmt=jpeg)

（代码中还有哲学问题？）

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0944wO6ibwauQwWakk0qNJf7X6HS0ys4Rl1piaqnycLmKtVUBZRGkkk7R9gO2lppnONwn5MroUI9tPQ/640?wx_fmt=png)

因为以前老师问过我们这个问题, 为什么呢, 用一句模糊的话来说 "无限接近就是相等"。

![](https://mmbiz.qpic.cn/mmbiz_png/T5oTIrKiajIHJRr18iczX1Npb4iblBSBIgfRibnCQNEiccibqzGqsqEmpr4jaZpqLhaytialPP3AOBzkv9aSe3poXdibJA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/CvOqicPgTH0307aOFI1SickLEjaqCJwsvicPlYR2PJjjsYhhbRibVZN8pP7THGvofuKCjicibBgnaDYBSsBLgAFicPpGg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rEu21icic9rbZBXknnicnbOZntUS297gYoHt3I8tS6OQAZZoADXIJPCQYeuS8TeYKlyR1eajrfD8Pw9sBtWv5fH0A/640?wx_fmt=png)

in_array() 函数问题

![](https://mmbiz.qpic.cn/mmbiz_png/165jdibJnGcUAxqeh4b1mTZjIzBhOXg6t5AmDhsbbz9lACibgYGLvRc1EUqxXTUGePTNRouZsJrbwUdYGD4TdOWw/640?wx_fmt=png)

知识补充

```
in_array( mixed $needle     , array $haystack   [, bool $strict = false    ] ) : bool
```

— 检查数组中是否存在某个值, 若第三个参数 strict 为默认的 false, 则使用松散比较。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0944wO6ibwauQwWakk0qNJf7nMyEEwdYGV4KNRC4ThzFicibicmfjBXib8BWIL8L5ceZGcPVicmgUb66wsA/640?wx_fmt=png)

这是便我们尝试对比的结果了。

相关题目 (php 审计题目)：

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0944wO6ibwauQwWakk0qNJf7adibOduz0X6MTcCpuQYibKicKtjvqxHmWCcT3kUMTRdnvm3tyFmEtPZUw/640?wx_fmt=png)

首先我们发现 in_array() 并没有使用第三个参数, 所以为默认值, 可以进行松散比较。我们只要再 *.php 前面加上一个在 range(1,24), 比如 23a.php。

![](https://mmbiz.qpic.cn/mmbiz_png/T5oTIrKiajIHJRr18iczX1Npb4iblBSBIgfRibnCQNEiccibqzGqsqEmpr4jaZpqLhaytialPP3AOBzkv9aSe3poXdibJA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/CvOqicPgTH0307aOFI1SickLEjaqCJwsvicPlYR2PJjjsYhhbRibVZN8pP7THGvofuKCjicibBgnaDYBSsBLgAFicPpGg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rEu21icic9rbZBXknnicnbOZntUS297gYoHt3I8tS6OQAZZoADXIJPCQYeuS8TeYKlyR1eajrfD8Pw9sBtWv5fH0A/640?wx_fmt=png)

array_search() 问题

```
array_search ( mixed $needle , array $haystack [, bool $strict = false ] ) : mixed
```

— 在数组中搜索给定的值, 如果成功则返回首个相应的键名, 与 in_array() 函数类似。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0944wO6ibwauQwWakk0qNJf7Grsp3ekLXpatKBGo7rIsHt8UPyOnbduH3gYoacV5SKicZL75QhP6b5Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/T5oTIrKiajIHJRr18iczX1Npb4iblBSBIgfRibnCQNEiccibqzGqsqEmpr4jaZpqLhaytialPP3AOBzkv9aSe3poXdibJA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/CvOqicPgTH0307aOFI1SickLEjaqCJwsvicPlYR2PJjjsYhhbRibVZN8pP7THGvofuKCjicibBgnaDYBSsBLgAFicPpGg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rEu21icic9rbZBXknnicnbOZntUS297gYoHt3I8tS6OQAZZoADXIJPCQYeuS8TeYKlyR1eajrfD8Pw9sBtWv5fH0A/640?wx_fmt=png)

strcmp() 函数问题

![](https://mmbiz.qpic.cn/mmbiz_png/165jdibJnGcUAxqeh4b1mTZjIzBhOXg6t5AmDhsbbz9lACibgYGLvRc1EUqxXTUGePTNRouZsJrbwUdYGD4TdOWw/640?wx_fmt=png)

知识补充

比较两个字符串（区分大小写）

```
strcmp(string1,string2)
```

![](https://mmbiz.qpic.cn/mmbiz_png/P30WKINsw4Kd67h3Ogicicib3FBs6jviaiaGsUDID5jDcevIZWlDrvmATgEiaPqPMcpttJBQzXzkNXuOXYl2zXwXFs7w/640?wx_fmt=png)

返回值：

• 0 - 如果两个字符串相等

• <0 - 如果 string1 小于 string2

• >0 - 如果 string1 大于 string2

测试缺陷的方法和 MD5 函数类似, 我们不给予这个函数 string 类型, 而是给它 array 类型的值。

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0944wO6ibwauQwWakk0qNJf797xapiadDHOF04zy3XWRka1pNvXucJm29v341vFZMBEsic5gEoLMMHVw/640?wx_fmt=png)

发现它依然是给出警告, 但依然判断为 ture, 打印出了 ok。（**题目来自南京邮电大学网络攻防训练平台 - pass check**）

```
<?php
$pass=@$_POST['pass'];
$pass1=***********;//被隐藏起来的密码
if(isset($pass))
{
if(@!strcmp($pass,$pass1)){
echo "flag:nctf{*}";
}else{
echo "the pass is wrong!";
}
}else{
echo "please input pass!";
}
?>




/*
wp:
<?php
$k[]=1;
var_dump(!strcmp($k, "flag"));
printf("\n");
?>
*/
```

![](https://mmbiz.qpic.cn/mmbiz_jpg/RXib24CCXQ0944wO6ibwauQwWakk0qNJf74ngEvRUGibB5NXIRcM8niatIiaBS41Q3IXUBK8Ta0xYgP5dEIdoia8ddMA/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_png/T5oTIrKiajIHJRr18iczX1Npb4iblBSBIgfRibnCQNEiccibqzGqsqEmpr4jaZpqLhaytialPP3AOBzkv9aSe3poXdibJA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/CvOqicPgTH0307aOFI1SickLEjaqCJwsvicPlYR2PJjjsYhhbRibVZN8pP7THGvofuKCjicibBgnaDYBSsBLgAFicPpGg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/rEu21icic9rbZBXknnicnbOZntUS297gYoHt3I8tS6OQAZZoADXIJPCQYeuS8TeYKlyR1eajrfD8Pw9sBtWv5fH0A/640?wx_fmt=png)

switch 相关的问题

如果 switch 的 case 是数字类型的判断的时候。switch 会将参数转换为 int 类型。  

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0944wO6ibwauQwWakk0qNJf73DCpyicNXicjgMpqvy94Nm2Eyj5yjgI3wssuDwOfA9HibicSXFpul4v7Gw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_jpg/RXib24CCXQ0944wO6ibwauQwWakk0qNJf7VibeTJodc3g7XwnDoHWrAdYxWOVIdHLCTpovbibCdiazUnc9ibq1RmcmKA/640?wx_fmt=jpeg)

不要慌张，继续加油哈。  

end

  

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0icgJnwz55vaCiatpsqriaW2GZ7rRw3kbvpDFicsKcLcp9Q7tYiaMwLANvcHAoByTiaGaus4HBukgfIXt9g/640?wx_fmt=png)