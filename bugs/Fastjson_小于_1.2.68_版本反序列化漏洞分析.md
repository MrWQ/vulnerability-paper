\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/cb7\_\_ZWaBuyjFRCRv45SyQ)

前言
--

迟到的 Fastjson 反序列化漏洞分析，按照国际惯例这次依旧没有放 poc。道理还是那个道理，但利用方式多种多样。除了之前放出来用于文件读写的利用方式以外其实还可以用于 SSRF。

一、漏洞概述
------

在之前其他大佬文章中，我们可以看到的利用方式为通过清空指定文件向指定文件写入指定内容 (用到第三方库)。当 gadget 是继承的第一个类的子类的时候，满足攻击 fastjson 的条件。此时寻找到的需要 gadget 满足能利用期望类绕过 checkAutoType。

本文分析了一种利用反序列化指向 fastjson 自带类进行攻击利用，可实现文件读取、SSRF 攻击等。

二、调试分析
------

### 1\. 漏洞调试

从更新的补丁中可以看到 expectClass 类新增了三个方法分别为：

java.lang.Runnable、java.lang.Readable、java.lang.AutoCloseable

首先，parseObject 方法对传入的数据进行处理。通过词法解析得到类型名称，如果不是数字则开始 checkAutoType 检查。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39kNr3LcfnpjicOV6OWcjoP9VrcHAV6kaD6qZibyqp59z9adcr5u89PzfyiaUdFibAOOJzAxOicRPTeUYA/640?wx_fmt=jpeg)

当传入的数据不是数字的时候，默认设置期望类为空，进入 checkAutoType 进行检查传入的类。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39kNr3LcfnpjicOV6OWcjoP95FKS2p3BDeicBpib8NvBGynaKQicJYGHoEYaCuDujcPJJWefhbGzcVSqQ/640?wx_fmt=jpeg)

判断期望类，此时期望类为 null。往下走的代码中，autoCloseable 满足不在白名单内, 不在黑名单内，autoTypeSupport 没有开启，expectClassFlag 为 false。

其中：

A. 计算哈希值进行内部白名单校验

B. 计算哈希值进行黑名单校验

C. 非内部白名单且开启 autoTypeSupport 或者是期望类的，进行 hash 校验白名单 acceptHashCodes、黑名单 denyHashCodes。如果在 acceptHashCodes 内则进行加载 (defaultClassLoader), 在黑名单内则抛出 autoType is not support。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39kNr3LcfnpjicOV6OWcjoP9RzbvDegwSC5F4icAm4zVxSUSz3MFEfS1PCLhroicaMY4picJXibiaT4TGmQ/640?wx_fmt=jpeg)满足条件 C 后来到 clazz 的赋值，解析来的代码中对 clazz 进行了各种判断。

从明文缓存中取出 autoCloseable 赋值给 clazz。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39kNr3LcfnpjicOV6OWcjoP939bicqYOgaRqdYPqMCaibUe3r02JgkHzrjZ0ibV4Zl6IKsoliaVjnm96lg/640?wx_fmt=jpeg)![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39kNr3LcfnpjicOV6OWcjoP9WD66eFpdcPxHpMbxjZ6JeibH7maB43ictshh8Ary1IJjInBB1EIicalKA/640?wx_fmt=jpeg)当 clazz 不为空时，expectClassFlag 为空不满足条件，返回 clazz, 至此，第一次的 checkAutoType 检查完毕。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39kNr3LcfnpjicOV6OWcjoP98R434nqVzL6tFs7yKtu8JvCYicW7zHOdQjGbT1mqFUV7AibPAWFnBia9w/640?wx_fmt=jpeg)

