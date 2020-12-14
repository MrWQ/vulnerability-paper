> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/yxHZakwT7EFkIQ8e9tpKVA)

哈哈哈，那个菜逼回来了，今天给大家讲讲最近审的一个 CMS，大佬勿喷

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGLfGiaXHic9zEBdCp9M820yTVvJJMSvpM81OfA2GfPHuWIESbubcq94ZA/640?wx_fmt=png)

前奏
--

俗话说的好：“工欲善其事，必先利其器”，下面我理了一下这次审计的思路

1：查看目录结构，了解大体的框架（主要是为了查看是否有框架加入，如：TP、WeiPHP 等）

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGbK7781rEPqfU1jt5HZKv3JUzJ6IMCPZ5VlPXh6ZmF4Rtlp8vGFX6JQ/640?wx_fmt=png)

2：查看引入文件，找到重要文件，如过滤函数、变量集中定义文件等

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pG6KYBwtP627iaTTjsrkzUuWLibw3wlWSEpa7NFmBZwebT2UdNrmftfwNQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGEl77U6vdgxl1g5mM1ETgeQ9pf0Q7PicT2GAssDZuLmcjyUzhACeLKTA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGmcibVR4qYgTe96lVIzJr9A29z5L9k49RcK0Hr73mZ4wibLzOBKURRhiag/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGPQ2N4Tib9cXh86G40uNDE1S7438lbtb5QZ06icVp0AfO1CpxJDZStMwA/640?wx_fmt=png)

3：访问特定功能点，进行特定代码审计，也就是说一个功能点看一段代码（这里如果出现了过滤函数，基本上可以在 2 中找到）

审计之旅
----

先打开首页看看，看到有登陆框和注册框，那就先从注册框开始审计

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGQFmL93bj41bLpJTC8R6EXnaM3RzLcTsvoz32wZQo6p5d2AcVVPpZ4g/640?wx_fmt=png)

### 注册框 SQL 注入

打开注册框界面

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGFRLSNAmicLLO8oVAxIhIicAJKiaDE2yEt5f79gTCXHBWA4jbsUiby3D65g/640?wx_fmt=png)

现在的问题是怎么找到对应的代码，这里看到 URL 中有 member 和 register，使用 Seay 全局搜索

观察发现，**m 参数对应的值应该是文件夹，f 参数对应的值就是函数了**

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGCCGBpBC13jHzibZslZLD5PNUjJEtVApqaZsLkGFjrH8C0Oadib0G7wVw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGdxScUG31MzVDbBGbc4GbSoXdxppibYzbOic9oZprP60rn5lxRleOlibmQ/640?wx_fmt=png)

进入 member 目录的 index.php 看看，果然存在 register() 函数

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGE9Glibd79hO9UaNDjnjXdaylzXICHc6E86wL0jnw9ibZlZiaraqpbaU2w/640?wx_fmt=png)

再往下看看，发现 register_save() 函数通过 **safe_html()** 函数过滤以后，直接将数据插入到数据库中

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pG3nKhInicgOHxkY1blibpexqiabezebjxVEUHYX4N5y0DMnFYzkn10uFHg/640?wx_fmt=png)

而 **safe_html()** 正是上面从引入文件中找到的过滤函数文件中定义的一个函数，仔细观察发现，这里可以用大小写或者双写进行绕过

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGqcTNSkWEy8ic7dUhvTgRdISmQG0oSlb5HkfdrUJsnjm0vnkW99fMZ8w/640?wx_fmt=png)

接下来验证一下，在注册框的用户名中加入'，看结果如何

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGYe5Zicb4jIB8gpGBpibyrFfz0GDibkics18ocGV9e7qrPyQk4Mlw9hPskw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGic2RDckLk23ECdnxxbj2Z4tc1YKqPNdlFaCKu1UMfz5bgURiasaibNE5A/640?wx_fmt=png)

芜湖，报错了，直接用 payload 打它，嘿嘿嘿

**payload：'or updatexml(1,concat(0x7e,(selEct concat(username,password) frOm c_admin),0x7e),1)#**

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGUVvTC5QkpTJL14C7pLQB7OHiazA6HdVia74XU23PDzibuiawhqtQK02SAA/640?wx_fmt=png)

### 登录框任意 URL 跳转

注册过后，就要进行登录了，先进入登陆框看看，观察到 URL 中带有 gourl 参数，可能有跳转

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGERWJpnjs6x32JibfBs6AibYEGgIyg90mNBOHqcR8ICB2qsicv6LJI9iaEg/640?wx_fmt=png)

去看看对应的源码，发现这里接收了 gourl 参数后，判断是否有用户后，没有进行参数过滤，直接跳转 gourl 对应的值

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGB93AHVzOvdZPgCxJxaNJ6A5PAGdzqsyunvQ810IrLZ2zmvPJbmicm5A/640?wx_fmt=png)

