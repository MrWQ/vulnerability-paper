> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/3IkQLljtT60OUOmG89M7aw)

**1、描述**

  

首先介绍一下

MyBatis：一种操作数据库的框架，提供一种 Mapper 类，支持让你用 java 代码进行增删改查的数据库操作，省去了每次都要手写 sql 语句的麻烦。但是！有一个前提，你得先在 xml 中写好 sql 语句，很麻烦，于是有了 Mybatis-plus.

MyBatis-plus: 国人团队苞米豆在 Mybatis 的基础上开发的框架，在 Mybatis 基础上扩展了许多功能，荣获了 2018 最受欢迎国产开源软件第 5 名

**2、影响范围**

  

Mybatis-plus  

  

  

  

  

  

**3、漏洞追踪**

  

使用 Idea 打开项目，修改配置文件数据库地址、账户密码、导入 SQL 文件，或在 Mybatis-plus 官网自行搭建，运行项目，访问 selectPage 接口

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibBicTylCoAH2SOf8YWgPVlpH4tyXcqpIPQO49YuzY9asicafdiaAPzwlekibibZ01VuFlXutVticqX6iaHdg/640?wx_fmt=png)

使用报错注入 payload：

```
http://127.0.0.1:8081/user/selectPage?ascs=extractvalue(1,concat(char(126),md5(123)))&ascs=1
```

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibBicTylCoAH2SOf8YWgPVlpHb7s0Xb2IdVxGRlCTTSicqfFKj0QAYvmyzicYbfxpn2QqlWxayGuwooWw/640?wx_fmt=png)

  

断点分析

进入 Page 实体中

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibBicTylCoAH2SOf8YWgPVlpH0ZiaItIalGBJFdK9DvNZ514Pllibtfwu0bwmAibTsE5lcbpNfUicrGUP1g/640?wx_fmt=png)

255 行断点，此处接收的是个 List 类型参数：

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibBicTylCoAH2SOf8YWgPVlpHv6RZALtZialQuoz5KyKBmDicvmV8MuqSkTfsicQKXzpib0Vebnnlk9PY9w/640?wx_fmt=png)

我们只发送一个 ascs 参数：

```
ascs=extractvalue(1,concat(char(126),md5(123)))
```

可以看到 ascs 被以逗号分割成了 3 份，会导致后续 SQL 拼接的语句语法错误（URL 编码结果一样）：

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibBicTylCoAH2SOf8YWgPVlpHiaSPhhIxyK1RtbP5wJNq5E8KujzhwskL2lmbZic29KsBuvVT4DChIWjw/640?wx_fmt=png)

因为我们这里传入两个 ascs 参数（至于为什么会这样，推测是 SpringMVC 的设计）：

```
ascs=extractvalue(1,concat(char(126),md5(123)))&ascs=1
```

再断点：

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibBicTylCoAH2SOf8YWgPVlpHFvwbr39TvWt6v16gCOOeJu7iclAk8IUFI2hcoAJia4oE8YD3dSLPib23Q/640?wx_fmt=png)

这里我们的 payload 就不会被分割了，两个参数成了 List 的两个元素。

查看 Page 分页拦截器

```
mybatis-plus-extension-3.4.2.jar!/com/baomidou/mybatisplus/extension/plugins/PaginationInterceptor.class
```

127 行断点：

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibBicTylCoAH2SOf8YWgPVlpHGFfBMb6k1qItmA74EVugRN3UcLWso0DiaRdv3Y8qlSiajjOTOj3NRZoQ/640?wx_fmt=png)

SQL 代码就是在此处拼接完成的，具体拼接流程是这两行：

```
plainSelect.setOrderByElements(orderByElementsReturn);
 return plainSelect.toString();
```

orderByElementsReturn 就是我们传入的 payload 数组，plainSelect 是 mybatis 中的原始 sql 语句，此处先将 orderByElementsReturn，set 到 plainSelect 的属性中，之后重写了 toString 方法，跟入 toString：

387 行将 payload 加上 ORDER BY 字符串后 append 到原始 sql 中：

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibBicTylCoAH2SOf8YWgPVlpHxOtP6yffdiaLFrqjbuMuV3WAZp9JN1wwezic2G4xYvoPEjt9BNNyzqPQ/640?wx_fmt=png)

orderByToString 方法：

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibBicTylCoAH2SOf8YWgPVlpHuvQfhz8blxqwUAahxA8nBJYJ1bKgBAQs2Jjhh2Gmeev7BsRtgU3WuA/640?wx_fmt=png)

至此 Payload 就被拼接到了 Mybatis 原始 SQL 语句中。

公众号

最后再给大家介绍一下漏洞库，地址：wiki.xypbk.com  

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibBicTylCoAH2SOf8YWgPVlpHEmc1M8Wz9W8hbIqZ3Pb2IaN9mjicbfVN69EmlWjaSZpjEDhEm42RG3Q/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibBicTylCoAH2SOf8YWgPVlpHeGQ0SrdqrjtnVkhVXuvuglVEBL6Cw2XDUDSeguMfx0z74hXY6lMBVw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/nMQkaGYuOibBicTylCoAH2SOf8YWgPVlpHgeRyoZEj4nQ68fCON9iaNrQ8nm1iacaMjk9WNDw0f0CnL2sIVh1vQEtQ/640?wx_fmt=png)

漏洞库内容来源于互联网 && 零组文库 &&peiqi 文库 && 自挖漏洞 && 乐于分享的师傅，供大家方便检索，绝无任何利益。  

由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，文章作者不为此承担任何责任。

若有愿意分享自挖漏洞的佬师傅请公众号后台留言，本站将把您供上，并在此署名，天天烧香那种！