将检查完毕的 autoCloseable 进行反序列化，该类使用的是 JavaBeanDeserializer 反序列化器，从 MapDeserializer 中继承。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39kNr3LcfnpjicOV6OWcjoP9EVUGICICUjTK2FNSUd9icmwkNgItgyE84nYVfRnedzjD4ValbJJPqQg/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39kNr3LcfnpjicOV6OWcjoP9TNMFgQyccPqfCD0j8acPaea9NjC6vSzAAibVQM7wMx8oayEWlxx0c0Q/640?wx_fmt=jpeg)

JSON.DEFAULT\_TYPE\_KEY 为 @type , 并给它赋值传入的 key @type , 将第二个类也就是这次 的 gadget 传入。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39kNr3LcfnpjicOV6OWcjoP9ZtBWGuM7D97iaaBjaYlMNEicSjVhmkJWqUYfHowRxpxwNnQQgWPJ04NQ/640?wx_fmt=jpeg)

期望类在这里发生了变化，expectClass 的值变为 java.lang.AutoCloseable，typeName 为 gadget，

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39kNr3LcfnpjicOV6OWcjoP9uhrUgBmtVcW4Z69cicvPMuKBZ3MvZKJvKRseic2KoibJyImYKUIP3Xgvw/640?wx_fmt=jpeg)

来到 JSONType 注解，取 typename gadget 转换变为路径，resource 通过将 “.” 替换为”/“得到路径 。其实已经开始读取 gadget 了，它本意应该是加载 AutoCloseable。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39kNr3LcfnpjicOV6OWcjoP9DscnXfXibcPibDzfLh4BwlnLbbfCxA4LBEVJN2GZ8bkbCAEaaSRnS4pg/640?wx_fmt=jpeg)

可以看到这里有读取文件的功能。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39kNr3LcfnpjicOV6OWcjoP9n4Lp1clsWQiarZE7x80ZtOypQYKGEehdPBiasmMORXc8fibT80GslAKdQ/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39kNr3LcfnpjicOV6OWcjoP9eKhnJ3XHdhKG8MDfnfibKic2ZoQlia2FIyq7BxuIMT7Nft0hpEWiaCPP8Q/640?wx_fmt=jpeg)

isAssignableFrom() 这个方法用于判断里面的类是否为继承类，当利用了 java.lang.AutoCloseable 这个方法去攻击 fastjson，那么后续反序列化的链路一定是要继承于该类的子类。

TypeUtils.addMapping(typeName, clazz) 这一步成功把 gadget 加入缓存中并返回被赋值 gadget 的 clazz.

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39kNr3LcfnpjicOV6OWcjoP9rZaf6ic8LOaMIA3bzXEwm1pBjGrUgEorEBic6LvBGvs7ITVhWWjATKrA/640?wx_fmt=jpeg)checkAutoType 正式检查完毕，此时用 deserializer = parser.getConfig().getDeserializer(userType); userType 既 gadget 进行反序列化。

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39kNr3LcfnpjicOV6OWcjoP9eiavgMr4m8FKLLUoXqXX2myXSthCl2ZNM1THcgwiba6fLhibwDVnLiaycg/640?wx_fmt=jpeg)

进入 coreConnect()

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39kNr3LcfnpjicOV6OWcjoP9cicia0vAJV7w2mmqicyPx1jebKp5ia7WtPw1icqnfp8zyHdFjsqRo65Dx5g/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39kNr3LcfnpjicOV6OWcjoP9LDnd7tyfpHkACRkWIqGI3lWgJcLiab6hlV7G71xCW7HYUGt7OicL19ng/640?wx_fmt=jpeg)

在这里进行连接。至此漏洞利用完结。

### 2\. 总结：

在本次反序列化漏洞中，笔者认为关键点在于找到合适并且可利用的常用 jar 包中的 gadget。gadget 在被反序列化后即可执行类里的恶意的功能 (不仅限于 RCE 还包括任意文件读取 / 创建, SSRF 等)。也可以使本漏洞得到最大化的利用。

三、参考考链接
-------

> https://b1ue.cn/archives/348.html
> 
> https://daybr4ak.github.io/2020/07/20/fastjson%201.6.68%20autotype%20bypass/