那么这里我将 gourl 值改为 http://www.baidu.com，然后登录，看是否跳转

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGr1qtHsxIX5TC1gv5lojwdASBEqulAo9TicFspVzhfpV6DsHodtgjyOA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pG1ZgO46m0FMibubu8BrY7hIa0ibspQond61tExiaOH3te8qxXzkUH6cpBQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGlWeZ1GRnVaToCOS2viarxD4cA7yjUBFRupkt6Yicvibs55G03u0Ey6LDg/640?wx_fmt=png)

### 普通用户登录界面 Cookie 注入

用刚才注册的用户登录后，进行漏洞挖掘，观察到这里有个收件箱，点进去看看功能

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGbV4f9blYPsIz8DO5nseemupMvsK4k3ATd9blUL32XQAl2dIKLIZ7kQ/640?wx_fmt=png)

有收件箱、发件箱、写信息三个功能

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGQga2JTHJda10HoibcD07h3iatwRFVw3PD60UcFkGsjGu8uZO3X3VSL5g/640?wx_fmt=png)

查看收件箱功能相关代码，发现这里 **COOKIE** 的 member_user 参数，也是只经过 safe_html 函数过滤，所以可以直接注入

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGfWm8FrXPhaMGQYfOLeZjzgicKZDGDvic6IDibOtWKjJE82mn3GFupBXcA/640?wx_fmt=png)

将包保存为 txt 文件，用 sqlmap 跑

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGeDxZfmSe3VsbDOh2kYutQd4y7vlwkwticF8Mmm9E8yDzfxFQKrCQ34A/640?wx_fmt=png)

### 普通用户登录界面存储 XSS

点击资料管理，观察姓名处，看到姓名的值是直接插在 **value** 属性值中

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGVUibOLjj2oVME09Pn8azL0tEEsd7LicdHxNrYOko2AbeL327yMMF291A/640?wx_fmt=png)

查看源代码，芜湖，发现没有进行过滤，那就直接插啊

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGdRQwFAjudJ7M8mTspMpVuQE6fc4nw7SstouQuwibmDv4s4XbDWQfz7Q/640?wx_fmt=png)

**payload："><script>alert(1)</script>**

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGTmoyiaXibDOGvBrY39kPibN5SARgqicm5Libde9iaq7MXciaC9yGm2CgqkYHw/640?wx_fmt=png)

**其他的功能点，要么不能用，要么洞都是跟上面一样，普通用户登录界面就到这了**

### 后台登录界面文件上传 + 文件包含 = Getshell

登录后台后，找到上传点

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGsWGxmSsMicqBETkKf49yfqHbNACibzhA2icESn37UNmwdfqcPGAMiaHYWA/640?wx_fmt=png)

查看相关代码，发现是白名单机制，所以如果想要 Getshell，需要配合文件包含或者解析漏洞

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGiamTmQ9SqBlWMZQeGXPTqKIWP7bs7AsqpajAfGoZyr60Qj43qWZNvYQ/640?wx_fmt=png)

Seay 全局搜索 include，寻找文件包含漏洞

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGibyEb0ibr8dAY2SrLNLOlChWuqpZknQ8X6hSnjnmelicogU8Miczkdz5Fg/640?wx_fmt=png)

打开 / api/index.php，查看代码，芜湖，没有进行过滤，直接调用，舒服了（这里默认后缀为. php）

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGwnlnXmOgwuUZo53yX9W20iahH4ZIaZvzcEicYSscSe3OJR5Q53xP7mxw/640?wx_fmt=png)

在同名目录下创建 phpinfo.php，访问 http://127.0.0.1/api/index.php?c=phpinfo，进行测试，OK！！！

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGy3L3KyP3fBWibepYVBAd98IgXevJoW5iaFfKpQC5QdF1A1DLtFBcoooQ/640?wx_fmt=png)

首先上传图片马

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGE0GY60vmRnkCw2icQicuTIuTXVTlpGvYIh5viaGibrxeQzcVmMmPkzewQA/640?wx_fmt=png)

菜刀直接配合 %00 截断，进行 getshell

http://127.0.0.1/index.php?c=../uploadfile/image/20201204/202012041021240.jpg%00

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGbEe9MjJASAPcwzfryOmfm8rwiaHLGYt6CZCPgOuu4QMCibrURfb5Nkvw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGaQfiahSMeXYLKOtNupeXU96R0JpQGj9kn6sTWiafPDDuJ54Gj60OeBsg/640?wx_fmt=png)

小结
--

**这个 CMS 审计就告一段落了（PS：主要被大佬们都日穿了，呜呜呜）**

**![](https://mmbiz.qpic.cn/mmbiz_png/dAMlD06OYdI1h5Ce5HGPBpjichw3jq2pGQvpNap6tC3UXnZrBtriaJLnl5PPB0hVecxtKf9LafBsla6jRPQ9221A/640?wx_fmt=png)**