\> 本文由 \[简悦 SimpRead\](http://ksria.com/simpread/) 转码， 原文地址 \[mp.weixin.qq.com\](https://mp.weixin.qq.com/s/dmFoMJaUH\_ULnhu\_T9jSGA)

简单测试

**1.1、环境搭建**

**测试环境：**

在官⽹下载好源码包，解压后访问 upload ⽬录，根据提示安装好测试环境，即可进⼊后台⻚⾯

![](https://mmbiz.qpic.cn/mmbiz_jpg/RXib24CCXQ0icxuI7kLVuBdDLdfYB2fE54BX81nZiabeOmZuanEicGutERYdkFPAicVkBcllgFBFbHKm070ibMWXaG2w/640?wx_fmt=jpeg)

**1.2、测试 XSS**

后台可以新增内容，先试试增加⼀篇⽂章，这⾥框写的是 <script>alert(1)</script>

![](https://mmbiz.qpic.cn/mmbiz_jpg/RXib24CCXQ0icxuI7kLVuBdDLdfYB2fE54Rtvrdo69CA20QKGs09IXepDf3zoeXpr8glUXsZSqAEAeaufSLic3ciag/640?wx_fmt=jpeg)

然后发现⻚⾯⾃动跳转到了⽂章列表⻚，并弹出 1

![](https://mmbiz.qpic.cn/mmbiz_jpg/RXib24CCXQ0icxuI7kLVuBdDLdfYB2fE5452khXic1h4TltIL9giaBZ68oheBAchb8RHh5bplBgicFwmKDAnavo1jzA/640?wx_fmt=jpeg)

打开前台⻚⾯，发现也有弹框 1，是⼀个存储型的 XSS 漏洞

![](https://mmbiz.qpic.cn/mmbiz_jpg/RXib24CCXQ0icxuI7kLVuBdDLdfYB2fE5419HOvU6uO1iaGTpnqBSbJqgRHiaE4goBS3USkJ85Vib7TIsGpmzPPJzHQ/640?wx_fmt=jpeg)

源码分析

**2.1、如何保存到数据库**

使⽤ Seay 代码审计系统对⽹站源码进⾏⾃动审计，通过软件提供的 Mysql 监控功能，发现新建 这篇⽂章时，执⾏的 SQL 语句，除了⽂章描述部分的 <> 被转化成了实体字符，其他如 title 处的 < script>alert(1)</script > 都被完整插⼊数据库中

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0icxuI7kLVuBdDLdfYB2fE540UvmSrBMSuQLuMlGzQUtCeQBj5ntt3JT8RKJIqrxf9RHAicYNgpYpHw/640?wx_fmt=png)

查看 admin/article.php 源码进⾏分析，看起来似乎代码并没有对 $\_POST 传递的值进⾏过滤

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0icxuI7kLVuBdDLdfYB2fE54I4r1PkAn51s9eNRS8XINr2JGkgqOPfcrSuGn2iaqaicyRjKaSDdd0knQ/640?wx_fmt=png)

实际上，admin/article.php 在最开始引⼊了 / inculde/init .php ⽂件

![](https://mmbiz.qpic.cn/mmbiz_jpg/RXib24CCXQ0icxuI7kLVuBdDLdfYB2fE54tsmjdqXwD3rDjeYichRfpz8InHxmZOiaE8gNMkibo6eG8hy2TVIhZjOBA/640?wx_fmt=jpeg)

⽽在 admin/inculde/init .php ⽂件中，实例化了 Check() 与 Firewall 这两个类，调⽤了 dou\_ﬁrewall() ⽅法

![](https://mmbiz.qpic.cn/mmbiz_jpg/RXib24CCXQ0icxuI7kLVuBdDLdfYB2fE54D1EZT4n0h1WYuntb5TNAdNibQhPjyJuWqicn6hAhhd1xianSZO29plic6Q/640?wx_fmt=jpeg)

这两个类是通过 include/check.class.php 与 include/ﬁrewall.class.php 这两个⽂件来引⼊，数据的过滤⽅法就在这⾥。

![](https://mmbiz.qpic.cn/mmbiz_jpg/RXib24CCXQ0icxuI7kLVuBdDLdfYB2fE54TFibaTicFuFibdiamgKIEyjImyKH5aSRC2WkrVpSrG4L7KfaXCXcBaMdmQ/640?wx_fmt=jpeg)

其中，include/check.class.php ⽂件的 is\_number ⽅法，使⽤正则对参数进⾏了过滤，确保传递的 参数是数字

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0icxuI7kLVuBdDLdfYB2fE542biaLH0nhAxFJdGnTXIjHTLcE9vXPqbwNPHibicl87KPokVOGkzHOt5lg/640?wx_fmt=png)

在 admin/article.php 中调⽤了该⽅法，确保 cat \_id 参数是数字

![](https://mmbiz.qpic.cn/mmbiz_jpg/RXib24CCXQ0icxuI7kLVuBdDLdfYB2fE541ibZMIlIjouI39enZ81iaHqXMxmhicIMQ7YLBrQAgPgQHbJeNSYBeS5SA/640?wx_fmt=jpeg)

include/ﬁrewall.class.php 这个⽂件中，dou\_ﬁrewall() 调⽤了 dou\_magic\_quot es() ⽅法

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0icxuI7kLVuBdDLdfYB2fE544cBQUuwOZcicxlU8oAUKic1iaDXwWxPfAL2WZpPF05DRwDJNbUoWOIMicQ/640?wx_fmt=png)

dou\_magic\_quotes() ⽅法的作⽤，是在 magic\_quotes\_gpc 没有开启时，调⽤ addslashes\_deep() ⽅法

![](https://mmbiz.qpic.cn/mmbiz_jpg/RXib24CCXQ0icxuI7kLVuBdDLdfYB2fE54X78MEiaHxud7Ls2UzoGAW9tAgCeyuHGyLRDMwz1T48ibVjG8r8AHSGyw/640?wx_fmt=jpeg)

addslashes\_deep()⽅法的作⽤，是通过递归的⽅式，利⽤ addslashes()函数对' " \\ 等特殊字符进⾏转义，问题应该就是出在这⾥，函数并未对 <>/() 这些特殊字符进⾏转义，导致

<script>alert(1)</script > 被完整保存到数据库中

![](https://mmbiz.qpic.cn/mmbiz_jpg/RXib24CCXQ0icxuI7kLVuBdDLdfYB2fE54QQiafssk51lQTnF5mFnfvMLtk1fc17ROyoXuSoBgia2YGPpEDAZwhMYQ/640?wx_fmt=jpeg)

**2.2、如何调⽤数据**

点击⽂章列表时会弹窗，回头再看 admin/article.php 中的⽂章列表模块源码，将 $row\['title'\] 赋值给 "title"，未过滤

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0icxuI7kLVuBdDLdfYB2fE54ianyMOzDoldCUAQria8XlRHLC03aKJT0RibzoIqBzsxWKmNdMsJGibZR1g/640?wx_fmt=png)

通过实例化的对象 $smarty 来调⽤调⽤ assign ⽅法，未过滤

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0icxuI7kLVuBdDLdfYB2fE54UdcdribxvKCV0SWicrwt7qQhEibI6pDBZ6xP2GZbm76azjz6gdKWvYnGA/640?wx_fmt=png)

最后在 admin/templat es/article.htm 中直接取得 $article.title 的值，未过滤

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0icxuI7kLVuBdDLdfYB2fE54tGxicb2GUJv9BWPbOjAXOaNym0r9YOA6TnzNvOcqib4PvBneKWBQYxfA/640?wx_fmt=png)

最终导致了存储型 XSS 的产⽣

总结

只是整理了下 XSS 的思路，还请各位师傅指正。  

end

  

![](https://mmbiz.qpic.cn/mmbiz_png/RXib24CCXQ0icxuI7kLVuBdDLdfYB2fE54PkmHeRqcpF3Vq32L6h0xqHL3icB3iaiaJHOPo6VHbVB5iawxHdF08tCXXw/640?wx_fmt=png)