![](https://mmbiz.qpic.cn/mmbiz_gif/qq5rfBadR38Tm7G07JF6t0KtSAuSbyWtgFA8ywcatrPPlURJ9sDvFMNwRT0vpKpQ14qrYwN2eibp43uDENdXxgg/640?wx_fmt=gif)

![](http://mmbiz.qpic.cn/mmbiz_png/3Uce810Z1ibJ71wq8iaokyw684qmZXrhOEkB72dq4AGTwHmHQHAcuZ7DLBvSlxGyEC1U21UMgSKOxDGicUBM7icWHQ/640?wx_fmt=png&wxfrom=200) 交易担保 FreeBuf+ FreeBuf + 小程序：把安全装进口袋 小程序

精彩推荐

  

  

  

  

****![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ib2xibAss1xbykgjtgKvut2LUribibnyiaBpicTkS10Asn4m4HgpknoH9icgqE0b0TVSGfGzs0q8sJfWiaFg/640?wx_fmt=jpeg)****

[![](https://mmbiz.qpic.cn/mmbiz_png/qq5rfBadR3icpSmNbdiaVpmTEfDHJFoS2OIO0ibau3Xo0W3W5icSIT9hIQY4gmlK4nOY8jcVq2hngIe7Fug8w6lHyQ/640?wx_fmt=png)](https://mp.weixin.qq.com/s?__biz=Mzg2MTAwNzg1Ng==&mid=2247484287&idx=1&sn=16a9b2dc0e205a0e5fe86ae5cae9fe2e&scene=21#wechat_redirect)[![](https://mmbiz.qpic.cn/mmbiz_png/qq5rfBadR39823fgk2Py1fbU5wCoewwO0AKFIGmCLF6bY37GDicGMDRicgQf6xW1jtjY8Raby8RjiauX5205Zg8Dg/640?wx_fmt=png)](https://mp.weixin.qq.com/s?__biz=Mzg2MTAwNzg1Ng==&mid=2247484370&idx=1&sn=8b79701a2936e04e390f165344e5fcdc&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/qq5rfBadR3ibrCNytjecubJy4a2EMQHuiaJseib0icuF3QialdBMY21aib2icNEy1uiblZrnHFVLD9De6kTz9icls4NSn9g/640?wx_fmt=png)](https://mp.weixin.qq.com/s?__biz=Mzg2MTAwNzg1Ng==&mid=2247484890&idx=1&sn=a35949908769038c4fa7004f0618d485&scene=21#wechat_redirect)[![](https://mmbiz.qpic.cn/mmbiz_png/qq5rfBadR38XdBNjyyYJQx29A4xTU2rFxaQEpccgZTXv5ku4FnoF7NwItEIsia7NxGibWQopRhWtEsIfnLduv17g/640?wx_fmt=png)](https://mp.weixin.qq.com/s?__biz=Mzg2MTAwNzg1Ng==&mid=2247484700&idx=1&sn=73e33756f2fe0b8ea7041b310bb74d00&scene=21#wechat_redirect)[![](https://mmbiz.qpic.cn/mmbiz_png/qq5rfBadR3ibjR7ZXs1HYUB8M7n0R8KOBj92Aia1FRhRV2ag4cnYRyJu2qibEAVt4iaibWrLpzxUZojenQvycBicSYhw/640?wx_fmt=png)](https://mp.weixin.qq.com/s?__biz=Mzg2MTAwNzg1Ng==&mid=2247484688&idx=1&sn=cfd5efde08add1e69709773e0b8c87cf&scene=21#wechat_redirect)

**************![](https://mmbiz.qpic.cn/mmbiz_gif/qq5rfBadR3icF8RMnJbsqatMibR6OicVrUDaz0fyxNtBDpPlLfibJZILzHQcwaKkb4ia57xAShIJfQ54HjOG1oPXBew/640?wx_fmt=gif)**************