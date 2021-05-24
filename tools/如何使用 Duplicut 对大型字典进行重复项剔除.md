> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/MjdQ19-p647vORt2-E3uSw)

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ib77P8Jzu2YGSH9kxlZj4icDeVEtXm0sFtnjhXQHY9Z2gVITRwic30NESvYhjWk9NGgrsfaxTaFLCxw/640?wx_fmt=jpeg)

概述
--

现代密码字典在创建过程中通常会连接多个数据源，在理想情况下，最有可能成功的密码一般都位于字典列表的开头部分，这样才能够确保密码在最短的时间里被破解成功。

使用现有的消除重复数据的工具，还必须通过排序的方法来实现，这样就没办法确保可能性最大的密码排在前列了。

很不幸的是，字典的创建通常要求满足下列条件：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ib77P8Jzu2YGSH9kxlZj4icDw9YJssua5L80R3pPwt0heUqdRYpCpdK7klQqlvzawLrAiaWt4yXWzBg/640?wx_fmt=jpeg)

Duplicut 这款工具可以帮助广大研究人员在不需要对字典密码排序的情况下，轻松剔除重复项，以实现更快速的基于字典的密码暴力破解。

功能介绍
----

> 处理大型字典，即使其大小超过了可用 RAM；
> 
> 通过定义最大长度过滤字典行（-l 选项）；
> 
> 能够移除包含了不可打印 ASCII 字符的字典行（-p 选项）；
> 
> 按下任意键即可显示程序运行时状态；

技术实现
----

> Duplicut 基于纯 C 语言开发，运行速度非常快；
> 
> 在 64 位平台上压缩 Hashmap；
> 
> 多线程支持；

限制条件
----

> 长度超过 255 个字符的字典行将被忽略；
> 
> 仅在 Linux x64 平台上进行了测试；

快速使用
----

```
git clone https://github.com/nil0x42/duplicut

cd duplicut/ && make

./duplicut wordlist.txt -o clean-wordlist.txt
```

功能选项
----

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ib77P8Jzu2YGSH9kxlZj4icDibBfVHn8U1HkIQSHkWn5tXpZpq1xSAq0Xh1LSc4ibT1DGSDb4mCPG2jw/640?wx_fmt=jpeg)

技术细节
----

### 内存优化

使用了 uni64 在 Hashmap 中实现快速索引：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ib77P8Jzu2YGSH9kxlZj4icDXxZGRQE4r4IgUib3x4AyKP9RZs2w0tVCSpK0DIUWxtHRxJJEUHbvfQA/640?wx_fmt=jpeg)

### 大型文件处理

如果整个文件超过了内存大小，则会被切割为多个虚拟数据块，并单独进行测试：

![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ib77P8Jzu2YGSH9kxlZj4icD50qnkeSBIyrUERaoguDAxvzjmZSAGqOC76zM7l1xZfIJFJ0iax5ib4dg/640?wx_fmt=jpeg)

问题处理
----

如果你发现程序运行过程中存在漏洞，或者报错的话，请在调试模式下编译 Duplicut 并查看输出：

```
# debug level can be from 1 to 4

make debug level=1

./duplicut [OPTIONS] 2>&1 | tee /tmp/duplicut-debug.log
```

项目地址：点击底部【阅读原文】获取  

![](https://mmbiz.qpic.cn/mmbiz_gif/qq5rfBadR38Tm7G07JF6t0KtSAuSbyWtgFA8ywcatrPPlURJ9sDvFMNwRT0vpKpQ14qrYwN2eibp43uDENdXxgg/640?wx_fmt=gif)

![](http://mmbiz.qpic.cn/mmbiz_png/3Uce810Z1ibJ71wq8iaokyw684qmZXrhOEkB72dq4AGTwHmHQHAcuZ7DLBvSlxGyEC1U21UMgSKOxDGicUBM7icWHQ/640?wx_fmt=png&wxfrom=200) 交易担保 FreeBuf+ FreeBuf + 小程序：把安全装进口袋 小程序

  

精彩推荐

  

  

  

  

****![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR3ib2xibAss1xbykgjtgKvut2LUribibnyiaBpicTkS10Asn4m4HgpknoH9icgqE0b0TVSGfGzs0q8sJfWiaFg/640?wx_fmt=jpeg)****

  

[![](https://mmbiz.qpic.cn/mmbiz_png/qq5rfBadR38seEkNn8TH7jZibkFTmoEsk6RKElsJrrsciaM7x32aqsPkBRK96QbqftgV9wWoG4HzVibedTiaZffTcg/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=MjM5NjA0NjgyMA==&mid=2651124157&idx=2&sn=f122abf33374d9bb2d105bb7afa93c74&chksm=bd1f63368a68ea20963d042cbc7e65e763a169b27f9cab26b3ce940603ac7fe8976260701a35&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_png/qq5rfBadR39dEsdO2GpOvH87GrfzuscAMuA4JpicWAFbJtfakgMF2hheeTcSSwguAbjO45btx8ws2etnvSJlOzQ/640?wx_fmt=png)](http://mp.weixin.qq.com/s?__biz=Mzg2MTAwNzg1Ng==&mid=2247486070&idx=1&sn=c6957ca2d1878f316b7947b5ff990a01&chksm=ce1cf0e9f96b79fff5b27a3c146f9e8828728c33625a97366b0cae3df1853dbeda368c59177f&scene=21#wechat_redirect)

[![](https://mmbiz.qpic.cn/mmbiz_jpg/qq5rfBadR39n5GEibfNkw4IJCQ3PU5W4hScYnG2TeOSgTVGYX9BZfoBX4cvliaEolz3gepYFfNvlFMYvibbmn0Rzg/640?wx_fmt=jpeg)](https://mp.weixin.qq.com/s?__biz=Mzg2MTAwNzg1Ng==&mid=2247486050&idx=1&sn=7e7d54cc1319f1dadfd36b4f92974c62&scene=21#wechat_redirect)

**************![](https://mmbiz.qpic.cn/mmbiz_gif/qq5rfBadR3icF8RMnJbsqatMibR6OicVrUDaz0fyxNtBDpPlLfibJZILzHQcwaKkb4ia57xAShIJfQ54HjOG1oPXBew/640?wx_fmt=gif)**************